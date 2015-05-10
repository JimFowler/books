"""Choose an entry from the list."""


from PyQt4.QtCore import *
from PyQt4.QtGui import *

import ui_EntrySelect as ui_EntrySelect

class EntrySelect(QDialog, ui_EntrySelect.Ui_ShortTitleDisplay):

    def __init__(self, parent=None, shortTitleList=None):
        super(EntrySelect, self).__init__()

        self.setupUi(self)

        self.redBkgd = QTextCharFormat()
        self.redBkgd.setBackground(QBrush(QColor("red")))

        self.whiteBkgd = QTextCharFormat()
        self.whiteBkgd.setBackground(QBrush(QColor("white")))
        self.first = True
        if shortTitleList is not None:
            self.setText(shortTitleList)

        self.okButton.released.connect(self.returnEntry)
        self.cancelButton.released.connect(self.returnNone)
        self.textWindow.cursorPositionChanged.connect(self.highlight)
        self.textWindow.mouseDoubleClickEvent = self.mouseDoubleClick
        
    def mouseDoubleClick(self, mouseEvent):
        """Override the textBrowser's mouseDoubleClickEvent() function
        so we can choose the entry by double clicking."""
        self.returnEntry()

    def setText(self, text):
        self.textWindow.setText(text)
        self.cursor = self.textWindow.textCursor()
        self.cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.MoveAnchor)
        self.cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
        self.cursor.mergeCharFormat(self.whiteBkgd)
        self.first = True

    def returnNone(self):
        self.close()

    def returnEntry(self):
        # emit selection and close?
        #print('selected: %s '% self.cursor.selectedText())
        emitStr = self.cursor.selectedText()
        self.emit(SIGNAL("lineEmit"), (emitStr, ) )
        self.close()

    def highlight(self):
        if not self.first:
            self.cursor.mergeCharFormat(self.whiteBkgd)
        self.first = False
        self.cursor = self.textWindow.textCursor()
        self.cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.MoveAnchor)
        self.cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
        self.cursor.mergeCharFormat(self.redBkgd)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    ex = EntrySelect()
    ex.show()
    txtStr = """1 AJB 55.06.07 Author1, Title1
2 AJB 55.06.08 Author2, Title2
3 AJB 55.06.09 Author3, Title3
"""
    ex.setText(txtStr)

    app.exec_()
