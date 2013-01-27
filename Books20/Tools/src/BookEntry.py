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
      self.bf.setFileName('document1')
      self.setWinTitle('document1')

      createMenus(self, self.menubar)

      self.connect(self.quitButton, SIGNAL('released()'), self.quit )
      self.connect(self.newEntryButton, SIGNAL('released()'), self.newEntry )
      self.connect(self.acceptButton, SIGNAL('released()'), self.clearEntryDirty )


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
       self.close()

   def openNew(self):
      # check if entry or bookFile is dirty
      # save if neccessary
      # create empty bookFile
      # create new entry
      if self.tmpEntryDirty:
         print('entry dirty')

   def openFile(self):
      # check for dirty file before overwriting
      if self.bf.isDirty():
         self.statusbar.showMessage('WARNING: dirty file entry!')
      

      fname = QFileDialog.getOpenFileName(self,
          "%s -- Choose new file"%QApplication.applicationName(),
                                          ".", "*.txt")
      if fname:
         self.maxEntryNum = self.bf.readFile(fname)
         if self.maxEntryNum:
            self.statusbar.clearMessage()
            self.statusbar.showMessage('%d records found'%self.maxEntryNum, 6000)
            self.ofnumLabel.setText('of %d'%self.maxEntryNum)
            self.showEntry(1)
         else:
            self.statusbar.showMessage('No records found')
         self.setWinTitle(self.bf.getBaseName())


   def saveFile(self):
      # check if entry is dirty
      # call bf.writeFile
      pass

   def saveFileAs(self):
      # check if entry is dirty
      # get new filename
      # bf.setFileName
      # bf.writeFile
      pass

   def printEntry(self):
      pass

   def openSymbol(self):
      self.symbolTable = SymbolForm('./symbols.txt', 'FreeSans', 12)
      self.symbolTable.show()
      self.connect(self.symbolTable, SIGNAL('sigClicked'),
                   self.insertChar )

   def editHeader(self):
      self.headerWindow = HeaderWindow(self)
      self.headerWindow.setBookFile(self.bf)
      self.headerWindow.setWindowTitle(QApplication.translate("headerWindow", 
                                  "Edit Headers - %s" % (self.bf.getBaseName()),
                                  None, QApplication.UnicodeUTF8))
      self.headerWindow.setHeaderText(self.bf.getHeader())
      self.headerWindow.show()

   def on_prevButton_released(self):
      self.showEntry(self.curEntryNum - 1)

   def on_nextButton_released(self):
      self.showEntry(self.curEntryNum + 1)

   def saveEntry(self):
      pass

   def newEntry(self):
      if self.tmpEntryDirty:
         print('entry dirty')

   def setEntryDirty(self):
      self.tmpEntryDirty = True

   def clearEntryDirty(self):
      self.tmpEntryDirty = False


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



   def EntryToDisplay(self, displayEnt):
      """Given an entry, display the parts on the GUI display."""

      # AJB number
      a = displayEnt['Num']
      self.volNum.setText(str(a['volNum']))
      self.secNum.setText(str(a['sectionNum']))
      if int(a['subsectionNum']) > -1:
         self.subSecNum.setText(str(a['subsectionNum']))
      else:
         self.subSecNum.setText('0')
      self.itemNum.setText(str(a['entryNum']))

      # Authors
      astr = ''
      if displayEnt.notEmpty('Authors'):
         a = displayEnt['Authors']
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
      if displayEnt.notEmpty('Title'):
         astr += displayEnt['Title']
      self.titleEntry.setText(astr)

      # Publishers
      astr = ''
      if displayEnt.notEmpty('Publishers'):
         first = True
         for a in displayEnt['Publishers']:
            if not first:
               astr += '\n'
            first = False
            astr += a['Place'] + ' : ' + a['PublisherName']
      self.publEntry.setText(astr)

      # Year
      astr = ''
      if displayEnt.notEmpty('Year'):
         astr += displayEnt['Year']
      self.yearEntry.setText(astr)

      # Pagination
      astr = ''
      if displayEnt.notEmpty('Pagination'):
         astr += displayEnt['Pagination']
      self.pageEntry.setText(astr)

      # Price
      astr = ''
      if displayEnt.notEmpty('Price'):
         astr += displayEnt['Price']
      self.priceEntry.setText(astr)

      # Review
      astr = ''
      if displayEnt.notEmpty('Reviews'):
         rev = displayEnt['Reviews']
         if rev:
            for item in rev:
               astr += item + '\n'
      self.reviewsEntry.setPlainText(astr)

      # Language
      astr = ''
      if displayEnt.notEmpty('Language'):
         astr += displayEnt['Language']
      self.tolangEntry.setText(astr)

      # fromLanguage
      astr = ''
      if displayEnt.notEmpty('TranslatedFrom'):
         astr += displayEnt['TranslatedFrom']
      self.fromlangEntry.setText(astr)

      # Translators
      astr = ''
      if displayEnt.notEmpty('Translators'):
         a = displayEnt['Translators']
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
      if displayEnt.notEmpty('Compilers'):
         a = displayEnt['Compilers']
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
      if displayEnt.notEmpty('Contributors'):
         a = displayEnt['Contributors']
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
      if displayEnt.notEmpty('Others'):
         a = displayEnt['Others']
         first = True
         for b in a:
            if not first:
               astr += '\n'
            first = False
            astr += b
      self.commentsEntry.setPlainText(astr)

   def DisplayToEntry(self):
      """Copy the display into the tmpEntry"""
      pass


   def saveEntry(self):
      # save the tmpEntry to the bookFile
      pass

   def insertChar(self, obj):
      char = obj[0]
      print('BookEntry insertChar got %s'% (char))

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



if __name__ == '__main__':
   app = QApplication(sys.argv)
   app.setApplicationName('Book Entry')
   form = BookEntry()
   form.show()
   sys.exit(app.exec_())
   
#
# Parse the command line arguments
#
parser = argparse.ArgumentParser(description='Reduce a rho mount model data file\
 and provide a correction file suitable for adding to Tcs.')

parser.add_argument('-v', '--verbose', help='provide verbose output,', action='store_true')
parser.add_argument('-p', '--plot',
                    help='plot the output, theta vs phi and theta/phi vs rho when done,',
                    action='store_true')
parser.add_argument( '-t', '--title', type=str,
                     help='the name of the file to process.',
                     action='append')
parser.add_argument( '-o', '--output', type=str,
                     help='write the model to file name, instead of stdout',
                     action='append')
parser.add_argument( 'filename', type=str, help='the name of the file to process.')

args = parser.parse_args()

if args.title != None:
    title = args.title[0]
else:
    title = args.filename

if args.output != None:
    fp = open(args.output[0], 'w')
else:
    fp = sys.stdout



