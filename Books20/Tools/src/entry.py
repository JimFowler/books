"""An Entry defines a generic class for a book entry; Usually
entry objects will be either entriesbook listings from
Astronomisher Jahresbericht or Astronomy and Astrophysics
Abstracts.  Specific entry types should be subclassed from Entry.

Entry is a sub-class of dict so keyword:values may be accessed
directly.  A blank Entry objects look like:


['Index'] =       -1            # file index number
['Num'] =         {'volNum':-1,       # bibliography entry num
                   'sectionNum':-1,
                   'subsectionNum':-1,
                   'entryNum':-1,
                   'volume': ''}
[ 'Authors'] =    []   # list of nameparser::HumanName objects
[ 'Editors'] =    []   # list of nameparser::HumanName objects
[ 'Compilers'] =  []    # list of nameparser::HumanName objects
[ 'Contributors'] = [] # list of nameparser::HumanName objects
[ 'Translators']= []   # list of nameparser::HumanName objects
[ 'Others' ] =    []   # list strings from the comments that we can't parse
[ 'Title'] =      ''   # the title of the work
[ 'Publishers'] = []   # list of tuples (Place, PublisherName)
[ 'Year'] =       ''   # year of publication if known
[ 'Pagination'] = ''   # page count
[ 'Price'] =      ''   # publishers price if known
[ 'Reviews'] =    []   # bibliographic list of reviews, strings
[ 'Comments'] =   ''   # the original comment string
[ 'OrigStr'] =    ''   # the original book entry string if read from a string

"""

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
                               'volume': ''}
        self[ 'Authors'] =    []
        self[ 'Editors'] =    []
        self[ 'Compilers'] =    []
        self[ 'Contributors'] =    []
        self[ 'Translators']= []
        self[ 'Others']= []
        self[ 'Title'] =      ''
        self[ 'Publishers'] = []
        self[ 'Year'] =       -1
        self[ 'Pagination'] = ''
        self[ 'Price'] =      ''
        self[ 'Reviews'] =    []
        self[ 'Comments'] =   ''
        self[ 'OrigStr'] =    ''

    #
    # Functions to be provided by the sub-class
    #
    def isValid(self):
        """Is the entry valid by some criteria? The criteria will typically
        be set by the sub-class."""
        assert 0, 'Entry.isValid() needs to be defined'

    def read(self, line):
        """Read string and parse entry items out of it."""
        assert 0, 'Entry.read() method required'

    def write(self):
        """Write the entry items to a string that could be parsed."""
        assert 0, 'Entry.write() method required'
