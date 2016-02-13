"""Main window for the Collection database
"""
# -*- mode: Python;-*-

import traceback
import platform
import fileinput
import re

# Trouble shooting assistance
from pprint import *
pp = PrettyPrinter()

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

from nameparser import HumanName

import bookentry.symbol as symbol

import collection.menus as menus
import collection.ui_mainWindow as ui_mainWindow
import collection.selectDialog as selectDialog
import collection.librarian as library
import collection.book as book
#import collection.want as want
import collection.author as author
import collection.project as project
import collection.vendor as vendor
import collection.tasks as tasks

import os
__dirName, __basename  = os.path.split(symbol.__file__)
__DefaultSymbolTableName__ = __dirName + '/symbols.txt'
del __dirName
del __basename

__version__ = '1.0.0'


class Collection( QMainWindow, ui_mainWindow.Ui_MainWindow ):
    """Collection is the class which handles the mainWindow form
    for display of entries from the database.
    """
    def __init__( self, parent=None ):
        super(Collection, self).__init__(parent)
        self.setupUi(self)

        self.setWinTitle('')
        self.symbolTableName = __DefaultSymbolTableName__
        self.insertFunc = None

        self.db = library.collectionDB()

        self.book = book.Book(_db=self.db)
        #self.want = want.Want(_db=self.db)
        self.author = author.Author(_db=self.db)
        self.project = project.Project(_db=self.db)
        self.vendor = vendor.Vendor(_db=self.db)
        self.tasks = tasks.Task(_db=self.db)



        menus.createMenus(self, self.menubar)

        self.connect( self.Books_Button,    SIGNAL('released()'),
                      self.book.selectBook )
        #self.connect( self.Wants_Button,    SIGNAL('released()'),
        #              self.want.selectBook )
        self.connect( self.Authors_Button,  SIGNAL('released()'),
                      self.author.selectAuthor )
        self.connect( self.Vendors_Button,  SIGNAL('released()'),
                      self.vendor.selectVendor )
        self.connect( self.Projects_Button, SIGNAL('released()'),
                      self.project.selectProject )
        self.connect( self.Wants_Button,    SIGNAL('released()'),
                      self.selectWant )
        self.connect( self.ToDo_Button,     SIGNAL('released()'),
                      self.tasks.selectTask )

        #self.connect( self.Search_Button, SIGNAL('released()'), self.quit )
        #self.connect( self.Other_Button, SIGNAL('released()'), self.quit )
        #self.connect( self.Reports_Button, SIGNAL('released()'), self.quit )

        self.connect( self.quit_Button, SIGNAL('released()'), self.quit )


    #
    # Menu and button slots
    #
    def quit(self):
        '''Clean up and exit.'''
        self.db.closeDB()
        self.close()

    #
    # Set/Get functions
    #
    def setDatabaseName(self, database):
        '''Set the name of the database that we operate on.
        Return True if the name is valid and the database could be opened
        or False if this is an invalid name.'''
        # should really catch any open errors here
        # but this is a single user program
        return self.db.open(database)

    def getDatabaseName():
        '''Return the name of the current database.'''
        return self.db.getDBName()


    #
    # Edit menu functions
    #
    def openSymbol(self):
        """Open the symbol entry form."""
        self.symbolTable = symbol.SymbolForm(self.symbolTableName,
                                             'FreeSans', 14, self)
        self.symbolTable.show()
        self.connect(self.symbolTable, SIGNAL('sigClicked'),
                     self.insertChar )

    def setSymbolTableName(self, name):
        """Set the name of the symbol table to use in place of the
        default table."""
        self.symbolTableName = name
        
    #
    # Methods to deal with various display aspects
    #
    def setWinTitle( self, name ):
        """Creates the string 'Collection Database vx.x - name' and
        places it into the window title.
        """
        self.setWindowTitle(QApplication.translate("MainWindow", 
             "Collection Database  v %s   -   %s" % (__version__, name),
                               None, QApplication.UnicodeUTF8))

    def insertChar(self, obj):
        """Insert the charactor in obj[0] with self.insertFunc
        if insertFunc is not None."""
        
        char = obj[0]
        # invoke self.insertFunc(char)
        if self.insertFunc is not None:
            self.insertFunc(char)
        # take back focus somehow??

    def setFocusChanged(self, oldWidget, nowWidget ):
        """For items in setTextEntryList and setLineEntryList
        set insertFunc to be either insertPlainText or insert."""
        
        '''
        if oldWidget is None:
         pass
        elif oldWidget.objectName() == 'indexEntry':
         self.indexEntry.setText(str(self.curEntryNumber))

      if nowWidget is None:
         pass
      elif self.setTextEntryList.count(nowWidget.objectName()):
         self.insertFunc = nowWidget.insertPlainText
      elif self.setLineEntryList.count(nowWidget.objectName()):
         self.insertFunc = nowWidget.insert
      elif self.noEntryList.count(nowWidget.objectName()):
         self.insertFunc = None
         '''
        pass

    #
    # Button Functions
    #
    def selectBook(self):
        '''Get list of Books and open a selection window so the
        users can pick one.'''
        self.bookDict =self.db.getBookDict()
        l = list(self.bookDict.keys())

        self.bookSelect = selectDialog.selectDialog(
            _title='Book List',
            _list=l,
            _viewFunction=None,
            _newFunction=None)

        self.bookSelect.show()
        
    
    def selectWant(self):
        '''Get list of Wants and open a selection window so the
        users can pick one.'''
        return
        #self.wantDict =self.db.getWantDict()
        #l = list(self.wantDict.keys())

        #self.wantSelect = selectDialog.selectDialog(
        #    _title='Wants List',
        #    _list=wantlist,
        #    _viewFunction=None,
        #    _newFunction=None)

        #self.wantSelect.show()
        

    def selectAuthor(self):
        '''Get list of Authors and open a selection window so the
        users can pick one.'''
        self.authorDict = self.db.getAuthorDict()
        l = list(self.authorDict.keys())

        self.authorSelect = selectDialog.selectDialog(
            _title='Author List',
            _list=l,
            _viewFunction=None,
            _newFunction=None)

        self.authorSelect.show()
        

    def selectVendor(self):
        '''Get list of Vendor/Publishers and open a selection window so the
        users can pick one.'''
        self.vendorDict = self.db.getVendorDict()
        l = list(self.vendorDict.keys())

        self.vendorSelect = selectDialog.selectDialog(
            _title='Vendor/Publisher List',
            _list=l,
            _viewFunction=None,
            _newFunction=None)

        self.vendorSelect.show()
        


    def selectToDo(self):
        '''Get list of Todo tasks and open a selection window so the
        users can pick one.'''
        self.todoDict = self.db.getToDoDict()
        l = list(self.todoDict.keys())

        self.todoSelect = selectDialog.selectDialog(
            _title='ToDo List',
            _list=l,
            _viewFunction=None,
            _newFunction=None)

        self.todoSelect.show()
        
    #
    # Help menu functions
    #
    def helpString(self):
        helpStr = """<b>Collection Database</b> v {0}
        <p>Author: J. R. Fowler
        <p>Copyright &copy; 2015
        <p>All rights reserved.
        <p>This application is used to work with the database
        Collections.db3.  This database is the catalog of books
        in my library collection.
        <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(
            __version__, platform.python_version(),
            QT_VERSION_STR, PYQT_VERSION_STR,
            platform.system())

        return helpStr

    def helpAbout(self):
        hstr = self.helpString()
        QMessageBox.about(self, 'About books', hstr )

#
# Test routine
#

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    app.setApplicationName('Collection Database')

    form = Collection()
    fname = '/home/jrf/Documents/books/Collection/Collection.db3'
    if not form.setDatabaseName(fname):
        print('Could not open database', fname )
        sys.exit(1)
 

    form.show()
    sys.exit(app.exec_())

