#! /usr/bin/env python3
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/ajbbook/tests/test_bookfile.py
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
'''Provide the unittests for booksfile.py'''
import unittest
from lxml import etree
from aabooks.ajbbook import bookfile as bf
from aabooks.ajbbook import __sort_dict__

class BookFileFunctionTestCase(unittest.TestCase):
    '''Tests for the class BookFile.'''

    def setUp(self):
        '''Start every test afresh with a new BookFile.'''
        self.bookfile = bf.BookFile()

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
        self.assertEqual(len(shorttitle), 19742)

    def test_d_check_schema(self):
        '''Check the schema that defines a book file and check the file
        that we wrote when we tested write_file_xml().'''
        bf_schema = etree.XMLSchema(file='../../../../xml/bookfile.xsd')
        try:
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

    def test_e_add_bookfiles(self):
        '''Test the __add__() or '+' function in order to see
        what is happening. Not much of a test as it simply duplicates
        our first implementation of __add__().

        '''

        self.bookfile.read_file("testfile.xml")

        answer_file = bf.BookFile()
        for dummy in range(0, 2):
            for ent in self.bookfile:
                answer_file.append(ent)
        answer_file.set_header(self.bookfile.get_header() + '\n' + \
                             self.bookfile.get_header())
        test_file = self.bookfile + self.bookfile
        self.assertEqual(test_file, answer_file)
        self.assertEqual(test_file.get_header(),
                         answer_file.get_header())

        del test_file
        del answer_file

    def test_f_extend_list(self):
        '''Test the __extend__() function in order to see
        what is happening. Not much of a test as it simply duplicates
        the first implementation of __add__().

        '''
        self.bookfile.read_file("testfile.xml")

        answer_file =bf. BookFile()
        for dummy in range(0, 2):
            for ent in self.bookfile:
                answer_file.append(ent)
        answer_file.set_header(self.bookfile.get_header() + '\n' + \
                             self.bookfile.get_header())

        self.bookfile.extend(self.bookfile)

        self.assertEqual(self.bookfile, answer_file)
        self.assertEqual(self.bookfile.get_header(),
                         answer_file.get_header())

        del answer_file

class BookFileSortTestCase(unittest.TestCase):
    '''Tests for the class BookFile.'''

    def setUp(self):
        '''Start every test afresh with a new BookFile.'''
        self.bookfile = bf.BookFile()
        self.bookfile.read_file("testfile.xml")

    def tearDown(self):
        '''Clean up the mess after every test.'''

        del self.bookfile

    def is_sorted(self, key):
        '''Test if the bookfile is sorted by the given key. '''

        lower_key = __sort_dict__[key]
        first = ''
        for e in self.bookfile:
            if 'num' in lower_key:
                second = e.sort_num_str()
            elif 'author' in lower_key:
                if e['Authors']:
                    second = e['Authors'][0].last.lower()
                elif e['Editors']:
                    second = e['Editors'][0].last.lower()
                else:
                    second = ''
            else:
                second = e[key]
            if second < first:
                #print(f'author: {first = }  {second = }')
                return False
            first = second
        return True

    def test_a_sort_by_year(self):
        '''Test the sort_by routine with Year in ajbentry.py.

        '''

        self.assertFalse(self.is_sorted('Year'))
        self.bookfile.sort_by('Year')
        self.assertTrue(self.is_sorted('Year'))

    def test_b_sort_by_ajbnum(self):
        '''Test the sort_by routine by AJB num in ajbentry.py.

        '''

        self.bookfile.sort_by('AJB/AAA Num')
        self.assertTrue(self.is_sorted('AJB/AAA Num'))

    def test_c_sort_by_author(self):
        ''' Test the sort_by routine by Author in ajbentry.py

        '''

        self.assertFalse(self.is_sorted('Author/Editor'))
        self.bookfile.sort_by('Author/Editor')
        self.assertTrue(self.is_sorted('Author/Editor'))
