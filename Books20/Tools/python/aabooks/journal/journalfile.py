## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/journal/journalfile.py
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

'''Defines the class that handles disk files and entry lists'''

import os
from lxml import etree

from aabooks.lib import entrylist
from aabooks.journal import journalentry

__version__ = 0.1

__defaultHeader__ = '''
Default header for journal file
'''
# end of defaultHeader


class JournalFile(entrylist.EntryList):
    """The BookFile class handles the disk file and entry list
    for book lists from AJB/AAA. It handles all the translation
    between the disk file format and the AJBentry format."""

    def __init__(self, filename=None):
        '''Initialize with the parent class, then add any
        special metadata fro journals.

        '''

        super().__init__()

        if filename:
            self.read_file(filename)
            self.current_entry_number = 1
        else:
            self.set_header(__defaultHeader__)
            self.file_name = './document1'
            # 1 <= current_entry_number <= len(self._entry_list)
            self.current_entry_number = -1

        self._dirty = False

    def make_short_title_list(self):
        '''Create a string of short titles from all entries in the list.
        A short title is "count AJBnum Title" and is used to look quickly
        at the list of titles.'''

        short_title_list = ''
        for count, entry in enumerate(self):
            short_title_list = short_title_list + str(count+1) + \
                ' ' + entry['Title'][:50] + '\n'

        return short_title_list

    # file I/O
    def read_file_xml(self, filename=None):
        """Open and read the header stuff into _header and the entries
        into the entry list. If filename is not given, we use
        the value set in BookFile.set_file_name() if valid. Note that we
        do not care if the entries or header have been modified; that is
        the job of the calling routine.

        Return value is the number of record entries read."""

        if filename:
            self.filename = filename

        if self.filename == '' or not os.path.isfile(self.filename):
            return 0 # no records read

        # if we have a good file, then clear the entryList and header
        self.clear_list()

        count = 0

        # read the XML file
        jf_xml = etree.parse(self.filename)

        root_node = jf_xml.getroot()
        for child in root_node:
            if child.tag == 'Header':
                self.set_header(child.text)

            if child.tag == 'Journals':
                for entry in child:
                    temp_entry = journalentry.JournalEntry()
                    temp_entry.read_xml_to_entry(entry)
                    if temp_entry.is_valid():
                        count += 1
                        self.set_new_entry(temp_entry)

        self._dirty = False
        return count


    def write_file_xml(self, filename=None):
        """Write the entry list and header to a disk file.
        if filename is not given, we use aabooks._file_name instead.

        Returns True if the file could be written or False otherwise."""

        if filename:
            self.filename = filename
        #pylint: disable = consider-using-with
        try:
            file_descriptor = open(self.filename, 'w', encoding='UTF8')
        except (FileNotFoundError, PermissionError):
            return False
        #pylint: enable = consider-using-with

        # We do something clever here when we know how.
        jf_root = etree.Element('JournalFile')
        header = etree.SubElement(jf_root, 'Header')
        header.text = self.get_header()

        journals = etree.SubElement(jf_root, 'Journals')
        for entry in self:
            entry_xml = entry.write_xml_from_entry()
            journals.append(entry_xml)

        jf_string = etree.tostring(jf_root,
                                   xml_declaration=True,
                                   method='xml', encoding='UTF-8')
        strstr = jf_string.decode(encoding='UTF-8')
        file_descriptor.write(strstr)

        file_descriptor.close()
        self._dirty = False

        return True

    def __add__(self, journalf):
        '''Reimplement the __add__() or '+' function so that we can combine
        two JournalFile objects to create a third.        

        '''

        new_journalfile = JournalFile()
        new_journalfile.set_header(self.get_header() + '\n' + \
                                  journalf.get_header())
        list.extend(new_journalfile, self)
        list.extend(new_journalfile, journalf)

        return new_journalfile

    def extend(self, journalf):
        '''Reimplement the extend() function from list.'''

        self.set_header(self.get_header() + '\n' + journalf.get_header())
        list.extend(self, journalf)
        
if __name__ == "__main__":

    import unittest

    class JournalFileTestCase(unittest.TestCase):
        '''The unit tests for the class JournalFile.'''

        def setUp(self):
            '''Create a new JournalFile for each test.'''

            self.jfile = JournalFile()

        def tearDown(self):
            '''Clean up our mess from the last test.'''

            del self.jfile

        def test_a_read_file_xml(self):
            '''Test the JournalFile.read_file_xml() method.'''

            count = self.jfile.read_file('testjournals.xml')
            jfile2 = JournalFile('testjournals.xml')
            self.assertEqual(count, 235)
            self.assertEqual(self.jfile, jfile2)
            del jfile2

        def test_b_write_file_xml(self):
            '''Test the JournalFile.write_file_xml() method.'''

            count = self.jfile.read_file('testjournals.xml')
            self.assertEqual(count, 235)
            self.assertTrue(self.jfile.write_file('testjournals_tmp.xml'))

        def test_c_make_short_title_list(self):
            '''Test the JournalFile.make_short_title_list() method.'''

            count = self.jfile.read_file('testjournals.xml')
            self.assertEqual(count, 235)

            shorttitle = self.jfile.make_short_title_list()
            self.assertEqual(len(shorttitle), 8535)

        def test_d_check_schema(self):
            '''Test the written XML file against the XSD schema.'''

            test_parser = None

            count = self.jfile.read_file('testjournals.xml')
            self.assertEqual(count, 235)
            self.assertTrue(self.jfile.write_file('testjournals_tmp.xml'))

            try:
                test_schema = etree.XMLSchema(file='../../../xml/journalfile.xsd')
                test_parser = etree.XMLParser(schema=test_schema)
                schema_good = True
            except etree.XMLSchemaParseError:
                schema_good = False

                self.assertTrue(schema_good,
                                msg='the schema is not well formed')

                try:
                    # etree.parse() returns an Etree rather than an Element
                    etree.parse('./testjournals_tmp.xml', parser=test_parser)
                    xml_file_good = True
                except etree.XMLSyntaxError:
                    xml_file_good = False

                self.assertTrue(xml_file_good,
                                msg='The xml file is not well formed or is invalid')

        def test_e_add_journalfiles(self):
            '''Test the __add__() or '+' function in order to see
            what is happening. Not much of a test as it simply duplicates
            our first implementation of __add__().

            '''

            self.jfile.read_file("testjournals.xml")

            answer_file = JournalFile()
            for dummy in range(0, 2):
                for ent in self.jfile:
                    answer_file.append(ent)
            answer_file.set_header(self.jfile.get_header() + '\n' + \
                                 self.jfile.get_header())
            test_file = self.jfile + self.jfile
            self.assertEqual(test_file, answer_file)
            self.assertEqual(test_file.get_header(),
                             answer_file.get_header())

            del test_file
            del answer_file

        def test_f_extend_list(self):
            '''Test the __extend__() function in order to see
            what is happening. 

            '''
            self.jfile.read_file("testjournals.xml")

            answer_file = JournalFile()
            for dummy in range(0, 2):
                for ent in self.jfile:
                    answer_file.append(ent)
            answer_file.set_header(self.jfile.get_header() + '\n' + self.jfile.get_header())

            self.jfile.extend(self.jfile)

            self.assertEqual(self.jfile, answer_file)
            self.assertEqual(self.jfile.get_header(),
                             answer_file.get_header())

            del answer_file
                
    unittest.main()
