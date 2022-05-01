## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/lib/entryselect.py
##
##   Part of the Books20 Project
##
##   Copyright 2018 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrieval system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright
"""Choose an entry from the list.

Why don't we use a QListWidget here?"""

from PyQt5 import QtCore, QtGui, QtWidgets

import aabooks.lib.ui_EntrySelect as EntrySelect_ui

class EntrySelect(QtWidgets.QDialog, EntrySelect_ui.Ui_ShortTitleDisplay):
    '''Provides a dialog box from a list.  Selecting an item by
    double clicking or highlighting and selecting Ok will cause
    the item to be emitted as a signal.

    '''

    lineEmit = QtCore.pyqtSignal(object, name='lineEmit')

    def __init__(self, entry_list=None):
        super().__init__()

        self.setupUi(self)

        self.red_bkgd = QtGui.QTextCharFormat()
        self.red_bkgd.setBackground(QtGui.QBrush(QtGui.QColor("red")))

        self.white_bkgd = QtGui.QTextCharFormat()
        self.white_bkgd.setBackground(QtGui.QBrush(QtGui.QColor("white")))
        self.first = True
        if entry_list is not None:
            self.set_text(entry_list)

        # pylint: disable = no-value-for-parameter
        self.okButton.released.connect(self.return_entry)
        self.cancelButton.released.connect(self.return_none)
        self.textWindow.cursorPositionChanged.connect(self.highlight)
        # pylint: enable = no-value-for-parameter
        self.textWindow.mouseDoubleClickEvent = self.mouse_double_click

    def mouse_double_click(self, mouse_event):
        """Override the textBrowser's mouseDoubleClickEvent() function
        so we can choose the entry by double clicking."""
        if mouse_event:
            self.return_entry()

    def set_text(self, text):
        '''set text'''
        self.textWindow.setText(text)
        self.cursor = self.textWindow.textCursor()
        self.cursor.movePosition(QtGui.QTextCursor.StartOfLine,\
                                 QtGui.QTextCursor.MoveAnchor)
        self.cursor.movePosition(QtGui.QTextCursor.EndOfLine,
                                 QtGui.QTextCursor.KeepAnchor)
        self.cursor.mergeCharFormat(self.white_bkgd)
        self.first = True

    def return_none(self):
        ''' return none'''
        self.close()

    def return_entry(self):
        ''' return Entry'''
        emit_string = self.cursor.selectedText()
        self.lineEmit.emit((emit_string, ))
        self.close()

    def highlight(self):
        '''highlight'''
        if not self.first:
            self.cursor.mergeCharFormat(self.white_bkgd)
        self.first = False
        self.cursor = self.textWindow.textCursor()
        self.cursor.movePosition(QtGui.QTextCursor.StartOfLine,
                                 QtGui.QTextCursor.MoveAnchor)
        self.cursor.movePosition(QtGui.QTextCursor.EndOfLine,
                                 QtGui.QTextCursor.KeepAnchor)
        self.cursor.mergeCharFormat(self.red_bkgd)


if __name__ == '__main__':

    import sys

    def print_me(_me):
        ''' print me '''
        print('You selected line:', _me[0])

    APP = QtWidgets.QApplication(sys.argv)
    EX = EntrySelect()
    EX.show()
    TXTSTR = """1 AJB 55.06.07 Author1, Title1
2 AJB 55.06.08 Author2, Title2
3 AJB 55.06.09 Author3, Title3
"""
    EX.set_text(TXTSTR)
    EX.lineEmit.connect(print_me)

    APP.exec_()
