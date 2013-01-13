from PyQt4.QtCore import *
from PyQt4.QtGui  import *

from ui_HeaderEntry import *

class HeaderEdit(QDialog, Ui_HeaderEdit):

    def __init__(self, parent=None):
        super(HeaderEdit, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    app.setApplicationName('Book Entry')
    form = HeaderEdit()
    form.show()
    sys.exit(app.exec_())
   
    
