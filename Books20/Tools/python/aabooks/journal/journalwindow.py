#! /usr/bin/env python3
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/journal/journalwindow.py
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

'''
Main window for journal entries from AAA/AJB

  open existing journalFile or new one
  New button or search brings up Entry window with an already open file
  redoing a search sets the index number in the current entry
  Search by full name, abbreviation, closeness (how to do this)


To keep pylint happy,
   encapsulate non-public instance attributes in a dictionary self._attr_dict
   make all button/menu functions semi-private with _func()

'''
import os
import platform
# Trouble shooting assistance
from pprint import pprint

from fast_autocomplete import AutoComplete

from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport

from aabooks.lib import headerwindow as hw
from aabooks.lib import entryselect as es
#from aabooks.lib import search
from aabooks.lib import symbol
from aabooks.lib import version as libver

from aabooks.journal import ui_JournalEntry
from aabooks.journal import journalmenus as menus
from aabooks.journal import jsearch as journalsearch
from aabooks.journal import journalfile
from aabooks.journal import journalentry
from aabooks.journal import entrydisplay
from aabooks.journal import version as jourver



DIR_NAME, BASE_NAME = os.path.split(symbol.__file__)
__DEFAULT_SYMBOL_TABLE_NAME__ = DIR_NAME + '/symbols.txt'
del DIR_NAME
del BASE_NAME

__version__ = '1.0.0'

def help_string():
    '''Create help string.'''

    helpstring = f'''<b>Journals</b> v {jourver.__version__}
    <p>Author: J. R. Fowler
    <p>Copyright &copy; 2016 -- 2020
    <p>All rights reserved.
    <p>This application is used to create and visualize
    the XML files with the Journals found in the annual
    bibliographies of <b>Astronomischer Jahresbericht</b>.
    <p>aabook/lib v {libver.__version__}
    <p>Python {platform.python_version()} - Qt {QtCore.QT_VERSION_STR} -
     PyQt {QtCore.PYQT_VERSION_STR} on {platform.system()}'''

    return helpstring

