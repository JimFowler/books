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

"""An Entry defines a generic class for a book or journal entry;
Usually entry objects will be either book listings from Astronomisher
Jahresbericht or Astronomy and Astrophysics Abstracts.  Specific entry
types should be sub-classed from Entry.

"""


class Entry(dict):
    """The generic Entry class. The methods Entry.blank_entry() and
    Entry.is_valid() need to be provided by the sub-class if they are
    going to be used.

    Note that this base class does very little.  I am keeping it
    around in case I need to define any operation that might want to
    be generic to all entry types.

    """
    _version = "class: Entry(dict) v1.0.0 dtd 27 Sep 2012"

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

    e = Entry()
        
    try:
        e.is_valid()
    except NotImplementedError:
        print("""Entry() class fails properly with an NotImplementedError
        for is_valid() method.""")
