#! /usr/bin/env python3
#
# Begin copyright
##
# /home/jrf/Documents/books/Books20/Tools/python/aabooks/ajbbook/bookfile.py
##
# Part of the Books20 Project
##
# Copyright 2018 James R. Fowler
##
# All rights reserved. No part of this publication may be
# reproduced, stored in a retrival system, or transmitted
# in any form or by any means, electronic, mechanical,
# photocopying, recording, or otherwise, without prior written
# permission of the author.
##
##
# End copyright
"""Defines the class that handles disk files and entry lists"""

import fileinput
import os
import sys
import traceback
from lxml import etree

from aabooks.ajbbook import ajbentry

__VERSION__ = 0.1

__DEFAULTHEADER__ = """Entry format

Num AJB_ID Author [and author [and …]] [ed.|comp.], Title, Place, Publisher, year, description, price, review [and review [and …]], comments

AJB_ID   volume.section[(subsection)].entry, for example 68.144(1).25 would be volume 68, section 144, subsection 1, and entry number 25.

Commas are field separators for automatic parsing.  Use the word ‘comma’ if you want the character in field string. We will use global search and replace after parsing into fields.

Save as Unicode UTF-8 text encoding. Skip section 4 in Part 1

For volume AJB ?? Index to the Literature of ????, started, finished, proofread


"""
# end of defaultHeader


