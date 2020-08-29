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

"""The file entrylist.py contains the generic class EntryList which is
a sub-class of <list>. This class is a container for a list of entries
as well as the metadata associated with the entries.  The entries are
typically defined by event.py but may be defined as something else. An
EntryList typically consists of a header and a list of entries.

For the user of this class, the entries are counted from 1 to
max_entries(), however, the normal list style is to count from 0 to
max_entries() - 1. This will certainly change in the future to be
more pythonic.  Will need to update the documentation and unit tests
when I do.

The generic metadata that are associated with entries are

  * dirty_flag - has the list been modified since the last write to disk

  * filename - the full file name
               Used only in open() statement


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

__VERSION__ = 1.0


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

        # the first element is the header
        self.append('')

        self.filename = './document1.xml'
        self._dirty = False

    def is_dirty(self):
        """Returns a boolean. The value is True if any of the entries
        or the header has changed since the last read() or write().

        """
        return self._dirty

    def max_entries(self):
        '''Return the number of entries in the entry_list.

        '''
        return len(self) - 1

    # Functions to deal with the Header

    def set_header(self, headerstr):
        """Set the header entry to be headerStr.

        """

        # headerstr should be a string
        if isinstance(headerstr, str):
            self._dirty = True
            self[0] = headerstr
            return True

        return False

    def get_header(self):
        """Return the current header string.

        """
        return self[0]

    # current entry

    def set_new_entry(self, entry, count=-1):
        """Append an entry to the list or insert before entry 'count',
        if that value is given. Note that 1 <= count <= len(self.).
        The dirty flag is set for the file.

        """

        if not entry.is_valid():
            return False

        if 1 <= count <= len(self) - 1:
            # count is within the list, insert the entry
            self.insert(count, entry)
        else:
            # count is not within the list, append the entry
            self.append(entry)

        self._dirty = True

        return True

    def set_entry(self, entry, count=-1):
        """Write over an existing entry or the entry at position
        'count' if given.  Note that 1 <= count <= len(self.) - 1.
        The dirty flag is set for the file.

        Returns True or False indicating whether or not the entry
        was copied into the list.

        Should we consider generating an exception if we can't write?

        """
        if not entry.is_valid():
            return False

        if count != -1 and not 1 <= count <= len(self) - 1:
            return False


        self[count] = entry
        self._dirty = True

        return True

    def get_entry(self, count=-1):
        """Returns the entry at position count. If count is less than 1
        or greater than the number of entries, 'None' is returned. Note
        that 1 <= count <= len(self.).

        """
        if count < 1 or count > len(self) - 1:
            return None

        return self[count]

    def delete_entry(self, entrynum):
        """Delete the entryNum record in the list, if such exists.
        Return the length of the remaining list.

        """
        if 0 < entrynum <= len(self) - 1:
            self.pop(entrynum)
            self._dirty = True

        return len(self) - 1

    # file I/O
    def read_file(self, filename=None):
        """Select a reader function depending on the filename
        extension.  Return the number of entries read.

        """
        if filename:
            self.filename = filename

        if self.filename == '' or not os.path.isfile(self.filename):
            return 0  # no records read

        return eval('self.read_file_' + os.path.splitext(self.filename)[1][1:])

    def write_file(self, filename=None):
        """Select a writer function depending on the filename
        extension. If filename is not given, we use aabooks._fileName
        instead.

        Returns True if the file could be written or False otherwise.

        """
        if filename:
            self.filename = filename

        return eval('self.write_file_' + os.path.splitext(self.filename)[1][1:])



if __name__ == "__main__":

    import unittest
    from pathlib import Path

    class MyEntry(dict):
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
            """Delete the class variables at the end of each """

            del self.ev_list
            del self.entry1
            del self.entry2
            del self.entry3
            del self.entry4

        def test_a_initialize(self):
            """Test that the EntryList is initialized correctly.

            Test
              header is None
              filename
              dirty_flag

            """

            self.assertEqual(self.ev_list.get_header(), '')
            self.assertEqual(self.ev_list.filename, './document1.xml')
            self.assertFalse(self.ev_list.is_dirty())

        def test_c_header(self):
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

        def test_d_set_new_entry(self):
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
            self.assertEqual(self.ev_list.get_entry(1), self.entry1)
            self.assertTrue(self.ev_list.is_dirty())

            # test set_new_entry with second valid entry 12
            self.assertTrue(self.ev_list.set_new_entry(self.entry2))
            self.assertEqual(self.ev_list.get_entry(2), self.entry2)

            # test set_new_entry insertion of entry 312
            self.assertTrue(self.ev_list.set_new_entry(self.entry3, 1))
            self.assertEqual(self.ev_list.get_entry(1), self.entry3)

            # test set_new_entry insertion of entry with invalid count 3121
            self.assertTrue(self.ev_list.set_new_entry(self.entry1, 4))
            self.assertEqual(self.ev_list.get_entry(4), self.entry1)

            # test set_new_entry with invalid entry
            self.assertFalse(self.ev_list.set_new_entry(self.entry4))

        def test_e_get_entry(self):
            '''Test the EntryList.get_entry() function.'''

            # set up the list first 123
            self.assertTrue(self.ev_list.set_new_entry(self.entry1))
            self.assertTrue(self.ev_list.set_new_entry(self.entry2))
            self.assertTrue(self.ev_list.set_new_entry(self.entry3))

            # test get_entry with counts inside and outside of invalid values
            self.assertIsNone(self.ev_list.get_entry(0))
            self.assertIsNone(self.ev_list.get_entry(self.ev_list.max_entries()+1))
            self.assertEqual(self.ev_list.get_entry(1), self.entry1)
            self.assertEqual(self.ev_list.get_entry(self.ev_list.max_entries()), self.entry3)

        def test_f_set_entry(self):
            '''Test the EntryList.set_entry() function'''

            # set up the list first 1233
            self.assertTrue(self.ev_list.set_new_entry(self.entry1))
            self.assertTrue(self.ev_list.set_new_entry(self.entry2))
            self.assertTrue(self.ev_list.set_new_entry(self.entry3))
            self.assertTrue(self.ev_list.set_new_entry(self.entry3))

            # test set_entry with replacement of entry just inside valid counts 2233
            self.assertTrue(self.ev_list.set_entry(self.entry2, 1))
            self.assertEqual(self.ev_list.get_entry(1), self.entry2)
            self.assertTrue(self.ev_list.set_entry(self.entry1, self.ev_list.max_entries())) # 2221
            self.assertEqual(self.ev_list.get_entry(self.ev_list.max_entries()), self.entry1)

            # test set_entry with invalid entry
            self.assertFalse(self.ev_list.set_entry(self.entry4, 2))
            self.assertEqual(self.ev_list.get_entry(4), self.entry1)

            # test set_entry with invalid count
            self.assertFalse(self.ev_list.set_entry(self.entry2, 0))
            self.assertFalse(self.ev_list.set_entry(self.entry2, self.ev_list.max_entries()+1))

            # test delete_entry 221
            self.assertEqual(self.ev_list.max_entries(), 4)
            self.assertEqual(self.ev_list.delete_entry(1), 3)

            # test delete_entry with invalid count 123
            self.assertEqual(self.ev_list.delete_entry(0), 3)
            self.assertEqual(self.ev_list.delete_entry(self.ev_list.max_entries()+1), 3)

        def test_g_read_file(self):
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
            self.assertEqual(self.ev_list.filename, 'bogon.xml')
            try:
                os.remove('bogon.xml')
            except FileNotFoundError:
                pass

        def test_h_write_file(self):
            """test the write_file stub

            """
            filename = 'bogon.xml'

            with self.assertRaises(AttributeError):
                self.ev_list.write_file(filename)

            self.assertEqual(self.ev_list.filename, filename)


    unittest.main()
