## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/journal/tests/test_journalfile.py
##
##   Part of the Books20 Project
##
##   Copyright 2024 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrival system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright
'''Provide the unit tests for aabooks/journal/journalfile.py'''

import unittest
from lxml import etree

from aabooks.journal import journalfile as jf


class JournalFileTestCase(unittest.TestCase):
    '''The unit tests for the class JournalFile.'''

    def setUp(self):
        '''Create a new JournalFile for each test.'''

        self.jfile = jf.JournalFile()
        self.test_xml = './aabooks/journal/tests/testjournals.xml'

    def tearDown(self):
        '''Clean up our mess from the last test.'''

        del self.jfile

    def test_a_read_file_xml(self):
        '''Test the JournalFile.read_file_xml() method.'''

        count = self.jfile.read_file(self.test_xml)
        jfile2 = jf.JournalFile(self.test_xml)
        self.assertEqual(count, 235)
        self.assertEqual(self.jfile, jfile2)
        del jfile2

    def test_b_write_file_xml(self):
        '''Test the JournalFile.write_file_xml() method.'''

        count = self.jfile.read_file(self.test_xml)
        self.assertEqual(count, 235)
        self.assertTrue(self.jfile.write_file('testjournals_tmp.xml'))

    def test_c_make_short_title_list(self):
        '''Test the JournalFile.make_short_title_list() method.'''

        count = self.jfile.read_file(self.test_xml)
        self.assertEqual(count, 235)

        shorttitle = self.jfile.make_short_title_list()
        self.assertEqual(len(shorttitle), 8535)

    def test_d_check_schema(self):
        '''Test the written XML file against the XSD schema.'''

        test_parser = None

        count = self.jfile.read_file(self.test_xml)
        self.assertEqual(count, 235)
        self.assertTrue(self.jfile.write_file('testjournals_tmp.xml'))

        try:
            # Need a better way to find this schema file
            test_schema = etree.XMLSchema(file='../../../../xml/journalfile.xsd')
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

        self.jfile.read_file(self.test_xml)

        answer_file = jf.JournalFile()
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
        self.jfile.read_file(self.test_xml)

        answer_file = jf.JournalFile()
        for dummy in range(0, 2):
            for ent in self.jfile:
                answer_file.append(ent)
        answer_file.set_header(self.jfile.get_header() + '\n' + self.jfile.get_header())

        self.jfile.extend(self.jfile)

        self.assertEqual(self.jfile, answer_file)
        self.assertEqual(self.jfile.get_header(),
                         answer_file.get_header())

        del answer_file
