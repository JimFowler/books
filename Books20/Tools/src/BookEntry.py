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

# Trouble shooting assistance
from pprint import *
pp = PrettyPrinter()

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

from nameparser import HumanName
import ui_BookEntry
from bookfile import *
from menus import *
from headerWindow import *
from AJBentry import *
from symbol import *
from origstrWindow import *

__version__ = '1.0'


class BookEntry( QMainWindow, ui_BookEntry.Ui_MainWindow ):
   """BookEntry is the class which handles the BookEntry form
   for display of entries from the text files.
   """
   def __init__( self, parent=None ):
      super(BookEntry, self).__init__(parent)
      self.setupUi(self)

      self.tmpEntry = AJBentry()
      self.tmpEntryDirty = False

      self.curEntryNumber = 0
      self.maxEntryNumber = 0
      self.bf = BookFile()
      self.setWinTitle('document1')
      self.insertFunc = None
      self.defaultVolumeNumber = None

      # Fields within an Entry that we know about already
      self.knownEntryFields = ['Index', 'Num', 'Authors', 'Editors', 'Title',
                               'Publishers', 'Edition', 'Year',
                               'Pagination', 'Price', 'Reviews',
                               'Compilers', 'Contributors', 'Translators',
                               'Language', 'TranslatedFrom', 'Reference',
                               'Reprint', 'Others', 'OrigStr', 'Comments', ]

      # lists of which display fields may or may not have symbol entry allowed
      self.noEntryList = ['volNum', 'secNum', 'subSecNum', 'itemNum',
                          'yearEntry', 'pageEntry', 'indexEntry',
                          'editionEntry', 'referenceEntry', 'reprintEntry']
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

      self.connect(self.indexEntry, SIGNAL('returnPressed()'), self.indexChanged)

      self.connect(self.volNum, SIGNAL('textChanged(QString)'), self.setEntryDirty)
      self.connect(self.secNum, SIGNAL('textChanged(QString)'), self.setEntryDirty)
      self.connect(self.subSecNum, SIGNAL('textChanged(QString)'), self.setEntryDirty)
      self.connect(self.itemNum, SIGNAL('textChanged(QString)'), self.setEntryDirty)
      self.connect(self.authorEntry, SIGNAL('textChanged()'), self.setEntryDirty)
      self.connect(self.editorEntry, SIGNAL('textChanged()'), self.setEntryDirty)
      self.connect(self.titleEntry, SIGNAL('textChanged()'), self.setEntryDirty)
      self.connect(self.publEntry, SIGNAL('textChanged()'), self.setEntryDirty)
      self.connect(self.editionEntry, SIGNAL('textChanged(QString)'), self.setEntryDirty)
      self.connect(self.yearEntry, SIGNAL('textChanged(QString)'), self.setEntryDirty)
      self.connect(self.pageEntry, SIGNAL('textChanged(QString)'), self.setEntryDirty)
      self.connect(self.priceEntry, SIGNAL('textChanged(QString)'), self.setEntryDirty)
      self.connect(self.reviewsEntry, SIGNAL('textChanged()'), self.setEntryDirty)
      self.connect(self.reprintEntry, SIGNAL('textChanged(QString)'), self.setEntryDirty)
      self.connect(self.referenceEntry, SIGNAL('textChanged(QString)'), self.setEntryDirty)
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
      """Open an existing file, get the count of entries,
      and display the first entry."""

      self.maxEntryNumber = self.bf.readFile(name)
      if self.maxEntryNumber:
         self.statusbar.clearMessage()
         self.statusbar.showMessage('%d records found'%self.maxEntryNumber, 6000)
         self.ofnumLabel.setText('of %d'%self.maxEntryNumber)
         self.showEntry(1)
         self.clearEntryDirty()
      else:
         self.statusbar.showMessage('No records found in file %s' % name)
      self.setWinTitle(self.bf.getBaseName())


   def saveFile(self):
      """Ignore dirty entries and just save the file."""
      #print("saving file %s"%self.bf.getFileName())
      if self.bf.getFileName() is None:
         self.saveFileAs()
      else:
         self.bf.writeFile()


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
         self.maxEntryNumber = self.curEntryNumber
         self.ofnumLabel.setText('of %d'%self.maxEntryNumber)
      self.clearEntryDirty()

   def newEntry(self):
      """Create a new entry, save the old one if it has been modified."""
      if self.askSaveEntry() == QMessageBox.Cancel:
         return

      self.tmpEntry = AJBentry()
      self.curEntryNumber = self.maxEntryNumber + 1
      self.tmpEntry['Index'] = self.curEntryNumber
      self.EntryToDisplay(self.tmpEntry)
      self.indexEntry.setText(str(self.curEntryNumber))
      if self.defaultVolumeNumber is not None:
         self.volNum.setText(self.defaultVolumeNumber)
      self.volNum.setFocus()
      self.clearEntryDirty()

   def showEntry(self, recnum=1):
      """showEntry(recnum) where 0 <= recnum < maxEntryNumber.
      recnum is the index into the entry list, the displayed
      value will be (recnum + 1).  The buttons will wrap around
      the index values.
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
      self.clearEntryDirty()

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
      """Open the symbol entry form."""
      self.symbolTable = SymbolForm('./symbols.txt', 'FreeSans', 14)
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

   def showOrigStr(self):
      """Open a dialog box with the original string entry."""
      self.origstrWindow = OrigStrWindow()

      if self.tmpEntry.notEmpty('Index'):
         self.origstrWindow.setFileName(self.tmpEntry['Index'])
      else:
         self.origstrWindow.setFileName(-1)
         
      if self.tmpEntry.notEmpty('OrigStr'):
         self.origstrWindow.setOrigStrText(self.tmpEntry['OrigStr'])
      else:
         self.origstrWindow.setOrigStrText('Entry does not have the original string defined.')
      self.origstrWindow.show()

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
                                  "BookEntry v%s - %s" % (__version__, name),
                                  None, QApplication.UnicodeUTF8))

   def setDefaultVolumeNumber(self, num):
      """Sets the default volume number for new entries."""
      self.defaultVolumeNumber = num


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

      # Editors
      astr = ''
      if entry.notEmpty('Editors'):
         a = entry['Editors']
         if a:
            first = True
            for b in a:
               if not first:
                  astr += '\n'
               first = False
               astr += b.full_name
      self.editorEntry.setText(astr)

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

      # Edition
      astr = ''
      if entry.notEmpty('Edition'):
         astr += entry['Edition']
      self.editionEntry.setText(astr)

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
         first = True
         if rev:
            for item in rev:
               if not first:
                  astr += '\n' 
               astr += item 
               first = False
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

      # Reprint
      astr = ''
      if entry.notEmpty('Reprint'):
         astr += entry['Reprint']
      self.reprintEntry.setText(astr)

      # Reference
      astr = ''
      if entry.notEmpty('Reference'):
         astr += entry['Reference']
      self.referenceEntry.setText(astr)


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


      for field in entry.keys():
         if self.knownEntryFields.count(field) == 0:
            QMessageBox.warning( self, 'Unknown Entry Field',
                                 'Unknown field "%s:  %s"\n in entry %s\n "'%
                                 (field, entry[field], entry['Index']),
                                 QMessageBox.Ok)
         
   def DisplayToEntry(self):
      """Copy the display into a new entry and
      return the entry."""

      entry = AJBentry()

      # Index
      index = int(self.indexEntry.text())
      entry['Index'] = str(index - 1)

      # AJB number
      num = {}
      num['volume'] = 'AJB'
      num['volNum'] = int(self.volNum.text())
      num['sectionNum'] = int(self.secNum.text())
      num['subsectionNum'] = int(self.subSecNum.text())
      num['entryNum'] = int(self.itemNum.text())
      entry['Num'] = num
      if not entry.isValidAjbNum():
         QMessageBox.warning(self, 'Invalid number',
                             'Entry must havea valid AJB num  in order to be valid',
                             QMessageBox.Ok)
         return None

      # Authors
      entrya = []
      a = self.authorEntry.toPlainText()
      if len(a) != 0:
         alist = a.split('\n')
         for line in alist:
            nm = HumanName(line)
            entrya.append(nm)
      entry['Authors'] = entrya

      # Editors
      entrya = []
      a = self.editorEntry.toPlainText()
      if len(a) != 0:
         alist = a.split('\n')
         for line in alist:
            nm = HumanName(line)
            entrya.append(nm)
      entry['Editors'] = entrya

      # Title
      a = self.titleEntry.toPlainText()
      if len(a) != 0:
         entry['Title'] = a
      else:
         #warn that there is no title
         QMessageBox.warning( self, 'No Title',
                              'Entry must have a title in order to be valid',
                              QMessageBox.Ok)
         return None

      # Publishers
      entrya = []
      a = self.publEntry.toPlainText()
      if len(a) != 0:
         alist = a.split('\n')
         for line in alist:
            nm = {}
            place, publisher = line.split(':')
            if not place:
               place = ''
            if not publisher:
               publisher = ''
            nm['Place'] = place.strip()
            nm['PublisherName'] = publisher.strip()
            entrya.append(nm )
      entry['Publishers'] = entrya

      # Edition
      a = self.editionEntry.text()
      if len(a) != 0:
         entry['Edition'] = a

      # Year
      a = self.yearEntry.text()
      if len(a) != 0:
         entry['Year'] = a

      # Pagination
      a = self.pageEntry.text()
      if len(a) != 0:
         entry['Pagination'] = a

      # Price
      a = self.priceEntry.text()
      if len(a) != 0:
         entry['Price'] = a

      # Review
      entrya = []
      a = self.reviewsEntry.toPlainText()
      if len(a) != 0:
         alist = a.split('\n')
         for line in alist:
            entrya.append(line)
      entry['Reviews'] = entrya

      # Language
      a = self.tolangEntry.text()
      if len(a) != 0:
         entry['Language'] = a 

      # fromLanguage
      a = self.fromlangEntry.text()
      if len(a) != 0:
         entry['TranslatedFrom'] = a

      # Translators
      entrya = []
      a = self.translatorEntry.toPlainText()
      if len(a) != 0:
         alist = a.split('\n')
         for line in alist:
            nm = HumanName(line)
            entrya.append(nm)
      entry['Translators'] = entrya

      # Compilers
      entrya = []
      a = self.compilersEntry.toPlainText()
      if len(a) != 0:
         alist = a.split('\n')
         for line in alist:
            nm = HumanName(line)
            entrya.append(nm)
      entry['Compilers'] = entrya

      # Contributors
      entrya = []
      a = self.contribEntry.toPlainText()
      if len(a) != 0:
         alist = a.split('\n')
         for line in alist:
            nm = HumanName(line)
            entrya.append(nm)
      entry['Contributors'] = entrya

      # Reprint
      a = self.reprintEntry.text()
      if len(a) != 0:
         entry['Reprint'] = a

      # Reference
      a = self.referenceEntry.text()
      if len(a) != 0:
         entry['Reference'] = a

      # Others
      entrya = []
      a = self.commentsEntry.toPlainText()
      if len(a) != 0:
         alist = a.split('\n')
         for line in alist:
            entrya.append(line)
      entry['Others'] = entrya

      return entry   


   def insertChar(self, obj):
      """Insert the charactor in obj[0] with self.insertFunc
      if insertFunc is not None."""

      char = obj[0]
      # invoke self.insertFunc(char)
      if self.insertFunc is not None:
         self.insertFunc(char)

      #print('BookEntry insertChar got %s'% (char))

   def setFocusChanged(self, oldWidget, nowWidget ):
      """For items in setTextEntryList and setLineEntryList
      set insertFunc to be either insertPlainText or insert."""

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

   parser.add_argument('-V', '--verbose',
                       help='provide verbose output,',
                       action='store_true')
   parser.add_argument( '-i', '--input', type=str,
                        help='read the file INPUT for entries',
                        action='append')
   parser.add_argument('-v', '--volume', type=str,
                       help='default volume number,',
                       action='append')
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
                   form.setFocusChanged)

   if args.volume is not None:
      form.setDefaultVolumeNumber(args.volume[0])
      form.newEntry()

   if args.input is not None:
      form.openFile(args.input[0])

   form.show()
   sys.exit(app.exec_())



