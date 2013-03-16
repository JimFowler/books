import re

from nameparser import HumanName

from bookentry.entry import *
from bookentry.AJBcomments import *


__ajbVersion__ = 'class AJBentry(Entry) v1.0.0 dtd 5 Aug 2012'

class AJBentry(Entry):

    """Read the information from a string and put the data in the
    AJBentry dictionary. The entry is valid if there was a valid AJB
    number (vol.section.index) and a title.

    A line looks like:

    Index AJB_Num Author, Title, Place, Publisher, Year, \
    Pagination, Price, Reviews, Comments
    
    No field need be present except Index, AJB_Num, and Title.
    
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

       [n+nnn [and nn+nnn [and ...] pp]]

    Field 8 Reviews

       [Journal vol page [and Journal vol page [and ...]]]

    Field 9 Comment
     
       See AJBcomments.py for a description of the comments grammer

    """

    def version(self):
        return __ajbVersion__ + ": " + super(AJBentry, self).version()

    def numStr(self):
        """Return a stringfied version of the Num entry,
        ex. 'AJB 68.01(0).20'
        """
        a = self['Num']
        if a:
            st = str(a['volume'])
            st = st + ' ' + '%02d'%a['volNum']
            st = st + '.' + '%02d'%a['sectionNum']
            if a['subsectionNum'] > -1:
                st = st + '(' + str(a['subsectionNum']) + ')'
            st = st + '.' + '%02d'%a['entryNum']
            return st
        else:
            return None

    def isValid(self):
        """AJB entries are valid if they have a valid AJB num
        and a Title."""
        if self.isValidAjbNum() and self['Title'] != '':
            return True
        else:
            return False

    def notEmpty(self, key ):
        """Return the truth value of, 'key' existing
        in the entry and the key value is not empty."""
        if self.__contains__(key) and self[key]:
            return True
        return False

    def write(self):
        """Write an AJBentry back into the string format that it came from.
        It should be the case that write(read(ajbstr)) == ajbstr up to
        the order of the comments and that read(write(ajbent)) == ajbent."""

        if not self.isValid():
            return ''

        entryStr = self.numStr()[4:] + ' '

        if self.notEmpty('Authors'):
            entryStr +=  self._makeNameStr(self['Authors'])
        elif self.notEmpty('Editors'):
            entryStr +=  self._makeNameStr(self['Editors'])
            entryStr += ' ed.'

        entryStr = entryStr + ', ' + self['Title'].replace(', ', ' comma ' )

        if self.notEmpty('Publishers'):
            entryStr += ', '
            if self['Publishers'][0]['Place']:
                entryStr += self['Publishers'][0]['Place']

            entryStr += ', '
            if self['Publishers'][0]['PublisherName']:
                nm =  self['Publishers'][0]['PublisherName']
                nm = nm.replace(', ', ' comma ' )
                entryStr += nm
        else:
            entryStr += ', , '

        entryStr += ', '
        if self.notEmpty('Year'):
            entryStr += str(self['Year'])

        entryStr += ', '
        if self.notEmpty('Pagination'):
            entryStr += str(self['Pagination'])

        entryStr += ', '
        if self.notEmpty('Price'):
            entryStr += str(self['Price'])

        entryStr += ', '
        if self.notEmpty('Reviews'):
            first = True
            for r in self['Reviews']: 
                if not first:
                    entryStr += ' and '
                first = False
                entryStr += r

        # comments
        entryStr += ', '
        if self.notEmpty('Edition'):
            entryStr += str(self['Edition'])
            num = int(self['Edition'])
            if  num == 1:
                entryStr += 'st'
            elif num == 2:
                entryStr += 'nd'
            elif num == 3:
                entryStr += 'rd'
            else:
                entryStr += 'th'
            entryStr += ' edition;'

        if self.notEmpty('Reprint'):
            entryStr += 'reprint of '
            entryStr += str(self['Reprint'])
            entryStr += ';'

        if self.notEmpty('Compilers'):
            entryStr += 'compiled by '
            entryStr += self._makeNameStr(self['Compilers'])
            entryStr += ';'


        if self.notEmpty('Contributors'):
            entryStr += 'contributors '
            entryStr += self._makeNameStr(self['Contributors'])
            entryStr += ';'

        # translated from by
        if self.notEmpty('Translators') or self.notEmpty('TranslatedFrom'):
            entryStr += 'translated '
            if self.notEmpty('TranslatedFrom'):
                entryStr += 'from '
                entryStr += self['TranslatedFrom']
            if self.notEmpty('Translators'):
                entryStr += ' by '
                entryStr += self._makeNameStr(self['Translators'])
            entryStr += ';'

        # additional editors
        if self.notEmpty('Authors') and self.notEmpty('Editors'):
            # need to include editors in comments
            entryStr += 'edited by '
            entryStr += self._makeNameStr(self['Editors'])
            entryStr += ';'

        # additional publishers
        if self['Publishers'].__len__() > 1:
            extraPubl = self['Publishers'][1:]
            entryStr += 'also published '
            first = True
            for p in extraPubl:
                if not first:
                    entryStr += ' and '
                first = False
                entryStr += '%s: %s' % (p['Place'].replace(', ', ' comma '), p['PublisherName'].replace(', ', ' comma '))
            entryStr += ';'

        if self.notEmpty('Language'):
            entryStr += 'in '
            entryStr += self['Language']
            entryStr += ';'

        # others
        if self.notEmpty('Others'):
            for p in self['Others']:
                entryStr += 'other %s' % str(p).replace(', ', ' comma ')
                entryStr += '; '

        if self.notEmpty('Reference'):
            entryStr += 'reference '
            entryStr += self['Reference']
            entryStr += ';'


        return entryStr

    def read(self, line):
        """Parse a line with an AJB entry in it placing the values in the
        Entry dictionary. Returns True if this is a parsable line and 
        false if it is not."""
 
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
                field = field.replace(' comma ', ', ' )
                field = field.strip()
                if 0 == fieldNum:  # AJBnum and Authors
                    self._parseField0( field )
                    
                elif 1 == fieldNum:  # Title
                    self['Title'] =  field 
                    
                elif 2 == fieldNum:  # place of publication
                    Place = "" + field
                    
                elif 3 == fieldNum:  # Publisher
                    PublisherName = "" + field
                    self['Publishers'] = [ {'Place' : Place,
                                             'PublisherName' : PublisherName}]
                    
                elif 4 == fieldNum:   # Publication Year
                    self['Year'] = field
                    
                elif 5 == fieldNum:   # Page Count
                    self['Pagination'] = field 
                    
                elif 6 == fieldNum:   # Price
                    self['Price'] = field 
                    
                elif 7 == fieldNum:   # Reviews
                    self['Reviews'] = field.split(' and ') 

                elif 8 == fieldNum:   # Comments and other material
                    self['Comments'] = field
                    self._parseComments( field )
                    continue

            return True

        else:  # not if line and r1.match(line)
            return False

    def isValidAjbNum(self):
        """A valid AJB number has a volume number between 1-68
        and a section number between 1-150
        and an entry number > 0"""
        num = self['Num']
        if num['volNum'] > 0 and num['volNum'] < 69 \
        and num['sectionNum'] > 0 and num['sectionNum'] < 150 \
        and num['entryNum'] > 0:
            return True
        else:
            return False


        
    #
    # Private functions
    #
    def _parseField0( self, line ) : 

        fields = line.split( ' ', 2)
        
        self._parseFileIndex( fields[0] )

        self['Num'] = self._parseAJBNum( fields[1] )

        if len(fields) > 2 :
            self._parseAuthors( fields[2].strip() )
      

                    
    def _parseFileIndex(self, line ):
        """
        Get the file Index value (i.e. what number is this entry
        in the file.)
        """
        self['Index'] = line.strip()

    
    def _parseAJBNum(self, line ):
        """Get the Volume, Section, any possible subSection, and the
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
            nums[4] = 0 # or -1 for invalid???
            
        return {'volume':'AJB',
                'volNum': int(nums[1]),
                'sectionNum': int(nums[2]),
                'subsectionNum': int(nums[4]),
                'entryNum': int(nums[5]),
                }


    def _parseAuthors(self, line ) :
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

      names = self._makeNameList( line )

      if ed:
        self['Editors'] = names
      elif comp :
        self['Compilers'] = names
      else :
        self['Authors'] = names



    def _makeNameList(self,  line ) :
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

    def _makeNameStr( self, namelist):
        """Returns a string built from a list of HumanName objects.
        See the package nameparser for details about HumanName.
        """

        nameStr = ''
        if not namelist:
            return nameStr

        first = True
        for nm in namelist:
            if not first:
                nameStr += ' and '
            first = False
            nameStr += nm.full_name

        return nameStr


    def _parseComments( self, field ):
        
        cParser = Comment.parser()
        result = cParser.parse_string(field, reset=True)
        #
        # Look for translators, language, edition, and other publishers
        #
        if result:
            while result:
                grmName = result.elements[0].grammar_name
                if 'Edition' ==  grmName:
                    self['Edition'] = result.elements[0].edition_num

                elif 'Reference' == grmName:
                    self['Reference'] = str(result.find(AJBNum)).strip()

                elif 'Reprint' == grmName:
                    tmp = result.find(AJBNum)
                    if tmp:
                        self['Reprint'] = str(tmp).strip()
                    tmp = result.find(Year)
                    if tmp:
                        self['Reprint'] = str(tmp).strip()

                elif 'Editors' == grmName:
                    line = str(result.find(NameList))
                    nm = self._makeNameList( line )
                    if self.notEmpty('Editors'):
                        self['Editors'].extend( nm )
                    else:
                        self['Editors'] = nm

                elif 'Contributors' == grmName:
                    line = str(result.find(NameList))
                    nm = self._makeNameList( line )
                    if self.notEmpty('Contributors'):
                        self['Contributors'].extend( nm )
                    else:
                        self['Contributors'] = nm

                elif 'Compilers' == grmName:
                    line = str(result.find(NameList))
                    nm = self._makeNameList( line )
                    if self.notEmpty('Compilers'):
                        self['Compilers'].extend( nm )
                    else:
                        self['Compilers'] = nm

                elif 'Translation' == grmName :
                    tmp = result.find(FromLanguage)
                    if tmp:
                        self['TranslatedFrom'] = str(tmp.elements[1]).strip()

                    tmp = result.find(ToLanguage)
                    if tmp:
                        self['Language'] = str(tmp.elements[1]).strip()

                    tmp = result.find(NameList)
                    if tmp:
                        nm = self._makeNameList(str(tmp))
                        if self.notEmpty('Translators'):
                            self['Translators'].extend( nm )
                        else:
                            self['Translators'] = nm 

                elif 'Publishers' == grmName:
                    tmp = str(result.find(PublisherList))
                    # the space chars in the split avoids problems with 
                    # e.g. Rand McNally & Sons
                    list = tmp.split(' and ')
                    for l in list:
                        p = l.split(':')
                        self['Publishers'].append( {'Place' : p[0].strip(),
                                                    'PublisherName': p[1].strip()})

                elif 'Language' == grmName:
                    self['Language'] = str(result.find(uWord)).strip()

                elif 'Other' == grmName:
                    nm = str(result.find(uWords)).strip()
                    if not self.notEmpty('Others'):
                        self['Others'] = []
                    self['Others'].append( nm )

                else:
                    print('Unknown grammer name %s' % grmName)

                result = cParser.parse_string('')








if __name__ == '__main__':

    ajbstr = '4 66.145(1).29 P. W. Hodge, The Physics comma and Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other This is the ajbstr9;'

    authorstr = '4 66.145(1).29 P. W. Hodge and I. A. Author and A. N. Other, The Physics comma and Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other This is the authorstr;'

    editorstr = '4 66.145.29 P.-W. Hodge jr. and I. A. Author III and A. Other and A. V. de la Name ed., The Physics comma and Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other a first comment; edited by A. B. Name; translated from Italian into English by A. Trans; also published London: A Publishing Co.; other This is the editor string;'

    allfieldsstr = '4 66.145.29 P.-W. Hodge jr. and I. A. Author III and A. Other and A. V. de la Name, The Physics comma and Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other a first comment; 3rd edition; edited by A. B. Name; translated from Italian into English by A. Trans; also published London: A Publishing Co.; other This is the editor string; contributors A. B. Contrib; compiled by A. B. Compiler; in Frenchh; reprint of AJB 59.03.05; reprint of 1956; reference AJB 59.144.55;'

    allfieldsstr2 = '4 66.145.29 P.-W. Hodge jr. and I. A. Author III and A. Other and A. V. de la Name, The Physics comma and Astronomy of Galaxies and Cosmology, , , , , , Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, reference AJB 59.144.55'


    badajbstr = '27 xx.145(1).309 P. W. Hodge, The Physics comma and Astronomy of Galaxies and Cosmology , New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other This is the badstr;'

    badtitlestr = '27 66.145(1).309 P. W. Hodge, , New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other This is the badstr;'

    try:
        from pprint import pprint
    except:
        print('Pretty Print module unavailable')
        pprint = print


    try:
      badentry = Entry(ajbstr)
    except:
      print("Entry() class fails properly with no read() method.")
      
    allfieldajb = AJBentry(allfieldsstr)
    print('\nThe all fields ajb entry isValid() is %d and looks like:' % allfieldajb.isValid())
    pprint(allfieldajb)



def notest():
    ajb1 = AJBentry()
    print("\najb.py version:: %s \n" % ajb1.version())
    print('The empty ajb entry isValid() is %d and looks like:' % ajb1.isValid())
    pprint(ajb1)

    ajb2 = AJBentry(ajbstr)
    print("\najb.py version " + ajb2.version())
    print('The good ajb entry isValid() is %d and looks like:' % ajb2.isValid())
    pprint(ajb2)

    ajb3 = AJBentry(badajbstr)
    print('\nThe bad ajb entry isValid() is %d and looks like:' % ajb3.isValid())
    pprint(ajb3)

    ajb4 = AJBentry(badtitlestr)
    print('\nThe bad title ajb entry isValid() is %d and looks like:' % ajb4.isValid())
    pprint(ajb4)

    authorajb = AJBentry(authorstr)
    print('\nThe author ajb entry isValid() is %d and looks like:' % authorajb.isValid())
    pprint(authorajb)

    editorajb = AJBentry(editorstr)
    print('\nThe editor ajb entry isValid() is %d and looks like:' % editorajb.isValid())
    pprint(editorajb)

    #print(editorajb.numStr())
    #eds = editorajb['Editors']
    #print(eds[0].full_name)


