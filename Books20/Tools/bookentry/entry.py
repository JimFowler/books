"""An Entry defines a generic class for a book entry; Usually
entry objects will be either entriesbook listings from
Astronomisher Jahresbericht or Astronomy and Astrophysics
Abstracts.  Specific entry types should be sub-classed from Entry.
"""
# -*- coding: UTF-8 -*-
# -*- mode: Python;-*-

__version__ = "class: Entry(dict) v1.0.0 dtd 27 Sep 2012"

class Entry(dict):
    """The generic Entry class. Methods Entry.extract() and Entry.str()
    need to be provided by the sub-class."""

    def __init__(self, _entrystr=None):

        self.blankEntry()

        if _entrystr :
            self.read(_entrystr)

    def version(self):
        """Return the version string of the Entry class."""
        return str(__version__)


    def blankEntry(self):
        """Initialize a blank entry by setting known fields to
        null values and deleting all other fields.
        """
        keys = list(self.keys())
        for k in keys :
            del(self[k])

        self[ 'Index'] =      -1
        self[ 'Num'] =        {'volNum':-1,
                               'sectionNum':-1,
                               'subsectionNum':-1,
                               'entryNum':-1,
                               'entrySuf':'',
                               'volume': ''}
        self[ 'Authors'] =    []
        self[ 'Editors'] =    []
        self[ 'Compilers'] =  []
        self[ 'Contributors'] = []
        self[ 'Translators']= []
        self[ 'Others']=      []
        self[ 'Title'] =      ''
        self[ 'Publishers'] = []
        self[ 'Year'] =       ''
        self[ 'Pagination'] = ''
        self[ 'Price'] =      ''
        self[ 'Reviews'] =    []
        self[ 'Comments'] =   ''
        self[ 'OrigStr'] =    ''

    #
    # Functions to be provided by the sub-class
    #
    def isValid(self):
        """Return a boolean based on some criteria. The criteria
        must be set by the sub-class."""
        assert 0, 'Entry.isValid() needs to be defined'

    def read(self, line):
        """Read string and parse entry items out of it. Should return
        a boolean indicating whether the line was actually read correctly.
        The sub-class must provide this function."""
        assert 0, 'Entry.read() method required'

    def write(self):
        """Returns a string with the  entry items. This string should one
        that could be parsed by the read method. It is the responsiblity
        of the sub-class to implement this funtion. The sub-class must 
        provide this function."""
        assert 0, 'Entry.write() method required'
