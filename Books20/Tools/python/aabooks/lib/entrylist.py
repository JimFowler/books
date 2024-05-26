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