class BookFile():
    """The BookFile class handles the disk file and entry list
    for book lists from AJB/AAA. It handles all the translation
    between the disk file format and the AJBentry format."""

    # pylint: disable=too-many-instance-attributes,too-many-public-methods
    def __init__(self):
        self._header = __DEFAULTHEADER__
        self._entry_list = []

        self._volume_number = -1
        self._filename = './document1'
        self._dirname = './'
        self._basename = 'document1'
        self._extension = '.txt'
        # 1 <= current_entry_index <= len(self._entry_list)
        self.current_entry_index = -1

        self.set_filename('document1')
        self._dirty = False

    # dirty (modified) file

    def is_dirty(self):
        """Returns a boolean. The value is True if any of the entries
        or the header has changed since the last read() or write().
        """
        return self._dirty

    # volume number
    def set_volume_number(self, vol):
        """Set the default volume number for this file."""
        self._volume_number = vol

    def get_volume_number(self):
        """Return the current default volume number."""
        return self._volume_number

    # file name

    def set_filename(self, filename):
        """Set the name of the disk file. Thus one can read a file,
        set a new file name, and save the file. No validity checking
        is done at this stage."""
        self._filename = filename
        self._dirname, _basename = os.path.split(filename)
        self._basename, self._extension = os.path.splitext(_basename)
        self._dirty = True

    def get_filename(self):
        """Return the current value of the fileName."""
        return self._filename

    def get_dirname(self):
        """Returns the dirname() of the current filename."""
        return self._dirname

    def get_basename(self):
        """Returns the basename() of the current filename."""
        return self._basename

    def get_basename_with_extension(self):
        """Returns the baseName().extension() of the current filename."""
        return self._basename + self._extension

    def get_extension(self):
        """Returns the extension() of the current filename."""
        return self._extension

    # header

    def set_header(self, headerstr):
        """Set the header entry to be headerStr."""
        self._dirty = True
        self._header = headerstr

    def get_header(self):
        """Return the current header string."""
        return self._header

    # current entry

    def get_entry(self, count=-1):
        """Returns the entry at position count. If count is less than 0
        or greater than the number of entries, 'None' is returned. Note
        that 1 <= count <= len(self._entry_list).
        """
        if count < 1 or count > len(self._entry_list):
            return None

        self.current_entry_index = count - 1
        return self._entry_list[self.current_entry_index]

    def set_entry(self, entry, count=-1):
        """Write over the current entry or the entry at position
        'count' if given.  Note that 1 <= count <= len(self._entry_list).
        The dirty flag is set for the file."""

        if not entry.is_valid():
            print('bookfile().set_entry count %d entry:' % count)
            print(entry)
            return False

        if count < 1 or count > len(self._entry_list):
            return False

        self.current_entry_index = count - 1
        self._entry_list[self.current_entry_index] = entry
        self._dirty = True
        return True

    def set_new_entry(self, entry, count=-1):
        """Append an entry to the list or insert before entry 'count'
        if that value is given. Note that 1 <= count <= len(self._entry_list).
        The dirty flag is set for the file.
        """

        if not entry.is_valid():
            return False

        if 1 < count <= len(self._entry_list):
            # count is within the list, insert the entry
            self.current_entry_index = count - 1
            self._entry_list.insert(self.current_entry_index, entry)
        else:
            # count is not within the list, append the entry
            self._entry_list.append(entry)

        self._dirty = True
        return True

    def delete_entry(self, entrynum):
        '''Delete the (entryNum - 1) record in the list, if such exists.
        Return the length of the remaining list.'''
        if 0 < entrynum <= len(self._entry_list):
            self._entry_list.pop(entrynum - 1)
            self._dirty = True

        return len(self._entry_list)

    def make_short_title_list(self):
        '''Create a string of short titles from all entries in the list.
        A short title is "count AJBnum Title" and is used to look quickly
        at the list of titles.'''

        short_title_list = ''
        count = 1
        for _ent in self._entry_list:
            short_title_list = short_title_list + str(count) + ' ' + _ent.short_title()
            count += 1

        return short_title_list

    # file I/O
    def read_file(self, filename=None):
        '''Select a reader function depending on the filename
        extension.  Return the number of entries read.'''
        if filename:
            self.set_filename(filename)

        if self._filename == '' or not os.path.isfile(self._filename):
            return 0  # no records read

        if self._extension == '.txt':
            return self.read_file_text()

        if self._extension == '.xml':
            return self.read_file_xml()

        # return error to caller who should know about Qt message boxes.
        #print('Invalid file extension for %s' % self._filename)
        return 0

    def write_file(self, filename=None):
        '''Select a writer function depending on the filename
        extension. If filename is not given, we use aabooks._fileName
        instead.

        Returns True if the file could be written or False otherwise.'''
        if filename:
            self.set_filename(filename)

        if self._extension == '.txt':
            return self.write_file_text()

        if self._extension == '.xml':
            return self.write_file_xml()

        # return error to caller who should know about Qt message boxes.
        #print('Invalid file extension for %s' % self._filename)
        return 0

    # Specific file type I/O

    def read_file_text(self):
        """Open and read a .txt file and put the header stuff into
        _header and the entries into the entry list. The header is
        defined as everything before the first valid entry. If
        filename is not given, we use the value set in
        BookFile.set_filename() if valid. Note that we do not care if
        the entries or header have been modified; that is the job of
        the calling routine.

        Return value is the number of record entries read."""

        # if we have a good file, then clear the entryList and header
        self._entry_list = []
        self._header = ''
        self._dirty = False

        enttemp = ajbentry.AJBentry()
        count = 0

        for line in fileinput.input([self._filename]):
            line = line.strip()
            try:
                if not enttemp.read_text_to_entry(line) and not count:
                    self._header = self._header + line + '\n'
            except:
                print(line + '\n')
                traceback.print_exc()
                print('\n\n')

            if enttemp.is_valid():
                count += 1
                self._entry_list.append(enttemp)
                enttemp = ajbentry.AJBentry()

        self.current_entry_index = 1

        return count

    def write_file_text(self):
        """Write the entry list and header to a .txt disk file.
        if filename is not given, we use Aabooks._fileName instead.

        Returns True if the file could be written or False otherwise."""

        try:
            file_fd = open(self._filename, 'w', encoding='UTF8')
        except:
            return False

        if file_fd.newlines:
            newline = file_fd.newlines + file_fd.newline
        else:
            newline = '\n\n'

        file_fd.write(self._header)
        count = 1
        for ent in self._entry_list:
            file_fd.write(str(count) + ' ' + ent.write_text_from_entry() + newline)
            count += 1

        file_fd.close()
        self._dirty = False

        return True

    def read_file_xml(self):
        """Open and read the header stuff into _header and the entries
        into the entry list. If filename is not given, we use
        the value set in BookFile.set_filename() if valid. Note that we
        do not care if the entries or header have been modified; that is
        the job of the calling routine.

        Return value is the number of record entries read."""

        if self._filename == '' or not os.path.isfile(self._filename):
            return 0  # no records read

        # if we have a good file, then clear the entryList and header
        self._entry_list = []
        self._header = ''
        self._dirty = False

        count = 0

        # read the XML file
        try:
            bf_xml = etree.parse(self._filename)
        except etree.XMLSyntaxError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      limit=2, file=sys.stdout)
            print('The xml file is not well formed or is invalid')
            return 0

        bfchildren = bf_xml.getroot()
        for child in bfchildren:
            if child.tag == 'Header':
                self.set_header(child.text)

            if child.tag == 'Entries':
                for entry in child:
                    enttemp = ajbentry.AJBentry()
                    enttemp.read_xml_to_entry(entry)
                    if enttemp.is_valid():
                        count += 1
                        self._entry_list.append(enttemp)
                        enttemp = ajbentry.AJBentry()

        self._dirty = False

        return count

    def write_file_xml(self, filename=None):
        """Write the entry list and header to a .xml disk file.
        if filename is not given, we use aabooks._fileName instead.

        Returns True if the file could be written or False otherwise."""

        try:
            if filename is not None:
                file_fd = open(filename, 'w', encoding='UTF8')
                # only set _filename if we are successful in opening
                self._filename = filename
            else:
                file_fd = open(self._filename, 'w', encoding='UTF8')
        except (FileNotFoundError, PermissionError):
            # really should print the exception here
            return False

        # We do something clever here when we know how.
        elbf = etree.Element('BookFile')
        hdr = etree.SubElement(elbf, 'Header')
        hdr.text = self.get_header()

        ets = etree.SubElement(elbf, 'Entries')
        for entry in self._entry_list:
            # entry is of Class AJBentry
            ets.append(entry.write_xml_from_entry())

        bstr = etree.tostring(elbf,
                              xml_declaration=True,
                              method='xml', encoding='UTF-8')
        strstr = bstr.decode(encoding='UTF-8')
        file_fd.write(strstr)

        file_fd.close()
        self._dirty = False

        return True


