# -*- mode: Python;-*-

"""Main window for the Collection database
"""

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

import menus as menus
import ui_mainWindow as ui_mainWindow

import os
__dirName, __basename  = os.path.split(symbol.__file__)
__DefaultSymbolTableName__ = __dirName + '/symbols.txt'
del __dirName
del __basename

__version__ = '1.0'


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
        
        menus.createMenus(self, self.menubar)

        self.connect( self.quit_Button, SIGNAL('released()'), self.quit )


    #
    # Menu and button slots
    #
    def quit(self):
        '''Clean up and exit.'''
        self.close()

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
      
    def helpAbout(self):
        hstr = self.helpString()
        QMessageBox.about(self, 'About Collection', hstr )

#
# Test routine
#

if __name__ == '__main__':

   import sys

   app = QApplication(sys.argv)
   app.setApplicationName('Collection Database')
   form = Collection()
   #QObject.connect(app, SIGNAL("focusChanged(QWidget *, QWidget *)"), 
   #                form.setFocusChanged)

   form.show()
   sys.exit(app.exec_())

