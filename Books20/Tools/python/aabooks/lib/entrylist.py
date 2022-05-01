#! /usr/bin/env python
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/lib/entrylist.py
##
##   Part of the Books20 Project
##
##   Copyright 2020 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrieval system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright

'''The file entrylist.py contains the generic class EntryList which is
a sub-class of <list>. This class is a container for a list of entries
as well as the metadata associated with the entries.  The entries may
be any type of data, but should have an is_valid() method.  An
EntryList typically consists of a header and a list of entries.

For the user of this class, the entries are counted from 1 to
max_entries(), however, with the metadata header as element 0 so the
entry numbers go from 1 to len(self) - 1.

The generic metadata that are associated with entries are

  * dirty_flag - has the list been modified since the last write to disk

  * filename - the full file name. Used only in open() method

  * header - a string containing information about the entries. This is stored
    at the beginning of the list as self[0]

Users are free to add their own metadata to their sub-class.

Subclasses of EntryList must provided the functions to read/write entry
files from/to disk.  The generic read_file()/write_file() functions
are available but they are simply stubs that try to call
read_file_<extension>() where extension is the file extension.  For
example, if the file name is entries.xml, then read_file() will try to
run read_file_xml(). The same is true for the write_file() function.
Users are not required to use the read_file()/write_file() functions
and may provide their own reader and writer.

'''

import os

__VERSION__ = 1.0


class EntryList(list):
    '''The EntryList is a generic class which handles the disk file and
    entry list. It provides generic functions and metadata for a disk
    file containing a list of entries. Entries may be of any type but should
    provide a validity method, is_valid().

    '''

    # pylint: disable=eval-used
    def __init__(self):
        '''Initialize the generic metadata for the list and file.
        sub-classes of EntryList may define their own metadata
        and/or ignore this metadata.

        '''
        super().__init__()

        # the first element is the header
        self.header = ''

        self.filename = './document1.xml'
        self._dirty = False

    def is_dirty(self):
        '''Returns a boolean. The value is True if any of the entries
        or the header has changed since the last read() or write().

        '''
        return self._dirty

    def max_entries(self):
        '''Return the number of entries in the entry_list. This number
        will be len(self).

        '''
        return len(self)

    def clear_list(self):
        '''Delete all entries and put '' in the header. This will leave a list
        with only an empty header and no entries.  Returns
        max_entries(), which should be 0.

        '''

        self.clear()

        self.set_header('')
        self._dirty = False

        return self.max_entries()

    # Functions to deal with the filename
    def set_filename(self, filename):
        '''Set the filename.'''

        self.filename = filename

    def get_filename(self):
        '''Set the filename.'''

        return self.filename

    # Functions to deal with the Header
    def set_header(self, headerstr):
        '''Set the header entry to be headerstr.

        '''

        # headerstr should be a string
        if isinstance(headerstr, str):
            self._dirty = True
            self.header = headerstr
            return True

        return False

    def get_header(self):
        '''Return the current header string.

        '''
        return self.header

    # functions to deal with entries
    def set_new_entry(self, entry, count=-1):
        '''Append an entry to the list or insert before entry 'count', if that
        value is given. Note that 0 <= count < len(self) for
        insertion.  The dirty flag is set for the file.

        '''

        if not entry.is_valid():
            return False

        if 0 <= count < len(self):
            # count is within the list, insert the entry
            self.insert(count, entry)
        else:
            # count is not within the list, append the entry
            self.append(entry)

        self._dirty = True

        return True

    def set_entry(self, entry, entrynum=-1):
        '''Write over an existing entry or the entry at position
        'entrynum', if given.  Note that 0 <= entrynum < len(self).
        The dirty flag is set for the list.

        Returns True or False indicating whether or not the entry
        was copied into the list.

        Should we consider generating an exception if we can't write?

        '''
        if not entry.is_valid():
            return False

        if 0 <= entrynum < len(self):
            self[entrynum] = entry
            self._dirty = True
            return True

        return False

    def get_entry(self, entrynum=-1):
        '''Returns the entry at position entrynum. If entrynum is less than 1
        or greater than the number of entries, 'None' is
        returned. Note that 0 < entrynum < len(self.).

        '''
        if 0 <= entrynum < len(self):
            return self[entrynum]

        return None

    def delete_entry(self, entrynum):
        '''Delete the entrynum record in the list, if such exists.
        Return the length of the remaining list.

        '''
        if 0 <= entrynum < len(self):
            self.pop(entrynum)
            self._dirty = True

        return self.max_entries()

    # generic file I/O
    def read_file(self, filename=None):
        '''Select a reader function depending on the filename
        extension.  Return the number of entries read. If filename
        is not given, then read the file in self.filename. If the filename
        is given, then update self.filename and read the file.

        '''
        if filename:
            self.filename = filename

        if self.filename == '' or not os.path.isfile(self.filename):
            return 0  # no records read

        return eval('self.read_file_' + os.path.splitext(self.filename)[1][1:] + '()')

    def write_file(self, filename=None):
        '''Select a writer function depending on the filename
        extension. If filename is not given, we use self.fileName
        instead.

        Returns True if the file could be written or False otherwise.

        '''
        if filename:
            self.filename = filename

        return eval('self.write_file_' + os.path.splitext(self.filename)[1][1:] + '()')



