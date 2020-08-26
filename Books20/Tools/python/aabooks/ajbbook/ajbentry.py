#
# -*- mode: Python;-*-
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/ajbbook/AJBentry.py
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
"""AJBentry provides a class which can convert between a unicode text
entry and a representation in python, typically a dictionary entry of
the form Entry.py.entry()."""

from aabooks.lib import entry
from aabooks.ajbbook import entryxml
from aabooks.ajbbook import entrytext


class AJBentry(entry.Entry):

    """Read the information from a string and put the data in the
    AJBentry dictionary. The entry is valid if there was a valid AJB
    number (vol.section.index) and a title.

    A line looks like:

    Index AJB_Num Author, Title, Place, Publisher, Year, \
    Pagination, Price, Reviews, Comments]

    No field need be present except Index, AJB_Num, and Title.

    Field 1 Index AJB_Num Author has format

    Index AJB_Num [I. A. Author [jr.|III|...] [ and H. E. Another [and ...]]] \
       [ed.|comp.|something else]

    Field 2 Title

    Field 3 Place

       [name | name-name[-name[-...]] Name may contain spaces

    Field 4 Publisher

    Field 5 Year

    Field 6 Pagination

    Field 7 Price

       [n+nnn [and nn+nnn [and ...] pp]]

    Field 8 Reviews

       [Journal vol page [and Journal vol page [and ...]]]

    Field 9 Comment

       See AJBcomments.py for a description of the comments grammer

    """

    def __init__(self, _entry_str=None):

        super(AJBentry, self).__init__()

        self.blank_entry()

        if _entry_str:
            entrytext.entry_from_text(self, _entry_str)

    def blank_entry(self):
        """Initialize a blank entry by setting known fields to
        null values and deleting all other fields.
        """
        keys = list(self.keys())
        for k in keys:
            del self[k]

        self['Index'] = -1
        self['Num'] = {'volNum':-1,
                       'pageNum': -1,
                       'sectionNum':-1,
                       'subsectionNum':-1,
                       'entryNum':-1,
                       'entrySuf':'',
                       'volume': ''}
        self['Authors'] = []
        self['Editors'] = []
        self['Compilers'] = []
        self['Contributors'] = []
        self['Translators'] = []
        self['Others'] = []
        self['Title'] = ''
        self['Publishers'] = []
        self['Year'] = ''
        self['Pagination'] = ''
        self['Price'] = ''
        self['Reviews'] = []
        self['Comments'] = ''
        self['OrigStr'] = ''


    def is_valid_ajbnum(self):
        """A valid AJB number has a volume number between 1-68
        and a section number between 1-150
        and an entry number > 0"""

        num = self['Num']

        return bool(num['volNum'] > 0 and num['volNum'] < 69 \
                    and num['sectionNum'] > 0 and num['sectionNum'] < 150 \
                    and num['entryNum'] > 0 \
                    and (num['entrySuf'] == '' or num['entrySuf'] == 'a' \
                         or num['entrySuf'] == 'b' or num['entrySuf'] == 'c'))


    def num_str(self):
        """Return a stringfied version of the Num entry,
        ex. 'AJB 68.01(0).20'
        """
        anum = self['Num']
        if anum:
            strnum = str(anum['volume'])
            strnum = strnum + ' ' + '%02d'%anum['volNum']
            strnum = strnum + '.' + '%02d'%anum['sectionNum']
            if anum['subsectionNum'] > -1:
                strnum = strnum + '(' + str(anum['subsectionNum']) + ')'
            strnum = strnum + '.' + '%02d'%anum['entryNum']
            strnum = strnum + '%1s'%anum['entrySuf']
            return strnum

        return None

    def short_title(self):
        """Create a short title string for the entry. A short title
        is 'AJBnum 1stAuthor_lastname Title'."""
        string = self.num_str() + ' '
        if self.not_empty('Authors'):
            name = self['Authors'][0].last
        elif self.not_empty('Editors'):
            name = self['Editors'][0].last
        else:
            name = 'noAuthor'

        string = string + name + ', ' + self['Title'] + '\n'
        return string

    def is_valid(self):
        """AJB entries are valid if they have a valid AJB num
        and a Title."""
        return bool(self.is_valid_ajbnum() and self['Title'] != '')

    def not_empty(self, key):
        """Return the truth value of, 'key' existing
        in the entry and the key value is not empty."""
        if self.__contains__(key) and self[key]:
            return True
        return False

    #
    # Read/write the entry in the specified format
    #
    def read_xml_to_entry(self, xmlstr):
        '''A call to the entryxml routine entry_from_xml()'''
        entryxml.entry_from_xml(self, xmlstr)

    def write_xml_from_entry(self):
        '''A call to the entryxml routine entry_to_xml()'''
        return entryxml.entry_to_xml(self)

    def read_text_to_entry(self, line):
        '''A call to the entrytext routine entry_from_text()'''
        entrytext.entry_from_text(self, line)

    def write_text_from_entry(self):
        '''A call to the entrytext routine entry_to_text()'''
        entrytext.entry_to_text(self)

#
# Test everything
#
if __name__ == '__main__':

    print('Need to define test routines!')
