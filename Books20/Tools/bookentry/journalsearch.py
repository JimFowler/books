#! /usr/bin/env python3
# -*- mode: Python;-*-

"""Main window for journal entries from AAA/AJB

  open with Journal Search
  open existing journalFile or new one
  New button or search brings up Entry window with an already open file
  redoing a search sets the index number in the current entry
  Search by full name, abbreviation, closeness (how to do this)
"""
import sys
import os
import platform
import fileinput
import configparser

from PyQt5.QtCore import *
from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *

import bookentry.ui_JournalSearch as ui_journalSearch
import bookentry.search as search

# Trouble shooting assistance
from pprint import pprint

__version__ = '1.0.0'

class JournalSearch( QDialog, ui_journalSearch.Ui_JournalSearch ):

    def __init__(self, parent = None, searchDict = None ):
        super(JournalSearch, self).__init__(parent=parent)
        self.setupUi(self)

        self.searchdict = searchDict
        self.parent = parent
        
        self.searchEdit.textChanged.connect(self.SearchEditChanged)
        self.searchResults.itemDoubleClicked.connect(self.titleSelected)
      

        self.closeButton.released.connect(self.close)
        #Self.newButton.released.connect(self.newEntry)
  

    #
    # This function is the slot for the searchEdit.textChanged signal
    #
    def SearchEditChanged(self):
        """Run a search of the sdict and fill in the searchResults"""
        print('SearchEditChanged')
        try:
            self.searchEdit.textChanged.disconnect(self.SearchEditChanged)
        except:
            pass

        self.searchResults.clear()
        search_text = self.searchEdit.text()
        if len(search_text) > 2: 
            # Update the searchResults box
            try:
                self.currentSearchList = self.searchdict.search(search_text.strip())
            except KeyError:
                print('no entry in search dict')
                self.currentSearchList = []
                
            if len(self.currentSearchList) > 0:
                # add to searchResults
                self.searchResults.insertItem(0, search_text)
                for i in range(1, min(9,len(self.currentSearchList)+1)):
                    try:
                        self.searchResults.insertItem(i, self.currentSearchList[i][0])
                    except IndexError:
                        pass
            
        try:
            self.searchEdit.textChanged.connect(self.SearchEditChanged)
        except:
            pass
     
    def titleSelected(self, title):
        """If a title has been selected in the searchResults, then
        find that title in the currentSearchList, extract that record
        number and send a signal with the relevant record number. A
        record number of 0"""
        for t, i in self.currentSearchList:
            if t == title.text():
                print(title.text(), t, i)
                self.parent.showEntry(i+1./)
                return
        self.parent.newEntry()
        print('Creating new entry', title.text())

