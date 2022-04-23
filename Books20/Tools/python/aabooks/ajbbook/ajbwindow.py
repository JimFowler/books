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
import re
import os

# Trouble shooting assistance
from pprint import pprint

from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport

from aabooks.ajbbook import ui_BookEntry as BookEntry_ui
from aabooks.ajbbook import bookfile as bf
from aabooks.ajbbook import menus
from aabooks.ajbbook import origstrwindow as origstr
from aabooks.ajbbook import ajbentry
from aabooks.ajbbook import version as ajbver
from aabooks.ajbbook import entrydisplay

from aabooks.lib import headerwindow as hw
from aabooks.lib import symbol
from aabooks.lib import entryselect as es
from aabooks.lib import version as libver

__DIRNAME, __BASENAME = os.path.split(symbol.__file__)
__DEFAULT_SYMBOL_TABLE_NAME__ = __DIRNAME + '/symbols.txt'
del __DIRNAME
del __BASENAME


__version__ = '2.0'

# Note: that this regex will silently reject a suffix
#     that is not '' or [a-c].
r2 = re.compile(r'(\d+)([a-c]{0,1})', re.UNICODE)

# pylint: disable too-many-locals

def help_string():
    """comment"""
    help_str = """<b>AJB Book Entry</b> v {0}
  <p>Author: J. R. Fowler
  <p>Copyright &copy; 2012-2020
  <p>All rights reserved.
  <p>This application is used to create and visualize
  the text files with the books found in the annual
  bibliographies of <b>Astronomischer Jahresbericht</b>.
  <p>aabooks/lib v {1}
  <p>Python {2} - Qt {3} - PyQt {4} on {5}""".format(ajbver.__version__,
                                                     libver.__version__,
                                                     platform.python_version(),
                                                     QtCore.QT_VERSION_STR, QtCore.PYQT_VERSION_STR,
                                                     platform.system())

    return help_str

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
        self.default_volume_number = '1'
        self.default_volume_name = 'AJB'
        self.symbol_table_name = __DEFAULT_SYMBOL_TABLE_NAME__
        self.symbol_window = None
        self.header_window = None

        # Fields within an Entry that we know about already
        self.known_entry_fields = ['Index', 'Num', 'Authors', 'Editors', 'Title',
                                   'Publishers', 'Edition', 'Year',
                                   'Pagination', 'Price', 'Reviews',
                                   'Compilers', 'Contributors', 'Translators',
                                   'Language', 'TranslatedFrom', 'TranslationOf',
                                   'Reference', 'Reprint', 'Others', 'OrigStr',
                                   'Comments', 'Keywords']


        # lists of which display fields may or may not have symbol entry allowed
        self.no_entry_list = ['volNum', 'secNum', 'subSecNum', 'itemNum', 'pageNum'
                              'yearEntry', 'pageEntry', 'indexEntry',
                              'editionEntry', 'referenceEntry', 'reprintEntry',
                              'transofEntry']
        self.set_text_entry_list = ['authorEntry', 'editorEntry', 'titleEntry',
                                    'publEntry', 'reviewsEntry', 'translatorEntry',
                                    'compilersEntry', 'contribEntry', 'commentsEntry',
                                    'keywordEntry', 'headerEntry']
        self.set_line_entry_list = ['fromlangEntry', 'tolangEntry', 'priceEntry']

        menus.create_menus(self, self.menubar)

        self.quitButton.released.connect(self.quit)
        self.newEntryButton.released.connect(self.new_entry)
        self.acceptButton.released.connect(self.save_entry)
        self.deleteButton.released.connect(self.delete_entry)
        self.insertButton.released.connect(self.ask_insert_entry)
        self.nextButton.released.connect(self.on_next_button_released)
        self.prevButton.released.connect(self.on_prev_button_released)
        self.acceptButton.setEnabled(False)
        self.deleteButton.setEnabled(False)
        self.insertButton.setEnabled(False)

        self.indexEntry.returnPressed.connect(self.index_changed)

        self.volNum.textChanged.connect(self.set_entry_dirty)
        self.secNum.textChanged.connect(self.set_entry_dirty)
        self.subSecNum.textChanged.connect(self.set_entry_dirty)
        self.itemNum.textChanged.connect(self.set_entry_dirty)
        self.pageNum.textChanged.connect(self.set_entry_dirty)
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
        self.transofEntry.textChanged.connect(self.set_entry_dirty)
        self.compilersEntry.textChanged.connect(self.set_entry_dirty)
        self.contribEntry.textChanged.connect(self.set_entry_dirty)
        self.commentsEntry.textChanged.connect(self.set_entry_dirty)
        self.keywordEntry.textChanged.connect(self.set_entry_dirty)

        self.open_new_file()

    def set_max_entry_number(self, count):
        """comment"""
        if count < 0:
            count = 0
        self.max_entry_number = count

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
        if self.bookfile is not None and self.bookfile.is_dirty():
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
        fname, filter_a = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                "%s -- Choose new file" % QtWidgets.QApplication.applicationName(),
                                                                os.path.dirname(self.bookfile.filename),
                                                                "All Files (*.*);;Text Files (*.txt);;XML Files (*.xml)")
        if fname:
            name = os.path.splitext(fname)
            if name[1] == '':
                if filter_a == 'XML Files (*.xml)':
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
        self.set_window_title(os.path.basename(self.bookfile.filename))

    def save_file(self):
        """Ignore dirty entries and just save the file."""

        if self.bookfile.filename is None or os.path.basename(self.bookfile.filename) == 'document1.xml':
            if self.save_file_as() == QtWidgets.QMessageBox.Cancel:
                return QtWidgets.QMessageBox.Cancel

        self.bookfile.write_file()

        self.statusbar.showMessage(
            'Saving file ' + os.path.basename(self.bookfile.filename))
        QtCore.QTimer.singleShot(10000, self.statusbar.clearMessage)

        return QtWidgets.QMessageBox.Save

    def save_file_as(self):
        """Ignore dirty entries and save the file as..."""
        fname, filter_a = QtWidgets.QFileDialog.getSaveFileName(self,
                                                                "%s -- Choose file" % QtWidgets.QApplication.applicationName(),
                                                                os.path.dirname(self.bookfile.filename),
                                                                "All Files (*.*);;Text Files (*.txt);;XML Files (*.xml)")

        if fname:
            name = os.path.splitext(fname)
            if name[1] == '':
                if filter_a == 'XML Files (*.xml)':
                    fname += '.xml'
                else:
                    fname += '.txt'

            self.bookfile.write_file(fname)
            self.set_window_title(os.path.basename(self.bookfile.filename))
            return QtWidgets.QMessageBox.Save

        return QtWidgets.QMessageBox.Cancel

    #
    # Menu and button slots for Entry Actions on File menu
    #

    def display_entry_is_valid(self):
        """Check the entry for validity before we do anything else.  This
        function returns the tuple (valid, errorfield, errortb), where
        valid is True/False, errorfield is the field which is not
        valid, and errortb is the reason it is not valid, basicly the traceback
        from the exception.

        """

        valid = True
        error_string = ''

        try:
            int(self.indexEntry.text())
        except ValueError:
            valid = False
            error_string = 'Invalid index number.\n'

        num = {}
        try:
            num['volNum'] = int(self.volNum.text())
        except ValueError:
            valid = False
            error_string += 'Invalid volume number.\n'

        try:
            num['sectionNum'] = int(self.secNum.text())
        except ValueError:
            valid = False
            error_string += 'Invalid section number.\n'

        try:
            num['subsectionNum'] = int(self.subSecNum.text())
        except ValueError:
            valid = False
            error_string += 'Invalid sub-section number.\n'

        try:
            items = r2.split(self.itemNum.text().strip())
            num['entryNum'] = int(items[1])
            num['entrySuf'] = items[3]
        except (ValueError, IndexError):
            valid = False
            error_string += 'Invalid item number.\n'


        try:
            num['pageNum'] = int(self.pageNum.text())
        except ValueError:
            valid = False
            error_string += 'Invalid page number.'


        if valid: # Then test the complete AJB num
            entry = ajbentry.AJBentry()
            entry['Num'] = num
            if not entry.is_valid_ajbnum():
                valid = False
                error_string += 'AJB number is not valid.\n'

        if not self.titleEntry.toPlainText():
            # warn that there is no title
            valid = False
            error_string += 'Invalid or missing title string.\n'

        publ_entries = self.publEntry.toPlainText()
        if len(publ_entries) != 0:
            alist = publ_entries.split('\n')
            for line in alist:
                try:
                    line.split(':')
                except ValueError:
                    valid = False
                    error_string += 'No colon in publisher line: {}.\n'.format(line)

        return (valid, error_string)


    def save_entry(self):
        """Save the entry to the current entry number in the bookfile."""
        #
        # Save the back up file here
        #
        valid, error_str = self.display_entry_is_valid()
        if not valid:
            QtWidgets.QMessageBox.information(self, "Entry Invalid", error_str + \
                                              '\nEntry invalid!  Not saved in bookfile!')
            return

        self.tmp_entry = self.display_to_entry()

        if self.current_entry_number > self.max_entry_number:
            ret = self.bookfile.set_new_entry(self.tmp_entry, self.current_entry_number - 1)
        else:
            ret = self.bookfile.set_entry(self.tmp_entry, self.current_entry_number - 1)

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
        entry_select.set_text(self.bookfile.make_short_title_list())

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

        self.bookfile.set_new_entry(self.tmp_entry, num - 1)
        self.current_entry_number = num
        self.set_max_entry_number(self.max_entry_number + 1)
        self.show_entry(self.current_entry_number)

    def delete_entry(self):
        """Delete the entry at the current_entry_number but
        ask the user first."""
        ans = QtWidgets.QMessageBox.warning(self, 'Delete Entry?',
                                            'Are you sure you want to delete this entry? This action can not be undone!',
                                            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        if ans == QtWidgets.QMessageBox.Cancel:
            return

        self.set_max_entry_number(self.bookfile.delete_entry(self.current_entry_number - 1))
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

        # Display the actual entry data, the bookfile is 0-based
        self.tmp_entry = self.bookfile.get_entry(self.current_entry_number - 1)

        if not self.tmp_entry:
            return

        # Display record count
        self.indexEntry.setText(str(self.current_entry_number))
 
        self.entry_to_display(self.tmp_entry)
        self.deleteButton.setEnabled(True)
        self.clear_entry_dirty()

    def new_print_entry(self):
        """Print a postscript file of the current display."""
        pprint(self.bookfile.get_entry(self.current_entry_number))

    def print_entry(self):
        """Print a postscript file of the current display."""
        printer = QtPrintSupport.QPrinter()
        printer.setOutputFileName('book.pdf')
        printer.setFullPage(True)
        printer.setPaperSize(QtPrintSupport.QPrinter.Letter)

        painter = QtGui.QPainter(printer)
        self.render(painter)
        del painter

    #
    # Set/Clear flags for Entry
    #
    def set_entry_dirty(self):
        """Set the tmp_entry_dirty flag to True and enable the Save Entry
        button.

        """
        self.tmp_entry_dirty = True
        self.acceptButton.setEnabled(True)
        # set menu item enable to True as well

    def clear_entry_dirty(self):
        """Set the tmp_entry_dirty flag to False and disable the Save Entry
        button.

        """
        self.tmp_entry_dirty = False
        self.acceptButton.setEnabled(False)
        # set menu item enable False as well.
        # set Save File menu True

    def print_printer(self):
        """comment"""
        printer = QtPrintSupport.QPrinter()
        printer.setOutputFileName('book.pdf')
        printer.setFullPage(True)
        printer.setPaperSize(QtPrintSupport.QPrinter.Letter)

        self.prt = QtPrintSupport.QPrintDialog(printer, self)
        if self.prt.exec_():
            painter = QtGui.QPainter(printer)
            self.render(painter)
            del painter
        else:
            print('print dialog does not return')
    #
    # Edit menu functions
    #
    def open_symbol(self):
        """Open the symbol entry form."""
        self.symbol_window = symbol.SymbolForm(
            self.symbol_table_name, 'FreeSans', 14, parent=self)
        self.symbol_window.show()
        self.symbol_window.sigClicked.connect(self.insert_char)

    def set_symbol_table_name(self, name):
        """Set the name of the symbol table to use in place of the
        default table."""
        self.symbol_table_name = name

    def edit_header(self):
        """Open the edit header form."""
        self.header_window = hw.HeaderWindow(parent=self)
        self.header_window.set_bookfile(self.bookfile)
        self.header_window.setWindowTitle(QtWidgets.QApplication.translate("headerWindow",
                                                                           "Edit Headers - %s" % (os.path.basename(self.bookfile.filename)), None))
        self.header_window.set_header_text(self.bookfile.get_header())
        self.header_window.show()

    def show_orig_str(self):
        """Open a dialog box with the original string entry."""
        self.origstr_window = origstr.OrigStrWindow()

        if self.tmp_entry.not_empty('Index'):
            self.origstr_window.set_filename(self.tmp_entry['Index'])
        else:
            self.origstr_window.set_filename(-1)

        if self.tmp_entry.not_empty('OrigStr'):
            self.origstr_window.set_origstr_text(self.tmp_entry['OrigStr'])
        else:
            self.origstr_window.set_origstr_text(
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
            QtWidgets.QMessageBox.warning(self, 'Index Changed',
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

    def set_default_volume_name(self, name):
        """Sets the default volume name for new entries.
        Default is 'AJB'"""
        self.default_volume_name = name

    def set_volume_number_interactive(self):
        """Provides an interactive dialog to set the default
        volume number for new entries."""
        current_val = self.default_volume_number
        volume_num, is_ok = QtWidgets.QInputDialog.getText(self, 'Volume Number',
                                                           'Enter New Volume Number\n(next new entry will use this value)',
                                                           text=current_val)
        if is_ok:
            self.default_volume_number = volume_num

    def set_volume_name_interactive(self):
        """Provides an interactive dialog to set the default
        volume name for new entries."""
        current_val = self.default_volume_name
        volume_name, is_ok = QtWidgets.QInputDialog.getText(self, 'Volume Name',
                                                           'Enter New Volume Name\n(next new entry will use this value)',
                                                           text=current_val)
        if is_ok:
            self.default_volume_name = volume_name
            
    def insert_char(self, obj):
        """Insert the charactor in obj[0] with self.insert_function
        if insert_function is not None."""

        char = obj[0]
        # invoke self.insert_function(char)
        if self.insert_function is not None:
            self.insert_function(char)
        # take back focus somehow??

    def set_focus_changed(self, old_widget, now_widget):
        """For items in set_text_entry_list and set_line_entry_list
        set insert_function to be either insertPlainText or insert."""

        if old_widget is None:
            pass
        elif old_widget.objectName() == 'indexEntry':
            self.indexEntry.setText(str(self.current_entry_number))

        if now_widget is None:
            pass
        elif self.set_text_entry_list.count(now_widget.objectName()):
            self.insert_function = now_widget.insertPlainText
        elif self.set_line_entry_list.count(now_widget.objectName()):
            self.insert_function = now_widget.insert
        elif self.no_entry_list.count(now_widget.objectName()):
            self.insert_function = None

    def entry_to_display(self, entry):
        '''Given an entry, display the parts on the GUI display.'''

        entrydisplay.entry_to_display(self, entry)
        self.repaint()

    def display_to_entry(self):
        '''Copy the display into a new entry and
        return the entry.'''
        return entrydisplay.display_to_entry(self)

    #
    # Help menu functions
    #

    def help_about(self):
        """comment"""
        hstr = help_string()
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
