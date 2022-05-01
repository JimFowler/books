## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/journal/journalentry.py
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

'''journalEntry provides a class which can convert between a an XML
entry and a representation in python, typically a dictionary entry of
the form Entry.entry().'''

from aabooks.journal import entryxml

__version__ = 'class JournalEntry(Entry) v1.0.0 dtd 3 Jan 2015'

class JournalEntry(dict):

    """Read the information from an XML string and put the data in the
    journalEntry dictionary. The entry is valid if there is a valid
    title.

    The JournalEntry XML definition can be found in journalfile.xsd
    """

    def __init__(self, _entry_str=None):

        super().__init__()

        self.blank_entry()


    def blank_entry(self):
        """Initialize a blank entry by setting known fields to
        null values and deleting all other fields.
        """
        keys = list(self.keys())
        for k in keys:
            del self[k]

        self['Title'] = ''
        self['subTitle'] = ''
        self['subsubTitle'] = ''
        self['Publishers'] = []
        #
        #Publishers is list of dictionaries of the form
        #   {'Name'      : '', # required, all others optional
        #    'Place'     : '',
        #    'startDate' : '',
        #    'endDate'   : ''
        #   }
        #
        self['Abbreviations'] = [] # a list of strings
        self['startDate'] = '' # the start of publishing
        self['endDate'] = '' # the end of publishing
        self['linknext'] = [] # a list of strings'
        self['linkprevious'] = [] # a list of strings
        self['Designators'] = {}
        #
        # Designators is a dictionary of catalogue designations
        #   for example 'ISSN' : '9-123456-789-12-3'
        #     and       "ADS_Bibcode' : '....ApJ...'
        #    others can be
        #               'LCCN', 'DDCN', etc
        #
        self['Comments'] = [] # should be a list of strings

    def is_valid(self):
        """journal entries are valid if they have a valid Title."""
        return self['Title'] != ''

    def not_empty(self, key):
        """Return the truth value of, 'key' existing
        in the entry and the key value is not empty."""
        if self.__contains__(key) and self[key]:
            return True
        return False

    #
    # XML create routines
    #
    def write_xml_from_entry(self):
        '''Write an XML etree element from the entry'''

        return entryxml.entry_to_xml(self)

    def read_xml_to_entry(self, element):
        '''Fill an entry from an etree XML element.'''

        entryxml.entry_from_xml(self, element)

#
# Test everything
#
if __name__ == '__main__':

    from aabooks.journal import testentry
    import unittest
    from lxml import etree

    class JournalEntryTestCase(unittest.TestCase):
        '''Test the JournalEntry methods.'''

        def setUp(self):
            '''Initialize local stuff. We start with a fresh Entry object for each
            test. '''

            self.test_entry = JournalEntry()
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


    unittest.main()
