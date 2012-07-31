"""Parse line entries for the books abstracted from the
Astronomische Jahrbericht series. Provides a data structure
and object class for manipulating an AJB entry.

Classes
--------

ajbEntry()
    Takes a unicode string with comma separated fields
    and returns an entDict object.

Functions
---------

Some of the parsing functions may be public so that folks can
use them outside of the class object.

  A line looks like:
   Index AJB_Num Author, Title, Place, Publisher, Year, \
   Pagination, Price, Reviews, Comments

  No field need be present except Index and AJB_Num.

   Field 1 Index AJB_Num Author has format

    Index AJB_Num [I. A. Author [jr.|III|...] [ and H. E. Another [and ...]]] \
     [ed.|comp.|something else]

   Field 2 Title

   Field 3 Place

     [name | name-name[-name[-...]] Name may contain spaces

   Field 4 Publisher

   Field 5 Year

   Field 6 Pagination

   Field 7 Price

   Field 8 Reviews

     [Journal vol page [and Journal vol page [and ...]]]

     Need to pull the Journal and reference from here

   Field 9 Comment

     Need to do something with these. They contains editions, editors,
      translators, and other people as well as references and language.

  An ajbEntry object will return

  EntryDict = {
    'Index' : -1,
    'AJBNum' : {'volNum':-1, 'sectionNum':-1,
                'subsectionNum':-1, "entryNum":-1},
    'Authors' : [],   # array of author(s) in priority order
    'Editors' : [],   # array of editor(s)
    'Translators' : [], # array of translator(s)
    'Others' : [],    # array of other people associated with this expression
    'Title' : '',
    'Publishers' : [], # array of publishers 
    'Year' : -1,
    'Pagination' : '',
    'Price' : '',
    'Reviews' : [],
    'Comments' : '',
    }

    where Authors, Editors, Translators, and Other are lists of people.
    Each list entry will be a dictionary
         {'FirstName' : '', 
          'MiddleNames' : '',
          'LastName' : '',
          'Suffix' : '',
         }

    Publishers is also a list of dictionarys
         { 'Place' : '',
           'PublisherName' : ''
         }
"""     

#
# Parse the file of books enteries from Astronomischer Jahresbericht.
# The entries are found in the ajb??_books.txt file. Once we have the
# relevant data put the values into the database.  I don't know what the
# database final form is but is will most likely consist of data tables
# and relationship tables.
#
# created 6 July 2012
#
# usage: python ajb.py file1 [file2 [...]]
#
#   Work
#     (new or previously defined)
#     work attributes ???
#     general bibliography entries including AJB/AAA entries
#
#   Person/Corporation
#     Authors
#     Translations
#     Editors
#     Publishers
#      their relationship to the expression
#
#   Expressions
#    bibliography number (AJB num)
#    Year
#    Place
#    Pagination
#    Cost
#    Reviews
#    Relationship
#       e.g. translation, new edition, Dover release, etc.
#
# Parse comments for additional Person/Corporation
#
# To Do:
#  subsitute ',' for ' comma '
#  check authors string for editors, drop the ' ed.|comp.'
#  check comments for translators, editions, other publishers
#      reference link, languages from/to,
#  what to do about error checking?
#

import re

