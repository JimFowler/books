## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/journal/tests/tests_journalentry.py
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
'''Provide the unit tests for aabooks/journal/journalentry.py'''
import unittest
from lxml import etree

from aabooks.journal.tests import testentry
from aabooks.journal import journalentry as je

class JournalEntryTestCase(unittest.TestCase):
    '''Test the JournalEntry methods.'''

    def setUp(self):
        '''Initialize local stuff. We start with a fresh Entry object for each
        test. '''

        self.test_entry = je.JournalEntry()
        self.test_str = testentry.ENTRY_XML_STR
        self.ent_xml = etree.fromstring(self.test_str)

    def tearDown(self):
        '''Dispose of the Entry object at the end of every test.'''

        del self.test_str
        del self.test_entry
        del self.ent_xml

    def test_is_valid(self):
        '''Test the is_valid() method on an empty entry'''

        self.assertFalse(self.test_entry.is_valid())

    def test_read_xml(self):
        '''Test that we can read/write the XML string to an JournalEntry'''

        self.test_entry.read_xml_to_entry(self.ent_xml)

        self.assertTrue(self.test_entry.is_valid())

    def test_write_xml(self):
        '''Test that we can write an XML string from a JournalEntry
        and that it matchs the one we started with.'''

        self.test_entry.read_xml_to_entry(self.ent_xml)
        new_str = etree.tostring(self.test_entry.write_xml_from_entry(),
                                 pretty_print=True, encoding='unicode')

        self.assertEqual(len(self.test_str), len(new_str))
        locs = [i for i in range(len(self.test_str)) if self.test_str[i] != new_str[i]]

        # locs should be an empty list
        self.assertFalse(locs, msg='input and output strings differ')
