#! /usr/bin/env python3
# -*- mode: Python;-*-

"""AJB/AAA dialog to review and edit books entries
"""

import traceback
import sys
import os
import platform
import fileinput
import argparse

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import ui_BookEntry
from bookfile import *
from menus import *
from headerWindow import *
from AJBentry import *
from symbol import *

__version__ = '0.1'


class BookEntry( QMainWindow, ui_BookEntry.Ui_MainWindow ):
   """BookEntry is the class which handles the BookEntry form
   for display of entries from the text files.
   """
   def __init__( self, parent=None ):
      super(BookEntry, self).__init__(parent)
      self.setupUi(self)

      self.tmpEntry = AJBentry()
      self.tmpEntryDirty = False

      self.curEntryNum = 0
      self.maxEntryNum = 0
      self.bf = BookFile()
      self.setWinTitle('document1')
      self.insertFunc = None

      self.noEntryList = ['volNum', 'secNum', 'subSecNum', 'itemNum',
                          'yearEntry', 'pageEntry', 'indexEntry']
      self.setTextEntryList = ['authorEntry', 'editorEntry', 'titleEntry',
                               'publEntry', 'reviewsEntry',  'translatorEntry',
                               'compilersEntry', 'contribEntry', 'commentsEntry',
                               'headerEntry' ]
      self.setLineEntryList = ['fromlangEntry', 'tolangEntry', 'priceEntry']

      createMenus(self, self.menubar)

      self.connect(self.quitButton, SIGNAL('released()'), self.quit )
      self.connect(self.newEntryButton, SIGNAL('released()'), self.newEntry )
      self.connect(self.acceptButton, SIGNAL('released()'), self.saveEntry )
      self.acceptButton.setEnabled(False)


      self.connect(self.volNum, SIGNAL('textChanged(QString)'), self.setEntryDirty)
      self.connect(self.secNum, SIGNAL('textChanged(QString)'), self.setEntryDirty)
      self.connect(self.subSecNum, SIGNAL('textChanged(QString)'), self.setEntryDirty)
      self.connect(self.itemNum, SIGNAL('textChanged(QString)'), self.setEntryDirty)
      self.connect(self.authorEntry, SIGNAL('textChanged()'), self.setEntryDirty)
      self.connect(self.editorEntry, SIGNAL('textChanged()'), self.setEntryDirty)
      self.connect(self.titleEntry, SIGNAL('textChanged()'), self.setEntryDirty)
      self.connect(self.publEntry, SIGNAL('textChanged()'), self.setEntryDirty)
      self.connect(self.yearEntry, SIGNAL('textChanged(QString)'), self.setEntryDirty)
      self.connect(self.pageEntry, SIGNAL('textChanged(QString)'), self.setEntryDirty)
      self.connect(self.priceEntry, SIGNAL('textChanged(QString)'), self.setEntryDirty)
      self.connect(self.reviewsEntry, SIGNAL('textChanged()'), self.setEntryDirty)
      self.connect(self.fromlangEntry, SIGNAL('textChanged(QString)'), self.setEntryDirty)
      self.connect(self.tolangEntry, SIGNAL('textChanged(QString)'), self.setEntryDirty)
      self.connect(self.translatorEntry, SIGNAL('textChanged()'), self.setEntryDirty)
      self.connect(self.compilersEntry, SIGNAL('textChanged()'), self.setEntryDirty)
      self.connect(self.contribEntry, SIGNAL('textChanged()'), self.setEntryDirty)
      self.connect(self.commentsEntry, SIGNAL('textChanged()'), self.setEntryDirty)

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
      if self.askSaveEntry() == QMessageBox.Cancel:
         return

      if self.askSaveFile() == QMessageBox.Cancel:
         return

      self.bf = BookFile()

   def openFile(self, name=None):
      self.maxEntryNum = self.bf.readFile(name)
      if self.maxEntryNum:
         self.statusbar.clearMessage()
         self.statusbar.showMessage('%d records found'%self.maxEntryNum, 6000)
         self.ofnumLabel.setText('of %d'%self.maxEntryNum)
         self.showEntry(1)
         self.clearEntryDirty()
      else:
         self.statusbar.showMessage('No records found in file %s' % name)
      self.setWinTitle(self.bf.getBaseName())


   def saveFile(self):
      """Ignores dirty entries and just save the file."""
      if self.bf.getFileName() is not None:
         self.saveFileAs()
      else:
         self.bf.writeFile()


   def saveFileAs(self):
      """Ignore dirty entries and save the file as..."""
      fname = QFileDialog.getSaveFileName(self,
          "%s -- Choose file"%QApplication.applicationName(),
                                          ".", "*.txt")
      if fname:
         self.bf.writefile(fname)

   #
   # Menu and button slots for Entry Actions
   #
   def saveEntry(self):
      """Save the entry to the current entry number in the bookfile."""
      self.DisplayToEntry(self.tmpEntry)
      self.bf.setEntry(self.tmpEntry, self.curEntryNumber)
      self.clearEntryDirty()

   def newEntry(self):
      """Create a new entry, save the old one if it has been modified."""
      if self.askSaveEntry() == QMessageBox.Cancel:
         return

      self.tmpEntry = AJBentry()
      self.curEntryNum = self.maxEntryNum + 1
      self.EntryToDisplay(self.tmpEntry)
      self.clearEntryDirty()

   def showEntry(self, recnum=1):
      """showEntry(recnum) where 0 <= recnum < maxEntryNums.
      recnum is the index into the entry list, the displayed
      value will be (recnum + 1).  The buttons will wrap around
      the index values.
      """
      self.prevButton.setEnabled(True)

      self.nextButton.setEnabled(True)

      if recnum < 1:
         # We add here because recnum is zero or negative already
         self.curEntryNum = self.maxEntryNum + recnum
      elif recnum > self.maxEntryNum:
         self.curEntryNum = recnum - self.maxEntryNum
      else:
         self.curEntryNum = recnum

      # Display the actual entry data
      self.tmpEntry = self.bf.getEntry(self.curEntryNum)

      if not self.tmpEntry:
         return

      # Display record count
      self.indexEntry.setText(str(self.curEntryNum))

      self.EntryToDisplay(self.tmpEntry)

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

   def clearEntryDirty(self):
      """Set the tmpEntryDirty flag to False and disable the Save Entry button."""
      self.tmpEntryDirty = False
      self.acceptButton.setEnabled(False)


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
      """Open the symbol dialog form."""
      self.symbolTable = SymbolForm('./symbols.txt', 'FreeSans', 12)
      self.symbolTable.show()
      self.connect(self.symbolTable, SIGNAL('sigClicked'),
                   self.insertChar )

   def editHeader(self):
      """Open the edit header form."""
      self.headerWindow = HeaderWindow(self)
      self.headerWindow.setBookFile(self.bf)
      self.headerWindow.setWindowTitle(QApplication.translate("headerWindow", 
                                  "Edit Headers - %s" % (self.bf.getBaseName()),
                                  None, QApplication.UnicodeUTF8))
      self.headerWindow.setHeaderText(self.bf.getHeader())
      self.headerWindow.show()

   #
   # Button slots
   #
   def on_prevButton_released(self):
      self.showEntry(self.curEntryNum - 1)

   def on_nextButton_released(self):
      self.showEntry(self.curEntryNum + 1)

   #
   # Various useful dialogs
   #
   def askSaveEntry(self):
      """Ask if we should save the dirty entry."""
      if self.tmpEntryDirty:
         ans = QMessageBox.warning( self, 'Save Entry?',
                                    'Entry has changed. Do you want to save it?',
                                    QMessageBox.Save,
                                    QMessageBox.Ignore,
                                    QMessageBox.Cancel )

         if ans == QMessageBox.Save:
            self.saveEntry()

         return ans
      return None

   def askSaveFile(self):
      """Ask if we should save the dirty file."""
      if self.bf.isDirty():
         ans = QMessageBox.warning( self, 'Save file?',
                                    'The File has changed. Do you want to save it?',
                                    QMessageBox.Save,
                                    QMessageBox.Ignore,
                                    QMessageBox.Cancel )

         if ans == QMessageBox.Save:
            self.saveFile()

         return ans
      return None

   def askOpenFile(self):
      """Open an existing file saving the old one if it is dirty."""
      if self.askSaveEntry() == QMessageBox.Cancel:
         return

      if self.askSaveFile() == QMessageBox.Cancel:
         return

      # else get a file name 
      fname = QFileDialog.getOpenFileName(self,
          "%s -- Choose new file"%QApplication.applicationName(),
                                          ".", "*.txt")
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
                                  "BookEntry v%s - %s" % (__version__, name),
                                  None, QApplication.UnicodeUTF8))




   def EntryToDisplay(self, entry):
      """Given an entry, display the parts on the GUI display."""

      # AJB number
      a = entry['Num']
      self.volNum.setText(str(a['volNum']))
      self.secNum.setText(str(a['sectionNum']))
      if int(a['subsectionNum']) > -1:
         self.subSecNum.setText(str(a['subsectionNum']))
      else:
         self.subSecNum.setText('0')
      self.itemNum.setText(str(a['entryNum']))

      # Authors
      astr = ''
      if entry.notEmpty('Authors'):
         a = entry['Authors']
         if a:
            first = True
            for b in a:
               if not first:
                  astr += '\n'
               first = False
               astr += b.full_name
      self.authorEntry.setText(astr)

      # Title
      astr = ''
      if entry.notEmpty('Title'):
         astr += entry['Title']
      self.titleEntry.setText(astr)

      # Publishers
      astr = ''
      if entry.notEmpty('Publishers'):
         first = True
         for a in entry['Publishers']:
            if not first:
               astr += '\n'
            first = False
            astr += a['Place'] + ' : ' + a['PublisherName']
      self.publEntry.setText(astr)

      # Year
      astr = ''
      if entry.notEmpty('Year'):
         astr += entry['Year']
      self.yearEntry.setText(astr)

      # Pagination
      astr = ''
      if entry.notEmpty('Pagination'):
         astr += entry['Pagination']
      self.pageEntry.setText(astr)

      # Price
      astr = ''
      if entry.notEmpty('Price'):
         astr += entry['Price']
      self.priceEntry.setText(astr)

      # Review
      astr = ''
      if entry.notEmpty('Reviews'):
         rev = entry['Reviews']
         if rev:
            for item in rev:
               astr += item + '\n'
      self.reviewsEntry.setPlainText(astr)

      # Language
      astr = ''
      if entry.notEmpty('Language'):
         astr += entry['Language']
      self.tolangEntry.setText(astr)

      # fromLanguage
      astr = ''
      if entry.notEmpty('TranslatedFrom'):
         astr += entry['TranslatedFrom']
      self.fromlangEntry.setText(astr)

      # Translators
      astr = ''
      if entry.notEmpty('Translators'):
         a = entry['Translators']
         if a:
            first = True
            for b in a:
               if not first:
                  astr += '\n'
               first = False
               astr += b.full_name
      self.translatorEntry.setText(astr)

      # Compilers
      astr = ''
      if entry.notEmpty('Compilers'):
         a = entry['Compilers']
         if a:
            first = True
            for b in a:
               if not first:
                  astr += '\n'
               first = False
               astr += b.full_name
      self.compilersEntry.setText(astr)

      # Contributors
      astr = ''
      if entry.notEmpty('Contributors'):
         a = entry['Contributors']
         if a:
            first = True
            for b in a:
               if not first:
                  astr += '\n'
               first = False
               astr += b.full_name
      self.contribEntry.setText(astr)


      # Others
      astr = ''
      if entry.notEmpty('Others'):
         a = entry['Others']
         first = True
         for b in a:
            if not first:
               astr += '\n'
            first = False
            astr += b
      self.commentsEntry.setPlainText(astr)

   def DisplayToEntry(self, entry):
      """Copy the display into entry"""
      pass


   def insertChar(self, obj):
      """Insert the charactor in obj[0] with self.insertFunc
      if insertFunc is not None."""

      char = obj[0]
      # invoke self.insertFunc(char)
      if self.insertFunc is not None:
         self.insertFunc(char)

      #print('BookEntry insertChar got %s'% (char))

   def setInsertFunc(self, oldWidget, nowWidget ):
      """For items in setTextEntryList and setLineEntryList
      set insertFunc to be either insertPlainText or insert."""

      if nowWidget is None:
         pass
      elif self.setTextEntryList.count(nowWidget.objectName()):
         self.insertFunc = nowWidget.insertPlainText
      elif self.setLineEntryList.count(nowWidget.objectName()):
         self.insertFunc = nowWidget.insert
      elif self.noEntryList.count(nowWidget.objectName()):
         self.insertFunc = None


   #
   # Help menu functions
   #
   def helpAbout(self):
      QMessageBox.about(self, 'About BookEntry',
                """<b>AJB Book Entry</b> v {0}
                <p>Author: J. R. Fowler
                <p>Copyright &copy; 2012
                <p>All rights reserved.
                <p>This application is used to create and visualize
                the text files with the books found in
                the annual bibliographies of <b>Astronomische Jahrberichts</b>.
                <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(
            __version__, platform.python_version(),
            QT_VERSION_STR, PYQT_VERSION_STR,
            platform.system()))




#
# Parse the command line arguments
#
def getargs():
   parser = argparse.ArgumentParser(description='Create or edit an ajb??_books.txt file')

   parser.add_argument('-v', '--verbose',
                       help='provide verbose output,',
                       action='store_true')
   parser.add_argument( '-i', '--input', type=str,
                        help='read the file INPUT for entries',
                        action='append')
   #parser.add_argument('-p', '--plot',
   #                    help='plot the output, theta vs phi and theta/phi vs rho when done,',
   #                    action='store_true')
   #parser.add_argument( '-t', '--title', type=str,
   #                     help='the name of the file to process.',
   #                     action='append')
   #parser.add_argument( 'filename', type=str,
   #                     help='the name of the file to process.',
   #                     action='append')

   args = parser.parse_args()

   return args


#
# The main body
#

if __name__ == '__main__':

   args = getargs()

   app = QApplication(sys.argv)
   app.setApplicationName('Book Entry')
   form = BookEntry()
   QObject.connect(app, SIGNAL("focusChanged(QWidget *, QWidget *)"), 
                   form.setInsertFunc)
   if args.input is not None:
      form.openFile(args.input[0])
   form.show()
   sys.exit(app.exec_())



