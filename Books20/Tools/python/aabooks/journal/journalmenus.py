## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/journal/journalmenus.py
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


"""Create the menus for the Journals window.
"""
# -*- mode: Python;-*-
# pylint: disable=too-many-arguments,eval-used

from PyQt5 import QtGui, QtWidgets

def create_action(self, text, slot=None, shortcut=None, icon=None,
                  tip=None, checkable=False, signal="triggered"):
    """Usage: create_action(self, text, slot=None, shortcut=None, icon=None,
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
        eval('action.' + signal + '.connect(' + slot + ')')
    else:
        action.enabled = False
    if checkable:
        action.setCheckable(True)
    return action


def create_menus(self, menu_bar):
    '''Create a set of menus for journal window'''
    # set up the File menus
    menu = menu_bar.addMenu('&File')

    action = create_action(self, '&New File',
                           slot='self._open_new_file',
                           shortcut='Ctrl+N')
    menu.addAction(action)

    action = create_action(self, '&Open File...',
                           slot='self._ask_open_file',
                           shortcut='Ctrl+O')
    menu.addAction(action)

    action = create_action(self, '&Save File',
                           slot='self._save_file',
                           shortcut='Ctrl+S')
    menu.addAction(action)

    action = create_action(self, 'Save File &As...',
                           slot='self._save_file_as',
                           shortcut='Ctrl+A')
    menu.addAction(action)

    menu.addSeparator()

    action = create_action(self, '&Quit',
                           slot='self._quit',
                           shortcut='Ctrl+Q',
                           icon='filequit',
                           tip='Close the Application')
    menu.addAction(action)


    # set up the Edit menus, Cut, Copy, Paste, Delete  make gray
    menu = menu_bar.addMenu('Edit')

    action = create_action(self, 'Cu&t', shortcut='Ctrl+X')
    action.setEnabled(False)
    menu.addAction(action)

    action = create_action(self, '&Copy', shortcut='Ctrl+C')
    action.setEnabled(False)
    menu.addAction(action)

    action = create_action(self, '&Paste', shortcut='Ctrl+V')
    action.setEnabled(False)
    menu.addAction(action)

    action = create_action(self, '&Delete', shortcut='Del')
    action.setEnabled(False)
    menu.addAction(action)

    menu.addSeparator()

    #action = create_action(self, 'Additional &Info...',
    #                       shortcut='Ctrl+T')
    #menu.addAction(action)

    action = create_action(self, '&Insert Symbol...',
                           slot='self._open_symbol_dialog',
                           shortcut='Ctrl+I')
    menu.addAction(action)

    action = create_action(self, 'Edit &Header...',
                           slot='self._edit_header',
                           shortcut='Ctrl+H')
    menu.addAction(action)

    # Create sort sub-menu
    sort_menu = menu.addMenu('Sort By')

    action = create_action(self, 'Journal Title')
    action.setEnabled(False)
    sort_menu.addAction(action)

    # set up the Entry menus
    menu = menu_bar.addMenu('Entry')

    action = create_action(self, 'New &Entry',
                           slot='self._new_entry',
                           shortcut='Ctrl+E')
    menu.addAction(action)

    action = create_action(self, 'Save Ent&ry',
                           slot='self._save_entry',
                           shortcut='Ctrl+R')
    menu.addAction(action)

    action = create_action(self, 'Insert Entry',
                           slot='self._ask_insert_entry')
    menu.addAction(action)

    action = create_action(self, '&Delete Entry',
                           slot='self._delete_entry',
                           shortcut='Ctrl+D')
    menu.addAction(action)

    action = create_action(self, '&Print Entry',
                           slot='self._print_entry',
                           shortcut='Ctrl+P')
    menu.addAction(action)



    # set up the Help menus
    menu = menu_bar.addMenu('&Help')
    action = create_action(self, '&About Journals...',
                           slot='self._help_about')
    menu.addAction(action)
