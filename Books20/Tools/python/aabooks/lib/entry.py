## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/lib/entry.py
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


"""An Entry defines a generic class for a book entry; Usually
entry objects will be either entriesbook listings from
Astronomisher Jahresbericht or Astronomy and Astrophysics
Abstracts.  Specific entry types should be sub-classed from Entry.
"""

__version__ = "class: Entry(dict) v1.0.0 dtd 27 Sep 2012"

class Entry(dict):
    """The generic Entry class. Methods Entry.extract() and Entry.str()
    need to be provided by the sub-class."""

    def __init__(self, _entrystr=None):

        self.blankEntry()

        if _entrystr :
            self.read_Text_to_Entry(_entrystr)

    def version(self):
        """Return the version string of the Entry class."""
        return str(__version__)


    #
    # Functions to be provided by the sub-class
    #
    def blankEntry(self):
        """Initialize a blank entry by setting known fields to
        null values and deleting all other fields. The sub-class
        must provide this function.
        """
        assert 0, 'Entry.blankEntry() needs to be defined'


    def isValid(self):
        """Return a boolean based on some criteria. The criteria
        must be set by the sub-class."""
        assert 0, 'Entry.isValid() needs to be defined'

    def read_Text_to_Entry(self, line):
        """Read string and parse entry items out of it. Should return
        a boolean indicating whether the line was actually read correctly.
        The sub-class must provide this function."""
        assert 0, 'Entry.read() method required'

    def write_Text_from_Entry(self):
        """Returns a string with the  entry items. This string should one
        that could be parsed by the read method. It is the responsiblity
        of the sub-class to implement this funtion. The sub-class must 
        provide this function."""
        assert 0, 'Entry.write() method required'


if __name__ == '__main__':

    try:
        badentry = Entry(ajbstr)
    except:
        print("Entry() class fails properly with no read() method.")
