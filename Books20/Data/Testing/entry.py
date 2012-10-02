""" An entry class based on dict
"""

class Entry(dict):
    def __init__(self, _entrystr=None):
        self._entryVersion = "class: Entry(dict) v1.0.0 dtd 27 Sep 2012"
        self._Valid = False

        self.blankEntry()

        if(_entrystr):
            self.extract(_entrystr)

    def isValid(self):
        return self._Valid

    def version(self):
        return self._entryVersion

    def blankEntry(self):
        """Initialize a blank entry by setting known fields to
        null values and deleting all other fields.
        """
        keys = list(self.keys())
        for k in keys :
            del(self[k])

        self['Index'] =       -1
        self['Num'] =         {'volNum':-1,
                               'sectionNum':-1,
                               'subsectionNum':-1,
                               'entryNum':-1,
                               'volume': ''}
        self[ 'Authors'] =    []
        self[ 'Editors'] =    []
        self[ 'Translators']= []
        self[ 'Others'] =     []
        self[ 'Title'] =      ''
        self[ 'Publishers'] = []
        self[ 'Year'] =       -1
        self[ 'Pagination'] = ''
        self[ 'Price'] =      ''
        self[ 'Reviews'] =    []
        self[ 'Comments'] =   ''
        self[ 'OrigStr'] =    ''

    def extract(self, line):
        assert 0, "extract() method required"


import re
from AJBcomments import *
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
    _ajbVersion = 'class AJBentry(Entry) v1.0.0 dtd 5 Aug 2012'

    def version(self):
        return self._ajbVersion + " " + self._entryVersion


    def extract(self, line):
        Place = ""
        PublisherName = ""

        #
        # This regular expression is used to check the beginning of a line
        # for an item number, volnum and section number. If no numbers are
        # seen, then we reject the line.
        #
        r1 = re.compile(r'\A\d+ +\d+\.\d+', re.UNICODE)
    
        if line and r1.match(line):
            self['OrigStr'] = line
            #print(line)
            fields = line.split(',')
            fieldNum = -1
            for field in fields :
                
                fieldNum += 1
                field = field.strip()
                field = field.replace(' comma ', ', ' )
                if 0 == fieldNum:
                    self.parseField0( field )
                    
                elif 1 == fieldNum:
                    self['Title'] =  field 
                    
                elif 2 == fieldNum:
                    Place = "" + field
                    
                elif 3 == fieldNum:
                    PublisherName = "" + field
                    self['Publishers'] = [ {'Place' : Place,
                                             'PublisherName' : PublisherName}]
                    
                elif 4 == fieldNum:
                    self['Year'] = field
                    
                elif 5 == fieldNum:
                    self['Pagination'] = field 
                    
                elif 6 == fieldNum:
                    self['Price'] = field 
                    
                elif 7 == fieldNum:
                    self['Reviews'] = field.split(' and ') 
                    
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
        self['Index'] = line.strip()

    
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
            
        return {'volume':'AJB',
                'volNum':nums[1],
                'sectionNum':nums[2],
                'subsectionNum':nums[4],
                'entryNum':nums[5],
                }

    def parseField0( self, line ) : 

        fields = line.split( ' ', 2)
        
        self.parseFileIndex( fields[0] )

        self['Num'] = self.parseAJBNum( fields[1] )

        if len(fields) > 2 :
            self.parseAuthors( fields[2].strip() )
      

    def parseAuthors(self, line ) :
      """split out the authors/editors
      """
      ed = False
      comp = False

      if line.endswith('ed.') :
        ed = True
        line = line.replace('ed.', '   ')
      elif line.endswith('comp.') :
        comp = True
        line = line.replace('comp.', '    ')

      names = self.MakeNameList( line )

      if ed:
        self['Editors'] = names
      elif comp :
        self['Compilers'] = names
      else :
        self['Authors'] = names



    def MakeNameList(self,  line ) :
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

    def parseComments( self, field ):
        

        cParser = Comment.parser()
        result = cParser.parse_string(field, reset=True)
        #
        # Look for translators, language, edition, and other publishers
        #
        if result:
            self['Comments'] = 'Good  ' + field



    def numStr(self):
        """Return a stringfied version of the Num entry
        """
        a = self['Num']
        if a:
            st = '' + a['volume'] + ' ' + a['volNum'] + '.'  +a['sectionNum']
            if a['subsectionNum']:
                st = st + '(' + a['subsectionNum'] + ')'
            st = st + '.' + a['entryNum']
            return st
        else:
            return None





if __name__ == '__main__':

    ajbstr = '4 66.145(1).29 P. W. Hodge, The Physics comma and Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other This is a comment for item 4 AJBnumber 66.145(1).29;'

    authorstr = '4 66.145(1).29 P. W. Hodge and I. A. Author and A. N. Other, The Physics comma and Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, otherThis is a comment or item 4 AJBnumber 66.145(1).29;'

    editorstr = '4 66.145.29 P.-W. Hodge jr. and I. A. Author III and A. Other and A. V. de la Name ed., The Physics comma and Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, This is a comment or item 4 AJBnumber 66.145(1).29'


    badajbstr = 'xxx 66.145(1).309 P. W. Hodge, The Physics comma and Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other This is a comment for bad item 4 AJBnumber 66.145(1).29;'

    try:
        from pprint import pprint
    except:
        print('Pretty Print module unavailable')
        pprint = print


    try:
      badentry = Entry(ajbstr)
    except:
      print("Entry() class fails properly with no extract method.")
      
    ajb1 = AJBentry()
    print("\najb.py version " + ajb1.version())
    print('The empty ajb entry isValid() is %d and looks like:' % ajb1.isValid())
    pprint(ajb1)


    ajb2 = AJBentry(ajbstr)
    print("\najb.py version " + ajb2.version())
    print('The good ajb entry isValid() is %d and looks like:' % ajb2.isValid())
    pprint(ajb2)

    ajb3 = AJBentry(badajbstr)
    print('\nThe bad ajb entry isValid() is %d and looks like:' % ajb3.isValid())
    pprint(ajb3)

    authorajb = AJBentry(authorstr)
    print('\nThe author ajb entry isValid() is %d and looks like:' % authorajb.isValid())
    pprint(authorajb)

    editorajb = AJBentry(editorstr)
    print('\nThe editor ajb entry isValid() is %d and looks like:' % editorajb.isValid())
    pprint(editorajb)

    print(editorajb.numStr())
    eds = editorajb['Editors']
    print(eds[0].full_name)


