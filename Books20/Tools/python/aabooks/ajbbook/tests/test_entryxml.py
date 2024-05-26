#! /usr/bin/env python3
##
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/ajbbook/tests/test_entryxml.py
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
'''Provide the unit tests for aabooks/ajbbook'''
import unittest
from lxml import etree

from aabooks.ajbbook import ajbentry
from aabooks.ajbbook.tests import testentryxml as testentry

class EntryTestCase(unittest.TestCase):
    '''Set up the unit tests'''

    def setUp(self):
        '''Initialize local stuff. We start with a fresh Entry object
        for every test.'''

        self.test_str = testentry.ENTRY_XML_STR
        self.test_entry = ajbentry.AJBentry()
        self.ent_xml = etree.fromstring(self.test_str)

    def tearDown(self):
        '''Dispose of the Entry object at the end of every test.'''

        del self.test_str
        del self.test_entry
        del self.ent_xml

    def test_read_write(self):
        '''Test that we can read/write the XML string to an AJBentry'''

        self.test_entry.read_xml_to_entry(self.ent_xml)
        new_str = etree.tostring(self.test_entry.write_xml_from_entry(),
                                 pretty_print=True, encoding='unicode')

        self.assertEqual(len(self.test_str), len(new_str))
        locs = [i for i in range(len(self.test_str)) if self.test_str[i] != new_str[i]]

        # locs should be an empty list
        self.assertFalse(locs, msg='input and output strings differ')