class JournalWindow(QtWidgets.QMainWindow, ui_JournalEntry.Ui_JournalEntry):
    '''The main window for the journal program.'''
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        #
        # Set up an empty journal set
        #
        self._vardict = {}
        self._vardict['journal_file'] = journalfile.JournalFile()
        self._vardict['cur_entry_number'] = 0
        self._vardict['insert_func'] = None
        self._vardict['entry_dirty'] = False
        self._vardict['search_flag'] = False
        self._vardict['current_search_list'] = []
        self._vardict['sdict'] = None
        self._vardict['temp_entry'] = None
        self._vardict['entry_select'] = None
        self._vardict['symbol_table'] = None
        self._vardict['header_window'] = None
        self._vardict['jsearch'] = None

        self.set_max_entry_count(0)
        self.set_window_title('document1')
        self.set_symbol_table_name(__DEFAULT_SYMBOL_TABLE_NAME__)


        # Fields within an Entry that we know about already
        self.known_entry_fields = ['Index', 'Num', 'Authors', 'Editors', 'Title',
                                   'Publishers', 'Edition', 'Year',
                                   'Pagination', 'Price', 'Reviews',
                                   'Compilers', 'Contributors', 'Translators',
                                   'Language', 'TranslatedFrom', 'Reference',
                                   'Reprint', 'Others', 'OrigStr', 'Comments']

        # lists of which display fields may or may not have symbol entry allowed
        self.no_entry_list = ['indexEntry', 'startDateEdit', 'endDateEdit']

        self.set_text_entry_list = ['titleEdit', 'subTitleEdit', 'subsubTitleEdit',
                                    'publisherEdit', 'abbreviationsEdit',
                                    'LinkPreviousEdit', 'LinkNextEdit',
                                    'CommentsEdit']
        self.set_line_entry_list = ['searchEdit']


        menus.create_menus(self, self.menubar)

        self.saveButton.setEnabled(False)
        self.deleteButton.setEnabled(False)
        self.newButton.setEnabled(True)

        #pylint: disable = no-value-for-parameter
        self.searchButton.released.connect(self._search_entry)
        self.newButton.released.connect(self.new_entry)
        self.saveButton.released.connect(self._save_entry)
        self.insertButton.released.connect(self._ask_insert_entry)
        self.deleteButton.released.connect(self._delete_entry)
        self.quitButton.released.connect(self._quit)

        self.indexEntry.returnPressed.connect(self.index_changed)

        self.titleEdit.textChanged.connect(self._set_entry_dirty)
        self.publisherEdit.textChanged.connect(self._set_entry_dirty)
        self.abbreviationsEdit.textChanged.connect(self._set_entry_dirty)
        self.startDateEdit.textChanged.connect(self._set_entry_dirty)
        self.endDateEdit.textChanged.connect(self._set_entry_dirty)
        self.LinkPreviousEdit.textChanged.connect(self._set_entry_dirty)
        self.LinkNextEdit.textChanged.connect(self._set_entry_dirty)
        self.designatorEdit.textChanged.connect(self._set_entry_dirty)
        self.CommentsEdit.textChanged.connect(self._set_entry_dirty)
        #pylint: enable = no-value-for-parameter


    def sort_triggered(self, action):
        '''Slot for QActionGroup.triggered.  'self' is the QAction
        that was triggered.
        '''
        if self._vardict['journal_file']:
            self._vardict['journal_file'].sort_by(action.iconText())
    
    def display_is_valid(self):
        '''Check the display values for a valid journal entry.
        A valid journal entry has at least a title.  Returns
        True or False.

        '''
        mem = self.titleEdit.toPlainText().strip()
        if len(mem) == 0:
            return False
        return True

    def set_max_entry_count(self, count):
        '''Comment'''
        self.max_entry_count = max(count, 0)

        if self.max_entry_count == 0:
            self.prevButton.setEnabled(False)
            self.nextButton.setEnabled(False)
        else:
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(True)

            self.ofnumLabel.setText(f'of {self.max_entry_count}')

    #
    # Menu and button slots
    #
    def _quit(self):
        '''Comment'''
        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        if self.ask_save_file() == QtWidgets.QMessageBox.Cancel:
            return

        self.close()


    #
    # Deal with the Search Dictionary
    #
    def _build_search_dictionary(self):
        '''Takes a JournalFile and returns an AutoComplete object.

        '''

        words = {}
        synonyms = {}
        del self._vardict['sdict']

        for count, entry in enumerate(self._vardict['journal_file']):

            title = entry['Title']
            sub_title = entry['subTitle']
            subsub_title = entry['subsubTitle']

            words[title.lower()] = {'Title' : title,
                                    'Index' : count}

            synonyms[title] = [sub_title.lower(), subsub_title.lower()]
            for abbrev in entry['Abbreviations']:
                if abbrev:
                    synonyms[title].append(str(abbrev.lower()))

        self._vardict['sdict']  = AutoComplete(words=words, synonyms=synonyms)


    #
    # Search for an existing entry
    #  This function called when Search... button is pressed
    #
    def _search_entry(self):
        '''open search dialog
        link search to self.showSearchSelect()'''

        self._vardict['jsearch'] = journalsearch.JournalSearch(parent=self,\
                                        searchDict=self._vardict['sdict'])

        self._vardict['jsearch'].show()

    #
    # Menu and button slots for File actions
    #
    def _open_new_file(self):
        '''Create a new bookfile saving the old one if it is dirty.'''
        if self._vardict['journal_file'] is not None:
            if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
                return

            if self.ask_save_file() == QtWidgets.QMessageBox.Cancel:
                return

        self._vardict['journal_file'] = journalfile.JournalFile()
        self.set_max_entry_count(0)
        self.new_entry()

    def open_file(self, name=None):
        '''Open an existing file, get the count of entries, and display
        the first entry. If no records are found we assume that this is
        a new file and we automatically generate a new entry.'''

        self.set_max_entry_count(self._vardict['journal_file'].read_file(name))
        if self.max_entry_count:
            self.statusbar.clearMessage()
            self.statusbar.showMessage(f'{self.max_entry_count} records found', 6000)
            self._build_search_dictionary()
            self._clear_search_flag()
            self.show_entry(1)
            self._clear_entry_dirty()
        else:
            self.statusbar.showMessage(f'No records found in file {name}')
            self.new_entry()
        self.set_window_title(os.path.basename(self._vardict['journal_file'].filename))


    def _save_file(self):
        '''Ignore dirty entries and just save the file.'''
        if self._vardict['journal_file'].filename is None:
            self._save_file_as()
        else:
            self._vardict['journal_file'].write_file_xml()

        self.statusbar.showMessage('Saving file ' \
                                   + os.path.basename(self._vardict['journal_file'].filename))
        QtCore.QTimer.singleShot(10000, self.statusbar.clearMessage)


    def _save_file_as(self):
        '''Ignore dirty entries and save the file as...'''
        fname, dummy = QtWidgets.QFileDialog.getSaveFileName(self,\
                f'{QtWidgets.QApplication.applicationName()} -- Choose file',\
                '.', '*.xml')

        if fname:
            name = os.path.splitext(fname)
            if name[1] == '':
                fname += '.xml'

            self._vardict['journal_file'].write_file_xml(fname)
            self.set_window_title(os.path.basename(self._vardict['journal_file'].filename))

    #
    # Menu and button slots for Entry Actions
    #
    def _save_entry(self):
        '''Save the entry to the current entry number in the bookfile.'''
        if not self.display_is_valid():
            msg = '1 Entry invalid. No Title!\nNot saved in journalfile!'
            QtWidgets.QMessageBox.information(self, 'Entry Invalid', msg)

            return

        self._vardict['temp_entry'] = entrydisplay.display_to_entry(self)
        if self._vardict['cur_entry_number'] > self.max_entry_count:
            ret = self._vardict['journal_file'].set_new_entry(\
                            self._vardict['temp_entry'], \
                            self._vardict['cur_entry_number'] - 1)
        else:
            ret = self._vardict['journal_file'].set_entry(\
                            self._vardict['temp_entry'], \
                            self._vardict['cur_entry_number'] - 1)

        if not ret:
            msg = '2 Entry invalid. No Title!\nNot saved in journalfile!'
            QtWidgets.QMessageBox.information(self, 'Entry Invalid', msg)

            return

        if self._vardict['cur_entry_number'] > self.max_entry_count:
            self.set_max_entry_count(self._vardict['cur_entry_number'])

        self.deleteButton.setEnabled(True)
        self._build_search_dictionary()
        self._clear_search_flag()
        self._clear_entry_dirty()

    def new_entry(self):
        '''Create a new entry, save the old one if it has been modified.'''
        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        self._clear_search_flag()
        self._vardict['temp_entry'] = journalentry.JournalEntry()
        self._vardict['cur_entry_number'] = self.max_entry_count + 1
        entrydisplay.entry_to_display(self, self._vardict['temp_entry'])
        self.repaint()
        self.indexEntry.setText(str(self._vardict['cur_entry_number']))
        self.titleEdit.setFocus()
        self._set_search_flag()
        self._clear_entry_dirty()

    def _ask_insert_entry(self):
        '''Open the entry_select form if we have a valid entry to insert.
        If the user selects an insertion location, then we execute the
        method insert_entry()'''
        self._vardict['temp_entry'] = entrydisplay.display_to_entry(self)
        if not self.display_is_valid():
            QtWidgets.QMessageBox.information(self, 'Entry Invalid',
                                              '3 Entry invalid. No title!\nNot saved in bookfile!')
            return

        self._vardict['entry_select'] = es.EntrySelect()
        self._vardict['entry_select'].set_text(\
                            self._vardict['journal_file'].make_short_title_list())

        self._vardict['entry_select'].show()
        #self.connect(self._vardict['entry_select'], SIGNAL('lineEmit'),
        #             self.insert_entry )
        self._vardict['entry_select'].lineEmit.connect(self._insert_entry)

    def _insert_entry(self, line):
        '''Parse the short title line, get the index number and insert
        the current display entry in front of this entry in the booklist.'''

        words = line[0].split(' ')

        num = int(words[0])
        if not num or num < 1 or num > self.max_entry_count:
            return

        self._vardict['journal_file'].set_new_entry(self._vardict['temp_entry'], num - 1)
        self._build_search_dictionary()
        self._vardict['cur_entry_number'] = num
        self.set_max_entry_count(self.max_entry_count + 1)
        self.show_entry(self._vardict['cur_entry_number'])

    def _delete_entry(self):
        '''Delete the entry at the cur_entry_number but
        ask the user first.'''
        ans = QtWidgets.QMessageBox.warning(self, 'Delete Entry?',\
            'Are you sure you want to delete this entry? This action can not be undone!',\
            QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)

        if ans == QtWidgets.QMessageBox.Cancel:
            return

        self.set_max_entry_count(self._vardict['journal_file'].delete_entry(\
                                           self._vardict['cur_entry_number'] - 1))
        self._build_search_dictionary()
        if self.max_entry_count < 1:
            self.insertButton.setEnable(False)
            self.new_entry()
        else:
            self.show_entry(self._vardict['cur_entry_number'])

    def show_entry(self, recnum=1):
        '''show_entry(recnum) where 1 <= recnum <= max_entry_count.
        recnum is the index into the entry list.  The buttons will
        wrap around the index values.
        '''
        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        if self.max_entry_count < 1:
            return

        self.prevButton.setEnabled(True)

        self.nextButton.setEnabled(True)

        if recnum < 1:
            # We add here because recnum is zero or negative already
            self._vardict['cur_entry_number'] = self.max_entry_count + recnum
        elif recnum > self.max_entry_count:
            self._vardict['cur_entry_number'] = recnum - self.max_entry_count
        else:
            self._vardict['cur_entry_number'] = recnum

        # Display the actual entry data
        self._vardict['temp_entry'] = self._vardict['journal_file'].get_entry(\
                                                self._vardict['cur_entry_number'] - 1)

        if not self._vardict['temp_entry']:
            return

        # Display record count
        self.indexEntry.setText(str(self._vardict['cur_entry_number']))

        entrydisplay.entry_to_display(self, self._vardict['temp_entry'])
        self.repaint()
        self.deleteButton.setEnabled(True)
        self._clear_entry_dirty()

    def _print_entry(self):
        '''Print a postscript file of the current display.'''
        pprint(self._vardict['journal_file'].get_entry(self._vardict['cur_entry_number'] - 1))

    def search(self, string):
        '''Search the existing Titles and abbreviations for any entries
        that match or partially match the string in titleEdit. Pop a
        list window. If the users double clicks an entry, then return
        the index of the entry selected from the list and clear the
        searchflag.  Clear the search_flag if the users selects
        stopSearch.'''
        try:
            self._vardict['current_search_list'] = \
                                        self._vardict['sdict'].search(string.strip())
        except KeyError:
            self._vardict['current_search_list'] = None


    #
    # Set/Clear flags for Entry
    #
    def _set_search_flag(self):
        '''Set the  searchflag to True to enable searchs'''
        self._vardict['search_flag'] = True

    def _clear_search_flag(self):
        '''Set the search flag to False and disable searchs.'''
        self._vardict['search_flag'] = False

    def _set_entry_dirty(self):
        '''Set the entry_dirty flag to True and enable the Save Entry
        button.'''
        self._vardict['entry_dirty'] = True
        self.saveButton.setEnabled(True)
        # set menu item enable to True as well

    def _clear_entry_dirty(self):
        '''Set the entry_dirty flag to False and disable the Save
        Entry button.'''
        self._vardict['entry_dirty'] = False
        self.saveButton.setEnabled(False)
        # set menu item enable False as well.
        # set Save File menu True

    def print_printer(self):
        '''Comment'''
        printer = QtPrintSupport.QPrinter()
        printer.setOutputFileName('book.pdf')
        printer.setFullPage(True)
        printer.setPaperSize(QtPrintSupport.QPrinter.Letter)

        print_dialog = QtPrintSupport.QPrintDialog(printer, self)
        if print_dialog.exec_():
            painter = QtGui.QPainter(printer)
            self.render(painter)
            del painter


    #
    # Edit menu functions
    #
    def _open_symbol_dialog(self):
        '''Open the symbol entry form.'''
        self._vardict['symbol_table'] = symbol.SymbolForm(\
                self._vardict['symbol_table_name'], 'FreeSans', 14, parent=self)
        self._vardict['symbol_table'].sigClicked.connect(self.insert_char)
        self._vardict['symbol_table'].show()

    def set_symbol_table_name(self, name):
        '''Set the name of the symbol table to use in place of the
        default table.'''
        self._vardict['symbol_table_name'] = name

    def insert_char(self, obj):
        '''Insert the charactor in obj[0] with self._vardict['insert_func']
        if insert_func is not None.'''

        char = obj[0]
        # invoke self._vardict['insert_func'](char)
        if self._vardict['insert_func'] is not None:
            self._vardict['insert_func'](char)
        # take back focus somehow??

    def set_focus_changed(self, old_widget, now_widget):
        '''For items in set_text_entry_list and set_line_entry_list
        set insert_func to be either insertPlainText() or insert().'''

        if old_widget is None:
            pass
        elif old_widget.objectName() == 'indexEntry':
            self.indexEntry.setText(str(self._vardict['cur_entry_number']))

        if now_widget is None:
            pass
        elif self.set_text_entry_list.count(now_widget.objectName()):
            self._vardict['insert_func'] = now_widget.insertPlainText
        elif self.set_line_entry_list.count(now_widget.objectName()):
            self._vardict['insert_func'] = now_widget.insert
        elif self.no_entry_list.count(now_widget.objectName()):
            self._vardict['insert_func'] = None


    def _edit_header(self):
        '''Open the edit header form.'''
        self._vardict['header_window'] = hw.HeaderWindow(self, parent=self)
        self._vardict['header_window'].set_bookfile(self._vardict['journal_file'])
        self._vardict['header_window'].setWindowTitle(\
                QtWidgets.QApplication.translate('headerWindow',\
                f"Edit heaaders - {os.path.basename(self._vardict['journal_file'].filename)}",\
                                        None))
        self._vardict['header_window'].set_header_text(\
                                        self._vardict['journal_file'].get_header())
        self._vardict['header_window'].show()

    #
    # Help menu functions
    #
    def _help_about(self):
        '''Show help string.'''
        QtWidgets.QMessageBox.about(self, 'About Journals', help_string())

    #
    # Button slots and Signals
    #
    #pylint: disable = invalid-name
    def on_prevButton_released(self):
        '''comment'''
        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        self.show_entry(self._vardict['cur_entry_number'] - 1)

    def on_nextButton_released(self):
        '''comment'''
        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        self.show_entry(self._vardict['cur_entry_number'] + 1)
    #pylint: enable = invalid-name

    def index_changed(self):
        '''Comment'''
        enum = int(self.indexEntry.text())

        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        self.show_entry(enum)

    #
    # Various useful dialogs
    #
    def ask_save_entry(self):
        '''Ask if we should save the dirty entry.'''
        ans = None
        if self._vardict['entry_dirty']:
            ans = QtWidgets.QMessageBox.warning(self, 'Save Entry?',
                                                'Entry has changed. Do you want to save it?',
                                                QtWidgets.QMessageBox.Save
                                                | QtWidgets.QMessageBox.No
                                                | QtWidgets.QMessageBox.Cancel)

            if ans == QtWidgets.QMessageBox.Save:
                self._save_entry()

        return ans

    def ask_save_file(self):
        '''Ask if we should save the dirty file.'''
        ans = None
        if self._vardict['journal_file'].is_dirty():
            ans = QtWidgets.QMessageBox.warning(self, 'Save file?',\
                        'The File has changed. Do you want to save it?',\
                        QtWidgets.QMessageBox.Save\
                        | QtWidgets.QMessageBox.Discard\
                        | QtWidgets.QMessageBox.Cancel)

            if ans == QtWidgets.QMessageBox.Save:
                self._save_file()
                # set save file menu enable to False

        return ans

    def _ask_open_file(self):
        '''Open an existing file saving the old one if it is dirty.'''
        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        if self.ask_save_file() == QtWidgets.QMessageBox.Cancel:
            return

        fname, dummy = QtWidgets.QFileDialog.getOpenFileName(self,\
            f'{QtWidgets.QApplication.applicationName()} -- Choose new file',\
            os.path.dirname(self._vardict['journal_file'].filename), '*.xml')
        if fname:
            self.open_file(fname)

    #
    # Methods to deal with various display aspects
    #
    def set_window_title(self, name):
        '''Creates the string 'Journal Entry vx.x - name' and
        places it into the window title.
        '''
        title = QtWidgets.QApplication.translate('MainWindow',
                         f'Journal Entry  v {__version__}   -   {name}',
                                                 None)
        self.setWindowTitle(title)


#
# Test routine
#


if __name__ == '__main__':

    import sys

    APP = QtWidgets.QApplication(sys.argv)
    APP.setApplicationName('Journal Entry')
    FORM = JournalWindow()
    #pylint: disable = no-value-for-parameter
    APP.focusChanged.connect(FORM.set_focus_changed)
    #pylint: enable = no-value-for-parameter

    FORM.show()
    sys.exit(APP.exec_())
