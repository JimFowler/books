## Begin copyright
##
## /home/jrf/Documents/books/Books20/Tools/python/aabooks/ajbbook/mainWindow.py
##
## Part of the Books20 Project
##
## Copyright 2018 James R. Fowler
##
## All rights reserved. No part of this publication may be
## reproduced, stored in a retrival system, or transmitted
## in any form or by any means, electronic, mechanical,
## photocopying, recording, or otherwise, without prior written
## permission of the author.
##
##
## End copyright

"""AJB/AAA dialog to review and edit books entries
"""

# pylint: disable=line-too-long
import platform
import sys
import traceback
import re
import os

# Trouble shooting assistance
from pprint import pprint

from PyQt5 import QtCore, QtGui, QtWidgets

from nameparser import HumanName

from aabooks.ajbbook import ui_BookEntry as BookEntry_ui
from aabooks.ajbbook import bookfile as bf
from aabooks.ajbbook import menus
from aabooks.ajbbook import origstrwindow as origstr
from aabooks.ajbbook import ajbentry
from aabooks.lib import headerwindow as hw
from aabooks.lib import symbol
from aabooks.lib import entryselect as es

__DIRNAME, __BASENAME = os.path.split(symbol.__file__)
__DEFAULT_SYMBOL_TABLE_NAME__ = __DIRNAME + '/symbols.txt'
del __DIRNAME
del __BASENAME


__version__ = '2.0'

# pylint: disable too-many-locals

