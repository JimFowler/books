#! /usr/bin/env python3
# -*- mode: Python;-*-

"""Main window for journal entries from AAA/AJB

  open with Journal Search
  New button or search brings up Entry window with an already open file
  redoing a search sets the index number in the current entry
  Search by full name, abbreviation, closeness (how to do this)

  flags
   --help
   --version
   --input journal entry file
   --symbol use alternate ymbol table

Menus
  File
    New File new journal file
    Open open journal file
    New Entry  new journal entry
    Save    save current journal file
    Save As  save current journal entries in new file
    Print print current journal entry ??
    Quit  quit

  Edit
   Cut
   Copy
   Paste
   Delete
   
  Help
    About
"""

import sys
import os
import argparse
from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import bookentry.ui_JournalSearch as ui_journalSearch
#import bookentry.journalfile as jf
import bookentry.symbol as symbol

# Trouble shooting assistance
from pprint import *
pp = PrettyPrinter()


__dirName, __basename  = os.path.split(symbol.__file__)
__DefaultSymbolTableName__ = __dirName + '/symbols.txt'
del __dirName
del __basename



class JournalSearch( QMainWindow, ui_journalSearch.Ui_JournalSearch ):

    def __init__(self, parent = None ):
        super(JournalSearch, self).__init__(parent)
        self.setupUi(self)

        self.connect(self.QuitButton, SIGNAL('released()'), self.close)


        