if __name__ == '__main__':

    import unittest
    from pathlib import Path

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

            self.ev_list = EntryList()
            self.entry1 = MyEntry('The quick brown fox')
            self.entry2 = MyEntry('jumped over the')
            self.entry3 = MyEntry('lazy dogs back')
            self.entry4 = MyEntry() # invalid entry

        def tearDown(self):
            '''Delete the class variables at the end of each '''

            del self.ev_list
            del self.entry1
            del self.entry2
            del self.entry3
            del self.entry4

        def test_a_initialize(self):
            '''Test that the EntryList is initialized correctly.

            Test
              header is None
              filename
              dirty_flag

            '''

            self.assertEqual(self.ev_list.get_header(), '')
            self.assertEqual(self.ev_list.filename, './document1.xml')
            self.assertFalse(self.ev_list.is_dirty())

        def test_b_header(self):
            '''Test header manipulation.

            test
              set_header and verify dirty flag
              get_header
              invalid header
            '''

            header = '''This is the new header.

It contains three lines.'''
            self.assertTrue(self.ev_list.set_header(header))
            self.assertEqual(self.ev_list.get_header(), header)
            self.assertTrue(self.ev_list.is_dirty())

            # should not be able to write a non-string to the header
            self.ev_list = EntryList()
            self.assertFalse(self.ev_list.set_header(5))
            self.assertFalse(self.ev_list.is_dirty())

        def test_c_set_new_entry(self):
            '''Test entry manipulation.

            '''

            # test set_new_entry with
            #  valid entry
            #  second valid entry
            #  insert an entry
            #  invalid entry

            # verify that self.ev_list is clean initially
            self.assertFalse(self.ev_list.is_dirty())

            # test set_new_entry with valid entry and check dirty flag set 1
            self.assertTrue(self.ev_list.set_new_entry(self.entry1))
            self.assertEqual(self.ev_list.get_entry(0), self.entry1)
            self.assertTrue(self.ev_list.is_dirty())

            # test set_new_entry with second valid entry 12
            self.assertTrue(self.ev_list.set_new_entry(self.entry2))
            self.assertEqual(self.ev_list.get_entry(1), self.entry2)

            # test set_new_entry insertion of entry 312
            self.assertTrue(self.ev_list.set_new_entry(self.entry3, 0))
            self.assertEqual(self.ev_list.get_entry(0), self.entry3)

            # test set_new_entry insertion of entry with invalid count 3121
            self.assertTrue(self.ev_list.set_new_entry(self.entry1, 3))
            self.assertEqual(self.ev_list.get_entry(3), self.entry1)

            # test set_new_entry with invalid entry
            self.assertFalse(self.ev_list.set_new_entry(self.entry4))

        def test_d_get_entry(self):
            '''Test the EntryList.get_entry() function.'''

            # set up the list first 123
            self.assertTrue(self.ev_list.set_new_entry(self.entry1))
            self.assertTrue(self.ev_list.set_new_entry(self.entry2))
            self.assertTrue(self.ev_list.set_new_entry(self.entry3))

            # test get_entry with counts inside and outside of invalid values
            self.assertIsNone(self.ev_list.get_entry(-1))
            self.assertIsNone(self.ev_list.get_entry(self.ev_list.max_entries()))
            self.assertEqual(self.ev_list.get_entry(0), self.entry1)
            self.assertEqual(self.ev_list.get_entry(self.ev_list.max_entries() - 1), self.entry3)

        def test_d_set_entry(self):
            '''Test the EntryList.set_entry() function'''

            # set up the list first 1233
            self.assertTrue(self.ev_list.set_new_entry(self.entry1))
            self.assertTrue(self.ev_list.set_new_entry(self.entry2))
            self.assertTrue(self.ev_list.set_new_entry(self.entry3))
            self.assertTrue(self.ev_list.set_new_entry(self.entry3))

            # test set_entry with replacement of entry just inside valid counts 2233
            self.assertTrue(self.ev_list.set_entry(self.entry2, 0))
            self.assertEqual(self.ev_list.get_entry(0), self.entry2)
            self.assertTrue(self.ev_list.set_entry(self.entry1,
                                    self.ev_list.max_entries()-1)) # 2221

            self.assertEqual(self.ev_list.get_entry(self.ev_list.max_entries()-1), self.entry1)

            # test set_entry with invalid entry
            self.assertFalse(self.ev_list.set_entry(self.entry4, 2))
            self.assertEqual(self.ev_list.get_entry(3), self.entry1)

            # test set_entry with invalid count
            self.assertFalse(self.ev_list.set_entry(self.entry2, -1))
            self.assertFalse(self.ev_list.set_entry(self.entry2, self.ev_list.max_entries()))

            # test delete_entry 221
            self.assertEqual(self.ev_list.max_entries(), 4)
            self.assertEqual(self.ev_list.delete_entry(1), 3)

            # test delete_entry with invalid count 123
            self.assertEqual(self.ev_list.delete_entry(-1), 3)
            self.assertEqual(self.ev_list.delete_entry(self.ev_list.max_entries()+1), 3)

        def test_f_clear_list(self):
            '''Test the EntryList.clear_list() function.'''

            # set up the list first 1231
            self.assertTrue(self.ev_list.set_new_entry(self.entry1))
            self.assertTrue(self.ev_list.set_new_entry(self.entry2))
            self.assertTrue(self.ev_list.set_new_entry(self.entry3))
            self.assertTrue(self.ev_list.set_new_entry(self.entry1))

            self.assertEqual(self.ev_list.clear_list(), 0)
            # should have no entries in the list
            self.assertEqual(len(self.ev_list), 0)

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

            self.assertEqual(self.ev_list.read_file(filename), 0)

            # test read_file with real (but empty) filename
            Path('bogon.xml').touch()
            with self.assertRaises(AttributeError):
                self.ev_list.read_file('bogon.xml')

            # test that filename was updated
            self.assertEqual(self.ev_list.filename, 'bogon.xml')
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
                self.ev_list.write_file(filename)

            self.assertEqual(self.ev_list.filename, filename)


    unittest.main()
