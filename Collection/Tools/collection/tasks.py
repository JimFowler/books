'''Stuff that knows about ToDo tasks within
the Collection database.'''

# -*- mode: python; -*-

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import bookentry.symbol as symbol

import collection.ui_tasks as ui_tasks
import collection.selectDialog as selectDialog

# Debugging
import pprint
pp = pprint.PrettyPrinter()

class TaskView( QDialog, ui_tasks.Ui_Dialog):
    '''View the information about a specific ToDo tasks
    Must be called with _taskId = to a specific Task ID
    or None if you want to create a new task. _db is the
    database we are currently working with.  It doesn't make
    any sense to not pass the _db to the class.
    '''
    def __init__( self, parent=None, _db=None ):
        super(TaskView, self).__init__(parent)
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

        # for a line edit box
        self.connect(self.summaryEdit, SIGNAL('textChanged(QString)'),
                     self.setTaskDirty)
        self.connect(self.createdEdit, SIGNAL('textChanged(QString)'),
                     self.setTaskDirty)
        self.connect(self.completionEdit, SIGNAL('textChanged(QString)'),
                     self.setTaskDirty)

        # for a text edit box
        self.connect(self.descriptionEdit, SIGNAL('textChanged()'),
                     self.setTaskDirty)

        self.db = _db
        self.taskId = None
        self.isNew = True
        self.dirty = False


    def setTaskDirty(self):
        #print('setTaskDirty')
        self.dirty = True

    def clearTaskDirty(self):
        #print('clearTaskDirty')
        self.dirty = False

    def SaveIfDirty(self):
        #print('SaveIfDirty', self.dirty)
        if self.dirty:
            ans = QMessageBox.warning( self, 'Save ToDo task?',
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
            queryStmt = 'DELETE FROM ToDo WHERE ToDoId = %d;' % (self.taskId)
            # ask yes/no
            ans = QMessageBox.warning( self, 'Delete ToDo task?',
                                       'Are you sure you want to delete this task? This action can not be undone!',
                                       QMessageBox.Yes,
                                       QMessageBox.No )
            if ans == QMessageBox.Yes:
                self.db.execute(queryStmt)
                self.db.commit()
                self.clearTaskDirty()
                self.quit()

    def save(self):
        # needs db.cursor or database
        if self.isNew:

            summary = self.summaryEdit.text()
            create = self.createdEdit.text()
            complete = self.completionEdit.text()
            description = self.descriptionEdit.toPlainText()
            # add other info TODO
            queryStmt = 'INSERT INTO ToDo (Summary, Description, DateOfEntry, DateCompleted) VALUES ("%s", "%s", "%s", "%s");' % (summary, description, create, complete)
            self.db.execute(queryStmt)

            # get new task id somehow, requires Name to be unique
            queryStmt = 'SELECT ToDoId FROM ToDo WHERE Summary = "%s";' % (summary)
            res = self.db.execute(queryStmt)
            task = res.fetchone()
            self.taskId = int(task[0])
            self.idLabel.setText(self.taskId)
            self.clearTaskDirty()
            self.isNew = False

        elif self.dirty:

            summary = self.summaryEdit.text()
            create = self.createdEdit.text()
            complete = self.completionEdit.text()
            description = self.descriptionEdit.toPlainText()
            queryStmt = "UPDATE ToDo SET Summary = '%s', Task = '%s', DateOfEntry = '%s', DateCompleted = '%s' WHERE VendorId = %d;" % (summary, description, create, completion, self.vendorId)
            print(queryStmt)
            self.db.execute(queryStmt)
            self.clearTaskDirty()

        self.db.commit()
        return

    def clearForm(self):
        self.summaryEdit.setText('New To Do Task')
        self.createdEdit.clear()
        self.completionEdit.clear()
        self.descriptionEdit.setText('Enter task description')

    def new(self):
        self.SaveIfDirty()
        self.taskId = None
        self.clearForm()
        self.isNew = True
        self.clearTaskDirty()
        
    def quit(self):
        self.SaveIfDirty()
        self.close()


    #
    # various functions to get information about a ToDo Task
    #
    def setTaskId(self, _taskId):
        self.SaveIfDirty()
        if _taskId is None:
            # Create a new task
            self.new()
        else:
            # Look up an old task
            search =  'SELECT * from ToDo WHERE ToDoId = %d' % (_taskId)

            res = self.db.execute(search)
            vendor = res.fetchone()
            self.taskId = _taskId
            self.idLabel.setText(    str(vendor[0]))
            self.summaryEdit.setText(    vendor[1] )
            self.descriptionEdit.setText(vendor[2] )
            self.createdEdit.setText(    vendor[3] )
            self.completionEdit.setText( vendor[4] )
            self.isNew = False
            self.clearTaskDirty()


        self.show()


class Task(object):
    '''Handle the general ToDo Task stuff.  It makes
     no sense to call this class and not pass a database
    as _db to it.'''

    def __init__(self, parent=None, _db=None):

        if _db is None:
            pass

        # A dictionary of VendorName: VendorId
        self.taskDict = {}

        # the database to talk to for information
        # We pass this to our views so they can talk to the
        # database also.
        self.db = _db

        # a vendor view
        self.view = None
        # but what if we want more than one vendor view???


    def getTasks(self):
        self.tasksDict = self.db.getToDoDict()
        
    def selectTask(self):
        '''Get list of Vendors and open a selection window so the
        users can pick one.'''
        self.getTasks()
        l = list(self.tasksDict.keys())
        l.sort()
        
        self.taskSelect = selectDialog.selectDialog(
            _title='To Do Task List',
            _list=l,
            _viewFunction=self.taskView,
            _newFunction=self.taskView)
        
        self.taskSelect.show()
        

    def taskView(self, name):

        if name is not None:
            self.getTasks()
            taskId = self.tasksDict[name]
        else:
            taskId = None

        self.view = TaskView(_db = self.db)
        self.view.setTaskId(taskId)




