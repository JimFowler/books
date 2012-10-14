"""AJB/AAA dialog to review books entries
"""

import sys
import traceback
import os
import fileinput
from PyQt4.QtCore import *
from PyQt4.QtGui  import *
import ui_BookEntry
from entry import *

class BookEntry( QDialog, ui_BookEntry.Ui_BookEntry ):
   """BookEntry is the class which handles the BookEntry form
   for display of entries from the text files.
   """
   def __init__( self, parent=None ):
      super(BookEntry, self).__init__(parent)
      self.setupUi(self)
      self.curRecord = 0
      self.maxRecord = 0
      self.btnPrevious.setEnabled(False)
      self.btnNext.setEnabled(False)
      self.entList = []

   def on_btnGetNextFile_released(self):
      fname = QFileDialog.getOpenFileName(self,
                                          "%s -- Choose new file" \
                                          % QApplication.applicationName(),
                                          ".", "*.txt")
      if fname:
         self.GetRecords(fname)

   def GetRecords(self, fname=None):
      """open file, get records into list
      set maxRecords
      if successful
      show record 1

      change current working file name to basename
      """
      if not os.path.isfile(fname):
         self.lblFileName.setText('Invalid file')
         return

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
      self.lblFileName.setText(tlist)
      if 0 != count:
         self.showRecord(0)
      else:
         self.lblFileName.setText('Invalid file: no entries')

   def on_btnPrevious_released(self):
      self.showRecord(self.curRecord - 1)

   def on_btnNext_released(self):
      self.showRecord(self.curRecord + 1)


   def showRecord(self, recnum=0):
      """showRecord(recnum) where 0 <= recnum < maxRecords.
      recnum is the index into the entry list, the displayed
      value will be (recnum + 1).  The buttons will wrap around
      the index values.
      """
      self.btnPrevious.setEnabled(True)
      self.btnNext.setEnabled(True)

      if recnum < 0:
         # We add here because recnum is negative already
         self.curRecord = self.maxRecord + recnum
      elif recnum >= self.maxRecord:
         self.curRecord = recnum - self.maxRecord
      else:
         self.curRecord = recnum

      # Display record count
      self.lblRecordCount.setText( 'Record %d of %d' % (self.curRecord + 1, self.maxRecord))

      # Display the actual entry data
      displayEnt = self.entList[self.curRecord]
      self.lblAJBnum.setText(displayEnt.numStr())
      self.lblTitle.setText(displayEnt['Title'])
      self.lblItem.setText(displayEnt['Index'])
      self.lblYear.setText(displayEnt['Year'])
      self.lblPageCnt.setText(displayEnt['Pagination'])
      self.lblPrice.setText(displayEnt['Price'])
      rev = displayEnt['Reviews']
      revstr = ''
      if rev:
         for item in rev:
            revstr = revstr + item + '\n'
         self.teReviews.setPlainText(revstr)
      self.teComments.setPlainText(displayEnt['Comments'])
      a = displayEnt['Authors']
      if a:
         self.lblAuthor1.setText(a[0].full_name)
      else:
         self.lblAuthor1.setText(" ")

if __name__ == '__main__':
   app = QApplication(sys.argv)
   app.setApplicationName('Book Entry')
   form = BookEntry()
   form.show()
   app.exec_()
   
