# -*- mode: Python;-*-

"""AJB/AAA dialog to review and edit books entries
"""

import platform
import fileinput
import sys, traceback
import re

# Trouble shooting assistance
from pprint import *
pp = PrettyPrinter()

from PyQt5.QtCore import *
from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *
   
from nameparser import HumanName

import bookentry.ui_BookEntry as ui_BookEntry
import bookentry.bookfile as bf
import bookentry.menus as menus
import bookentry.headerWindow as hw
import bookentry.AJBentry as AJBentry
import bookentry.symbol as symbol
import bookentry.origstrWindow as origstr
import bookentry.entryselect as es


import os
__dirName, __basename  = os.path.split(symbol.__file__)
__DefaultSymbolTableName__ = __dirName + '/symbols.txt'
del __dirName
del __basename

__version__ = '2.0'


class BookEntry( QMainWindow, ui_BookEntry.Ui_MainWindow ):
   """BookEntry is the class which handles the BookEntry form
   for display of entries from the text files.
   """
   def __init__( self, parent=None ):
      super(BookEntry, self).__init__(parent)
      self.setupUi(self)

      self.tmpEntry = AJBentry.AJBentry()
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
      self.defaultVolumeNumber = None
      self.symbolTableName = __DefaultSymbolTableName__

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

      menus.createMenus(self, self.menubar)

      self.quitButton.released.connect( self.quit )
      self.newEntryButton.released.connect( self.newEntry )
      self.acceptButton.released.connect( self.saveEntry )
      self.deleteButton.released.connect( self.deleteEntry )
      self.insertButton.released.connect( self.askInsertEntry )
      self.acceptButton.setEnabled(False)
      self.deleteButton.setEnabled(False)
      self.insertButton.setEnabled(False)

      self.indexEntry.returnPressed.connect( self.indexChanged)

      self.volNum.textChanged.connect( self.setEntryDirty)
      self.secNum.textChanged.connect( self.setEntryDirty)
      self.subSecNum.textChanged.connect( self.setEntryDirty)
      self.itemNum.textChanged.connect( self.setEntryDirty)
      self.authorEntry.textChanged.connect( self.setEntryDirty)
      self.editorEntry.textChanged.connect( self.setEntryDirty)
      self.titleEntry.textChanged.connect( self.setEntryDirty)
      self.publEntry.textChanged.connect( self.setEntryDirty)
      self.editionEntry.textChanged.connect( self.setEntryDirty)
      self.yearEntry.textChanged.connect( self.setEntryDirty)
      self.pageEntry.textChanged.connect( self.setEntryDirty)
      self.priceEntry.textChanged.connect( self.setEntryDirty)
      self.reviewsEntry.textChanged.connect( self.setEntryDirty)
      self.reprintEntry.textChanged.connect( self.setEntryDirty)
      self.referenceEntry.textChanged.connect( self.setEntryDirty)
      self.fromlangEntry.textChanged.connect( self.setEntryDirty)
      self.tolangEntry.textChanged.connect( self.setEntryDirty)
      self.translatorEntry.textChanged.connect( self.setEntryDirty)
      self.compilersEntry.textChanged.connect( self.setEntryDirty)
      self.contribEntry.textChanged.connect( self.setEntryDirty)
      self.commentsEntry.textChanged.connect(self.setEntryDirty)

      self.openNewFile()

   def setMaxEntryNumber(self, n):
      if n < 0:
         n = 0
      self.maxEntryNumber = n

      if self.maxEntryNumber == 0:
         self.prevButton.setEnabled(False)
         self.nextButton.setEnabled(False)
      else :
         self.prevButton.setEnabled(True)
         self.nextButton.setEnabled(True)

      self.ofnumLabel.setText('of %d'%self.maxEntryNumber)

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

   def askOpenFile(self):
      """Open an existing file saving the old one if it is dirty."""
      if self.askSaveEntry() == QMessageBox.Cancel:
         return

      if self.askSaveFile() == QMessageBox.Cancel:
         return

      # else get a file name 
      fname, filterA = QFileDialog.getOpenFileName(self,
          "%s -- Choose new file"%QApplication.applicationName(),
                            self.bf.getDirName(), "All Files (*.*);;Text Files (*.txt);;XML Files (*.xml)")
      if fname:
         name, ext = os.path.splitext(fname)
         if ext == '':
            if filterA == 'XML Files (*.xml)':
               fname += '.xml'
            else:
               fname +='.txt'
               
         self.openFile(fname)

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
      self.setWinTitle(self.bf.getBaseNameWithExtension())


   def saveFile(self):
      """Ignore dirty entries and just save the file."""

      if self.bf.getFileName() is None or self.bf.getBaseName() == 'document1':
         if self.saveFileAs() == QMessageBox.Cancel:
            return QMessageBox.Cancel

      self.bf.writeFile()

      self.statusbar.showMessage('Saving file ' + self.bf.getBaseNameWithExtension())
      QTimer.singleShot(10000, self.statusbar.clearMessage  )

      return QMessageBox.Save


   def saveFileAs(self):
      """Ignore dirty entries and save the file as..."""
      fname, filterA = QFileDialog.getSaveFileName(self,
          "%s -- Choose file"%QApplication.applicationName(),
                                             self.bf.getDirName(),
           "All Files (*.*);;Text Files (*.txt);;XML Files (*.xml)")

      if fname:
         name, ext = os.path.splitext(fname)
         if ext == '':
            if filterA == 'XML Files (*.xml)':
               fname += '.xml'
            else:
               fname +='.txt'
               
         self.bf.writeFile(fname)
         self.setWinTitle(self.bf.getBaseNameWithExtension())
         return QMessageBox.Save
      else:
         return QMessageBox.Cancel
         

   #
   # Menu and button slots for Entry Actions on File menu
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
      self.entrySelect.lineEmit.connect( self.insertEntry )

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
                                 QMessageBox.Ok| QMessageBox.Cancel )
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
   #
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
      self.symbolTable.sigClicked.connect( self.insertChar )

   def setSymbolTableName(self, name):
      """Set the name of the symbol table to use in place of the
      default table."""
      self.symbolTableName = name

   def editHeader(self):
      """Open the edit header form."""
      self.headerWindow = hw.HeaderWindow(self)
      self.headerWindow.setBookFile(self.bf)
      self.headerWindow.setWindowTitle(QApplication.translate("headerWindow", 
                                  "Edit Headers - %s" % (self.bf.getBaseNameWithExtension()), None))
      self.headerWindow.setHeaderText(self.bf.getHeader())
      self.headerWindow.show()

   def showOrigStr(self):
      """Open a dialog box with the original string entry."""
      self.origstrWindow = origstr.OrigStrWindow()

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
                                    QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                                    QMessageBox.Save)

         if ans == QMessageBox.Save:
            self.saveEntry()

      return ans

   def askSaveFile(self):
      """Ask if we should save the dirty file."""
      ans = None
      if self.bf.isDirty():
         ans = QMessageBox.warning( self, 'Save file?',
                                    'The File has changed. Do you want to save it?',
                                    QMessageBox.Save|QMessageBox.Discard|QMessageBox.Cancel )

         if ans == QMessageBox.Save:
            ans = self.saveFile()
            # set save file menu enable to False

      return ans


   #
   # Methods to deal with various display aspects
   #
   def setWinTitle( self, name ):
      """Creates the string 'BookEntry vx.x - name' and
      places it into the window title.
      """
      #self.setWindowTitle(QApplication.translate("MainWindow", 
      #                            "AJB Book Entry  v %s   -   %s" % (__version__, name),
      #                            None, QApplication.UnicodeUTF8))
      self.setWindowTitle(QApplication.translate("MainWindow", 
                                  "AJB Book Entry  v %s   -   %s" % (__version__, name),
                                  None))

   def setDefaultVolumeNumber(self, num):
      """Sets the default volume number for new entries."""
      self.defaultVolumeNumber = num

   def setVolumeNumberInteractive(self):
      """Provides an interactive dialog to set the default
      volume number for new entries."""
      curVal = self.defaultVolumeNumber
      numVal, ok = QInputDialog.getText(self, 'Volume Number',
                                   'Enter New Volume Number\n(next new entry will use this value)',
                                   text=curVal )
      if ok:
         self.defaultVolumeNumber = numVal


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
      self.itemNum.setText(str(a['entryNum']) + a['entrySuf'])

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
               astr += str(b)
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
               astr += str(b)
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
               astr += str(b)
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
               astr += str(b)
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
               astr += str(b)
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

      # Note: that this regex will silently reject a suffix
      #     that is not '' or [a-c].
      r2 = re.compile(r'(\d+)([a-c]{0,1})', re.UNICODE)
      items = r2.split(self.itemNum.text().strip())

      entry = AJBentry.AJBentry()

      # Index
      index = int(self.indexEntry.text())
      try:
         entry['Index'] = str(index - 1)
      except:
         exc_type, exc_value, exc_traceback = sys.exc_info()
         tb = traceback.format_tb(exc_traceback)
         tb_str = ''
         for s in tb:
            tb_str = tb_str + s
         tb_str = tb_str + '\n\n Invalid Index number'
         QMessageBox.warning(self, 'Invalid Index Num', tb_str, QMessageBox.Ok)
         return None

      # AJB number
      num = {}
      num['volume'] = 'AJB'
      
      try:
         num['volNum'] = int(self.volNum.text())
         num['sectionNum'] = int(self.secNum.text())
         num['subsectionNum'] = int(self.subSecNum.text())
         num['entryNum'] = int(items[1])
         num['entrySuf'] = items[2]
      except:
         exc_type, exc_value, exc_traceback = sys.exc_info()
         tb = traceback.format_tb(exc_traceback)
         tb_str = ''
         for s in tb:
            tb_str = tb_str + s
         tb_str = tb_str + '\n\n Invalid AJB Entry number'
         QMessageBox.warning(self, 'Invalid AJB Num', tb_str, QMessageBox.Ok)
         return None
         
      entry['Num'] = num
      if not entry.isValidAjbNum():
         QMessageBox.warning(self, 'Invalid number',
                             'Entry must have a valid AJB num in order to be valid',
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
            try:
               place, publisher = line.split(':')
            except:
               #warn that there is no title
               QMessageBox.warning( self, 'No Colon in publishing',
                                    'Publishing field must be Place : PublisherName.\nColon is missing.',
                                    QMessageBox.Ok)
               return None
               
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
      # take back focus somehow??

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
   def helpString(self):
      helpStr = """<b>AJB Book Entry</b> v {0}
      <p>Author: J. R. Fowler
      <p>Copyright &copy; 2012-2017
      <p>All rights reserved.
      <p>This application is used to create and visualize
      the text files with the books found in the annual
      bibliographies of <b>Astronomischer Jahresbericht</b>.
      <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(
         __version__, platform.python_version(),
         QT_VERSION_STR, PYQT_VERSION_STR,
         platform.system())

      return helpStr
      
   def helpAbout(self):
      hstr = self.helpString()
      QMessageBox.about(self, 'About BookEntry', hstr )





#
# Test routine
#

if __name__ == '__main__':

   import sys

   app = QApplication(sys.argv)
   app.setApplicationName('Book Entry')
   form = BookEntry()
   app.focusChanged.connect(form.setFocusChanged)

   form.show()
   sys.exit(app.exec_())



