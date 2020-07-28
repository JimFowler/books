## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/lib/entry.py
##
##   Part of the Books20 Project
##
##   Copyright 2012 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrival system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright

"""An Entry defines a generic class, typically for a book or journal entry.
The Entry class is a sub-class of dictionary.  Since this class does
not defined much it is always possible to define your own type of
entry.  The blank_entry() and is_valid() function would normally be
expected to occur in custom Entry declaration.

"""


class Entry(dict):
    """The generic Entry class. The methods Entry.blank_entry() and
    Entry.is_valid() need to be provided by the sub-class if they are
    going to be used.

    Note that this base class does very little.  I am keeping it
    around in case I need to define any operation that might want to
    be generic to all entry types.

    """
    _version = 'class: Entry(dict) v1.0.0 dtd 27 Sep 2012'

    def __init__(self, _entry_str=None):

        super(Entry, self).__init__()


    def version(self):
        """Return the version string for this class."""
        return str(self._version)
    #
    # Functions to be provided by the sub-class
    #
    def blank_entry(self):
        """Initialize a blank entry by setting known fields to
        null values and deleting all other fields. The sub-class
        must provide this function.
        """
        raise NotImplementedError('Implement me in subclass')

    def is_valid(self):
        """Return a boolean based on some criteria. The criteria
        must be set by the sub-class."""
        raise NotImplementedError('Implement me in subclass')


if __name__ == '__main__':

    import unittest

    class EntryTestCase(unittest.TestCase):
        """Set up the unit tests"""

        def setUp(self):
            """Initialize local stuff. We start with a fresh Entry object
            for every test."""
            self.test_entry = Entry()

        def tearDown(self):
            """Displose of the Entry object at the end of every test."""
            del self.test_entry

        def test_is_valid(self):
            """Test the Entry.is_valid() function. Should raise
            NotImplementedError."""

            with self.assertRaises(NotImplementedError):
                self.test_entry.is_valid()

        def test_blank_entry(self):
            """Test the Entry.blank_entry() function. Should raise
            NotImplementedError."""

            with self.assertRaises(NotImplementedError):
                self.test_entry.blank_entry()

        def test_version(self):
            """Test the Entry.version() function."""

            self.assertEqual(self.test_entry.version(), 'class: Entry(dict) v1.0.0 dtd 27 Sep 2012')

    unittest.main()
