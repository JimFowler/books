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

"""The file entrylist.py contains the generic class EntryList which is
a sub-class of <list>. This class is a container for a list of entries
as well as the metadata associated with the entries.  The entries are
typically defined by event.py but may be defined as something else. An
EntryList typically consists of a header and a list of entries.

The list internally has 0-based indexing and does allow the use of
indexing from the end of the list with -1, etc.

The generic metadate that are associated with entries are

  * dirty_flag - has the list been modified since the last write to disk

  * header - any header information associated with the file

  * filename - the full file name

  * dirname - this directory the file is located in 

  * basename - the base name of the file

  * extension - the file extension or type (e.g .xml, .txt)

Users are free to add their own metadata to their sub-class.

Note also that users must provide the functions to read/write entry
files from/to disk.  The generic read_file()/write_file() functions
are available but they are simply stubs that try to call
read_file_<extension>() where extension is the file extension.  For
example, the file file is entries.xml, then read_file() will try to
run read_file_xml(). The same is true for the write_file() function.
Users are not required to use the read_file()/write_file() functions
and may provide their own reader and writer.

"""

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

        # the index of the current entry (record)
        self._current_index = 0

        self._dirty = False

    def is_dirty(self):
        """Returns a boolean. The value is True if any of the entries
        or the header has changed since the last read() or write().

        """
        return self._dirty

    def set_current_index(self, index):
        '''Set the current_index to index, if count is
        a legal list index, i.e. -n <= count < n, where n is
        the length of the list.

        returns True or False

        '''

        length = len(self)
        if -length <= index < 0:
            self._current_index = length - index
            return True
        elif 0 <= index < length:
            self._current_index = index
            return True

        return False

    def get_current_index(self):
        """Get the value of the metadata current_index. This indicates
        what entry (record) we are working on currently.

        """
        return self.current_index

    
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

    def set_new_entry(self, entry, index=None):
        """Append an entry to the list or insert before entry 'index',
        if that value is given. Note that -len(self) <= index < len(self).
        The dirty flag is set for the file.

        This does the insert and append actions
        """

        if not entry.is_valid():
            return False

        if count is None or -len(self) <= count < len(self):
            # index is not within the list, append the entry
            self.append(entry)
            self.set_current_index(len(self))
        else:
            # count is within the list, insert the entry
            self.current_index = count
            self.insert(self.current_entry_index, entry)

        self._dirty = True

        return True

    def set_entry(self, entry, count=-1):
        """Write over an existing entry or the entry at position
        'count' if given.  Note that 1 <= count <= len(self.).
        The dirty flag is set for the file.

        Returns True or False indicating whether or not the entry
        was copied into the list.

        Should we consider generating an exception if we can't write?

        This does the replace action.

        """
        if not entry.is_valid():
            return False

        if count != -1 and not 0 <= count < len(self):
            return False

        if count != -1:
            self.current_entry_index = count

        self[self.current_entry_index] = entry
        self._dirty = True

        return True

    def get_entry(self, count=None):
        """Returns the entry at position count. If count is less than 1
        or greater than the number of entries, 'None' is returned. Note
        that 1 <= count <= len(self.).

        """
        #if count < 1 or count > len(self):
        if count is not None:
            self._set_index_count(count)
            
        return self[self.current_entry_index]

    def delete_entry(self, entrynum):
        """Delete the entryNum record in the list, if such exists.
        Return the length of the remaining list.

        This does the delete action

        """

        self.pop(entrynum)
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
        """Set up the unit tests"""
        def setUp(self):
            """Start with a fresh EntryList and Entry's for
            each test."""

            self.ev_list = EntryList()
            self.entry1 = MyEntry('The quick brown fox')
            self.entry2 = MyEntry('jumped over the')
            self.entry3 = MyEntry('lazy dogs back')
            self.entry4 = MyEntry() # invalid entry

        def tearDown(self):
            """Delete the class variables at the end of each test."""
            
            del self.ev_list
            del self.entry1
            del self.entry2
            del self.entry3
            del self.entry4

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

            self.assertIsNone(self.ev_list.get_header())
            self.assertEqual(self.ev_list.get_filename(), './document1.txt')
            self.assertEqual(self.ev_list.get_dirname(), './')
            self.assertEqual(self.ev_list.get_basename(), 'document1')
            self.assertEqual(self.ev_list.get_extension(), '.txt')
            self.assertEqual(self.ev_list.get_basename_with_extension(),
                             'document1.txt')
            self.assertFalse(self.ev_list.is_dirty())


        def test_set_filename(self):
            """Test set_filename and all the get_*name functions

            """

            self.assertTrue(self.ev_list.set_filename('./files/test_file.xml'))
            self.assertEqual(self.ev_list.get_filename(), './files/test_file.xml')
            self.assertEqual(self.ev_list.get_dirname(), './files')
            self.assertEqual(self.ev_list.get_basename(), 'test_file')
            self.assertEqual(self.ev_list.get_extension(), '.xml')
            self.assertEqual(self.ev_list.get_basename_with_extension(),
                             'test_file.xml')
            self.assertTrue(self.ev_list.is_dirty())

            # should not be able to set a non-string as the filename
            self.assertFalse(self.ev_list.set_filename(5))
            self.assertEqual(self.ev_list.get_filename(), './files/test_file.xml')


        def test_header(self):
            """Test header manipulation.

            test
              set_header and verify dirty flag
              get_header
              invalid header
            """

            header = """This is the new header.

It contains three lines."""
            self.assertTrue(self.ev_list.set_header(header))
            self.assertEqual(self.ev_list.get_header(), header)
            self.assertTrue(self.ev_list.is_dirty())
            del self.ev_list

            # should not be able to write a non-string to the header
            self.ev_list = EntryList()
            self.assertFalse(self.ev_list.set_header(5))
            self.assertFalse(self.ev_list.is_dirty())


        def test_entry(self):
            """Test entry manipulation.

            """

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

            
            # test get_entry with counts inside and outside of invalid values
            self.assertIsNone(self.ev_list.get_entry(-1))
            self.assertIsNone(self.ev_list.get_entry(len(self.ev_list)))
            self.assertEqual(self.ev_list.get_entry(0), self.entry3)
            self.assertEqual(self.ev_list.get_entry(-1), self.entry1)

            # Test set_entry

            # test set_entry with replacement of entry just inside valid counts 2121
            self.assertTrue(self.ev_list.set_entry(self.entry2, 1))
            self.assertEqual(self.ev_list.get_entry(1), self.entry2)
            self.assertTrue(self.ev_list.set_entry(self.entry3, self.ev_list.max_entries())) # 2123
            self.assertEqual(self.ev_list.get_entry(self.ev_list.max_entries()), self.entry3)

            # test set_entry with invalid entry
            self.assertFalse(self.ev_list.set_entry(self.entry4, 2))
            self.assertEqual(self.ev_list.get_entry(4), self.entry3)

            # test set_entry with invalid count
            self.assertFalse(self.ev_list.set_entry(self.entry2, 0))
            self.assertFalse(self.ev_list.set_entry(self.entry2, len(self.ev_list)))

            # test delete_entry 123
            self.assertEqual(self.ev_list.max_entries(), 4)
            self.assertEqual(self.ev_list.delete_entry(1), 3)

            # test delete_entry with invalid count 123
            self.assertEqual(self.ev_list.delete_entry(0), 3)
            self.assertEqual(self.ev_list.delete_entry(len(self.ev_list), 3))


        def test_read_file(self):
            """Test the read_file stub.

            """

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

            # test that _filename was updated
            self.assertEqual(self.ev_list.get_filename(), 'bogon.xml')
            try:
                os.remove('bogon.xml')
            except FileNotFoundError:
                pass


        def test_write_file(self):
            """test the write_file stub

            """
            filename = 'bogon.xml'

            with self.assertRaises(AttributeError):
                self.ev_list.write_file(filename)

            self.assertEqual(self.ev_list.get_filename(), filename)


    unittest.main()
