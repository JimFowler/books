#! /usr/bin/env python3
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/journal/journalsearch.py
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

'''Dialog window for journal entries from AAA/AJB

  open with Journal Search
  open existing journalFile or new one
  New button or search brings up Entry window with an already open file
  redoing a search sets the index number in the current entry
  Search by full name, abbreviation, closeness (how to do this)
'''
from PyQt5 import QtWidgets

from aabooks.journal import ui_JournalSearch

class JournalSearch(QtWidgets.QDialog, ui_JournalSearch.Ui_JournalSearch):
    '''The main class to create a widget and allow searchs.'''

    def __init__(self, parent=None, searchDict=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.searchdict = searchDict
        self.parent = parent
        self.current_search_list = []
        #pylint: disable = no-value-for-parameter
        self.searchEdit.textChanged.connect(self.search_edit_changed)
        self.searchResults.itemDoubleClicked.connect(self.title_selected)


        self.closeButton.released.connect(self.close)
        self.newButton.released.connect(self.parent._new_entry)
        #pylint: enable = no-value-for-parameter


    #
    # This function is the slot for the searchEdit.textChanged signal
    #
    def search_edit_changed(self):
        """Run a search of the sdict and fill in the searchResults"""
        #pylint: disable = no-value-for-parameter
        self.searchEdit.textChanged.disconnect(self.search_edit_changed)
        #pylint: enable = no-value-for-parameter

        search_text = self.searchEdit.text()
        self.searchResults.clear()
        self.searchResults.insertItem(0, search_text.strip())
        self.current_search_list = []

        try:
            search_results = self.searchdict.search(word=search_text)
            for sres in search_results:
                context = self.searchdict.words[sres[-1]]
                self.current_search_list.append((context['Title'],
                                                 context['Index']))
        except KeyError:
            self.current_search_list = []

        max_items = len(self.current_search_list)
        if max_items > 0:
            # add to searchResults
            for i in range(1, (max_items + 1)):
                try:
                    self.searchResults.insertItem(i, self.current_search_list[i-1][0])
                except IndexError:
                    pass
        #pylint: disable = no-value-for-parameter
        self.searchEdit.textChanged.connect(self.search_edit_changed)
        #pylint: enable = no-value-for-parameter

    def title_selected(self, search_title):
        """If a title has been selected in the searchResults, then find that
        title in the current_search_list, extract that record number
        and show the entry with the relevant record number.

        """
        title_text = search_title.text()
        for title, index in self.current_search_list:
            if title == title_text:
                self.parent.show_entry(index + 1)
                return

        self.parent.new_entry()
        self.parent.titleEdit.setText(title_text)
