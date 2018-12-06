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
import configparser
# Trouble shooting assistance
from pprint import pprint

from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport

from aabooks.journal import ui_JournalEntry
from aabooks.journal import journalmenus as menus
from aabooks.journal import jsearch as journalsearch
from aabooks.journal import journalfile
from aabooks.journal import journalentry

from aabooks.lib import headerwindow as hw
from aabooks.lib import entryselect as es
from aabooks.lib import search
from aabooks.lib import symbol



DIR_NAME, BASE_NAME = os.path.split(symbol.__file__)
__DEFAULT_SYMBOL_TABLE_NAME__ = DIR_NAME + '/symbols.txt'
del DIR_NAME
del BASE_NAME

__version__ = '1.0.0'

class JournalWindow(QtWidgets.QMainWindow, ui_JournalEntry.Ui_JournalEntry):
    '''The main window for the journal program.'''
    def __init__(self, parent=None, config_name=None):
        super(JournalWindow, self).__init__(parent=parent)
        self.setupUi(self)

        #
        # Set up an empty journal set
        #
        self.journal_file = journalfile.JournalFile()
        self.cur_entry_number = 0
        self.set_max_entry_count(0)
        self.set_window_title('document1')
        self.insert_func = None
        self.set_symbol_table_name(__DEFAULT_SYMBOL_TABLE_NAME__)
        self.entry_dirty = False
        self.search_flag = False
        self.current_search_list = []
        self.sdict = search.SearchDict()
        self.temp_entry = None
        self.entry_select = None
        self.symbol_table = None
        self.header_window = None
        self.jsearch = None


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

        self.searchButton.released.connect(self._search_entry)
        self.newButton.released.connect(self._new_entry)
        self.saveButton.released.connect(self._save_entry)
        self.insertButton.released.connect(self._ask_insert_entry)
        self.deleteButton.released.connect(self._delete_entry)
        self.quitButton.released.connect(self._quit)

        self.saveButton.setEnabled(False)
        self.deleteButton.setEnabled(False)
        self.newButton.setEnabled(True)

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

        #
        # Read the config file
        #
        self.config = configparser.ConfigParser()
        self.config.read(config_name)
        self.journal_file.set_schema_name(self.config['DEFAULT']['journal_xsd'])
        jf_name = self.config['DEFAULT']['journal_file_dir'] + '/' + \
                  self.config['DEFAULT']['journal_file_name'] + '.' + \
                  self.config['DEFAULT']['journal_file_ext']

        if jf_name is not None and os.path.isfile(jf_name):
            self.open_file(jf_name)

    def set_max_entry_count(self, count):
        """Comment"""
        if count < 0:
            count = 0
        self.max_entry_count = count

        if self.max_entry_count == 0:
            self.prevButton.setEnabled(False)
            self.nextButton.setEnabled(False)
        else:
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(True)

            self.ofnumLabel.setText('of %d'%self.max_entry_count)

    #
    # Menu and button slots
    #
    def _quit(self):
        """Comment"""
        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        if self.ask_save_file() == QtWidgets.QMessageBox.Cancel:
            return

        self.close()

    #
    # Deal with the Search Dictionary
    #
    def _build_search_dictionary(self):
        '''Add all the titles and abbreviations to the search
        dictionary'''
        self.sdict.clear()
        index = 0
        for entry in self.journal_file._entry_list:
            title = entry['Title']
            self.sdict.add_sub_strings(title, (title, index))

            sub_title = entry['subTitle']
            self.sdict.add_sub_strings(sub_title, (sub_title, index))

            subsub_title = entry['subsubTitle']
            self.sdict.add_sub_strings(subsub_title, (subsub_title, index))

            for abr in entry['Abbreviations']:
                if abr is not None:
                    self.sdict.add_sub_strings(abr, (abr, index))
            index += 1


    #
    # Search for an existing entry
    #  This function called when Search... button is pressed
    #
    def _search_entry(self):
        '''open search dialog
        link search to self.showSearchSelect()'''

        self.jsearch = journalsearch.JournalSearch(parent=self, searchDict=self.sdict)

        self.jsearch.show()

    #
    # Menu and button slots for File actions
    #
    def _open_new_file(self):
        """Create a new bookfile saving the old one if it is dirty."""
        if self.journal_file is not None:
            if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
                return

            if self.ask_save_file() == QtWidgets.QMessageBox.Cancel:
                return

        self.journal_file = journalfile.JournalFile()
        self.set_max_entry_count(0)
        self._new_entry()

    def open_file(self, name=None):
        """Open an existing file, get the count of entries, and display
        the first entry. If no records are found we assume that this is
        a new file and we automatically generate a new entry."""

        self.set_max_entry_count(self.journal_file.read_xml_file(name))
        if self.max_entry_count:
            self.statusbar.clearMessage()
            self.statusbar.showMessage('%d records found'%self.max_entry_count, 6000)
            self._build_search_dictionary()
            self._clear_search_flag()
            self.show_entry(1)
            self._clear_entry_dirty()
        else:
            self.statusbar.showMessage('No records found in file %s' % name)
            self._new_entry()
        self.set_window_title(self.journal_file.get_base_name())


    def _save_file(self):
        """Ignore dirty entries and just save the file."""
        if self.journal_file.get_file_name() is None:
            self.save_file_as()
        else:
            self.journal_file.write_xml_file()

        self.statusbar.showMessage('Saving file ' + self.journal_file.get_base_name())
        QtCore.QTimer.singleShot(10000, self.statusbar.clearMessage)


    def _save_file_as(self):
        """Ignore dirty entries and save the file as..."""
        fname, dummy = QtWidgets.QFileDialog.getSaveFileName(self,
                                                             "%s -- Choose file"%QtWidgets.QApplication.applicationName(),
                                                             ".", "*.xml")
        if fname:
            self.journal_file.write_xml_file(fname)
            self.set_window_title(self.journal_file.get_base_name())

    #
    # Menu and button slots for Entry Actions
    #
    def _save_entry(self):
        """Save the entry to the current entry number in the bookfile."""
        self.temp_entry = self.display_to_entry()
        if not self.temp_entry:
            QtWidgets.QMessageBox.information(self, "Entry Invalid",
                                              "Entry invalid!  Not saved in journalfile!")
            return

        if self.cur_entry_number > self.max_entry_count:
            ret = self.journal_file.set_new_entry(self.temp_entry, self.cur_entry_number)
        else:
            ret = self.journal_file.set_entry(self.temp_entry, self.cur_entry_number)

        if not ret:
            QtWidgets.QMessageBox.information(self, "Entry Invalid",
                                              "Entry invalid!  Not saved in journalfile!")
            return

        if self.cur_entry_number > self.max_entry_count:
            self.set_max_entry_count(self.cur_entry_number)

        self.deleteButton.setEnabled(True)
        self.build_search_dictionary()
        self._clear_search_flag()
        self._clear_entry_dirty()

    def _new_entry(self):
        """Create a new entry, save the old one if it has been modified."""
        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        self._clear_search_flag()
        self.temp_entry = journalentry.JournalEntry()
        self.cur_entry_number = self.max_entry_count + 1
        self.entry_to_display(self.temp_entry)
        self.indexEntry.setText(str(self.cur_entry_number))
        self.titleEdit.setFocus()
        self._set_search_flag()
        self._clear_entry_dirty()

    def _ask_insert_entry(self):
        """Open the entry_select form if we have a valid entry to insert.
        If the user selects an insertion location, then we execute the
        method insert_entry()"""
        self.temp_entry = self.display_to_entry()
        if not self.temp_entry or not self.temp_entry.is_valid():
            QtWidgets.QMessageBox.information(self, "Entry Invalid",
                                              "Entry invalid!  Not saved in bookfile!")
            return

        self.entry_select = es.EntrySelect()
        self.entry_select.set_text(self.journal_file.make_short_title_list())

        self.entry_select.show()
        #self.connect(self.entry_select, SIGNAL('lineEmit'),
        #             self.insert_entry )
        self.entry_select.lineEmit.connect(self._insert_entry)

    def _insert_entry(self, line):
        """Parse the short title line, get the index number and insert
        the current display entry in front of this entry in the booklist."""

        words = line[0].split(' ')

        num = int(words[0])
        if not num or num < 1 or num > self.max_entry_count:
            return

        self.journal_file.set_new_entry(self.temp_entry, num)
        self.build_search_dictionary()
        self.cur_entry_number = num
        self.set_max_entry_count(self.max_entry_count + 1)
        self.show_entry(self.cur_entry_number)

    def _delete_entry(self):
        """Delete the entry at the cur_entry_number but
        ask the user first."""
        ans = QtWidgets.QMessageBox.warning(self, 'Delete Entry?',
                                            'Are you sure you want to delete this entry? This action can not be undone!',
                                            QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)
        if ans == QtWidgets.QMessageBox.Cancel:
            return

        self.set_max_entry_count(self.journal_file.delete_entry(self.cur_entry_number))
        self.build_search_dictionary()
        if self.max_entry_count < 1:
            self.insertButton.setEnable(False)
            self.new_entry()
        else:
            self.show_entry(self.cur_entry_number)

    def show_entry(self, recnum=1):
        """show_entry(recnum) where 1 <= recnum <= max_entry_count.
        recnum is the index into the entry list.  The buttons will
        wrap around the index values.
        """
        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        if self.max_entry_count < 1:
            return

        self.prevButton.setEnabled(True)

        self.nextButton.setEnabled(True)

        if recnum < 1:
            # We add here because recnum is zero or negative already
            self.cur_entry_number = self.max_entry_count + recnum
        elif recnum > self.max_entry_count:
            self.cur_entry_number = recnum - self.max_entry_count
        else:
            self.cur_entry_number = recnum

        # Display the actual entry data
        self.temp_entry = self.journal_file.get_entry(self.cur_entry_number)

        if not self.temp_entry:
            return

        # Display record count
        self.indexEntry.setText(str(self.cur_entry_number))

        self.entry_to_display(self.temp_entry)
        self.deleteButton.setEnabled(True)
        self._clear_entry_dirty()

    def _print_entry(self):
        """Print a postscript file of the current display."""
        pprint(self.journal_file.get_entry(self.cur_entry_number))

    def search(self, string):
        '''Search the existing Titles and abbreviations for any entries
        that match or partially match the string in titleEdit. Pop a
        list window. If the users double clicks an entry, then return
        the index of the entry selected from the list and clear the
        searchflag.  Clear the search_flag if the users selects
        stopSearch.'''
        try:
            self.current_search_list = self.sdict.search(string.strip())
        except KeyError:
            self.current_search_list = None


    #
    # Set/Clear flags for Entry
    #
    def _set_search_flag(self):
        """Set the  searchflag to True to enable searchs"""
        self.search_flag = True

    def _clear_search_flag(self):
        """Set the search flag to False and disable searchs."""
        self.search_flag = False

    def _set_entry_dirty(self):
        """Set the entry_dirty flag to True and enable the Save Entry
        button."""
        self.entry_dirty = True
        self.saveButton.setEnabled(True)
        # set menu item enable to True as well

    def _clear_entry_dirty(self):
        """Set the entry_dirty flag to False and disable the Save
        Entry button."""
        self.entry_dirty = False
        self.saveButton.setEnabled(False)
        # set menu item enable False as well.
        # set Save File menu True

    def print_printer(self):
        """Comment"""
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
        """Open the symbol entry form."""
        self.symbol_table = symbol.SymbolForm(self.symbol_table_name, 'FreeSans', 14)
        self.symbol_table.sigClicked.connect(self.insert_char)
        self.symbol_table.show()

    def set_symbol_table_name(self, name):
        """Set the name of the symbol table to use in place of the
        default table."""
        self.symbol_table_name = name

    def insert_char(self, obj):
        """Insert the charactor in obj[0] with self.insert_func
        if insert_func is not None."""

        char = obj[0]
        # invoke self.insert_func(char)
        if self.insert_func is not None:
            self.insert_func(char)
        # take back focus somehow??

    def set_focus_changed(self, old_widget, now_widget):
        """For items in set_text_entry_list and set_line_entry_list
        set insert_func to be either insertPlainText() or insert()."""

        if old_widget is None:
            pass
        elif old_widget.objectName() == 'indexEntry':
            self.indexEntry.setText(str(self.cur_entry_number))

        if now_widget is None:
            pass
        elif self.set_text_entry_list.count(now_widget.objectName()):
            self.insert_func = now_widget.insertPlainText
        elif self.set_line_entry_list.count(now_widget.objectName()):
            self.insert_func = now_widget.insert
        elif self.no_entry_list.count(now_widget.objectName()):
            self.insert_func = None


    def _edit_header(self):
        """Open the edit header form."""
        self.header_window = hw.HeaderWindow(self)
        self.header_window.set_bookfile(self.journal_file)
        self.header_window.setWindowTitle(QtWidgets.QApplication.translate("headerWindow",
                                                                           "Edit heaaders - %s" % (self.journal_file.get_base_name()),
                                                                           None))
        self.header_window.set_header_text(self.journal_file.get_header())
        self.header_window.show()

    #
    # Help menu functions
    #
    def help_string(self):
        """Create help string."""
        helpstring = """<b>Journals</b> v {0}
        <p>Author: J. R. Fowler
        <p>Copyright &copy; 2016
        <p>All rights reserved.
        <p>This application is used to create and visualize
        the XML files with the journals found in the annual
        bibliographies of <b>Astronomischer Jahresbericht</b>.
        <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(
            __version__, platform.python_version(),
            QtCore.QT_VERSION_STR, QtCore.PYQT_VERSION_STR,
            platform.system())
        return helpstring

    def _help_about(self):
        """Show help string."""
        QtWidgets.QMessageBox.about(self, 'About Journals', self.help_string())


    #
    # Button slots and Signals
    #
    def on_prevButton_released(self):
        """comment"""
        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        self.show_entry(self.cur_entry_number - 1)

    def on_nextButton_released(self):
        """comment"""
        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        self.show_entry(self.cur_entry_number + 1)

    def index_changed(self):
        """Comment"""
        enum = int(self.indexEntry.text())

        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        self.show_entry(enum)

    #
    # Various useful dialogs
    #
    def ask_save_entry(self):
        """Ask if we should save the dirty entry."""
        ans = None
        if self.entry_dirty:
            ans = QtWidgets.QMessageBox.warning(self, 'Save Entry?',
                                                'Entry has changed. Do you want to save it?',
                                                QtWidgets.QMessageBox.Save
                                                | QtWidgets.QMessageBox.No
                                                | QtWidgets.QMessageBox.Cancel)

            if ans == QtWidgets.QMessageBox.Save:
                self.save_entry()

        return ans

    def ask_save_file(self):
        """Ask if we should save the dirty file."""
        ans = None
        if self.journal_file.is_dirty():
            ans = QtWidgets.QMessageBox.warning(self, 'Save file?',
                                                'The File has changed. Do you want to save it?',
                                                QtWidgets.QMessageBox.Save
                                                | QtWidgets.QMessageBox.Discard
                                                | QtWidgets.QMessageBox.Cancel)

            if ans == QtWidgets.QMessageBox.Save:
                self.save_file()
                # set save file menu enable to False

        return ans

    def _ask_open_file(self):
        """Open an existing file saving the old one if it is dirty."""
        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        if self.ask_save_file() == QtWidgets.QMessageBox.Cancel:
            return

        fname, dummy = QtWidgets.QFileDialog.getOpenFileName(self,
                                                             '%s -- Choose new file' %
                                                             QtWidgets.QApplication.applicationName(),
                                                             self.journal_file.get_dir_name(),
                                                             '*.xml')
        if fname:
            self.open_file(fname)

    #
    # Methods to deal with various display aspects
    #
    def set_window_title(self, name):
        """Creates the string 'Journal Entry vx.x - name' and
        places it into the window title.
        """
        title = QtWidgets.QApplication.translate('MainWindow',
                                                 'Journal Entry  v %s   -   %s' %
                                                 (__version__, name),
                                                 None)
        self.setWindowTitle(title)

    def entry_to_display(self, entry):
        """Given an entry, display the parts on the GUI display."""

        astr = ''
        if entry.not_empty('Title'):
            astr += entry['Title']
        if entry.not_empty('subTitle'):
            astr = astr + '\n' + entry['subTitle']
        if entry.not_empty('subsubTitle'):
            astr = astr + '\n' + entry['subsubTitle']
        self.titleEdit.setText(astr)

        astr = ''
        if entry.not_empty('Publishers'):
            first = True
            for mem in entry['Publishers']:
                if not first:
                    astr += '\n'
                first = False
                if mem.__contains__('Place'):
                    astr += mem['Place']
                astr += ' : '
                if mem.__contains__('Name'):
                    astr += mem['Name']
                astr += ' : '
                if mem.__contains__('startDate'):
                    astr += mem['startDate']
                astr += ' : '
                if mem.__contains__('endDate'):
                    astr += mem['endDate']
        self.publisherEdit.setText(astr)


        astr = ''
        if entry.not_empty('Abbreviations'):
            first = True
            for mem in entry['Abbreviations']:
                if not first:
                    astr += '\n'
                first = False
                astr += mem
        self.abbreviationsEdit.setText(astr)

        astr = ''
        if entry.not_empty('startDate'):
            astr += entry['startDate']
        self.startDateEdit.setText(astr)

        astr = ''
        if entry.not_empty('endDate'):
            astr += entry['endDate']
        self.endDateEdit.setText(astr)

        astr = ''
        if entry.not_empty('linkprevious'):
            first = True
            for mem in entry['linkprevious']:
                if not first:
                    astr += '\n'
                first = False
                astr += mem
        self.LinkPreviousEdit.setText(astr)

        astr = ''
        if entry.not_empty('linknext'):
            first = True
            for mem in entry['linknext']:
                if not first:
                    astr += '\n'
                first = False
                astr += mem
        self.LinkNextEdit.setText(astr)

        astr = ''
        if entry.not_empty('Designators'):
            first = True
            for mem in entry['Designators']:
                if not first:
                    astr += '\n'
                first = False
                astr += mem
                astr += ' : '
                astr += entry['Designators'][mem]
        self.designatorEdit.setText(astr)


        astr = ''
        if entry.not_empty('Comments'):
            first = True
            for mem in entry['Comments']:
                if not first:
                    astr += '\n'
                first = False
                astr += mem
        self.CommentsEdit.setText(astr)

        self.repaint()


    def display_to_entry(self):
        """Copy the display into a new entry and
        return the entry."""
        entry = journalentry.JournalEntry()

        # Titles
        mem = self.titleEdit.toPlainText().strip()
        if mem:
            alist = mem.split('\n')
            alist_len = len(alist)
            if not alist:
                return None
            entry['Title'] = alist[0]
            if alist_len > 1 and  alist[1] != 0:
                entry['subTitle'] = alist[1]
            if alist_len > 2 and alist[2] != 0:
                entry['subsubTitle'] = alist[2]


        # Publishers
        mem = self.publisherEdit.toPlainText()
        if mem:
            alist = mem.split('\n')
            for line in alist:
                pubd = {}
                fields = line.split(':')
                num_fields = len(fields)
                # Check len(flds) here, pop dialog if not 4
                if num_fields > 0:
                    pubd['Place'] = fields[0].strip()
                if num_fields > 1:
                    pubd['Name'] = fields[1].strip()
                if num_fields > 2:
                    pubd['startDate'] = fields[2].strip()
                if num_fields > 3:
                    pubd['endDate'] = fields[3].strip()

                entry['Publishers'].append(pubd)


        # Abbreviations
        mem = self.abbreviationsEdit.toPlainText()
        if mem:
            alist = mem.split('\n')
            for line in alist:
                entry['Abbreviations'].append(line.strip())

        # startDate
        entry['startDate'] = self.startDateEdit.text().strip()

        # endDate
        entry['endDate'] = self.endDateEdit.text().strip()

        # link previous
        mem = self.LinkPreviousEdit.toPlainText()
        if mem:
            alist = mem.split('\n')
            for line in alist:
                entry['linkprevious'].append(line.strip())

        # link next
        mem = self.LinkNextEdit.toPlainText()
        if mem:
            alist = mem.split('\n')
            for line in alist:
                entry['linknext'].append(line.strip())

        # Designators
        mem = self.designatorEdit.toPlainText()
        if mem:
            alist = mem.split('\n')
            for line in alist:
                flds = line.split(':')
                entry['Designators'][flds[0].strip()] = flds[1].strip()


        # Comments
        mem = self.CommentsEdit.toPlainText()
        if mem:
            alist = mem.split('\n')
            for line in alist:
                entry['Comments'].append(line)

        return entry
