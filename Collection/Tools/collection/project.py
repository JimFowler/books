'''Stuff that knows about projects within
the Collection database.'''

# -*- mode: python; -*-

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import bookentry.symbol as symbol

import collection.ui_project as ui_project
import collection.selectDialog as selectDialog

# Debugging
import pprint
pp = pprint.PrettyPrinter()

class ProjectView( QDialog, ui_project.Ui_Dialog):
    '''View the information about a specific project.
    Must be called with _projid = to a specific project ID
    or None if you want to create a new project. _db is the
    database we are currently working with.  It doesn't make
    any sense to not pass the _db to the class.
    '''
    def __init__( self, parent=None, _db=None ):
        super(ProjectView, self).__init__(parent)
        self.setupUi(self)

        self.connect( self.closeButton,
                      SIGNAL('released()'),
                      self.quit )

        self.connect( self.saveButton,
                      SIGNAL('released()'),
                      self.save )

        self.connect( self.deleteButton,
                      SIGNAL('released()'),
                      self.delete )

        self.connect( self.newButton,
                      SIGNAL('released()'),
                      self.new )


        self.connect(self.projectNameEdit,
                     SIGNAL('textChanged(QString)'),
                     self.setProjectDirty)
       
        self.connect(self.descriptionEdit,
                     SIGNAL('textChanged()'),
                     self.setProjectDirty)
        '''
        self.connect(self.bookList,
                     SIGNAL('itemDoubleClicked(QListWidgetItem*)'),
                     self.getItem)

        self.connect(self.bookList,
                     SIGNAL('itemClicked()'),
                     self.getItem)
                     '''
        self.db = _db
        self.projectId = None
        self.isNew = True
        self.dirty = False


    def setProjectDirty(self):
        #print('setProjectDirty')
        self.dirty = True

    def clearProjectDirty(self):
        #print('clearProjectDirty')
        self.dirty = False

    def SaveIfDirty(self):
        #print('SaveIfDirty', self.dirty)
        if self.dirty:
            ans = QMessageBox.warning( self, 'Save Project?',
                                       'Entry has changed. Do you want to save it?',
                                       QMessageBox.Save,
                                       QMessageBox.No,
                                       QMessageBox.Cancel )
            if ans == QMessageBox.Save:
                self.save()

        
    #
    # Button actions
    #
    def delete(self):
        if not self.isNew:
            queryStmt = 'DELETE FROM Projects WHERE ProjectId = %d;' % (self.projectId)
            # ask yes/no
            ans = QMessageBox.warning( self, 'Delete Project?',
                                       'Are you sure you want to delete this project? This action can not be undone!',
                                       QMessageBox.Yes,
                                       QMessageBox.No )
            if ans == QMessageBox.Yes:
                self.db.execute(queryStmt)
                self.db.commit()
                self.clearProjectDirty()
                self.quit()

    def save(self):
        # needs db.cursor or database
        if self.isNew:

            name = self.projectNameEdit.text()
            description = self.descriptionEdit.toPlainText()
            queryStmt = 'INSERT INTO Projects (ProjectName, Description) VALUES ("%s", "%s");' % (name, description)
            self.db.execute(queryStmt)

            # get new project id somehow
            queryStmt = 'SELECT ProjectId FROM Projects WHERE ProjectName = "%s";' % (name)
            res = self.db.execute(queryStmt)
            proj = res.fetchone()
            self.projectId = int(proj[0])
            
            self.clearProjectDirty()
            self.isNew = False

        elif self.dirty:

            name = self.projectNameEdit.text()
            description = self.descriptionEdit.toPlainText()
            queryStmt = "UPDATE Projects SET ProjectName = '%s', Description = '%s' WHERE ProjectId = %d;" % (name, description, self.projectId)
            print(queryStmt)
            self.db.execute(queryStmt)
            self.clearProjectDirty()

        self.db.commit()
        return

    def new(self):
        self.SaveIfDirty()
        self.projectId = None
        self.projectNameEdit.setText('New Project')
        self.descriptionEdit.setText('Enter project description')
        self.bookList.clear()
        self.isNew = True
        self.clearProjectDirty()
        
    def quit(self):
        self.SaveIfDirty()
        self.close()


    #
    # various functions to get information about a Project
    #
    def setProjId(self, _projId):
        self.SaveIfDirty()
        if _projId is None:
            # Create a new project
            self.new()
        else:
            # Look up an old project
            search =  'SELECT ProjectName, Description from Projects WHERE ProjectId = %d' % (_projId)

            res = self.db.execute(search)
            proj = res.fetchone()
            self.projectId = _projId
            self.projectNameEdit.setText( proj[0])
            self.descriptionEdit.setText(proj[1])
            self.isNew = False
            self.getBookList(_projId)
            self.clearProjectDirty()


        self.show()

    def getBookList(self, _projId):
        self.bookproj = self.db.getBooksInProject(_projId)
        for b in self.bookproj:
            if b[3] == '':
                name = b[2]
            else:
                name = b[3]

            ent = '%s,   %s,   %s' % (b[0], name, b[1])
            self.bookList.addItem(ent)

            
    def getItem(self, item):
        #print('ProjectView: getItem called with:')
        #print(item.text())
        row = self.bookList.currentRow()
        #print('row is', row, 'item should be')
        #print(self.bookproj[row])
        bookId = self.bookproj[row][4]
        print('calling bookView with bookId %d and title %s' % (bookId, self.bookproj[row][0]))
        #call book view with bookId


class Project(object):
    '''Handle the general projects stuff.  It makes
    no sense to call this class and not pass a database
    as _db to it.'''

    def __init__(self, parent=None, _db=None):

        # A dictionary of projectName: ProjectId
        self.projectDict = {}

        # the database to talk to for information
        # We pass this to our views so they can talk to the
        # database also.
        self.db = _db

        # a project view
        self.view = None
        # but what if we want more than one project view???


    def getProjects(self):
        self.projectDict = self.db.getProjectDict()
        
    def selectProject(self):
        '''Get list of Projects and open a selection window so the
        users can pick one.'''
        self.getProjects()
        l = list(self.projectDict.keys())
        l.sort()
        
        self.projSelect = selectDialog.selectDialog(
            _title='Project List',
            _list=l,
            _viewFunction=self.projView,
            _newFunction=self.projView)
        
        self.projSelect.show()
        

    def projView(self, name):

        if name is not None:
            self.getProjects()
            projId = self.projectDict[name]
        else:
            projId = None

        self.view = ProjectView(_db = self.db)
        self.view.setProjId(projId)




