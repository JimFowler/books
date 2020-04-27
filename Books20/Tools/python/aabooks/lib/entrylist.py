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
##   reproduced, stored in a retrival system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright


"""Defines the generic class that handles disk files and entry lists"""

import os

__VERSION__ = 0.1


class EntryList(list):
    """The EntryList is a generic class which handles the disk file and
    entry list. It provides generic functions and metadata for a disk
    file containing a list of entries.

    """

    # pylint: disable=eval-used
    def __init__(self):
        """Intialize the generic metadata for the list and file.
        sub-classes of EntryList may define their own metadata
        and/or ignore this metadata.

        """
        super(EntryList, self).__init__()

        self._header = None

        self._filename = './document1.txt'
        self._dirname = './'
        self._basename = 'document1'
        self._extension = '.txt'

        # 1 <= current_entry_index <= len(self.)
        self.current_entry_index = -1

        self._dirty = False

    def is_dirty(self):
        """Returns a boolean. The value is True if any of the entries
        or the header has changed since the last read() or write().

        """
        return self._dirty

    def max_entries(self):
        '''Return the number of entries in the entry_list.

        '''
        return len(self)

    # Functions dealing with the file name

    def set_filename(self, filename):
        """Set the name of the disk file. Thus one can read a file,
        set a new file name, and save the file. No validity checking
        is done at this stage.

        Returns True if the filename was set, otherwise it return False
        """

        if isinstance(filename, str):
            self._filename = filename
            self._dirname, _basename = os.path.split(filename)
            self._basename, self._extension = os.path.splitext(_basename)
            self._dirty = True
            return True

        return False

    def get_filename(self):
        """Return the current value of the fileName.

        """
        return self._filename

    def get_dirname(self):
        """Returns the dirname() of the current filename.

        """
        return self._dirname

    def get_basename(self):
        """Returns the basename() of the current filename.

        """
        return self._basename

    def get_basename_with_extension(self):
        """Returns the baseName().extension() of the current filename.

        """
        return self._basename + self._extension

    def get_extension(self):
        """Returns the extension() of the current filename.

        """
        return self._extension

    # Functions to deal with the Header

    def set_header(self, headerstr):
        """Set the header entry to be headerStr.

        """

        # headerstr should be a string
        if isinstance(headerstr, str):
            self._dirty = True
            self._header = headerstr
            return True

        return False

    def get_header(self):
        """Return the current header string.

        """
        return self._header

    # current entry

    def set_new_entry(self, entry, count=-1):
        """Append an entry to the list or insert before entry 'count',
        if that value is given. Note that 1 <= count <= len(self.).
        The dirty flag is set for the file.

        """

        if not entry.is_valid():
            return False

        if 1 <= count <= len(self):
            # count is within the list, insert the entry
            self.current_entry_index = count - 1
            self.insert(self.current_entry_index, entry)
        else:
            # count is not within the list, append the entry
            self.append(entry)

        self._dirty = True

        return True

    def set_entry(self, entry, count=-1):
        """Write over an existing entry or the entry at position
        'count' if given.  Note that 1 <= count <= len(self.).
        The dirty flag is set for the file.

        Returns True or False indicating whether or not the entry
        was copied into the list.

        Should we consider generating an exception if we can't write?

        """
        if not entry.is_valid():
            return False

        if count != -1 and not 1 <= count <= len(self):
            return False

        if count != -1:
            self.current_entry_index = count - 1

        self[self.current_entry_index] = entry
        self._dirty = True

        return True

    def get_entry(self, count=-1):
        """Returns the entry at position count. If count is less than 1
        or greater than the number of entries, 'None' is returned. Note
        that 1 <= count <= len(self.).

        """
        if count < 1 or count > len(self):
            return None

        # the list actually counts with a zero-based index
        self.current_entry_index = count - 1
        return self[self.current_entry_index]

    def delete_entry(self, entrynum):
        """Delete the (entryNum - 1) record in the list, if such exists.
        Return the length of the remaining list.

        """
        if 0 < entrynum <= len(self):
            self.pop(entrynum - 1)
            self._dirty = True

        return len(self)

    # file I/O
    def read_file(self, filename=None):
        """Select a reader function depending on the filename
        extension.  Return the number of entries read.

        """
        if filename:
            self.set_filename(filename)

        if self._filename == '' or not os.path.isfile(self._filename):
            return 0  # no records read

        return eval('self.read_file_' + self._extension[1:])

    def write_file(self, filename=None):
        """Select a writer function depending on the filename
        extension. If filename is not given, we use aabooks._fileName
        instead.

        Returns True if the file could be written or False otherwise.

        """
        if filename:
            self.set_filename(filename)

        return eval('self.write_file_' + self._extension[1:])



