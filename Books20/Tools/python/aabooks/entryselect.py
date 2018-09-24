## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/entryselect.py
##  
##   Part of the Books20 Project
##
##   Copyright 2018 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrival system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright


"""Choose an entry from the list."""


try:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
except:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *

import aabooks.ui_EntrySelect as ui_EntrySelect

class EntrySelect(QDialog, ui_EntrySelect.Ui_ShortTitleDisplay):

    lineEmit = pyqtSignal( object, name='lineEmit')

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
        self.lineEmit.emit( (emitStr, ) )
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

    def printMe(l):
        print('You selected line:', l[0])
        
    app = QApplication(sys.argv)
    ex = EntrySelect()
    ex.show()
    txtStr = """1 AJB 55.06.07 Author1, Title1
2 AJB 55.06.08 Author2, Title2
3 AJB 55.06.09 Author3, Title3
"""
    ex.setText(txtStr)
    ex.lineEmit.connect(printMe)

    app.exec_()
