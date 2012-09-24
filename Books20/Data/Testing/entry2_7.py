"""Parse line entries for the books abstracted from the
Astronomische Jahrbericht series. Provides a data structure
and object class for manipulating an AJB entry.

Classes
--------
Entry()
    Provided a generic super-class for AJBentry() and AAAentry()

AJBentry( Entry )
    Takes a unicode string with comma separated fields from the
    files ajb??_books.txt and fills the Entry data

AAAentry( Entry )
    Takes a unicode string with comma separated fields from the
    files ajb??_books.txt and fills the Entry data

  An Entry data look like

  _EntryDict = {
    'Index' : -1,
    'AJBNum' : {'volume':'', 'volNum':-1, 'sectionNum':-1,
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

    where Authors, Editors, Translators, and Other are lists of class
    HumanName() from nameparser::parser.py

    Publishers is also a list of dictionarys
         { 'Place' : '',
           'PublisherName' : ''
         }

Functions
---------
No public functions are provided by this module.
"""     

# To Do:
# check comments for translators, editions, other publishers
#      reference link, languages from/to,
# consider grammer for parsing AAA
#
# what to do about error checking?
# replace pprint with __repr__
# What to do with names like A.-B. Last, parses as AB Last in nameparser
#    but should probably be A -B Last, replace ".-" with ". -" or "-"?
# get super().version to work
#

import re

class Entry(object):
    """Class that manages a generic book entry and associated information

    Functions:
      __init__(line) -- creates a new, empty entry with the values
          listed below as predfined in the dictionary. If line
          is present, then it will be parsed by the sub-class and
          the values put into the new entry.

      extract(line) -- virtual function that must be provided by sub-classes

      getVal(ValueName:) -- get the value of one of the entries

      setVal("ValueName", value) -- replace an existing value or 
          add a new value.  Possibly set reference data based on
          existing data values in the database.

      version()
          return the current version number as a string
          major.minor.bugfix

      pprint()
    """
    _Version = "class: Entry(object) v1.0.0 dtd 6 Apr 2012"
    
    def __init__(self, _entrystr=None):
        """Initialize the entry dictionary with empty or null
        data structure.  If the string _entrystr is present, try
        to parse it for data to fill entry dictionary.
        """
        self._EntryDict = {}
        self.blankEntry()
        self._Valid = False

        if _entrystr :
            self.extract(_entrystr)

    def isValid(self):
        return self._Valid


    def blankEntry(self):
        """Initialize a blank entry by setting known fields to
        null values and deleting all other fields.
        """
        keys = self._EntryDict.keys()
        for k in keys :
            del(self._EntryDict[k])
        
        self.setval('Index',         -1 )
        self.setval('Num',          {u'volNum':-1,
                                     u'sectionNum':-1,
                                     u'subsectionNum':-1,
                                     u'entryNum':-1,
                                     u'volume': ''} )
        self.setval( 'Authors',      [] )
        self.setval( 'Editors',      [] )
        self.setval( 'Translators',  [] )
        self.setval( 'Others',       [] )
        self.setval( 'Title',        u'' )
        self.setval( 'Publishers',   [] )
        self.setval( 'Year',         -1 )
        self.setval( 'Pagination',   u'' )
        self.setval( 'Price',        u'' )
        self.setval( 'Reviews',      [] )
        self.setval( 'Comments',     u'' )
        self.setval( 'OrigStr',      u'' )
        
    #
    # should change this to __repr__()


    def pprint(self, stream=None, indent=1, width=80, depth=None):
        """Pretty print the entry dictionary to the stream.
        See also pprint.py for further info.
        """
        try:
            from pprint import pprint
            pprint(self._EntryDict, stream, indent, width, depth)
        except:
            print "Unable to pretty print this entry"

        
        return

    def version(self):
        return self._Version

    def setval( self, name, value ):
        self._EntryDict[name] = value

    def getval( self, name ):
        if self._EntryDict.has_key( name ) :
            return self._EntryDict[name]
        else :
            return None

    def extract(self, line):
        assert 0, "extract() method required"


from nameparser import HumanName

class AJBentry(Entry):
    """Extract the information for a line in ajb??_books.txt and
    put the data in the _EntryDict dictionary.

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

    """
    _ajbVersion = 'class AJBentry v1.0.0 dtd 5 Aug 2012'

    def version(self):
        #supVer = super(AJBentry,self).version()
        return self._ajbVersion

    def __repr__(self) :
