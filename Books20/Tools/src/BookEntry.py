#! /usr/bin/env python3
# -*- mode: Python;-*-

"""AJB/AAA dialog to review books entries
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
from entry import *
from menus import *

__version__ = '0.1'

class BookEntry( QMainWindow, ui_BookEntry.Ui_MainWindow ):
   """BookEntry is the class which handles the BookEntry form
   for display of entries from the text files.
   """
   def __init__( self, parent=None ):
      super(BookEntry, self).__init__(parent)
      self.setupUi(self)
      self.curRecord = 0
      self.maxRecord = 0
      self.entList = []
      createMenus(self, self.menubar)

      self.connect(self.quitButton, SIGNAL('released()'), self.quit )
   #
   # Menu slots
   #
   def quit(self):
       self.close()

   def openNew(self):
       pass

   def openFile(self):
      fname = QFileDialog.getOpenFileName(self,
                                          "%s -- Choose new file" \
                                          % QApplication.applicationName(),
                                          ".", "*.txt")
      if fname:
         self.GetRecords(fname)


   def saveFile(self):
      pass

   def saveFileAs(self):
      pass

   def printEntry(self):
      pass

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

   #
   # Methods to deal with the records.
   #
   def GetRecords(self, fname=None):
      """open the named file, get records into list
      set maxRecords
      if successful
      show record 1

      change current working file name to basename
      """
      if not os.path.isfile(fname):
         self.statusbar.showMessage('Invalid file')
         return

      self.statusbar.clearMessage()

      # if we have a good file, then clear the entlist
      self.entList = []
      entTemp = AJBentry()
      count = 0

      for line in fileinput.input([fname]):
         line = line.strip()
         try:
            entTemp.extract(line)
         except:
            print(line + '\n')
            traceback.print_exc()
            print('\n\n')


         if entTemp.isValid():
            count += 1
            self.entList.append(entTemp)
            entTemp = AJBentry()
      
      self.maxRecord = count
      tlist = os.path.basename(fname)
      self.setWinTitle(tlist)
      self.statusbar.showMessage(tlist)
      if 0 != count:
         self.showRecord(0)
      else:
         self.statusbar.showMessage('Invalid file: no entries')

   def on_prevButton_released(self):
      self.showRecord(self.curRecord - 1)

   def on_nextButton_released(self):
      self.showRecord(self.curRecord + 1)

   def showRecord(self, recnum=0):
      """showRecord(recnum) where 0 <= recnum < maxRecords.
      recnum is the index into the entry list, the displayed
      value will be (recnum + 1).  The buttons will wrap around
      the index values.
      """
      self.prevButton.setEnabled(True)
      self.nextButton.setEnabled(True)

      if recnum < 0:
         # We add here because recnum is negative already
         self.curRecord = self.maxRecord + recnum
      elif recnum >= self.maxRecord:
         self.curRecord = recnum - self.maxRecord
      else:
         self.curRecord = recnum

      # Display record count
      #self.lblRecordCount.setText( 'Record %d of %d' % (self.curRecord + 1, self.maxRecord))

      # Display the actual entry data
      displayEnt = self.entList[self.curRecord]

      self.indexLabel.setText('Index - %s' % str(self.curRecord+1))
      #self.lblAJBnum.setText(displayEnt.numStr())

      a = displayEnt['Authors']
      if a:
         self.authorEntry.setText(a[0].full_name)
      else:
         self.authorEntry.setText(" ")

      self.titleEntry.setText(displayEnt['Title'])
      self.yearEntry.setText(displayEnt['Year'])
      self.placeEntry.setText(displayEnt['Publishers'][0]['Place'])
      self.publEntry.setText(displayEnt['Publishers'][0]['PublisherName'])
      self.pageEntry.setText(displayEnt['Pagination'])
      self.priceEntry.setText(displayEnt['Price'])
      rev = displayEnt['Reviews']
      revstr = ''
      if rev:
         for item in rev:
            revstr = revstr + item + '\n'
         self.reviewsEntry.setPlainText(revstr)
      self.commentsEntry.setPlainText(displayEnt['Comments'])


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