class BookEntry(QtWidgets.QMainWindow, BookEntry_ui.Ui_MainWindow):
    """BookEntry is the class which handles the BookEntry form
    for display of entries from the text files.
    """

    def __init__(self):
        super(BookEntry, self).__init__()
        self.setupUi(self)

        self.tmp_entry = ajbentry.AJBentry()
        # This boolean indicates that the window entries
        # have been modified and that we should not change the
        # window contents without asking the user if they should
        # be saved.
        self.tmp_entry_dirty = False
        self.bookfile = None
        self.current_entry_number = 0
        self.set_max_entry_number(0)
        self.set_window_title('document1')
        self.insert_function = None
        self.default_volume_number = None
        self.symbol_table_name = __DEFAULTUSYMBOL_TABLE_NAME__
        self.symbol_table = None

        # Fields within an Entry that we know about already
        self.known_entry_fields = ['Index', 'Num', 'Authors', 'Editors', 'Title',
                                   'Publishers', 'Edition', 'Year',
                                   'Pagination', 'Price', 'Reviews',
                                   'Compilers', 'Contributors', 'Translators',
                                   'Language', 'TranslatedFrom', 'Reference',
                                   'Reprint', 'Others', 'OrigStr', 'Comments', ]

        # lists of which display fields may or may not have symbol entry allowed
        self.no_entry_list = ['volNum', 'secNum', 'subSecNum', 'itemNum',
                              'yearEntry', 'pageEntry', 'indexEntry',
                              'editionEntry', 'referenceEntry', 'reprintEntry']
        self.set_text_entry_list = ['authorEntry', 'editorEntry', 'titleEntry',
                                    'publEntry', 'reviewsEntry', 'translatorEntry',
                                    'compilersEntry', 'contribEntry', 'commentsEntry',
                                    'headerEntry']
        self.set_line_entry_list = ['fromlangEntry', 'tolangEntry', 'priceEntry']

        menus.create_menus(self, self.menubar)

        self.quitButton.released.connect(self.quit)
        self.newEntryButton.released.connect(self.new_entry)
        self.acceptButton.released.connect(self.save_entry)
        self.deleteButton.released.connect(self.delete_entry)
        self.insertButton.released.connect(self.ask_insert_entry)
        # self.nextButton.released.connect(self.on_nextButton_released)
        # self.prevButton.released.connect(self.on_prevButton_released)
        self.acceptButton.setEnabled(False)
        self.deleteButton.setEnabled(False)
        self.insertButton.setEnabled(False)

        self.indexEntry.returnPressed.connect(self.index_changed)

        self.volNum.textChanged.connect(self.set_entry_dirty)
        self.secNum.textChanged.connect(self.set_entry_dirty)
        self.subSecNum.textChanged.connect(self.set_entry_dirty)
        self.itemNum.textChanged.connect(self.set_entry_dirty)
        self.authorEntry.textChanged.connect(self.set_entry_dirty)
        self.editorEntry.textChanged.connect(self.set_entry_dirty)
        self.titleEntry.textChanged.connect(self.set_entry_dirty)
        self.publEntry.textChanged.connect(self.set_entry_dirty)
        self.editionEntry.textChanged.connect(self.set_entry_dirty)
        self.yearEntry.textChanged.connect(self.set_entry_dirty)
        self.pageEntry.textChanged.connect(self.set_entry_dirty)
        self.priceEntry.textChanged.connect(self.set_entry_dirty)
        self.reviewsEntry.textChanged.connect(self.set_entry_dirty)
        self.reprintEntry.textChanged.connect(self.set_entry_dirty)
        self.referenceEntry.textChanged.connect(self.set_entry_dirty)
        self.fromlangEntry.textChanged.connect(self.set_entry_dirty)
        self.tolangEntry.textChanged.connect(self.set_entry_dirty)
        self.translatorEntry.textChanged.connect(self.set_entry_dirty)
        self.compilersEntry.textChanged.connect(self.set_entry_dirty)
        self.contribEntry.textChanged.connect(self.set_entry_dirty)
        self.commentsEntry.textChanged.connect(self.set_entry_dirty)

        self.open_new_file()

    def set_max_entry_number(self, n):
        """comment"""
        if n < 0:
            n = 0
        self.max_entry_number = n

        if self.max_entry_number == 0:
            self.prevButton.setEnabled(False)
            self.nextButton.setEnabled(False)
        else:
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(True)

        self.ofnumLabel.setText('of %d' % self.max_entry_number)

    #
    # Menu and button slots
    #
    def quit(self):
        """comment"""
        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        if self.ask_save_file() == QtWidgets.QMessageBox.Cancel:
            return

        self.close()

    #
    # Menu and button slots for File actions
    #
    def open_new_file(self):
        """Create a new bookfile saving the old one if it is dirty."""
        if self.bf is not None:
            if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
                return

            if self.ask_save_file() == QtWidgets.QMessageBox.Cancel:
                return

        self.bookfile = bf.BookFile()
        self.set_max_entry_number(0)
        self.new_entry()

    def ask_open_file(self):
        """Open an existing file saving the old one if it is dirty."""
        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        if self.ask_save_file() == QtWidgets.QMessageBox.Cancel:
            return

        # else get a file name
        fname, filtera = QtWidgets.QFileDialog.getOpenFileName(self,
                                                               "%s -- Choose new file" % QtGui.QApplication.applicationName(),
                                                               self.bookfile.get_dirname(),
                                                               "All Files (*.*);;Text Files (*.txt);;XML Files (*.xml)")
        if fname:
            name, ext = os.path.splitext(fname)
            if ext == '':
                if filtera == 'XML Files (*.xml)':
                    fname += '.xml'
                else:
                    fname += '.txt'

            self.open_file(fname)

    def open_file(self, name=None):
        """Open an existing file, get the count of entries, and display
        the first entry. If no records are found we assume that this is
        a new file and we automatically generate a new entry."""

        self.set_max_entry_number(self.bookfile.read_file(name))
        if self.max_entry_number:
            self.statusbar.clearMessage()
            self.statusbar.showMessage(
                '%d records found' % self.max_entry_number, 6000)
            self.show_entry(1)
            self.insertButton.setEnabled(True)
            self.clear_entry_dirty()
        else:
            self.statusbar.showMessage('No records found in file %s' % name)
            self.new_entry()
        self.set_window_title(self.bookfile.get_basename_with_extension())

    def save_file(self):
        """Ignore dirty entries and just save the file."""

        if self.bookfile.get_filename() is None or self.bookfile.get_basename() == 'document1':
            if self.save_fileAs() == QtWidgets.QMessageBox.Cancel:
                return QtWidgets.QMessageBox.Cancel

        self.bookfile.write_file()

        self.statusbar.showMessage(
            'Saving file ' + self.bookfile.get_basename_with_extension())
        QtWidgets.QTimer.singleShot(10000, self.statusbar.clearMessage)

        return QtWidgets.QMessageBox.Save

    def save_file_as(self):
        """Ignore dirty entries and save the file as..."""
        fname, filterA = QtWidgets.QFileDialog.getSaveFileName(self,
                                                               "%s -- Choose file" % QtGui.QApplication.applicationName(),
                                                               self.bookfile.get_dirname(),
                                                               "All Files (*.*);;Text Files (*.txt);;XML Files (*.xml)")

        if fname:
            name, ext = os.path.splitext(fname)
            if ext == '':
                if filterA == 'XML Files (*.xml)':
                    fname += '.xml'
                else:
                    fname += '.txt'

            self.bookfile.write_file(fname)
            self.set_window_title(self.bookfile.get_basename_with_extension())
            return QtWidgets.QMessageBox.Save
        else:
            return QtWidgets.QMessageBox.Cancel

    #
    # Menu and button slots for Entry Actions on File menu
    #

    def save_entry(self):
        """Save the entry to the current entry number in the bookfile."""
        #
        # Save the back up file here
        #
        self.tmp_entry = self.display_to_entry()
        if not self.tmp_entry:
            QtWidgets.QMessageBox.information(self, "Entry Invalid",
                                              "Entry invalid!  Not saved in bookfile!")
            return

        if self.current_entry_number > self.max_entry_number:
            ret = self.bookfile.set_new_entry(self.tmp_entry, self.current_entry_number)
        else:
            ret = self.bookfile.set_entry(self.tmp_entry, self.current_entry_number)

        if not ret:
            QtWidgets.QMessageBox.information(self, "Entry Invalid",
                                              "Entry invalid!  Not saved in bookfile!")
            return

        if self.current_entry_number > self.max_entry_number:
            self.set_max_entry_number(self.current_entry_number)
        self.deleteButton.setEnabled(True)
        self.clear_entry_dirty()

    def new_entry(self):
        """Create a new entry, save the old one if it has been modified."""
        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        self.tmp_entry = ajbentry.AJBentry()
        self.current_entry_number = self.max_entry_number + 1
        self.tmp_entry['Index'] = self.current_entry_number
        self.entry_to_display(self.tmp_entry)
        self.indexEntry.setText(str(self.current_entry_number))
        if self.default_volume_number is not None:
            self.volNum.setText(self.default_volume_number)
        self.volNum.setFocus()
        self.deleteButton.setEnabled(False)
        if self.max_entry_number > 0:
            self.insertButton.setEnabled(True)
        self.clear_entry_dirty()

    def ask_insert_entry(self):
        """Open the entry_select form if we have a valid entry to insert.
        If the user selects an insertion location, then we execute the
        method insert_entry()"""
        self.tmp_entry = self.display_to_entry()
        if not self.tmp_entry or not self.tmp_entry.is_valid():
            QtWidgets.QMessageBox.information(self, "Entry Invalid",
                                              "Entry invalid!  Not saved in bookfile!")
            return

        entry_select = es.EntrySelect()
        entry_select.setText(self.bookfile.make_short_title_list())

        entry_select.show()
        entry_select.lineEmit.connect(self.insert_entry)

    def insert_entry(self, line):
        """Parse the short title line, get the index number and insert
        the current display entry in front of this entry in the booklist."""

        words = line[0].split(' ')

        try:
            num = int(words[0])
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Insert Invalid",
                                          "Unable to insert before {0}".format(words[0]))
            return

        if not num or num < 1 or num > self.max_entry_number:
            return

        self.bookfile.set_new_entry(self.tmp_entry, num)
        self.current_entry_number = num
        self.set_max_entry_number(self.max_entry_number + 1)
        self.show_entry(self.current_entry_number)
        pass

    def delete_entry(self):
        """Delete the entry at the current_entry_number but
        ask the user first."""
        ans = QtWidgets.QMessageBox.warning(self, 'Delete Entry?',
                                            'Are you sure you want to delete this entry? This action can not be undone!',
                                            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        if ans == QtWidgets.QMessageBox.Cancel:
            return

        self.set_max_entry_number(self.bookfile.delete_entry(self.current_entry_number))
        if self.max_entry_number < 1:
            self.insertButton.setEnable(False)
            self.new_entry()
        else:
            self.show_entry(self.current_entry_number)

    def show_entry(self, recnum=1):
        """show_entry(recnum) where 1 <= recnum <= max_entry_number.
        recnum is the index into the entry list.  The buttons will
        wrap around the index values.
        """
        self.prevButton.setEnabled(True)

        self.nextButton.setEnabled(True)

        if recnum < 1:
            # We add here because recnum is zero or negative already
            self.current_entry_number = self.max_entry_number + recnum
        elif recnum > self.max_entry_number:
            self.current_entry_number = recnum - self.max_entry_number
        else:
            self.current_entry_number = recnum

        # Display the actual entry data
        self.tmp_entry = self.bookfile.get_entry(self.current_entry_number)

        if not self.tmp_entry:
            return

        # Display record count
        self.indexEntry.setText(str(self.current_entry_number))

        self.EntryToDisplay(self.tmp_entry)
        self.deleteButton.setEnabled(True)
        self.clear_entry_dirty()

    def new_print_entry(self):
        """Print a postscript file of the current display."""
        pprint(self.bookfile.get_entry(self.current_entry_number))

    def print_entry(self):
        """Print a postscript file of the current display."""
        printer = QtGui.QPrinter()
        printer.setOutputFileName('book.pdf')
        printer.setFullPage(True)
        printer.setPaperSize(QtGui.QPrinter.Letter)

        painter = QtGui.QPainter(printer)
        self.render(painter)
        del painter

    #
    # Set/Clear flags for Entry
    #
    def set_entry_dirty(self):
        """Set the tmp_entry_dirty flag to True and enable the Save Entry button."""
        self.tmp_entry_dirty = True
        self.acceptButton.setEnabled(True)
        # set menu item enable to True as well

    def clear_entry_dirty(self):
        """Set the tmp_entry_dirty flag to False and disable the Save Entry button."""
        self.tmp_entry_dirty = False
        self.acceptButton.setEnabled(False)
        # set menu item enable False as well.
        # set Save File menu True

    def print_printer(self):
        """comment"""
        printer = QtGui.QPrinter()
        printer.setOutputFileName('book.pdf')
        printer.setFullPage(True)
        printer.setPaperSize(QtGui.QPrinter.Letter)

        prt = QtGui.QPrintDialog(pr, self)
        if prt.exec_():
            painter = QtGui.QPainter(pr)
            self.render(painter)
            del painter

    #
    # Edit menu functions
    #
    def open_symbol(self):
        """Open the symbol entry form."""
        self.symbol_table = symbol.SymbolForm(
            self.symbol_table_name, 'FreeSans', 14, self)
        self.symbol_table.show()
        self.symbol_table.sigClicked.connect(self.insert_char)

    def set_symbol_table_name(self, name):
        """Set the name of the symbol table to use in place of the
        default table."""
        self.symbol_table_name = name

    def edit_header(self):
        """Open the edit header form."""
        header_window = hw.HeaderWindow(self)
        header_window.set_book_file(self.bookfile)
        header_window.setWindowTitle(QtWidgets.QApplication.translate("headerWindow",
                                                                      "Edit Headers - %s" % (self.bookfile.get_basename_with_extension()), None))
        header_window.set_header_text(self.bookfile.getHeader())
        header_window.show()

    def show_orig_str(self):
        """Open a dialog box with the original string entry."""
        self.origstr_window = origstr.OrigStrWindow()

        if self.tmp_entry.not_empty('Index'):
            self.origstr_window.setFileName(self.tmp_entry['Index'])
        else:
            self.origstr_window.setFileName(-1)

        if self.tmp_entry.not_empty('OrigStr'):
            self.origstr_window.setOrigStrText(self.tmp_entry['OrigStr'])
        else:
            self.origstr_window.setOrigStrText(
                'Entry does not have the original string defined.')
        self.origstr_window.show()

    #
    # Button slots and Signals
    #
    def on_prev_button_released(self):
        """comment"""
        if self.ask_save_entry() != QtWidgets.QMessageBox.Cancel:
            self.show_entry(self.current_entry_number - 1)

    def on_next_button_released(self):
        """comment"""
        if self.ask_save_entry() != QtWidgets.QMessageBox.Cancel:
            self.show_entry(self.current_entry_number + 1)

    def index_changed(self):
        """comment"""
        try:
            enum = int(self.indexEntry.text())
        except ValueError:
            QtWidgets.QMessageBos.warning(self, 'Index Changed',
                                          'Invalid index entry {0}'.format(self.indexEntry.text()),
                                          QtWidgets.QMessageBox.Ok)
            return

        if self.ask_save_entry() == QtWidgets.QMessageBox.Cancel:
            return

        self.show_entry(enum)

    #
    # Various useful dialogs
    #
    def ask_save_entry(self):
        """Ask if we should save the dirty entry."""
        ans = None
        if self.tmp_entry_dirty:
            ans = QtWidgets.QMessageBox.warning(self, 'Save Entry?',
                                                'Entry has changed. Do you want to save it?',
                                                QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel,
                                                QtWidgets.QMessageBox.Save)

            if ans == QtWidgets.QMessageBox.Save:
                self.save_entry()

        return ans

    def ask_save_file(self):
        """Ask if we should save the dirty file."""
        ans = None
        if self.bookfile.is_dirty():
            ans = QtWidgets.QMessageBox.warning(self, 'Save file?',
                                                'The File has changed. Do you want to save it?',
                                                QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)

            if ans == QtWidgets.QMessageBox.Save:
                ans = self.save_file()
                # set save file menu enable to False

        return ans

    #
    # Methods to deal with various display aspects
    #
    def set_window_title(self, name):
        """Creates the string 'AJB Book Entry vx.x - name' and
        places it into the window title.
        """
        self.setWindowTitle(QtWidgets.QApplication.translate("MainWindow",
                                                             "AJB Book Entry  v %s   -   %s" % (
                                                                 __version__, name),
                                                             None))

    def set_default_volume_number(self, num):
        """Sets the default volume number for new entries."""
        self.default_volume_number = num

    def set_volume_number_interactive(self):
        """Provides an interactive dialog to set the default
        volume number for new entries."""
        curVal = self.default_volume_number
        numVal, ok = QtWidgets.QInputDialog.getText(self, 'Volume Number',
                                                    'Enter New Volume Number\n(next new entry will use this value)',
                                                    text=curVal)
        if ok:
            self.default_volume_number = numVal

    def entry_to_display(self, entry):
        """Given an entry, display the parts on the GUI display."""

        # AJB number
        a = entry['Num']
        self.volNum.setText(str(a['volNum']))
        self.secNum.setText(str(a['sectionNum']))
        if int(a['subsectionNum']) > -1:
            self.subSecNum.setText(str(a['subsectionNum']))
        else:
            self.subSecNum.setText('0')
        self.itemNum.setText(str(a['entryNum']) + a['entrySuf'])

        # Authors
        astr = ''
        if entry.not_empty('Authors'):
            a = entry['Authors']
            if a:
                first = True
                for b in a:
                    if not first:
                        astr += '\n'
                    first = False
                    astr += str(b)
        self.authorEntry.setText(astr)

        # Editors
        astr = ''
        if entry.not_empty('Editors'):
            a = entry['Editors']
            if a:
                first = True
                for b in a:
                    if not first:
                        astr += '\n'
                    first = False
                    astr += str(b)
        self.editorEntry.setText(astr)

        # Title
        astr = ''
        if entry.not_empty('Title'):
            astr += entry['Title']
        self.titleEntry.setText(astr)

        # Publishers
        astr = ''
        if entry.not_empty('Publishers'):
            first = True
            for a in entry['Publishers']:
                if not first:
                    astr += '\n'
                first = False
                astr += a['Place'] + ' : ' + a['PublisherName']
        self.publEntry.setText(astr)

        # Edition
        astr = ''
        if entry.not_empty('Edition'):
            astr += entry['Edition']
        self.editionEntry.setText(astr)

        # Year
        astr = ''
        if entry.not_empty('Year'):
            astr += entry['Year']
        self.yearEntry.setText(astr)

        # Pagination
        astr = ''
        if entry.not_empty('Pagination'):
            astr += entry['Pagination']
        self.pageEntry.setText(astr)

        # Price
        astr = ''
        if entry.not_empty('Price'):
            astr += entry['Price']
        self.priceEntry.setText(astr)

        # Review
        astr = ''
        if entry.not_empty('Reviews'):
            rev = entry['Reviews']
            first = True
            if rev:
                for item in rev:
                    if not first:
                        astr += '\n'
                    astr += item
                    first = False
        self.reviewsEntry.setPlainText(astr)

        # Language
        astr = ''
        if entry.not_empty('Language'):
            astr += entry['Language']
        self.tolangEntry.setText(astr)

        # fromLanguage
        astr = ''
        if entry.not_empty('TranslatedFrom'):
            astr += entry['TranslatedFrom']
        self.fromlangEntry.setText(astr)

        # Translators
        astr = ''
        if entry.not_empty('Translators'):
            a = entry['Translators']
            if a:
                first = True
                for b in a:
                    if not first:
                        astr += '\n'
                    first = False
                    astr += str(b)
        self.translatorEntry.setText(astr)

        # Compilers
        astr = ''
        if entry.not_empty('Compilers'):
            a = entry['Compilers']
            if a:
                first = True
                for b in a:
                    if not first:
                        astr += '\n'
                    first = False
                    astr += str(b)
        self.compilersEntry.setText(astr)

        # Contributors
        astr = ''
        if entry.not_empty('Contributors'):
            a = entry['Contributors']
            if a:
                first = True
                for b in a:
                    if not first:
                        astr += '\n'
                    first = False
                    astr += str(b)
        self.contribEntry.setText(astr)

        # Reprint
        astr = ''
        if entry.not_empty('Reprint'):
            astr += entry['Reprint']
        self.reprintEntry.setText(astr)

        # Reference
        astr = ''
        if entry.not_empty('Reference'):
            astr += entry['Reference']
        self.referenceEntry.setText(astr)

        # Others
        astr = ''
        if entry.not_empty('Others'):
            a = entry['Others']
            first = True
            for b in a:
                if not first:
                    astr += '\n'
                first = False
                astr += str(b)
        self.commentsEntry.setPlainText(astr)

        for field in entry.keys():
            if self.known_entry_fields.count(field) == 0:
                QMessageBox.warning(self, 'Unknown Entry Field',
                                    'Unknown field "%s:  %s"\n in entry %s\n "' %
                                    (field, entry[field], entry['Index']),
                                    QMessageBox.Ok)
        self.repaint()

    def display_to_entry(self):
        """Copy the display into a new entry and
        return the entry."""

        # Note: that this regex will silently reject a suffix
        #     that is not '' or [a-c].
        r2 = re.compile(r'(\d+)([a-c]{0,1})', re.UNICODE)
        items = r2.split(self.itemNum.text().strip())

        entry = ajbentry.AJBentry()

        # Index
        try:
            index = int(self.indexEntry.text())
            entry['Index'] = str(index - 1)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb = traceback.format_tb(exc_traceback)
            tb_str = ''
            for s in tb:
                tb_str = tb_str + s
            tb_str = tb_str + '\n\n Invalid Index number'
            QtWidgets.QMessageBox.warning(self, 'Invalid Index Num',
                                          tb_str, QMessageBox.Ok)
            return None

        # AJB number
        num = {}
        num['volume'] = 'AJB'

        try:
            num['volNum'] = int(self.volNum.text())
            num['sectionNum'] = int(self.secNum.text())
            num['subsectionNum'] = int(self.subSecNum.text())
            num['entryNum'] = int(items[1])
            num['entrySuf'] = items[2]
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb = traceback.format_tb(exc_traceback)
            tb_str = ''
            for s in tb:
                tb_str = tb_str + s
            tb_str = tb_str + '\n\n Invalid AJB Entry number'
            QtWidgets.QMessageBox.warning(self, 'Invalid AJB Num',
                                          tb_str, QMessageBox.Ok)
            return None

        entry['Num'] = num
        if not entry.is_valid_ajbNum():
            QtWidgets.QMessageBox.warning(self, 'Invalid number',
                                          'Entry must have a valid AJB num in order to be valid',
                                          QtWidgets.QMessageBox.Ok)
            return None

        # Authors
        entrya = []
        a = self.authorEntry.toPlainText()
        if a:
            alist = a.split('\n')
            for line in alist:
                nm = HumanName(line)
                entrya.append(nm)
        entry['Authors'] = entrya

        # Editors
        entrya = []
        a = self.editorEntry.toPlainText()
        if a:
            alist = a.split('\n')
            for line in alist:
                nm = HumanName(line)
                entrya.append(nm)
        entry['Editors'] = entrya

        # Title
        a = self.titleEntry.toPlainText()
        if a:
            entry['Title'] = a
        else:
            # warn that there is no title
            QtWidgets.QMessageBox.warning(self, 'No Title',
                                          'Entry must have a title in order to be valid',
                                          QtWidgets.QMessageBox.Ok)
            return None

        # Publishers
        entrya = []
        a = self.publEntry.toPlainText()
        if len(a) != 0:
            alist = a.split('\n')
            for line in alist:
                nm = {}
                try:
                    place, publisher = line.split(':')
                except:
                    # warn that there is no title
                    QtWidgets.QMessageBox.warning(self, 'No Colon in publishing',
                                                  'Publishing field must be Place : PublisherName.\nColon is missing.',
                                                  QtWidgets.QMessageBox.Ok)
                    return None

                if not place:
                    place = ''
                if not publisher:
                    publisher = ''
                nm['Place'] = place.strip()
                nm['PublisherName'] = publisher.strip()
                entrya.append(nm)
        entry['Publishers'] = entrya

        # Edition
        a = self.editionEntry.text()
        if len(a) != 0:
            entry['Edition'] = a

        # Year
        a = self.yearEntry.text()
        if len(a) != 0:
            entry['Year'] = a

        # Pagination
        a = self.pageEntry.text()
        if len(a) != 0:
            entry['Pagination'] = a

        # Price
        a = self.priceEntry.text()
        if len(a) != 0:
            entry['Price'] = a

        # Review
        entrya = []
        a = self.reviewsEntry.toPlainText()
        if len(a) != 0:
            alist = a.split('\n')
            for line in alist:
                entrya.append(line)
        entry['Reviews'] = entrya

        # Language
        a = self.tolangEntry.text()
        if len(a) != 0:
            entry['Language'] = a

        # fromLanguage
        a = self.fromlangEntry.text()
        if len(a) != 0:
            entry['TranslatedFrom'] = a

        # Translators
        entrya = []
        a = self.translatorEntry.toPlainText()
        if len(a) != 0:
            alist = a.split('\n')
            for line in alist:
                nm = HumanName(line)
                entrya.append(nm)
        entry['Translators'] = entrya

        # Compilers
        entrya = []
        a = self.compilersEntry.toPlainText()
        if len(a) != 0:
            alist = a.split('\n')
            for line in alist:
                nm = HumanName(line)
                entrya.append(nm)
        entry['Compilers'] = entrya

        # Contributors
        entrya = []
        a = self.contribEntry.toPlainText()
        if len(a) != 0:
            alist = a.split('\n')
            for line in alist:
                nm = HumanName(line)
                entrya.append(nm)
        entry['Contributors'] = entrya

        # Reprint
        a = self.reprintEntry.text()
        if len(a) != 0:
            entry['Reprint'] = a

        # Reference
        a = self.referenceEntry.text()
        if len(a) != 0:
            entry['Reference'] = a

        # Others
        entrya = []
        a = self.commentsEntry.toPlainText()
        if len(a) != 0:
            alist = a.split('\n')
            for line in alist:
                entrya.append(line)
        entry['Others'] = entrya

        return entry

    def insert_char(self, obj):
        """Insert the charactor in obj[0] with self.insert_function
        if insert_function is not None."""

        char = obj[0]
        # invoke self.insert_function(char)
        if self.insert_function is not None:
            self.insert_function(char)
        # take back focus somehow??

    def set_focus_changed(self, oldWidget, nowWidget):
        """For items in set_text_entry_list and set_line_entry_list
        set insert_function to be either insertPlainText or insert."""

        if oldWidget is None:
            pass
        elif oldWidget.objectName() == 'indexEntry':
            self.indexEntry.setText(str(self.current_entry_number))

        if nowWidget is None:
            pass
        elif self.set_text_entry_list.count(nowWidget.objectName()):
            self.insert_function = nowWidget.insertPlainText
        elif self.set_line_entry_list.count(nowWidget.objectName()):
            self.insert_function = nowWidget.insert
        elif self.no_entry_list.count(nowWidget.objectName()):
            self.insert_function = None

    #
    # Help menu functions
    #

    def help_string(self):
        """comment"""
        help_str = """<b>AJB Book Entry</b> v {0}
      <p>Author: J. R. Fowler
      <p>Copyright &copy; 2012-2017
      <p>All rights reserved.
      <p>This application is used to create and visualize
      the text files with the books found in the annual
      bibliographies of <b>Astronomischer Jahresbericht</b>.
      <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(__version__,
                                                         platform.python_version(),
                                                         QtCore.QT_VERSION_STR, QtCore.PYQT_VERSION_STR,
                                                         platform.system())

        return help_str

    def help_about(self):
        """comment"""
        hstr = self.help_string()
        QtWidgets.QMessageBox.about(self, 'About BookEntry', hstr)


#
# Test routine
#


if __name__ == '__main__':

    APP = QtWidgets.QApplication(sys.argv)
    APP.setApplicationName('Book Entry')
    FORM = BookEntry()
    APP.focusChanged.connect(FORM.set_focus_changed)

    FORM.show()
    sys.exit(APP.exec_())
