#! /usr/bin/env python3
# -*- mode: Python;-*-

"""Main window for journal entries from AAA/AJB

  open with Journal Search
  open existing journalFile or new one
  New button or search brings up Entry window with an already open file
  redoing a search sets the index number in the current entry
  Search by full name, abbreviation, closeness (how to do this)
"""
import sys
import os
import platform
import fileinput
import configparser

from PyQt5.QtCore import *
from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *

import bookentry.ui_JournalSearch as ui_journalSearch
import bookentry.journalFile as jf
import bookentry.journalMenus as menus
import bookentry.journalEntry as journalEntry
import bookentry.symbol as symbol
import bookentry.headerWindow as hw
import bookentry.search as search

__version__ = '1.0.0'

__dirName, __basename  = os.path.split(symbol.__file__)
__DefaultSymbolTableName__ = __dirName + '/symbols.txt'
del __dirName
del __basename

class JournalSearch( QMainWindow, ui_journalSearch.Ui_JournalSearch ):

    def __init__(self, parent = None, config_name=None ):
        super(JournalSearch, self).__init__(parent=parent)
        self.setupUi(self)
        
        self.jf = jf.JournalFile()
        self.curEntryNumber = 0
        self.setMaxEntryNumber(0)
        self.setWinTitle('document1')
        self.sdict = search.SearchDict()
        
        self.config = configparser.ConfigParser()
        self.config.read(config_name)
        self.jf.setSchemaName(self.config['DEFAULT']['journal_xsd'])
        jfName = self.config['DEFAULT']['journal_file_dir'] + '/' + self.config['DEFAULT']['journal_file_name'] + '.' + self.config['DEFAULT']['journal_file_ext']

        self.openFile(name=jfName)
        self.setWinTitle(self.jf.getBaseName())

        self.setSymbolTableName( __DefaultSymbolTableName__)


        menus.createMenus(self, self.menuBar)

        self.quitButton.released.connect(self.quit)
        #self.newButton.released.connect(self.newEntry)
  
      

    def quit(self):
      if self.askSaveFile() == QMessageBox.Cancel:
        return

      self.close()

    def openNewFile(self):
      """Create a new bookfile saving the old one if it is dirty."""
      if self.jf is not None:
         if self.askSaveFile() == QMessageBox.Cancel:
            return

      self.jf = jf.JournalFile()
      self.setMaxEntryNumber(0)

    def openFile(self, name=None):
      """Open an existing file, get the count of entries, and display
      the first entry. If no records are found we assume that this is
      a new file and we automatically generate a new entry."""
      print('self.openFile: opening', name)
      self.setMaxEntryNumber(self.jf.readfile_XML(name))
      if self.maxEntryNumber:
         self.statusBar.clearMessage()
         self.statusBar.showMessage('%d records found'%self.maxEntryNumber, 6000)
         self.buildSearchDict()
         self.clearSearchFlag()
      else:
         self.statusBar.showMessage('No records found in file %s' % name)
      self.setWinTitle(self.jf.getBaseName())


    def saveFile(self):
      """Ignore dirty entries and just save the file."""
      #print("saving file %s"%self.jf.getFileName())
      if self.jf.getFileName() is None:
         self.saveFileAs()
      else:
         self.jf.writefile_XML()

      self.statusBar.showMessage('Saving file ' + self.jf.getBaseName())
      QTimer.singleShot(10000, self.statusbar.clearMessage  )


    def saveFileAs(self):
      """Ignore dirty entries and save the file as..."""
      fname, filterA = QFileDialog.getSaveFileName(self,
          "%s -- Choose file"%QApplication.applicationName(),
                                          ".", "*.xml")
      if fname:
         self.jf.writefile_XML(fname)
         self.setWinTitle(self.jf.getBaseName())

    #
    # Methods to deal with various display aspects
    #
    def setWinTitle( self, name ):
      """Creates the string 'Journal Entry vx.x - name' and
      places it into the window title.
      """
      self.setWindowTitle(QApplication.translate("MainWindow", 
                  "Journal Entry  v %s   -   %s" % (__version__, name),
                  None))

    #
    # Methods to deal with the journal file
    #
    def setMaxEntryNumber(self, n):
        if n < 0:
          n = 0
        self.maxEntryNumber = n

    #
    # Deal with the Search Dictionary
    #
    def buildSearchDict(self):
      '''Add all the titles and abbreviations to the search
      dictionary'''
      self.sdict.clear()
      index = 0
      for l in self.jf._entryList:
        # print(index, l['Title'])
         self.sdict.addSubStrings(l['Title'], index)
         for abr in l['Abbreviations']:
            #print('   ', abr)
            if abr is not None:
               self.sdict.addSubStrings(abr, index)
         index += 1
      #pprint(self.sdict)

    def setSearchFlag(self):
      """Set the  searchflag to True to enable searchs"""
      self.searchFlag = True

    def clearSearchFlag(self):
      """Set the search flag to False and disable searchs."""
      self.searchFlag = False


    #
    # Edit menu functions
    #
    def openSymbol(self):
      """Open the symbol entry form."""
      self.symbolTable = symbol.SymbolForm(self.symbolTableName, 'FreeSans', 14, self)
      self.symbolTable.sigClicked.connect(self.insertChar )
      self.symbolTable.show()
      
    def setSymbolTableName(self, name):
      """Set the name of the symbol table to use in place of the
      default table."""
      self.symbolTableName = name



    #
    # Various useful dialogs
    #
    def askSaveEntry(self):
      """Ask if we should save the dirty entry."""
      ans = None
      if self.tmpEntryDirty:
          ans = QMessageBox.warning( self, 'Save Entry?',
                                    'Entry has changed. Do you want to save it?',
                                        QMessageBox.Save|QMessageBox.No|QMessageBox.Cancel )

          if ans == QMessageBox.Save:
            self.saveEntry()

      return ans

    def askSaveFile(self):
      """Ask if we should save the dirty file."""
      ans = None
      if self.jf.isDirty():
         ans = QMessageBox.warning( self, 'Save file?',
                                    'The File has changed. Do you want to save it?',
                                    QMessageBox.Save|QMessageBox.Discard|QMessageBox.Cancel )

         if ans == QMessageBox.Save:
            self.saveFile()
            # set save file menu enable to False

      return ans

    def editHeader(self):
      """Open the edit header form."""
      self.headerWindow = hw.HeaderWindow(self)
      self.headerWindow.setBookFile(self.jf)
      self.headerWindow.setWindowTitle(QApplication.translate("headerWindow", 
                         "Edit Headers - %s" % (self.jf.getBaseName()),None))
      self.headerWindow.setHeaderText(self.jf.getHeader())
      self.headerWindow.show()

    def askOpenFile(self):
      """Open an existing file saving the old one if it is dirty."""
      if self.askSaveEntry() == QMessageBox.Cancel:
         return

      if self.askSaveFile() == QMessageBox.Cancel:
         return

      # else get a file name 
      fname, filterA = QFileDialog.getOpenFileName(self,
          "%s -- Choose new file"%QApplication.applicationName(),
                            self.jf.getDirName(), "*.xml")
      if fname:
         self.openFile(fname)

    #
    # Help menu functions
    #
    def helpString(self):
      helpStr = """<b>Journal Entry</b> v {0}
      <p>Author: J. R. Fowler
      <p>Copyright &copy; 2016
      <p>All rights reserved.
      <p>This application is used to create and visualize
      the XML files with the journals found in the annual
      bibliographies of <b>Astronomischer Jahresbericht</b>.
      <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(
          __version__, platform.python_version(),
          QT_VERSION_STR, PYQT_VERSION_STR,
          platform.system())
      return helpStr
      
    def helpAbout(self):
      hstr = self.helpString()
      QMessageBox.about(self, 'About JournalEntry', hstr )
     



