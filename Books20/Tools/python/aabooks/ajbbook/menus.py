## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/ajbbook/menus.py
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


"""Create the menus for the AJB Book Entry window
"""
from PyQt5 import QtGui, QtWidgets

# pylint: disable=eval-used,too-many-arguments

def create_action(self, text, slot=None, shortcut=None, icon=None,
                  tip=None, checkable=False, signal='triggered'):
    """Usage: create_action( self, text, slot=None, shortcut=None, icon=None,
                            tip=None, checkable=False, signal="triggered")
         Note: the vars 'slot', 'shortcut', 'icon', 'tip',
               and 'signal' should be of type string.
    """
    action = QtWidgets.QAction(text, self)
    if icon is not None:
        action.setIcon(QtGui.QIcon(":/{0}.png".format(icon)))
    if shortcut is not None:
        action.setShortcut(shortcut)
    if tip is not None:
        action.setToolTip(tip)
        action.setStatusTip(tip)
    if slot is not None:
        #self.connect(action, SIGNAL(signal), slot)
        eval('action.' + signal + '.connect(' + slot + ')')
    else:
        action.enabled = False

    action.setCheckable(checkable)
    return action


def create_menus(self, menu_bar):
    """Create all the menus for ajbbooks main window."""

    create_file_menu(self, menu_bar)
    create_edit_menu(self, menu_bar)
    create_help_menu(self, menu_bar)


def create_file_menu(self, menu_bar):
    """Create the file menu/"""
    file_menu = menu_bar.addMenu('&File')

    new_action = create_action(self, '&New File',
                               slot='self.open_new_file',
                               shortcut='Ctrl+N')
    file_menu.addAction(new_action)

    new_action = create_action(self, '&Open File...',
                               slot='self.ask_open_file',
                               shortcut='Ctrl+O')
    file_menu.addAction(new_action)

    new_action = create_action(self, '&Save File',
                               slot='self.save_file',
                               shortcut='Ctrl+S')
    file_menu.addAction(new_action)

    new_action = create_action(self, 'Save File As...',
                               slot='self.save_file_as')
    file_menu.addAction(new_action)
    file_menu.addSeparator()


    new_action = create_action(self, 'New &Entry',
                               slot='self.new_entry',
                               shortcut='Ctrl+E')
    file_menu.addAction(new_action)

    new_action = create_action(self, 'Next Entry',
                               slot='self.on_nextButton_released',
                               shortcut=None)
    file_menu.addAction(new_action)

    new_action = create_action(self, 'Prev &Entry',
                               slot='self.on_prevButton_released',
                               shortcut=None)
    file_menu.addAction(new_action)

    new_action = create_action(self, 'Save Ent&ry',
                               slot='self.save_entry',
                               shortcut='Ctrl+R')
    file_menu.addAction(new_action)

    new_action = create_action(self, '&Print Entry',
                               slot='self.print_entry',
                               shortcut='Ctrl+P')
    file_menu.addAction(new_action)
    file_menu.addSeparator()


    new_action = create_action(self, '&Quit',
                               slot='self.quit',
                               shortcut='Ctrl+Q',
                               icon='filequit',
                               tip='Close the Application')
    file_menu.addAction(new_action)



def create_edit_menu(self, menu_bar):
    """Create the edit menu."""
    # set up the Edit menus, Cut, Copy, Paste, Delete  make gray
    cut_action = create_action(self, 'Cu&t', shortcut='Ctrl+X')
    cut_action.setEnabled(False)
    copy_action = create_action(self, '&Copy', shortcut='Ctrl+C')
    copy_action.setEnabled(False)
    paste_action = create_action(self, '&Paste', shortcut='Ctrl+V')
    paste_action.setEnabled(False)
    delete_action = create_action(self, '&Delete', shortcut='Del')
    delete_action.setEnabled(False)

    symbol_action = create_action(self, '&Insert Symbol...',
                                  slot='self.open_symbol',
                                  shortcut='Ctrl+I')

    header_action = create_action(self, 'Edit &Header...',
                                  slot='self.edit_header',
                                  shortcut='Ctrl+H')

    origstr_action = create_action(self, 'Show Original String',
                                   slot='self.show_orig_str')

    setvolnum_action = create_action(self, 'Set Volume Number...',
                                     slot='self.set_volume_number_interactive')


    edit_menu = menu_bar.addMenu('&Edit')
    edit_menu.addAction(cut_action)
    edit_menu.addAction(copy_action)
    edit_menu.addAction(paste_action)
    edit_menu.addAction(delete_action)
    edit_menu.addSeparator()
    edit_menu.addAction(symbol_action)
    edit_menu.addAction(header_action)
    edit_menu.addAction(origstr_action)
    edit_menu.addAction(setvolnum_action)


def create_help_menu(self, menu_bar):
    """Create the help menu."""

    # set up the Help menus
    help_menu = menu_bar.addMenu('&Help')
    about_action = create_action(self, '&About Book Entry...',
                                 'self.help_about')
    help_menu.addAction(about_action)


if __name__ == '__main__':
    print('No tests available yet')
