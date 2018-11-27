## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/ajbbook/origstrWindow.py
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

"""A window for viewing the original string entry
if it exists.
"""
from PyQt5 import QtWidgets

from aabooks.ajbbook import ui_OrigStr

class OrigStrWindow(QtWidgets.QDialog, ui_OrigStr.Ui_origstrDialog):
    """The class OrigStrWindow is a QDialog that can display the original
    string that an entry came from, assuming the entry was read from a
    text file.  Note that text files are depricated as of version
    2.0.

    """

    def __init__(self, textstr=None):
        super(OrigStrWindow, self).__init__()

        self.setupUi(self)

        self.set_origstr_text(textstr)

        self.closeButton.released.connect(self.close)

    def set_filename(self, num):
        """Set the title of the window with the filename that the entry came
        from.

        """

        self.setWindowTitle('Original String - Entry %s'%str(num))

    def set_origstr_text(self, textstr):
        """Set the string to be displayed in the window."""

        self.textEdit.setPlainText(textstr)

    def get_origstr_text(self):
        """Return the text in the window.  Don't know why one would want to do
        this but this funtion is here for symmetry.

        """

        return self.textEdit.toPlainText()


#
# Test functions
#
if __name__ == '__main__':
    import sys

    APP = QtWidgets.QApplication(sys.argv)
    FORM = OrigStrWindow('This is the display dialog for the original entry string')
    FORM.set_filename('52')
    FORM.show()
    APP.exec_()
