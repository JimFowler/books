#! /usr/bin/env python3
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/journalwindow.py
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
'''
import os
import platform
import configparser
# Trouble shooting assistance
from pprint import pprint

from PyQt5 import QtCore, QtWidgets

import aabooks.ui_JournalEntry as ui_journalentry
import aabooks.journalfile as journalfile
import aabooks.journalmenus as menus
import aabooks.journalentry as journalentry
import aabooks.jsearch as journalsearch
import aabooks.symbol as symbol
import aabooks.headerWindow as hw
import aabooks.entryselect as es
import aabooks.search as search



DIR_NAME, BASE_NAME = os.path.split(symbol.__file__)
__default_symbol_table_name__ = DIR_NAME + '/symbols.txt'
del DIR_NAME
del BASE_NAME

__version__ = '1.0.0'

class JournalWindow(QtWidgets.QMainWindow, ui_journalentry.Ui_JournalEntry):
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
        self.set_symbol_table_name(__default_symbol_table_name__)
        self.entry_dirty = False
        self.search_flag = False
        self.current_search_list = []
        self.sdict = search.SearchDict()

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

        self.searchButton.released.connect(self.search_entry)
        self.newButton.released.connect(self.new_entry)
        self.saveButton.released.connect(self.save_entry)
        self.insertButton.released.connect(self.ask_insert_entry)
        self.deleteButton.released.connect(self.delete_entry)
        self.quitButton.released.connect(self.quit)

        self.saveButton.setEnabled(False)
        self.deleteButton.setEnabled(False)
        self.newButton.setEnabled(True)

        self.indexEntry.returnPressed.connect(self.index_changed)

        self.titleEdit.textChanged.connect(self.set_entry_dirty)
        self.publisherEdit.textChanged.connect(self.set_entry_dirty)
        self.abbreviationsEdit.textChanged.connect(self.set_entry_dirty)
        self.startDateEdit.textChanged.connect(self.set_entry_dirty)
        self.endDateEdit.textChanged.connect(self.set_entry_dirty)
        self.LinkPreviousEdit.textChanged.connect(self.set_entry_dirty)
        self.LinkNextEdit.textChanged.connect(self.set_entry_dirty)
        self.designatorEdit.textChanged.connect(self.set_entry_dirty)
        self.CommentsEdit.textChanged.connect(self.set_entry_dirty)

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
    def quit(self):
        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        if self.ask_save_file() == QtWidgets.QMessageBox.Cancel:
            return

        self.close()

    #
    # Deal with the Search Dictionary
    #
    def build_search_dictionary(self):
        '''Add all the titles and abbreviations to the search
        dictionary'''
        self.sdict.clear()
        index = 0
        for entry in self.journal_file._entry_list:
            title = entry['Title']
            self.sdict.addSubStrings(title, (title, index))

            sub_title = entry['subTitle']
            self.sdict.addSubStrings(sub_title, (sub_title, index))

            subsub_title = entry['subsubTitle']
            self.sdict.addSubStrings(subsub_title, (subsub_title, index))

            for abr in entry['Abbreviations']:
                if abr is not None:
                    self.sdict.addSubStrings(abr, (abr, index))
            index += 1


    #
    # Search for an existing entry
    #  This function called when Search... button is pressed
    #
    def search_entry(self):
        '''open search dialog
        link search to self.showSearchSelect()'''

        self.jsearch = journalsearch.JournalSearch(parent=self, searchDict=self.sdict)

        self.jsearch.show()

        return

    #
    # Menu and button slots for File actions
    #
    def open_new_file(self):
        """Create a new bookfile saving the old one if it is dirty."""
        if self.journal_file is not None:
            if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
                return

            if self.ask_save_file() == QtWidgets.QMessageBox.Cancel:
                return

        self.journal_file = journalfile.JournalFile()
        self.set_max_entry_count(0)
        self.new_entry()

    def open_file(self, name=None):
        """Open an existing file, get the count of entries, and display
        the first entry. If no records are found we assume that this is
        a new file and we automatically generate a new entry."""

        self.set_max_entry_count(self.journal_file.read_xml_file(name))
        if self.max_entry_count:
            self.statusbar.clearMessage()
            self.statusbar.showMessage('%d records found'%self.max_entry_count, 6000)
            self.build_search_dictionary()
            self.clear_search_flag()
            self.show_entry(1)
            self.clear_entry_dirty()
        else:
            self.statusbar.showMessage('No records found in file %s' % name)
            self.new_entry()
        self.set_window_title(self.journal_file.get_base_name())


    def save_file(self):
        """Ignore dirty entries and just save the file."""
        #print("saving file %s"%self.journal_file.get_file_name())
        if self.journal_file.get_file_name() is None:
            self.save_file_as()
        else:
            self.journal_file.write_xml_file()

        self.statusbar.showMessage('Saving file ' + self.journal_file.get_base_name())
        QtCore.QTimer.singleShot(10000, self.statusbar.clearMessage)


    def save_file_as(self):
        """Ignore dirty entries and save the file as..."""
        fname, filtera = QtWidgets.QFileDialog.getSaveFileName(self,
                                                               "%s -- Choose file"%QtWidgets.QApplication.applicationName(),
                                                               ".", "*.xml")
        if fname:
            self.journal_file.write_xml_file(fname)
            self.set_window_title(self.journal_file.get_base_name())

    #
    # Menu and button slots for Entry Actions
    #
    def save_entry(self):
        """Save the entry to the current entry number in the bookfile."""
        self.tmpEntry = self.DisplayToEntry()
        if not self.tmpEntry:
            QtWidgets.QMessageBox.information(self, "Entry Invalid",
                                              "Entry invalid!  Not saved in journalfile!")
            return

        if self.cur_entry_number > self.max_entry_count:
            ret = self.journal_file.set_new_entry(self.tmpEntry, self.cur_entry_number)
        else:
            ret = self.journal_file.set_entry(self.tmpEntry, self.cur_entry_number)

        if not ret:
            QtWidgets.QMessageBox.information(self, "Entry Invalid",
                                              "Entry invalid!  Not saved in journalfile!")
            return

        if self.cur_entry_number > self.max_entry_count:
            self.set_max_entry_count(self.cur_entry_number)

        self.deleteButton.setEnabled(True)
        self.build_search_dictionary()
        self.clear_search_flag()
        self.clear_entry_dirty()

    def new_entry(self):
        """Create a new entry, save the old one if it has been modified."""
        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        self.clear_search_flag()
        self.tmpEntry = journalentry.JournalEntry()
        self.cur_entry_number = self.max_entry_count + 1
        self.EntryToDisplay(self.tmpEntry)
        self.indexEntry.setText(str(self.cur_entry_number))
        self.titleEdit.setFocus()
        self.set_search_flag()
        self.clear_entry_dirty()

    def ask_insert_entry(self):
        """Open the entry_select form if we have a valid entry to insert.
        If the user selects an insertion location, then we execute the
        method insert_entry()"""
        self.tmpEntry = self.DisplayToEntry()
        if not self.tmpEntry or not self.tmpEntry.is_valid():
            QtWidgets.QMessageBox.information(self, "Entry Invalid",
                                              "Entry invalid!  Not saved in bookfile!")
            return

        self.entry_select = es.EntrySelect()
        self.entry_select.setText(self.journal_file.make_short_title_list())

        self.entry_select.show()
        #self.connect(self.entry_select, SIGNAL('lineEmit'),
        #             self.insert_entry )
        self.entry_select.lineEmit.connect(self.insert_entry)

    def insert_entry(self, line):
        """Parse the short title line, get the index number and insert
        the current display entry in front of this entry in the booklist."""

        words = line[0].split(' ')

        num = int(words[0])
        if not num or num < 1 or num > self.max_entry_count:
            return

        self.journal_file.set_new_entry(self.tmpEntry, num)
        self.build_search_dictionary()
        self.cur_entry_number = num
        self.set_max_entry_count(self.max_entry_count + 1)
        self.show_entry(self.cur_entry_number)

    def delete_entry(self):
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
        self.tmpEntry = self.journal_file.get_entry(self.cur_entry_number)

        if not self.tmpEntry:
            return

        # Display record count
        self.indexEntry.setText(str(self.cur_entry_number))

        self.EntryToDisplay(self.tmpEntry)
        self.deleteButton.setEnabled(True)
        self.clear_entry_dirty()

    def print_entry(self):
        """Print a postscript file of the current display."""
        pprint(self.journal_file.get_entry(self.cur_entry_number))

    def oldprint_entry(self):
        """Print a postscript file of the current display."""
        printer = QtWidgets.QPrinter()
        printer.setOutputFileName('book.pdf')
        printer.setFullPage(True)
        printer.setPaperSize(QtWidgets.QPrinter.Letter)

        painter = QtWidgets.QPainter(printer)
        self.render(painter)
        del printer

    def search(self, string):
        '''Search the existing Titles and abbreviations for any entries
        that match or partially match the string in titleEdit. Pop a
        list window. If the users double clicks an entry, then return
        the index of the entry selected from the list and clear the
        searchflag.  Clear the search_flag if the users selects
        stopSearch.'''
        print('searching for "' + string + '"', self.search_flag)
        try:
            self.current_search_list = self.sdict.search(string.strip())
        except KeyError:
            self.current_search_list = None


    #
    # Set/Clear flags for Entry
    #
    def set_search_flag(self):
        """Set the  searchflag to True to enable searchs"""
        self.search_flag = True

    def clear_search_flag(self):
        """Set the search flag to False and disable searchs."""
        self.search_flag = False

    def set_entry_dirty(self):
        """Set the entry_dirty flag to True and enable the Save Entry
        button."""
        self.entry_dirty = True
        self.saveButton.setEnabled(True)
        # set menu item enable to True as well

    def clear_entry_dirty(self):
        """Set the entry_dirty flag to False and disable the Save
        Entry button."""
        self.entry_dirty = False
        self.saveButton.setEnabled(False)
        # set menu item enable False as well.
        # set Save File menu True

    def print_printer(self):
        printer = QtWidgets.QPrinter()
        printer.setOutputFileName('book.pdf')
        printer.setFullPage(True)
        printer.setPaperSize(QtWidgets.QPrinter.Letter)

        print_dialog = QtWidgets.QPrintDialog(printer, self)
        if print_dialog.exec_():
            painter = QtWidgets.QPainter(printer)
            self.render(painter)
            del painter


    #
    # Edit menu functions
    #
    def open_symbol_dialog(self):
        """Open the symbol entry form."""
        self.symbol_table = symbol.SymbolForm(self.symbol_table_name, 'FreeSans', 14, self)
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


    def edit_header(self):
        """Open the edit header form."""
        self.header_window = hw.HeaderWindow(self)
        self.header_window.setBookFile(self.journal_file)
        self.header_window.setWindowTitle(QtWidgets.QApplication.translate("headerWindow",
                                                                           "Edit heaaders - %s" % (self.journal_file.get_base_name()),
                                                                           None))
        self.header_window.setHeaderText(self.journal_file.get_header())
        self.header_window.show()

    #
    # Help menu functions
    #
    def help_string(self):
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

    def help_about(self):
        hstr = self.help_string()
        QtWidgets.QMessageBox.about(self, 'About Journals', hstr)


    #
    # Button slots and Signals
    #
    def on_prevButton_released(self):
        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        self.show_entry(self.cur_entry_number - 1)

    def on_nextButton_released(self):
        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        self.show_entry(self.cur_entry_number + 1)

    def index_changed(self):
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
                                                QtWidgets.QMessageBox.Save|QtWidgets.QMessageBox.No|QtWidgets.QMessageBox.Cancel)

            if ans == QtWidgets.QMessageBox.Save:
                self.save_entry()

        return ans

    def ask_save_file(self):
        """Ask if we should save the dirty file."""
        ans = None
        if self.journal_file.is_dirty():
            ans = QtWidgets.QMessageBox.warning(self, 'Save file?',
                                                'The File has changed. Do you want to save it?',
                                                QtWidgets.QMessageBox.Save|QtWidgets.QMessageBox.Discard|QtWidgets.QMessageBox.Cancel)

            if ans == QtWidgets.QMessageBox.Save:
                self.save_file()
                # set save file menu enable to False

        return ans

    def ask_open_file(self):
        """Open an existing file saving the old one if it is dirty."""
        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        if self.ask_save_file() == QtWidgets.QMessageBox.Cancel:
            return

        fname, filterA = QtWidgets.QFileDialog.getOpenFileName(self,
                                                               "%s -- Choose new file"%QtWidgets.QApplication.applicationName(),
                                                               self.journal_file.get_dir_name(), "*.xml")
        if fname:
            self.open_file(fname)

    #
    # Methods to deal with various display aspects
    #
    def set_window_title(self, name):
        """Creates the string 'Journal Entry vx.x - name' and
        places it into the window title.
        """
        title = QtWidgets.QApplication.translate("MainWindow",
                                                 "Journal Entry  v %s   -   %s" % (__version__, name),
                                                 None)
        self.setWindowTitle(title)

    def EntryToDisplay(self, entry):
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
            for p in entry['Publishers']:
                if not first:
                    astr += '\n'
                first = False
                if p.__contains__('Place'):
                    astr += p['Place']
                astr += ' : '
                if p.__contains__('Name'):
                    astr += p['Name']
                astr += ' : '
                if p.__contains__('startDate'):
                    astr += p['startDate']
                astr += ' : '
                if p.__contains__('endDate'):
                    astr += p['endDate']
        self.publisherEdit.setText(astr)


        astr = ''
        if entry.not_empty('Abbreviations'):
            first = True
            for a in entry['Abbreviations']:
                if not first:
                    astr += '\n'
                first = False
                astr += a
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
            for l in entry['linkprevious']:
                if not first:
                    astr += '\n'
                first = False
                astr += l
        self.LinkPreviousEdit.setText(astr)

        astr = ''
        if entry.not_empty('linknext'):
            first = True
            for l in entry['linknext']:
                if not first:
                    astr += '\n'
                first = False
                astr += l
        self.LinkNextEdit.setText(astr)

        astr = ''
        if entry.not_empty('Designators'):
            first = True
            for k in entry['Designators']:
                if not first:
                    astr += '\n'
                first = False
                astr += k
                astr += ' : '
                astr += entry['Designators'][k]
        self.designatorEdit.setText(astr)


        astr = ''
        if entry.not_empty('Comments'):
            first = True
            for c in entry['Comments']:
                if not first:
                    astr += '\n'
                first = False
                astr += c
        self.CommentsEdit.setText(astr)

        self.repaint()


    def DisplayToEntry(self):
        """Copy the display into a new entry and
        return the entry."""
        entry = journalentry.JournalEntry()

        # Titles
        a = self.titleEdit.toPlainText().strip()
        alen = len(a)
        if alen != 0:
            alist = a.split('\n')
            alist_len = len(alist)
            if len(alist[0]) == 0:
                return None
            entry['Title'] = alist[0]
            if alist_len > 1 and 0 != alist[1]:
                entry['subTitle'] = alist[1]
            if alist_len > 2 and 0 != alist[2]:
                entry['subsubTitle'] = alist[2]


        # Publishers
        a = self.publisherEdit.toPlainText()
        alen = len(a)
        if alen != 0:
            alist = a.split('\n')
            for line in alist:
                d = {}
                fields = line.split(':')
                num_fields = len(fields)
                # Check len(flds) here, pop dialog if not 4
                if num_fields > 0:
                    d['Place'] = fields[0].strip()
                if num_fields > 1:
                    d['Name'] = fields[1].strip()
                if num_fields > 2:
                    d['startDate'] = fields[2].strip()
                if num_fields > 3:
                    d['endDate'] = fields[3].strip()

                entry['Publishers'].append(d)


        # Abbreviations
        a = self.abbreviationsEdit.toPlainText()
        alen = len(a)
        if alen != 0:
            alist = a.split('\n')
            for line in alist:
                entry['Abbreviations'].append(line.strip())

        # startDate
        entry['startDate'] = self.startDateEdit.text().strip()

        # endDate
        entry['endDate'] = self.endDateEdit.text().strip()

        # link previous
        a = self.LinkPreviousEdit.toPlainText()
        alen = len(a)
        if alen != 0:
            alist = a.split('\n')
            for line in alist:
                entry['linkprevious'].append(line.strip())

        # link next
        a = self.LinkNextEdit.toPlainText()
        alen = len(a)
        if alen != 0:
            alist = a.split('\n')
            for line in alist:
                entry['linknext'].append(line.strip())

        # Designators
        a = self.designatorEdit.toPlainText()
        alen = len(a)
        if alen != 0:
            alist = a.split('\n')
            for line in alist:
                flds = line.split(':')
                entry['Designators'][flds[0].strip()] = flds[1].strip()


        # Comments
        a = self.CommentsEdit.toPlainText()
        alen = len(a)
        if alen != 0:
            alist = a.split('\n')
            for line in alist:
                entry['Comments'].append(line)

        return entry
