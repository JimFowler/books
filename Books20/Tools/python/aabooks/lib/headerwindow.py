## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/lib/headerWindow.py
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
"""A window for editing the header section of bookfiles.

Close button asks to save if file is dirty,
Save button saves header text to local bookfile,
Cancel button revert to header text from last save.

All text work done through the intermediate bookfile.
Need to explicitly save this bookfile to disk in order
to save your changed permenantly
"""
from PyQt5 import QtWidgets

from aabooks.lib import ui_HeaderEntry

class HeaderWindow(QtWidgets.QDialog, ui_HeaderEntry.Ui_HeaderEdit):
    '''A window to edit the header text with.'''
    def __init__(self, bf=None, parent=None):
        super(HeaderWindow, self).__init__(parent)

        self.setupUi(self)
        self.set_bookfile(bf)
        self.dirty = False

        self.headerEntry.textChanged.connect(self.set_dirty)
        self.closeButton.released.connect(self.ask_and_close)
        self.saveButton.released.connect(self.save_header_text)
        self.cancelButton.released.connect(self.revert_header)


    def set_filename(self, file):
        '''Set the window title with the file name being edited'''
        self.setWindowTitle('Edit Header - %s'%file)

    def set_bookfile(self, bookf):
        '''Set the bookfile that we want to edit the header of.'''
        self.bookfile = bookf

    def save_header_text(self):
        '''Save the current test in the bookfile object.'''
        if self.bookfile:
            self.bookfile.set_header(self.get_header_text())
            self.clear_dirty()

    def ask_and_close(self):
        '''If necessary, always ask before closing the file.'''
        if self.is_dirty():
            resp = QtWidgets.QMessageBox.warning(self, "Warning",
                                                 '''The header has been modified\n
                                                 Do you want to save your changes?''',
                                                 QtWidgets.QMessageBox.Save,
                                                 QtWidgets.QMessageBox.Discard,
                                                 QtWidgets.QMessageBox.Cancel)
            if resp == QtWidgets.QMessageBox.Save:
                self.save_close()
            elif resp == QtWidgets.QMessageBox.Discard:
                self.no_saveclose()
            elif resp == QtWidgets.QMessageBox.Cancel:
                return
        else:
            self.close()

    def save_close(self):
        '''Save the text in the bookfile and close the window'''
        self.save_header_text()
        self.close()

    def revert_header(self):
        '''Reset the test to the existing bookfile header.'''
        # restore the current header before closing
        self.set_header_text(self.bookfile.get_header())

    def no_save_close(self):
        '''Don't save the text, just close the window.'''
        self.close()

    def set_dirty(self):
        '''Set the dirty flag. This means that unsaved changes to the text
        have occurred. Enable the save button.'''
        self.saveButton.enable = True
        self.dirty = True

    def clear_dirty(self):
        '''Clear the dirty flag. This means that there are no unsaved changes
        to the text have occurred. Disable the save button.
        '''
        self.saveButton.enable = False
        self.dirty = False

    def is_dirty(self):
        '''Return the value of the dirty flag.'''
        return self.dirty

    def set_header_text(self, textstr):
        '''Set the text to edit.'''
        self.headerEntry.setPlainText(textstr)
        self.clear_dirty()

    def get_header_text(self):
        '''Get the text we have edited.'''
        return self.headerEntry.toPlainText()


#
# Test functions
#
if __name__ == '__main__':
    import aabooks.ajbbook.bookfile as Bookfile
    import sys

    APP = QtWidgets.QApplication(sys.argv)
    EX = HeaderWindow()
    BF = Bookfile.BookFile()
    EX.set_bookfile(BF)
    EX.set_filename('New File')
    EX.set_header_text(BF.get_header())
    EX.show()
    APP.exec_()

    print('The Header is:\n')
    print(BF.get_header())
