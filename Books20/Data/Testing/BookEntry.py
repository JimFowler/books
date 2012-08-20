"""AJB/AAA dialog to review books entries
"""

import sys
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
      note that os.path.basename() doesn't work on RedHat
      nor does os.path.split()
      """
      if not os.path.isfile(fname):
         self.lblFileName.setText('Invalid file')
         return

      entTemp = AJBentry()
      count = 0

      for line in fileinput.input([fname]):
         line = line.decode('UTF-8').strip()
         entTemp.extract(line)

         if entTemp.isValid():
            count += 1
            self.entList.append(entTemp)
            entTemp = AJBentry()
      
      self.maxRecord = count
      tlist = fname.split('/')  # unix systems only
      self.lblFileName.setText(tlist[-1])
      if 0 != count:
         self.showRecord(0)
      else:
         self.lblFileName.setText('Invalid file: no entries')

   def on_btnPrevious_released(self):
      self.curRecord -= 1
      self.showRecord(self.curRecord)

   def on_btnNext_released(self):
      self.curRecord += 1
      self.showRecord(self.curRecord)


   def showRecord(self, recnum=0):
      """showRecord(recnum) where 0 <= recnum < maxRecords.
      recnum is the index into the entry list, the displayed
      value will be (recnum + 1).
      """
      self.curRecord = recnum
      if self.curRecord <= 0:
         self.curRecord = 0
         self.btnPrevious.setEnabled(False)
      else:
         self.btnPrevious.setEnabled(True)

      if self.curRecord >= self.maxRecord:
         self.curRecord = self.maxRecord - 1
         self.btnNext.setEnabled(False)
      else:
         self.btnNext.setEnabled(True)

      self.lblRecordCount.setText( 'Record %d of %d' % (self.curRecord + 1, self.maxRecord))

      #print 'Showing record number %d (somehow...)' % self.curRecord
      displayEnt = self.entList[recnum]
      self.lblAJBnum.setText(displayEnt.numStr())
      self.lblTitle.setText(displayEnt.getval('Title'))
      self.lblItem.setText(displayEnt.getval('Index'))
      self.lblYear.setText(displayEnt.getval('Year'))
      self.lblPageCnt.setText(displayEnt.getval('Pagination'))
      self.lblPrice.setText(displayEnt.getval('Price'))
      a = displayEnt.getval('Authors')
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
   
