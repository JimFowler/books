"""A window for viewing the original string entry
if it exists.
"""

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import bookentry.ui_OrigStr as ui_OrigStr

class OrigStrWindow(QDialog, ui_OrigStr.Ui_origstrDialog):
    def __init__(self, str=None):
        super(OrigStrWindow, self).__init__()

        self.setupUi(self)

        self.closeButton.released.connect(self.Close)

    def Close(self):
        self.close()

    def setFileName(self, num):
        self.setWindowTitle('Original String - Entry %s'%str(num))

    def setOrigStrText(self, textstr):
        self.textEdit.setPlainText(textstr)

    def getOrigStrText(self):
        return self.textEdit.toPlainText()


#
# Test functions
#
def main():

    import sys

    app = QApplication(sys.argv)
    ex = OrigStrWindow()
    ex.setFileName('52')
    ex.setOrigStrText('This is the display dialog for the original entry string')
    ex.show()
    app.exec_()


if __name__ == '__main__':
    import sys
    main()

