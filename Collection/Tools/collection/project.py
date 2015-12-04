'''Stuff that knows about projects within
the Collection database.'''

# -*- mode: python; -*-

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import bookentry.symbol as symbol

import collection.ui_project as ui_project
import collection.selectDialog as selectDialog

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

        self.connect( self.closeButton, SIGNAL('released()'),
                      self.quit )
        self.connect( self.saveButton, SIGNAL('released()'),
                      self.save )
        #self.connect( self.deleteButton, SIGNAL('released()'),
        #              self.delete )
        self.connect( self.newButton, SIGNAL('released()'),
                      self.new )


        self.connect(self.projectNameEdit, SIGNAL('textChanged()'),
                     self.setProjectDirty)
       
        self.connect(self.descriptionEdit, SIGNAL('textChanged()'),
                     self.setProjectDirty)
       
        self.db = _db
        self.projectId = None
        self.isNew = True
        self.dirty = False


    def setProjectDirty(self):
        print('setProjectDirty')
        self.dirty = True

    def clearProjectDirty(self):
        print('clearProjectDirty')
        self.dirty = False

    def SaveIfDirty(self):
        print('SaveIfDirty', self.dirty)
        if self.dirty:
            ans = QMessageBox.warning( self, 'Save Project?',
                                       'Entry has changed. Do you want to save it?',
                                       QMessageBox.Save,
                                       QMessageBox.No,
                                       QMessageBox.Cancel )
            if ans == QMessageBox.Save:
                self.save()

    def save(self):
        # needs db.cursor or database
        if self.isNew:
            print('Inserting new record into projects')
        else:
            print('Updating old record into projects')

    def new(self):
        self.SaveIfDirty()
        
        self.projectId = None
        self.projectNameEdit.setText('New Project')
        self.descriptionEdit.setText('Enter project description')
        self.isNew = True
        self.clearProjectDirty()
        
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
            self.projectNameEdit.setText( proj[0])
            self.descriptionEdit.setText(proj[1])
            self.isNew = False
            self.getBookList(_projId)
            self.clearProjectDirty()

        self.show()

    def getBookList(self, _projId):
        search = 'SELECT Books.Title, Authors.LastName, BookAuthor.AsWritten FROM Projects INNER JOIN ((Books INNER JOIN (Authors INNER JOIN BookAuthor ON Authors.AuthorID = BookAuthor.AuthorID) ON Books.BookID = BookAuthor.BookID) INNER JOIN BookProject ON Books.BookID = BookProject.BookID) ON %d = BookProject.ProjectID WHERE (((BookAuthor.Priority)=1)) ORDER BY Books.Copyright;' % (_projId)
        books = self.db.execute(search)
        proj = books.fetchone()
        print(proj)

    def quit(self):
        self.SaveIfDirty()
        self.close()


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

        if self.view is None:
            self.view = ProjectView(_db = self.db)
        self.view.setProjId(projId)



'''get project information


'SELECT Books.Title Books.BookId
FROM Books INNER JOIN BookProject
WHERE BookProject.ProjectId == _projid'
'''