if __name__ == "__main__":

    import unittest
    from pathlib import Path
    import aabooks.lib.entry as en
    from pprint import pprint
    
    class MyEntry(en.Entry):
        """A simple entry class for testing.
        The entry consists of a single entry
        'value' : <string>
        since Entry is a sub-class of dictionary

        """

        def __init__(self, string=None):
            """The event initializer."""
            super(MyEntry, self).__init__()
            self.set_value(string)

        def is_valid(self):
            """Report if the entry is good."""
            return isinstance(self['value'], str)

        def blank_entry(self):
            """Create a new Entry."""


        def set_value(self, string):
            """Set the entry."""
            self['value'] = string


    class EntryListTestCase(unittest.TestCase):
        """Set up the unittests"""
        def setUp(self):
            """Initialize any local stuff."""

        def test_initialize(self):
            """Test that the EntryList is initialized correctly.

            Test
              header is None
              filename
              dirname
              basename
              extension
              dirty_flag

            """

            ev_list = EntryList()
            self.assertIsNone(ev_list.get_header())
            self.assertEqual(ev_list.get_filename(), './document1.txt')
            self.assertEqual(ev_list.get_dirname(), './')
            self.assertEqual(ev_list.get_basename(), 'document1')
            self.assertEqual(ev_list.get_extension(), '.txt')
            self.assertEqual(ev_list.get_basename_with_extension(),
                             'document1.txt')
            self.assertFalse(ev_list.is_dirty())

            del ev_list

        def test_set_filename(self):
            """Test set_filename and all the get_*name functions

            """

            ev_list = EntryList()
            self.assertTrue(ev_list.set_filename('./files/test_file.xml'))
            self.assertEqual(ev_list.get_filename(), './files/test_file.xml')
            self.assertEqual(ev_list.get_dirname(), './files')
            self.assertEqual(ev_list.get_basename(), 'test_file')
            self.assertEqual(ev_list.get_extension(), '.xml')
            self.assertEqual(ev_list.get_basename_with_extension(),
                             'test_file.xml')
            self.assertTrue(ev_list.is_dirty())

            # should not be able to set a non-string as the filename
            self.assertFalse(ev_list.set_filename(5))
            self.assertEqual(ev_list.get_filename(), './files/test_file.xml')

            del ev_list

        def test_header(self):
            """Test header manipulation.

            test
              set_header and verify dirty flag
              get_header
              invalid header
            """

            ev_list = EntryList()
            header = """This is the new header.

It contains three lines."""
            self.assertTrue(ev_list.set_header(header))
            self.assertEqual(ev_list.get_header(), header)
            self.assertTrue(ev_list.is_dirty())
            del ev_list

            # should not be able to write a non-string to the header
            ev_list = EntryList()
            self.assertFalse(ev_list.set_header(5))
            self.assertFalse(ev_list.is_dirty())
            del ev_list


        def test_entry(self):
            """Test entry manipulation.

            """

            # test set_new_entry with
            #  valid entry
            #  second valid entry
            #  insert an entry
            #  invalid entry

            ev_list = EntryList()
            entry1 = MyEntry('The quick brown fox')
            entry2 = MyEntry('jumped over the')
            entry3 = MyEntry('lazy dogs back')
            entry4 = MyEntry() # invalid entry

            # verify that ev_list is clean initially
            self.assertFalse(ev_list.is_dirty())

            # test set_new_entry with valid entry and check dirty flag set 1
            self.assertTrue(ev_list.set_new_entry(entry1))
            self.assertEqual(ev_list.get_entry(1), entry1)
            self.assertTrue(ev_list.is_dirty())

            # test set_new_entry with second valid entry 12
            self.assertTrue(ev_list.set_new_entry(entry2))
            self.assertEqual(ev_list.get_entry(2), entry2)

            # test set_new_entry insertion of entry 312
            self.assertTrue(ev_list.set_new_entry(entry3, 1))
            self.assertEqual(ev_list.get_entry(1), entry3)

            # test set_new_entry insertion of entry with invalid count 3121
            self.assertTrue(ev_list.set_new_entry(entry1, 4))
            self.assertEqual(ev_list.get_entry(4), entry1)

            # test set_new_entry with invalid entry
            self.assertFalse(ev_list.set_new_entry(entry4))

            
            # test get_entry with counts inside and outside of invalid values
            self.assertIsNone(ev_list.get_entry(0))
            self.assertIsNone(ev_list.get_entry(ev_list.max_entries()+1))
            self.assertEqual(ev_list.get_entry(1), entry3)
            self.assertEqual(ev_list.get_entry(ev_list.max_entries()), entry1)

            # Test set_entry

            # test set_entry with replacement of entry just inside valid counts 2121
            self.assertTrue(ev_list.set_entry(entry2, 1))
            self.assertEqual(ev_list.get_entry(1), entry2)
            self.assertTrue(ev_list.set_entry(entry3, ev_list.max_entries())) # 2123
            self.assertEqual(ev_list.get_entry(ev_list.max_entries()), entry3)

            # test set_entry with invalid entry
            self.assertFalse(ev_list.set_entry(entry4, 2))
            self.assertEqual(ev_list.get_entry(4), entry3)

            # test set_entry with invalid count
            self.assertFalse(ev_list.set_entry(entry2, 0))
            self.assertFalse(ev_list.set_entry(entry2, ev_list.max_entries()+1))

            # test delete_entry 123
            self.assertEqual(ev_list.max_entries(), 4)
            self.assertEqual(ev_list.delete_entry(1), 3)

            # test delete_entry with invalid count 123
            self.assertEqual(ev_list.delete_entry(0), 3)
            self.assertEqual(ev_list.delete_entry(ev_list.max_entries()+1), 3)

            del ev_list
            del entry1
            del entry2
            del entry3

        def test_read_file(self):
            """Test the read_file stub.

            """
            ev_list = EntryList()

            filename = 'bogon.xml'
            # test read_file with bogus file name
            try:
                os.remove(filename)
            except FileNotFoundError:
                pass

            self.assertEqual(ev_list.read_file(filename), 0)

            # test read_file with real (but empty) filename
            Path('bogon.xml').touch()
            with self.assertRaises(AttributeError):
                ev_list.read_file('bogon.xml')

            # test that _filename was updated
            self.assertEqual(ev_list.get_filename(), 'bogon.xml')
            try:
                os.remove('bogon.xml')
            except FileNotFoundError:
                pass

            del ev_list

        def test_write_file(self):
            """test the write_file stub

            """
            ev_list = EntryList()
            filename = 'bogon.xml'

            with self.assertRaises(AttributeError):
                ev_list.write_file(filename)

            self.assertEqual(ev_list.get_filename(), filename)

            del ev_list


    unittest.main()
