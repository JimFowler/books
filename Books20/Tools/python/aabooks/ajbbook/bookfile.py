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

from aabooks.lib import entrylist
from aabooks.ajbbook import ajbentry

__VERSION__ = 0.1

__DEFAULTHEADER__ = '''

Save as Unicode UTF-8 text encoding. Skip section 4 in Part 1

For volume AJB ?? Index to the Literature of ????, started, finished, proofread


'''
# end of defaultHeader


class BookFile(entrylist.EntryList):
    """The BookFile class handles the disk file and entry list
    for book lists from AJB/AAA. It handles all the translation
    between the disk file format and the AJBentry format."""

    # pylint: disable=too-many-instance-attributes,too-many-public-methods
    def __init__(self):
        super(BookFile, self).__init__()

        # general meta based defined in entrylist
        self.set_header(__DEFAULTHEADER__)

        # additional metadata
        self.volume_number = -1

    def make_short_title_list(self):
        '''Create a string of short titles from all entries in the list.
        A short title is "count AJBnum Title" and is used to look quickly
        at the list of titles.'''

        short_title_list = ''
        for count, ent in enumerate(self):
            short_title_list = short_title_list + str(count) + \
                ' ' + ent.short_title()

        return short_title_list

    # Specific file type I/O

    def read_file_txt(self):
        """Open and read a .txt file and put the header stuff into
        _header and the entries into the entry list. The header is
        defined as everything before the first valid entry. If
        filename is not given, we use the value set in
        BookFile.set_filename() if valid. Note that we do not care if
        the entries or header have been modified; that is the job of
        the calling routine.

        Return value is the number of record entries read."""

        self.clear_list()

        count = 0

        for line in fileinput.input([self.filename]):
            line = line.strip()
            enttemp = ajbentry.AJBentry()

            enttemp.read_text_to_entry(line)
            if not enttemp.is_valid() and not count:
                self.set_header(self.get_header() + line + '\n')

            if enttemp.is_valid():
                count += 1
                self.set_new_entry(enttemp)

            del enttemp

        return count

    def write_file_txt(self):
        """Write the entry list and header to a .txt disk file.
        if filename is not given, we use Aabooks._fileName instead.

        Returns True if the file could be written or False otherwise."""

        file_fd = open(self.filename, 'w', encoding='UTF8')

        if file_fd.newlines:
            newline = file_fd.newlines + file_fd.newline
        else:
            newline = '\n\n'

        file_fd.write(self.get_header())
        for count, ent in enumerate(self):
            file_fd.write(str(count) + ' ' + ent.write_text_from_entry() \
                          + newline)

        file_fd.close()
        self._dirty = False

        return True

    #
    # XML read/write
    #
    def read_file_xml(self):
        """Open and read the header stuff into _header and the entries
        into the entry list. If filename is not given, we use
        the value set in BookFile.set_filename() if valid. Note that we
        do not care if the entries or header have been modified; that is
        the job of the calling routine.

        Return value is the number of record entries read."""

        if self.filename == '' or not os.path.isfile(self.filename):
            return 0  # no records read

        # if we have a good file, then clear the entryList and header
        self.clear_list()

        # read the XML file
        count = 0
        try:
            bf_xml = etree.parse(self.filename)
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
                        self.set_new_entry(enttemp)

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
                self.filename = filename
            else:
                file_fd = open(self.filename, 'w', encoding='UTF8')
        except (FileNotFoundError, PermissionError):
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      limit=2, file=sys.stdout)
            return False

        # We do something clever here when we know how.
        elbf = etree.Element('BookFile')
        hdr = etree.SubElement(elbf, 'Header')
        hdr.text = self.get_header()

        ets = etree.SubElement(elbf, 'Entries')
        for count, entry in enumerate(self):
            # entry is of Class AJBentry
            ets.append(entry.write_xml_from_entry())

        bstr = etree.tostring(elbf,
                              xml_declaration=True,
                              method='xml', encoding='UTF-8')
        strstr = bstr.decode(encoding='UTF-8')
        file_fd.write(strstr)

        file_fd.close()
        self._dirty = False

        return not self.is_dirty()


if __name__ == "__main__":

    import unittest

    class BookFileTestCase(unittest.TestCase):
        '''Tests for the class BookFile.'''

        def setUp(self):
            '''Start every test afresh with a new BookFile.'''
            self.bookfile = BookFile()

        def tearDown(self):
            '''Clean up the mess after every test.'''

            del self.bookfile

        def test_a_read_file_xml(self):
            '''Test the BookFile.read_file_xml() method.'''

            self.assertEqual(self.bookfile.read_file("testfile.xml"), 400)

        def test_b_write_file_xml(self):
            '''Test the BookFile.write_file_xml() method.'''

            self.assertEqual(self.bookfile.read_file("testfile.xml"), 400)
            self.assertTrue(self.bookfile.write_file('testfile_tmp.xml'))

        def test_c_short_title_list(self):
            '''Test the Bookfile.make_short_title_list() method.'''

            self.assertEqual(self.bookfile.read_file("testfile.xml"), 400)
            shorttitle = self.bookfile.make_short_title_list()
            self.assertEqual(len(shorttitle), 19740)

        def test_d_read_file_text(self):
            '''Test the BookFile.read_file_text() method.'''

            self.assertEqual(self.bookfile.read_file("testfile.txt"), 11)

        def test_d_write_file_text(self):
            '''Test the BookFile.write_file_text() method.'''

            self.assertEqual(self.bookfile.read_file("testfile.txt"), 11)
            self.assertTrue(self.bookfile.write_file('testfile_tmp.txt'))

        def test_f_check_schema(self):
            '''Check the schema that defines a book file and check the file
            that we wrote when we tested write_file_xml().'''
            try:
                bf_schema = etree.XMLSchema(file='../../../xml/bookfile.xsd')
                parser = etree.XMLParser(schema=bf_schema)
                schema_good = True
            except etree.XMLSchemaParseError:
                schema_good = False
            self.assertTrue(schema_good, msg='the schema is not well formed')

            try:
                # etree.parse() returns an Etree rather than an Element
                etree.parse('testfile_tmp.xml',
                            parser=parser)
                xml_file_good = True
            except etree.XMLSyntaxError:
                xml_file_good = False
            self.assertTrue(xml_file_good,
                            msg='The xml file is not well formed or is invalid')

    unittest.main()
