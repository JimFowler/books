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

        self['Index'] = -1
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

    def sort_key(self, key):
        """Return a value that list.sort() can use to sort the JournalFile list.
        'key' must a a string value of one of dict keys in the entry. For
        the keys we do not yet now how to sort we do something???

        """

        sortkey = None

        lower_key = key.lower()
        sortkey = ''
        
        if 'year' in lower_key and self['startDate']:
            sortkey = self['startDate']

        if 'title' in lower_key:
            sortkey = self['Title']

        if 'place' in lower_key and self['Publishers'] \
           and 'Place' in self['Publishers'][0]:
            sortkey = self['Publishers'][0]['Place']

        if 'publisher' in lower_key and self['Publishers'] \
           and 'Name' in self['Publishers'][0]:
            sortkey = self['Publishers'][0]['PublisherName']

        if 'orig' in lower_key:
            sortkey = self['Index']

        return sortkey

    def is_valid(self):
        """journal entries are valid if they have a valid Title."""
        return self['Title'] != ''

    def not_empty(self, key):
        """Return the truth value of, 'key' existing
        in the entry and the key value is not empty."""
        if key in self and self[key]:
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