if __name__ == "__main__":

    BF = BookFile()
    print("%d entries found\n" % BF.read_file(
        "../../../../Data/Ajb/Old/ajb58_books.txt"))

    print('The header for %s' % BF.get_filename())
    print(BF.get_header())

    BF.write_file("testfile.txt")

    BF.read_file('testfile.txt')
    BF.write_file('testfile2.txt')
    print(' run "diff testfile2.txt testfile.txt"')

    ENT = ajbentry.AJBentry('500 58.04.05 , An Amazing Book')
    ENT2 = ajbentry.AJBentry('500 58.04.06 , An Amazing Book Too')
    BF.set_new_entry(ENT)  # append
    BF.set_new_entry(ENT2, 0)  # append
    BF.set_new_entry(ENT, 1)  # insert as ENTry 1
    BF.set_new_entry(ENT2, 5)  # insert as ENTry 5
    BF.set_entry(ENT, 4)  # replace ENTry 4
    BF.write_file('testfile3.txt')
    BF.set_new_entry(ENT, 5)
    BF.delete_entry(22)
    BF.delete_entry(0)
    BF.delete_entry(5)
    print('testfile3.txt should have new entry 1 and 5 and replaced entry 4')
    print('\n\n')
    BF.write_file_xml('ajb58_books.xml')
    print('We can also read and validate an XML file with the parse() function')
    try:
        BF_SCHEMA = etree.XMLSchema(file='../../../xml/bookfile.xsd')
        PARSER = etree.XMLParser(schema=BF_SCHEMA)
        print('The schema is well formed')
    except etree.XMLSchemaParseError:
        print('The schema is not well formed')
        sys.exit(1)
    try:
        # etree.parse() returns an Etree rather than an Element
        BF3 = etree.parse('ajb58_books.xml', parser=PARSER)
        print('The xml file is well formed and valid')
    except etree.XMLSyntaxError:
        print('The xml file is not well formed or is invalid')