#         if self.unparsable:
#            return u"<%(class)s : [ Unparsable ] >" % {'class': self.__class__.__name__,}

            return u"<%(class)s : [no entry] >" % {'class': self.__class__.__name__,}



    def extract(self, line):
        Place = u""
        PublisherName = u""

        #
        # This regular expression is used to check the beginning of a line
        # for an item number, volnum and section number. If no numbers are
        # seen, then we reject the line.
        #
        r1 = re.compile(r'\A\d+ +\d+\.\d+', re.UNICODE)
    
        if line and r1.match(line):
            self.setval('OrigStr', line)
            print line
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
                    Place = u"" + field
                    
                elif 3 == fieldNum:
                    PublisherName = u"" + field
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

            self._Valid = True
            return

        else:  # not a valid line
            self._Valid = False
            return
                    
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
        r2 = re.compile(r'(\d+)\.(\d+)(\((\d+)\))*\.(\d+)', re.UNICODE)

        nums = r2.split(line.strip())
        
        if not nums[4]:
            nums[4] = 0
            
        return {'volume':u'AJB',
                'volNum':nums[1],
                'sectionNum':nums[2],
                'subsectionNum':nums[4],
                'entryNum':nums[5],
                }

    def parseField0( self, line ) : 

        fields = line.split( ' ', 2)
        
        self.parseFileIndex( fields[0] )

        self.setval( 'Num', self.parseAJBNum( fields[1] ) )

        if len(fields) > 2 :
            self.parseAuthors( fields[2].strip() )
      

    def parseAuthors(self, line ) :
      """split out the authors/editors
      """
      ed = False
      comp = False

      if line.endswith(u'ed.') :
        ed = True
        line = line.replace(u'ed.', '   ')
      elif line.endswith(u'comp.') :
        comp = True
        line = line.replace(u'comp.', '    ')

      names = self.MakeAuthorList( line )

      if ed:
        self.setval( 'Editors', names )
      elif comp :
        self.setval( 'Others', names )
      else :
        self.setval( 'Authors', names )



    def MakeAuthorList(self,  line ) :
        """Returns a list of object of class HumanName. See the package
        nameparser for full info. The names have the following possible keys
        "Title", "First", "Middle", "Last", and "Suffix"
        """
        name_list = []
        names = line.split(' and ')
        
        for name in names :
            nm = HumanName( name )
            name_list.append(nm)

        return name_list


    def MakeAuthorList2(self,  line ) :
    
        authors_list = []

        r3 = re.compile(r'[jr|III|IV]\.*', re.IGNORECASE, re.UICODE)
        
    # split into a list of names
        names = line.split(' and ')
        
        for name in names :
            name_dict = {}
            name_list = name.split()

            newname = HumanName(name)
            newauthor_list.append(newname)

            # split names into dictionary
            name_last = name_list[-1].strip()
            if r3.match(name_last) :
                name_dict['Suffix'] = name_last
                del name_list[-1]
                
            if len(name_list) < 1 :
                assert 0, "Oops, no more names left"
                    
            #
            # Assume at least a last name. The syntax for AJB and my entries
            # are A. B. Lastname. Only the first and middle initials have a 
            # period in them. So we search and append names until a period
            # is found.
            #
            lastname = ""
            while -1 == name_list[-1].find( "." ) :
                lastname = name_list[-1].strip() + " " + lastname
                del name_list[-1]
            name_dict['Last'] = lastname.strip()
                
                
            # get first name
            if len(name_list) > 0 :
                name_dict['First'] = name_list[0].strip()
                del name_list[0]
                        
            # the rest must be middle names
            middle_name = ""
            for nm in name_list :
                middle_name = middle_name + " " + nm.strip() 
                
            if middle_name :
                name_dict['Middle'] = middle_name
                    
            # append to the author list
            authors_list.append(name_dict)

        print newauthor_list
        return authors_list

    def parseComments( self, field ):
        self.setval( 'Comments', field )
        #
        # Look for translators, language, edition, and other publishers
        #
        


    def numStr(self):
        """Return a stringfied version of the Num entry
        """
        a = self.getval('Num')
        if a:
            st = '' + a['volume'] + ' ' + a['volNum'] + '.'  +a['sectionNum']
            if a['subsectionNum']:
                st = st + '(' + a['subsectionNum'] + ')'
            st = st + '.' + a['entryNum']
            return st
        else:
            return None





if __name__ == '__main__':

    ajbstr = '4 66.145(1).29 P. W. Hodge, The Physics comma and Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, This is a comment comma for item 4 AJBnumber 66.145(1).29'

    authorstr = '4 66.145(1).29 P. W. Hodge and I. A. Author and A. N. Other, The Physics comma and Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, This is a comment comma for item 4 AJBnumber 66.145(1).29'

    editorstr = '4 66.145.29 P.-W. Hodge jr. and I. A. Author III and A. Other and A. V. de la Name ed., The Physics comma and Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, This is a comment comma for item 4 AJBnumber 66.145(1).29'


    badajbstr = 'xxx 66.145(1).309 P. W. Hodge, The Physics comma and Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, This is a comment comma for bad item 4 AJBnumber 66.145(1).29'

    try:
      badentry = Entry(ajbstr)
    except:
      print "entry() class fails properly with no extract method."
      
    ajb1 = AJBentry()
    print "\najb.py version " + ajb1.version()
    print 'The empty ajb entry isValid() is %d and looks like:' % ajb1.isValid()
    #ajb1.pprint()


    ajb2 = AJBentry(ajbstr)
    print "\najb.py version " + ajb2.version()
    print 'The good ajb entry isValid() is %d and looks like:' % ajb2.isValid()
    #ajb2.pprint()

    ajb3 = AJBentry(badajbstr)
    print '\nThe bad ajb entry isValid() is %d and looks like:' % ajb3.isValid()
    #ajb3.pprint()

    authorajb = AJBentry(authorstr)
    print '\nThe author ajb entry isValid() is %d and looks like:' % authorajb.isValid()
    #authorajb.pprint()

    editorajb = AJBentry(editorstr)
    print '\nThe editor ajb entry isValid() is %d and looks like:' % editorajb.isValid()
    editorajb.pprint()

    print editorajb.numStr()
    eds = editorajb.getval('Editors')
    print eds[0].full_name



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
