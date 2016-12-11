"""A window for editing the header section of bookfiles.

Close button asks to save if file is dirty,
Save button saves header text to local bookfile,
Cancel button revert to header text from last save.

All text work done through the intermediate bookfile.
Need to explicitly save this bookfile to disk in order
to save your changed permenantly
"""
try:
    from PyQt5.QtCore import *
    from PyQt5.QtGui  import *
    from PyQt5.QtWidgets import *
except:
    from PyQt4.QtCore import *
    from PyQt4.QtGui  import *

import bookentry.ui_HeaderEntry as ui_HeaderEntry

class HeaderWindow(QDialog, ui_HeaderEntry.Ui_HeaderEdit):
    def __init__(self, bf=None):
        super(HeaderWindow, self).__init__()

        self.setupUi(self)
        self.setBookFile(bf)

        self.headerEntry.textChanged.connect(self.setDirty)
        self.closeButton.released.connect(self.AskAndClose)
        self.saveButton.released.connect(self.saveHeaderText)
        self.cancelButton.released.connect(self.RevertHeader)


    def setFileName(self, file):
        self.setWindowTitle('Edit Header - %s'%file)

    def setBookFile(self, bf):
        self.bookfile = bf

    def saveHeaderText(self):
        if self.bookfile:
            self.bookfile.setHeader(self.getHeaderText())
            self.clearDirty()

    def AskAndClose(self):
        if self.isDirty() == True:
            resp = QMessageBox.warning(self, "Warning",
             '''The header has been modified\n
                Do you want to save your changes?''',
                                             QMessageBox.Save,
                                             QMessageBox.Discard,
                                             QMessageBox.Cancel )
            if resp == QMessageBox.Save:
                self.SaveClose()
            elif resp == QMessageBox.Discard:
                self.noSaveClose()
            elif resp == QMessageBox.Cancel:
                return
        else:
            self.close()
 
    def SaveClose(self):
        self.saveHeaderText()
        self.close()

    def RevertHeader(self):
        # restore the current header before closing
        self.setHeaderText(self.bookfile.getHeader())

    def noSaveClose(self):
        self.close()
    
    def setDirty(self):
        self.saveButton.enable = True
        self.dirty = True

    def clearDirty(self):
        self.saveButton.enable = False
        self.dirty = False

    def isDirty(self):
        return self.dirty

    def setHeaderText(self, textstr):
        self.headerEntry.setPlainText(textstr)
        self.clearDirty()

    def getHeaderText(self):
        return self.headerEntry.toPlainText()


#
# Test functions
#
def main():

    import sys

    app = QApplication(sys.argv)
    ex = HeaderWindow()
    bf = BookFile()
    ex.setBookFile(bf)
    ex.setHeaderText(bf.getHeader())
    ex.show()
    app.exec_()

    print('The Header is:\n')
    print(bf.getHeader())

if __name__ == '__main__':
    import sys
    from bookfile import *
    main()

