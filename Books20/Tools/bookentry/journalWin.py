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
from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import bookentry.ui_JournalSearch as ui_journalSearch
#import bookentry.journalfile as bf
import bookentry.journalMenus as menus
import bookentry.symbol as symbol
import bookentry.headerWindow as hw

# Trouble shooting assistance
from pprint import *
pp = PrettyPrinter()


__dirName, __basename  = os.path.split(symbol.__file__)
__DefaultSymbolTableName__ = __dirName + '/symbols.txt'
del __dirName
del __basename

__version__ = '1.0.0'

class JournalSearch( QMainWindow, ui_journalSearch.Ui_JournalSearch ):

   def __init__(self, parent = None ):
      super(JournalSearch, self).__init__(parent)
      self.setupUi(self)

      # This boolean indicates that the window entries
      # have been modified and that we should not change the
      # window contents without asking the user if they should
      # be saved.
      self.tmpEntryDirty = False
      self.bf = None
      self.curEntryNumber = 0
      self.setMaxEntryNumber(0)
      self.setWinTitle('document1')
      self.insertFunc = None
      self.setSymbolTableName( __DefaultSymbolTableName__)

      menus.createMenus(self, self.menubar)

      self.connect(self.QuitButton, SIGNAL('released()'), self.close)


   def setMaxEntryNumber(self, n):
      if n < 0:
          n = 0
      self.maxEntryNumber = n
      '''
      if self.maxEntryNumber == 0:
          self.prevButton.setEnabled(False)
          self.nextButton.setEnabled(False)
      else :
          self.prevButton.setEnabled(True)
          self.nextButton.setEnabled(True)

      self.ofnumLabel.setText('of %d'%self.maxEntryNumber)
      '''

   #
   # Menu and button slots
   #
   def quit(self):
      if self.askSaveEntry() == QMessageBox.Cancel:
         return

      if self.askSaveFile() == QMessageBox.Cancel:
         return

      self.close()

   #
   # Menu and button slots for File actions
   #
   def openNewFile(self):
      """Create a new bookfile saving the old one if it is dirty."""
      if self.bf is not None:
         if self.askSaveEntry() == QMessageBox.Cancel:
            return

         if self.askSaveFile() == QMessageBox.Cancel:
            return

      self.bf = bf.BookFile()
      self.setMaxEntryNumber(0)
      self.newEntry()

   def openFile(self, name=None):
      """Open an existing file, get the count of entries, and display
      the first entry. If no records are found we assume that this is
      a new file and we automatically generate a new entry."""

      self.setMaxEntryNumber(self.bf.readFile(name))
      if self.maxEntryNumber:
         self.statusbar.clearMessage()
         self.statusbar.showMessage('%d records found'%self.maxEntryNumber, 6000)
         self.showEntry(1)
         self.insertButton.setEnabled(True)
         self.clearEntryDirty()
      else:
         self.statusbar.showMessage('No records found in file %s' % name)
         self.newEntry()
      self.setWinTitle(self.bf.getBaseName())


   def saveFile(self):
      """Ignore dirty entries and just save the file."""
      #print("saving file %s"%self.bf.getFileName())
      if self.bf.getFileName() is None:
         self.saveFileAs()
      else:
         self.bf.writeFile()

      self.statusbar.showMessage('Saving file ' + self.bf.getBaseName())
      QTimer.singleShot(10000, self.statusbar.clearMessage  )


   def saveFileAs(self):
      """Ignore dirty entries and save the file as..."""
      fname = QFileDialog.getSaveFileName(self,
          "%s -- Choose file"%QApplication.applicationName(),
                                          ".", "*.txt")
      if fname:
         self.bf.writeFile(fname)
         self.setWinTitle(self.bf.getBaseName())

   #
   # Menu and button slots for Entry Actions
   #
   def saveEntry(self):
      """Save the entry to the current entry number in the bookfile."""
      self.tmpEntry = self.DisplayToEntry()
      if not self.tmpEntry:
         QMessageBox.information(self, "Entry Invalid", 
                                 "Entry invalid!  Not saved in bookfile!" )
         return

      #pp.pprint(self.tmpEntry)

      if self.curEntryNumber > self.maxEntryNumber:
         ret = self.bf.setNewEntry(self.tmpEntry, self.curEntryNumber)
      else:
         ret = self.bf.setEntry(self.tmpEntry, self.curEntryNumber)

      if not ret:
         QMessageBox.information(self, "Entry Invalid", 
                                 "Entry invalid!  Not saved in bookfile!" )
         return

      if self.curEntryNumber > self.maxEntryNumber:
         self.setMaxEntryNumber(self.curEntryNumber)
      self.deleteButton.setEnabled(True)
      self.clearEntryDirty()

   def newEntry(self):
      """Create a new entry, save the old one if it has been modified."""
      if self.askSaveEntry() == QMessageBox.Cancel:
         return

      self.tmpEntry = AJBentry.AJBentry()
      self.curEntryNumber = self.maxEntryNumber + 1
      self.tmpEntry['Index'] = self.curEntryNumber
      self.EntryToDisplay(self.tmpEntry)
      self.indexEntry.setText(str(self.curEntryNumber))
      if self.defaultVolumeNumber is not None:
         self.volNum.setText(self.defaultVolumeNumber)
      self.volNum.setFocus()
      self.deleteButton.setEnabled(False)
      if self.maxEntryNumber > 0:
         self.insertButton.setEnabled(True)
      self.clearEntryDirty()

   def askInsertEntry(self):
      """Open the entrySelect form if we have a valid entry to insert.
      If the user selects an insertion location, then we execute the 
      method insertEntry()"""
      self.tmpEntry = self.DisplayToEntry()
      if not self.tmpEntry or not self.tmpEntry.isValid():
         QMessageBox.information(self, "Entry Invalid", 
                                 "Entry invalid!  Not saved in bookfile!" )
         return

      self.entrySelect= es.EntrySelect()
      self.entrySelect.setText( self.bf.mkShortTitleList() )

      self.entrySelect.show()
      self.connect(self.entrySelect, SIGNAL('lineEmit'),
                   self.insertEntry )

   def insertEntry(self, line):
      """Parse the short title line, get the index number and insert
      the current display entry in front of this entry in the booklist."""

      words = line[0].split(' ')

      num = int(words[0])
      if not num or num < 1 or num > self.maxEntryNumber:
         return

      self.bf.setNewEntry(self.tmpEntry, num)
      self.curEntryNumber = num
      self.setMaxEntryNumber(self.maxEntryNumber + 1)
      self.showEntry(self.curEntryNumber)
      pass

   def deleteEntry(self):
      """Delete the entry at the curEntryNumber but
      ask the user first."""
      ans = QMessageBox.warning( self, 'Delete Entry?',
                                 'Are you sure you want to delete this entry? This action can not be undone!',
                                 QMessageBox.Ok,
                                 QMessageBox.Cancel )
      if ans == QMessageBox.Cancel:
         return

      self.setMaxEntryNumber(self.bf.deleteEntry(self.curEntryNumber))
      if self.maxEntryNumber < 1:
         self.insertButton.setEnable(False)
         self.newEntry()
      else:
         self.showEntry(self.curEntryNumber)

   def showEntry(self, recnum=1):
      """showEntry(recnum) where 1 <= recnum <= maxEntryNumber.
      recnum is the index into the entry list.  The buttons will
      wrap around the index values.
      """
      self.prevButton.setEnabled(True)

      self.nextButton.setEnabled(True)

      if recnum < 1:
         # We add here because recnum is zero or negative already
         self.curEntryNumber = self.maxEntryNumber + recnum
      elif recnum > self.maxEntryNumber:
         self.curEntryNumber = recnum - self.maxEntryNumber
      else:
         self.curEntryNumber = recnum

      # Display the actual entry data
      self.tmpEntry = self.bf.getEntry(self.curEntryNumber)

      if not self.tmpEntry:
         return

      # Display record count
      self.indexEntry.setText(str(self.curEntryNumber))

      self.EntryToDisplay(self.tmpEntry)
      self.deleteButton.setEnabled(True)
      self.clearEntryDirty()

   def newprintEntry(self):
      """Print a postscript file of the current display."""
      pp.pprint(self.bf.getEntry(self.curEntryNumber))

   def printEntry(self):
      """Print a postscript file of the current display."""
      pr = QPrinter()
      pr.setOutputFileName('BookEntry.pdf')
      pr.setFullPage(True)
      pr.setPaperSize(QPrinter.Letter)
      
      pt = QPainter(pr)
      self.render(pt)
      del pt

   #
   # Set/Clear flags for Entry
   def setEntryDirty(self):
      """Set the tmpEntryDirty flag to True and enable the Save Entry button."""
      self.tmpEntryDirty = True
      self.acceptButton.setEnabled(True)
      # set menu item enable to True as well

   def clearEntryDirty(self):
      """Set the tmpEntryDirty flag to False and disable the Save Entry button."""
      self.tmpEntryDirty = False
      self.acceptButton.setEnabled(False)
      # set menu item enable False as well.
      # set Save File menu True

   def printPrinter(self):
      pr = QPrinter()
      pr.setOutputFileName('BookEntry.pdf')
      pr.setFullPage(True)
      pr.setPaperSize(QPrinter.Letter)
      
      prt = QPrintDialog(pr, self)
      if prt.exec_():
         pt = QPainter(pr)
         self.render(pt)
         del pt


   #
   # Edit menu functions
   #
   def openSymbol(self):
      """Open the symbol entry form."""
      self.symbolTable = symbol.SymbolForm(self.symbolTableName, 'FreeSans', 14, self)
      self.symbolTable.show()
      self.connect(self.symbolTable, SIGNAL('sigClicked'),
                   self.insertChar )

   def setSymbolTableName(self, name):
      """Set the name of the symbol table to use in place of the
      default table."""
      self.symbolTableName = name

   def editHeader(self):
      """Open the edit header form."""
      self.headerWindow = hw.HeaderWindow(self)
      self.headerWindow.setBookFile(self.bf)
      self.headerWindow.setWindowTitle(QApplication.translate("headerWindow", 
                         "Edit Headers - %s" % (self.bf.getBaseName()),
                         None, QApplication.UnicodeUTF8))
      self.headerWindow.setHeaderText(self.bf.getHeader())
      self.headerWindow.show()

   #
   # Button slots and Signals
   #
   def on_prevButton_released(self):
      if self.askSaveEntry() == QMessageBox.Cancel:
         return

      self.showEntry(self.curEntryNumber - 1)

   def on_nextButton_released(self):
      if self.askSaveEntry() == QMessageBox.Cancel:
         return

      self.showEntry(self.curEntryNumber + 1)

   def indexChanged(self):
      enum = int(self.indexEntry.text())

      if self.askSaveEntry() == QMessageBox.Cancel:
         return

      self.showEntry(enum)

   #
   # Various useful dialogs
   #
   def askSaveEntry(self):
      """Ask if we should save the dirty entry."""
      ans = None
      if self.tmpEntryDirty:
         ans = QMessageBox.warning( self, 'Save Entry?',
                                    'Entry has changed. Do you want to save it?',
                                    QMessageBox.Save,
                                    QMessageBox.No,
                                    QMessageBox.Cancel )

         if ans == QMessageBox.Save:
            self.saveEntry()

      return ans

   def askSaveFile(self):
      """Ask if we should save the dirty file."""
      ans = None
      if self.bf.isDirty():
         ans = QMessageBox.warning( self, 'Save file?',
                                    'The File has changed. Do you want to save it?',
                                    QMessageBox.Save,
                                    QMessageBox.Discard,
                                    QMessageBox.Cancel )

         if ans == QMessageBox.Save:
            self.saveFile()
            # set save file menu enable to False

      return ans

   def askOpenFile(self):
      """Open an existing file saving the old one if it is dirty."""
      if self.askSaveEntry() == QMessageBox.Cancel:
         return

      if self.askSaveFile() == QMessageBox.Cancel:
         return

      # else get a file name 
      fname = QFileDialog.getOpenFileName(self,
          "%s -- Choose new file"%QApplication.applicationName(),
                            self.bf.getDirName(), "*.txt")
      if fname:
         self.openFile(fname)

        
   #
   # Methods to deal with various display aspects
   #
   def setWinTitle( self, name ):
      """Creates the string 'BookEntry vx.x - name' and
      places it into the window title.
      """
      self.setWindowTitle(QApplication.translate("MainWindow", 
                 "AJB Book Entry  v %s   -   %s" % (__version__, name),
                 None, QApplication.UnicodeUTF8))

   def EntryToDisplay(self, entry):
      """Given an entry, display the parts on the GUI display."""
      pass

   def DisplayToEntry(self):
      """Copy the display into a new entry and
      return the entry."""
      pass

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
      QMessageBox.about(self, 'About BookEntry', hstr )

