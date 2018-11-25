# -*- mode: Python; -*-
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/lib/symbol.py
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

"""A table of unicode characters (symbols) that may be inserted into
any of the text fields.

The basic code for the button and the window were taken from the
character_picker package developed by Rich Griswold and described
in his blog
http://richgriswold.wordpress.com/2009/10/17/character-picker/
(last accessed Mar 2013)

The packaged was modified for aabooks.
"""

from PyQt5 import QtCore, QtGui, QtWidgets

def make_buttons(file_name, parent):
    '''Make all the buttons for the parent window from the
    symbol file in file_name.
    '''
    button_dict = dict()

    row = 0
    col = 0
    col_max = 0
    index = 0

    try:
        # would like to use resource here ':/Resources/symbols.txt'
        #file = open( './aabooks/Resources/symbols.txt', 'r' )
        symfile = open(file_name, 'r')
    except IOError as ex:
        print(ex)
        return (row, col_max, button_dict)

    for line in symfile:
        line = line.strip()

        # start new row if line is empty
        if not line:
            row += 1
            col = 0
            continue

        # ignore comment line
        if line[0] == '#':
            continue

        try:
            char, tip = line.split(',')
        except ValueError as ex:
            print('Symbol Table ValueError: "%s"' % line)
            print(ex)
            continue

        button = MyButton(parent.scroll_area_widget_contents)
        button.setCheckable(True)
        button.setFont(parent.font)
        button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        button.setText(char)
        button.setToolTip(tip)
        button.setObjectName('%03d%03dButton'%(row, col))

        parent.grid_layout.addWidget(button, row, col, 1, 1)
        parent.button_group.addButton(button, index)

        button.sigClicked.connect(parent.slot_clicked)

        button_dict[row, col] = button

        col += 1
        index += 1
        if col > col_max:
            col_max = col

    return (row, col_max, button_dict)


class MyButton(QtWidgets.QToolButton):
    """Create a button with a associated text string,
    in our case a character. When the button is clicked
    it emits the text string.
    """

    sigClicked = QtCore.pyqtSignal(object, name='sigClicked')

    def __init__(self):
        super(MyButton, self).__init__()
        self.clicked.connect(self.slot_clicked)

    def slot_clicked(self):
        '''Emit the text if we are clicked.'''
        self.sigClicked.emit((self.text(), ))

class SymbolForm(QtWidgets.QDialog):
    """Create a table of buttons which emit their character
    when pressed."""

    sigClicked = QtCore.pyqtSignal(object, name='sigClicked')

    def __init__(self, file_name, font_family, font_size):
        super(SymbolForm, self).__init__()
        self.setObjectName('symbolForm')

        self.setWindowTitle('Insert Symbol...')

        self.clicked = False
        self.font = QtGui.QFont(font_family, int(font_size))

        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget_contents = QtWidgets.QWidget(self.scroll_area)
        self.grid_layout = QtWidgets.QGridLayout(self.scroll_area_widget_contents)
        self.grid_layout.setSpacing(0)
        self.scroll_area.setWidget(self.scroll_area_widget_contents)

        self.button_group = QtWidgets.QButtonGroup()
        self.button_group.setExclusive(True)
        row_max, col_max, self.buttons = make_buttons(file_name, self)

        spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.grid_layout.addItem(spacer_item, 0, col_max, 1, 1)
        spacer_item = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.grid_layout.addItem(spacer_item, row_max, 0, 1, 1)
        self.setLayout(self.grid_layout)


    def slot_clicked(self, obj):
        '''Emit the object if we are clicked.'''
        char = obj[0]
        self.clicked = True
        self.sigClicked.emit((char, ))
        self.clicked = False



if __name__ == "__main__":
    import sys

    def print_me(character):
        '''Print the selected character.'''
        print('Char selected is', character[0])

    APP = QtWidgets.QApplication(sys.argv)
    MYFORM = SymbolForm('symbols.txt', 'FreeSans', 14)
    MYFORM.show()
    MYFORM.sigClicked.connect(print_me)
    sys.exit(APP.exec_())
