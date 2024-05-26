#! /usr/bin/env python
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/lib/tests/test_entrylist.py
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
'''Provides the unittests for aabooks/lib/entrylist.py'''
import os
import unittest
from pathlib import Path
from aabooks.lib import entrylist as el


class MyEntry(dict):
    '''A simple entry class for testing.
    The entry consists of a single entry
    'value' : <string>
    since Entry is a sub-class of dictionary

    '''

    def __init__(self, string=None):
        '''The event initializer.'''
        super().__init__()
        self.set_value(string)

    def is_valid(self):
        '''Report if the entry is good.'''
        return isinstance(self['value'], str)

    def blank_entry(self):
        '''Create a new Entry.'''

    def set_value(self, string):
        '''Set the entry.'''
        self['value'] = string


class EntryListTestCase(unittest.TestCase):
    '''Set up the unit tests'''
    def setUp(self):
        '''Start with a fresh EntryList and Entry's for
        each test.'''

        self.ent_list = el.EntryList()
        self.entry1 = MyEntry('The quick brown fox')
        self.entry2 = MyEntry('jumped over the')
        self.entry3 = MyEntry('lazy dogs back')
        self.entry4 = MyEntry() # invalid entry

        self.header = '''This is the new header.

It contains three lines.'''
    def tearDown(self):
        '''Delete the class variables at the end of each '''

        del self.ent_list
        del self.entry1
        del self.entry2
        del self.entry3
        del self.entry4
        del self.header

    def test_a_initialize(self):
        '''Test that the EntryList is initialized correctly.

        Test
          header is None
          filename
          dirty_flag

        '''

        self.assertEqual(self.ent_list.get_header(), '')
        self.assertEqual(self.ent_list.filename, './document1.xml')
        self.assertFalse(self.ent_list.is_dirty())

    def test_b_header(self):
        '''Test header manipulation.

        test
          set_header and verify dirty flag
          get_header
          invalid header
        '''

        self.assertTrue(self.ent_list.set_header(self.header))
        self.assertEqual(self.ent_list.get_header(), self.header)
        self.assertTrue(self.ent_list.is_dirty())

        # should not be able to write a non-string to the header
        self.ent_list = el.EntryList()
        self.assertFalse(self.ent_list.set_header(5))
        self.assertFalse(self.ent_list.is_dirty())

    def test_c_set_new_entry(self):
        '''Test entry manipulation.

        '''

        # test set_new_entry with
        #  valid entry
        #  second valid entry
        #  insert an entry
        #  invalid entry

        # verify that self.ent_list is clean initially
        self.assertFalse(self.ent_list.is_dirty())

        # test set_new_entry with valid entry and check dirty flag set 1
        self.assertTrue(self.ent_list.set_new_entry(self.entry1))
        self.assertEqual(self.ent_list.get_entry(0), self.entry1)
        self.assertTrue(self.ent_list.is_dirty())

        # test set_new_entry with second valid entry 12
        self.assertTrue(self.ent_list.set_new_entry(self.entry2))
        self.assertEqual(self.ent_list.get_entry(1), self.entry2)

        # test set_new_entry insertion of entry 312
        self.assertTrue(self.ent_list.set_new_entry(self.entry3, 0))
        self.assertEqual(self.ent_list.get_entry(0), self.entry3)

        # test set_new_entry insertion of entry with invalid count 3121
        self.assertTrue(self.ent_list.set_new_entry(self.entry1, 3))
        self.assertEqual(self.ent_list.get_entry(3), self.entry1)

        # test set_new_entry with invalid entry
        self.assertFalse(self.ent_list.set_new_entry(self.entry4))

    def test_d_get_entry(self):
        '''Test the EntryList.get_entry() function.'''

        # set up the list first 123
        self.assertTrue(self.ent_list.set_new_entry(self.entry1))
        self.assertTrue(self.ent_list.set_new_entry(self.entry2))
        self.assertTrue(self.ent_list.set_new_entry(self.entry3))

        # test get_entry with counts inside and outside of invalid values
        self.assertIsNone(self.ent_list.get_entry(-1))
        self.assertIsNone(self.ent_list.get_entry(self.ent_list.max_entries()))
        self.assertEqual(self.ent_list.get_entry(0), self.entry1)
        self.assertEqual(self.ent_list.get_entry(self.ent_list.max_entries() - 1), self.entry3)

    def test_d_set_entry(self):
        '''Test the EntryList.set_entry() function'''

        # set up the list first 1233
        self.assertTrue(self.ent_list.set_new_entry(self.entry1))
        self.assertTrue(self.ent_list.set_new_entry(self.entry2))
        self.assertTrue(self.ent_list.set_new_entry(self.entry3))
        self.assertTrue(self.ent_list.set_new_entry(self.entry3))

        # test set_entry with replacement of entry just inside valid counts 2233
        self.assertTrue(self.ent_list.set_entry(self.entry2, 0))
        self.assertEqual(self.ent_list.get_entry(0), self.entry2)
        self.assertTrue(self.ent_list.set_entry(self.entry1,
                                self.ent_list.max_entries()-1)) # 2221

        self.assertEqual(self.ent_list.get_entry(self.ent_list.max_entries()-1), self.entry1)

        # test set_entry with invalid entry
        self.assertFalse(self.ent_list.set_entry(self.entry4, 2))
        self.assertEqual(self.ent_list.get_entry(3), self.entry1)

        # test set_entry with invalid count
        self.assertFalse(self.ent_list.set_entry(self.entry2, -1))
        self.assertFalse(self.ent_list.set_entry(self.entry2, self.ent_list.max_entries()))

        # test delete_entry 221
        self.assertEqual(self.ent_list.max_entries(), 4)
        self.assertEqual(self.ent_list.delete_entry(1), 3)

        # test delete_entry with invalid count 123
        self.assertEqual(self.ent_list.delete_entry(-1), 3)
        self.assertEqual(self.ent_list.delete_entry(self.ent_list.max_entries()+1), 3)

    def test_f_clear_list(self):
        '''Test the EntryList.clear_list() function.'''

        # set up the list first 1231
        self.assertTrue(self.ent_list.set_new_entry(self.entry1))
        self.assertTrue(self.ent_list.set_new_entry(self.entry2))
        self.assertTrue(self.ent_list.set_new_entry(self.entry3))
        self.assertTrue(self.ent_list.set_new_entry(self.entry1))

        self.assertEqual(self.ent_list.clear_list(), 0)
        # should have no entries in the list
        self.assertEqual(len(self.ent_list), 0)

    def test_g_read_file(self):
        '''Test the read_file stub. Should not be able to read a file at
        this time because we don't have a read_file_xml() method yet. We
        touch the filename first to insure that we don't have a file
        not exists error.

        '''

        filename = 'bogon.xml'
        # test read_file with bogus file name
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass

        self.assertEqual(self.ent_list.read_file(filename), 0)

        # test read_file with real (but empty) filename
        Path('bogon.xml').touch()
        with self.assertRaises(AttributeError):
            self.ent_list.read_file('bogon.xml')

        # test that filename was updated
        self.assertEqual(self.ent_list.filename, 'bogon.xml')
        try:
            os.remove('bogon.xml')
        except FileNotFoundError:
            pass

    def test_h_write_file(self):
        '''test the write_file stub. Should not be able to write a file at
        this time.

        '''

        filename = 'bogon.xml'

        with self.assertRaises(AttributeError):
            self.ent_list.write_file(filename)

        self.assertEqual(self.ent_list.filename, filename)
        del filename