class AJBentry:
    """Class that manages an AJB entry and associated information

    Functions:
    __init__(line) -- creates a new, empty AJBentry with the values
          listed below as predfined in the dictionary. If line
          is present, then it will be parsed and the values
          put into the new entry.

      extract(line) -- extracts values from a text entry.

      getVal(ValueName:) -- get the value of one of the entries

      setVal("ValueName", value) -- replace an existing value or 
          add a new value.  Possibly set reference data based on
          existing data values in the database.

      version()
          return the current version number as a string
          major.minor.bugfix

      pprint()
    """

    def __init__(self, _ajbstr=None):
        """Initialize the entry dictionary with empty or null
        data structure.  If the string _ajbstr is present, try
        to parse it for data to fill entry dictionary.
        """

        self. _Version = { 'major'  : '1', 
                           'minor'  : '0',
                           'bugfix' : '0',}

        self._EntryDict = {}

        self.setval('Index', -1)

        self.setval('AJBNum',        {'volNum':-1,
                                      'sectionNum':-1,
                                      'subsectionNum':-1,
                                      "entryNum":-1} )
        self.setval( 'Authors',      [] )
        self.setval( 'Editors',      [] )
        self.setval( 'Translators',  [] )
        self.setval( 'Others',       [] )
        self.setval( 'Title',        '' )
        self.setval( 'Publishers',   [] )
        self.setval( 'Year',         -1 )
        self.setval( 'Pagination',   '' )
        self.setval( 'Price',        '' )
        self.setval( 'Reviews',      [] )
        self.setval( 'Comments',     '' )
        
        if _ajbstr :
            self.extract(_ajbstr)


    def pprint(self, stream=None, indent=1, width=80, depth=None):
        """Pretty print the entry dictionary to the stream.
        See also pprint.py for further info.
        """
        try:
            import pprint
            pprint.pprint(self._EntryDict, stream, indent, width, depth)
        except:
            None
        
        return

    def version(self):
        return "" + self._Version['major'] + "." + self._Version['minor'] + "." + self._Version['bugfix']

    def setval( self, name, value ):
        self._EntryDict[name] = value

    def getval( self, name ):
        return self._EntryDict[name]

    def extract(self, line):
        """Extract the information for a line in ajb??_books.txt and
        put the data in the _EntryDict dictionary. This function will
        return True if the line is good and false otherwise.
        """

        Place = ""
        PublisherName = ""

        #
        # This regular expression is used to check the beginning of a line
        # for an item number. If no item number is seen .
        #
        r1 = re.compile(r'\A\d+')
    
        if line and r1.match(line):
            fields = line.split(',')
            fieldNum = -1
            for field in fields :
                
                fieldNum += 1
                field = field.strip()
                field = field.replace(' comma ', ', ' )
                if 0 == fieldNum:
                    self.parseField0( field )
                    
                elif 1 == fieldNum:
                    self.setval( 'Title',  field )
                    
                elif 2 == fieldNum:
                    Place = field
                    
                elif 3 == fieldNum:
                    PublisherName = field
                    self.setval( 'Publishers', [ {'Place' : Place,
                                                   'PublisherName' : PublisherName}] )
                    
                elif 4 == fieldNum:
                    self.setval( 'Year', field )
                    
                elif 5 == fieldNum:
                    self.setval( 'Pagination', field )
                    
                elif 6 == fieldNum:
                    self.setval( 'Price', field )
                    
                elif 7 == fieldNum:
                    self.setval( 'Reviews',  field.split(' and ') )
                    
                elif 8 == fieldNum:
                    self.parseComments( field )

            return True

        else:
            return False
                    
    def parseFileIndex(self, line ):
        """
        Get the file Index value (i.e. what number is this entry
        in the file.)
        """
        self.setval( 'Index', line.strip() )

    
    def parseAJBNum(self, line ):
        """
        Get the Volume, Section, any possible subSection and the
        section entry number.  The subSection defaults to zero
        if no subSection value exists.
        """
        #
        # This regular expression is used to parse the AJB number
        # which is  of the form volNum.sectionNum[(subsectionNum)].entryNum,
        # where the subseectionNum is optional e.g. 66.18(1).25. It returns the list
        # [empty, volNum, sectionNum, string, subsectionNum, itemNum, empty].
        # Note that the subsectionNum may not be there in which case both 
        # item 3 and 4 will be NONE and the subsection number defaults to zero.
        #
        r2 = re.compile(r'(\d+)\.(\d+)(\((\d+)\))*\.(\d+)')


        nums = r2.split(line.strip())
        
        if not nums[4]:
            nums[4] = 0
            
        return {'volNum':nums[1],
                'sectionNum':nums[2],
                'subsectionNum':nums[4],
                'entryNum':nums[5],
                }

    def parseField0( self, line ) : 

        # split out the authors/editors
        fields = line.split( ' ', 2)
        
        self.parseFileIndex( fields[0] )
        
        self.setval( 'AJBNum', self.parseAJBNum( fields[1] ) )

        fields[2] = fields[2].strip()
        self.setval( 'Authors',  fields[2].split(' and ') )
        #
        # but check for editors
        #


    def parseComments( self, field ):
        self.setval( 'Comments', field )
        #
        # Look for translators, language, edition, and other publishers
        #
        










if __name__ == '__main__':

    ajbstr = '4 66.145(1).29 P. W. Hodge, The Physics comma and Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, This is a comment comma for item 4 AJBnumber 66.145(1).29'

    badajbstr = 'xxx 66.145(1).309 P. W. Hodge, The Physics comma and Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, This is a comment comma for bad item 4 AJBnumber 66.145(1).29'

    ajb1 = AJBentry()
    print "ajb.py version " + ajb1.version()
    print "The empty ajb entry looks like:"
    ajb1.pprint()


    ajb2 = AJBentry(ajbstr)
    print "ajb.py version " + ajb2.version()
    print "The good ajb entry looks like:"
    ajb2.pprint()

    ajb3 = AJBentry(badajbstr)
    print "The bad ajb entry looks like:"
    ajb3.pprint()

    print "Ajb2 still looks like:"
    ajb2.pprint()

#import fileinput
#for line in fileinput.input() : 
#   
#  line = line.strip()
        
