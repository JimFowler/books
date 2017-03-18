"""AJBentry provides a class which can convert between a unicode text
entry and a representation in python, typically a dictionary entry of
the form Entry.py.entry()."""
# -*- coding: UTF-8 -*-
# -*- mode: Python;-*-


from nameparser import HumanName
import re
from lxml import etree

import bookentry.entry as entry
import bookentry.AJBcomments as comments
import bookentry.utils as utils

__ajbVersion__ = 'class AJBentry(Entry) v1.0.0 dtd 5 Aug 2012'

class AJBentry(entry.Entry):

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
            st = st + '%1s'%a['entrySuf']
            return st
        else:
            return None

    def shortTitle(self):
        """Create a short title string for the entry. A short title
        is 'AJBnum 1stAuthor_lastname Title'."""
        st = self.numStr() + ' '
        if self.notEmpty('Authors'):
            name = self['Authors'][0].last
        elif self.notEmpty('Editors'):
            name = self['Editors'][0].last
        else:
            name = 'noAuthor'

        st = st + name + ', ' + self['Title'] + '\n'
        return st

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

    #
    # Ascii comma separated variable file, read/write functions
    #
    def write_Text_from_Entry(self):
        """Write an AJBentry back into the string format that it came from.
        It should be the case that write(read(ajbstr)) == ajbstr up to
        the order of the comments and that read(write(ajbent)) == ajbent."""

        if not self.isValid():
            return ''

        entryStr = self.numStr()[4:] + ' '

        if self.notEmpty('Authors'):
            entryStr +=  utils.makeNameStr(self['Authors'])
        elif self.notEmpty('Editors'):
            entryStr +=  utils.makeNameStr(self['Editors'])
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
            entryStr += utils.makeNameStr(self['Compilers'])
            entryStr += ';'


        if self.notEmpty('Contributors'):
            entryStr += 'contributors '
            entryStr += utils.makeNameStr(self['Contributors'])
            entryStr += ';'

        # translated from by
        if self.notEmpty('Translators') or self.notEmpty('TranslatedFrom'):
            entryStr += 'translated '
            if self.notEmpty('TranslatedFrom'):
                entryStr += 'from '
                entryStr += self['TranslatedFrom']
            if self.notEmpty('Translators'):
                entryStr += ' by '
                entryStr += utils.makeNameStr(self['Translators'])
            entryStr += ';'

        # additional editors
        if self.notEmpty('Authors') and self.notEmpty('Editors'):
            # need to include editors in comments
            entryStr += 'edited by '
            entryStr += utils.makeNameStr(self['Editors'])
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

    def read_Text_to_Entry(self, line):
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
            for field in fields:
                
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
                    if 0 < len(field):
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
        and num['entryNum'] > 0 \
        and (num['entrySuf'] == '' or num['entrySuf'] == 'a' \
                 or num['entrySuf'] == 'b' or num['entrySuf'] == 'c'):
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
        if no subSection value exists. Returns a dictionary with the 
        AJB number elements {'volume': 'AJB', 'volNum': int, 'sectionNum': int,
        'subsectionNum': int, 'entryNum': int, 'entrySuf': ''}.
        """
        #
        # This regular expression is used to parse the AJB number
        # which is of the form
        # [AJB ]volNum.sectionNum[(subsectionNum)].entryNum[entrySuf], where
        # the AJB, subsectionNum, and entrySuf are optional
        # e.g. 66.18(1).25a. It returns the list [empty, empty, 66,
        # 18, (1), 1, 25, 'a', empty].  Note
        # that the subsectionNum may not be there in which case both
        # item 4 and 5 will be empty strings and the subsection number defaults
        # to zero.
        #
        r2 = re.compile(r'([AJB]{0,1})(\d+)\.(\d+)(\((\d+)\))*\.(\d+)([a-c]{0,1})', re.UNICODE)

        nums = r2.split(line.strip())

        if not nums[0]: # volume
            nums[0] ='AJB'

        if not nums[5]: # subsectionNum
            nums[5] = 0 
            
        if not nums[7]: # entrySuf
            nums[7] = ''

        return {'volume': nums[0],
                'volNum': int(nums[2]),
                'sectionNum': int(nums[3]),
                'subsectionNum': int(nums[5]),
                'entryNum': int(nums[6]),
                'entrySuf': nums[7],
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

      names = utils.makeNameList( line )

      if ed:
        self['Editors'] = names
      elif comp :
        self['Compilers'] = names
      else :
        self['Authors'] = names





    def _parseComments( self, field ):
        
        cParser = comments.Comment.parser()
        results = cParser.parse_text(field, reset=True, multi=True)
        #
        # Look for translators, language, edition, and other publishers
        #
        if results:
             for result in results:
                grmName = result.elements[0].grammar_name
                if 'Edition' ==  grmName:
                    self['Edition'] = result.elements[0].edition_num

                elif 'Reference' == grmName:
                    self['Reference'] = str(result.find(comments.AJBNum)).strip()

                elif 'Reprint' == grmName:
                    tmp = result.find(comments.AJBNum)
                    if tmp:
                        self['Reprint'] = str(tmp).strip()
                    tmp = result.find(comments.Year)
                    if tmp:
                        self['Reprint'] = str(tmp).strip()

                elif 'Editors' == grmName:
                    line = str(result.find(comments.NameList))
                    nm = utils.makeNameList( line )
                    if self.notEmpty('Editors'):
                        self['Editors'].extend( nm )
                    else:
                        self['Editors'] = nm

                elif 'Contributors' == grmName:
                    line = str(result.find(comments.NameList))
                    nm = utils.makeNameList( line )
                    if self.notEmpty('Contributors'):
                        self['Contributors'].extend( nm )
                    else:
                        self['Contributors'] = nm

                elif 'Compilers' == grmName:
                    line = str(result.find(comments.NameList))
                    nm = utils.makeNameList( line )
                    if self.notEmpty('Compilers'):
                        self['Compilers'].extend( nm )
                    else:
                        self['Compilers'] = nm

                elif 'Translation' == grmName :
                    tmp = result.find(comments.FromLanguage)
                    if tmp:
                        self['TranslatedFrom'] = str(tmp.elements[1]).strip()

                    tmp = result.find(comments.ToLanguage)
                    if tmp:
                        self['Language'] = str(tmp.elements[1]).strip()

                    tmp = result.find(comments.NameList)
                    if tmp:
                        nm = utils.makeNameList(str(tmp))
                        if self.notEmpty('Translators'):
                            self['Translators'].extend( nm )
                        else:
                            self['Translators'] = nm 

                elif 'Publishers' == grmName:
                    tmp = str(result.find(comments.PublisherList))
                    # the space chars in the split avoids problems with 
                    # e.g. Rand McNally & Sons
                    list = tmp.split(' and ')
                    for l in list:
                        p = l.split(':')
                        self['Publishers'].append( {'Place' : p[0].strip(),
                                                    'PublisherName': p[1].strip()})

                elif 'Language' == grmName:
                    self['Language'] = str(result.find(comments.uWord)).strip()

                elif 'Other' == grmName:
                    nm = str(result.find(comments.uWords)).strip()
                    if not self.notEmpty('Others'):
                        self['Others'] = []
                    self['Others'].append( nm )

                else:
                    print('Unknown grammer name %s' % grmName)

    #
    # XML create routines
    #
    def write_XML_from_Entry(self):
        '''Create an XML etree element with the root tag Entry from
        the entry.'''

        if not self.isValid:
            return None

        # Title and Index are required of any entry
        entryXML = etree.Element('Entry')
    
        a = self['Num']
        entryXML.append(self.makeAJBNum_XML(a))
        
        el = etree.SubElement(entryXML, 'Title')
        el.text = self['Title']

        # This ends the required elements.  All further elements
        # may be missing or blank.
        
        if self.notEmpty('subTitle'):
            el = etree.SubElement(entryXML, 'SubTitle')
            el.text = self['subTitle']

        # Create the people list, right now these lists are
        # only HumanNames but we need to add business names
        # in the future.
        if 0 < len(self['Authors']):
            el = etree.SubElement(entryXML, 'Authors')
            for author in self['Authors']:
                al = etree.SubElement(el, 'Author')
                # all authors are humannames right now.
                ae = self.makePerson_XML(author)
                al.append(ae)

        if 0 < len(self['Editors']):
            el = etree.SubElement(entryXML, 'Editors')
            for editor in self['Editors']:
                al = etree.SubElement(el, 'Editor')
                # all authors are humannames right now.
                ae = self.makePerson_XML(editor)
                al.append(ae)

        if 0 < len(self['Publishers']):
            el = etree.SubElement(entryXML, 'Publishers')
            for publ in self['Publishers']:
                ep = etree.SubElement(el, 'Publisher')
                epp = etree.Element('Place')
                epp.text = publ['Place']
                ep.append(epp)

                epn = etree.Element('Name')
                epn.text = publ['PublisherName']
                ep.append(epn)

        if self.notEmpty('Year'):
            el = etree.SubElement(entryXML, 'Year')
            el.text = str(self['Year'])

        if self.notEmpty('Edition'):
            el = etree.SubElement(entryXML, 'Edition')
            el.text = str(self['Edition'])

        if self.notEmpty('Pagination'):
            el = etree.SubElement(entryXML, 'Pagination')
            el.text = str(self['Pagination'])

        # The schema defines a price with currency and value
        # but we need to do some intellegent parsing of the prices
        # before we can use this.  For now we just naively use
        # the string.
        if self.notEmpty('Price'):
            el = etree.SubElement(entryXML, 'Prices')
            for price in self['Price'].split(' and '):
                ep = etree.SubElement(el, 'Price')
                ep.text = price

        if 0 < len(self['Reviews']):
            el = etree.SubElement(entryXML, 'Reviews')
            for rev in self['Reviews']:
                er = etree.SubElement(el, 'Review')
                er.text = str(rev)

        if self.notEmpty('TranslatedFrom'):
            el = etree.SubElement(entryXML, 'TranslatedFrom')
            el.text = str(self['TranslatedFrom'])

        if self.notEmpty('Language'):
            el = etree.SubElement(entryXML, 'Language')
            el.text = str(self['Language'])

        if 0 < len(self['Translators']):
            el = etree.SubElement(entryXML, 'Translators')
            for trans in self['Translators']:
                al = etree.SubElement(el, 'Translator')
                # all translators are humannames right now.
                ae = self.makePerson_XML(trans)
                al.append(ae)

        if 0 < len(self['Compilers']):
            el = etree.SubElement(entryXML, 'Compilers')
            for compiler in self['Compilers']:
                al = etree.SubElement(el, 'Compiler')
                # all compilers are humannames right now.
                ae = self.makePerson_XML(compiler)
                al.append(ae)

        if 0 < len(self['Contributors']):
            el = etree.SubElement(entryXML, 'Contributors')
            for contrib in self['Contributors']:
                al = etree.SubElement(el, 'Contributor')
                # all contributors are humannames right now.
                ae = self.makePerson_XML(contrib)
                al.append(ae)

        # Sometimes the reprint can be just a year number rather than
        # an AJBnum.  An AJBnum should have decimal points in it and
        # Years should not, so we look for a decimal point to determine
        # which it is.
        if self.notEmpty('Reprint'):
            el = etree.SubElement(entryXML, 'ReprintOf')
            if 1 == len(self['Reprint'].split('.')):
                # Must be a year
                ey = etree.SubElement(el, 'Year')
                ey.text = self['Reprint']
            else:
                numDict = self._parseAJBNum(self['Reprint'])
                ei = self.makeAJBNum_XML(numDict)
                el.append(ei)

        if self.notEmpty('Reference'):
            el = etree.SubElement(entryXML, 'ReferenceOf')
            numDict = self._parseAJBNum(self['Reference'])
            aj = self.makeAJBNum_XML(numDict)
            el.append(aj)
            

        if 0 < len(self['Others']):
            el = etree.SubElement(entryXML, 'Comments')
            for comment in self['Others']:
                cl = etree.SubElement(el, 'Comment')
                cl.text = comment

        # return the root Entry element
        return entryXML


    def makeAJBNum_XML(self, ajbnum):
        '''Write an XML version of an AJB number as an index
        element. The index argument must be a dictionary'''
        index_XML = etree.Element('Index')
        el = etree.SubElement(index_XML, 'IndexName')
        el.text = str(ajbnum['volume']).strip()
        el = etree.SubElement(index_XML, 'VolumeNumber')
        el.text = str(ajbnum['volNum'])
        el = etree.SubElement(index_XML, 'SectionNumber')
        el.text = str(ajbnum['sectionNum'])
        el = etree.SubElement(index_XML, 'SubSectionNumber')
        el.text = str(ajbnum['subsectionNum'])
        el = etree.SubElement(index_XML, 'EntryNumber')
        el.text = str(ajbnum['entryNum']) + ajbnum['entrySuf']
    
        return index_XML


    def makePerson_XML(self, nm):
        '''Create a Person element from a HumanName object. Returns the
        Person element.'''

        person_XML = etree.Element('Person')

        if nm.title:
            el = etree.SubElement(person_XML, 'Prefix')
            el.text = nm.title
            
        if nm.first:
            el = etree.SubElement(person_XML, 'First')
            el.text = nm.first

        if nm.middle:
            el = etree.SubElement(person_XML, 'Middle')
            el.text = nm.middle

        if nm.last:
            el = etree.SubElement(person_XML, 'Last')
            el.text = nm.last

        if nm.suffix:
            el = etree.SubElement(person_XML, 'Suffix')
            el.text = nm.suffix

        return person_XML


    def read_XML_to_Entry(self, elXML):
        '''Parse an XML element of an Entry and place the information
        into the AJBentry dictionary. This is a bit tricky.  XML entries
        contain more information than the AJBentry does.'''

        r2 = re.compile(r'([0-9]+)([A-Za-z]*)', re.ASCII)
        for child in elXML:
            #print('child is ', child.tag)

            if child.tag == 'Index':
                for el in child:
                    if el.tag == 'IndexName':
                        self['Num']['volume'] = el.text
                    elif el.tag == 'VolumeNumber':
                        self['Num']['volNum'] = int(el.text)
                    elif el.tag == 'SectionNumber':
                        self['Num']['sectionNum'] = int(el.text)
                    elif el.tag == 'SubSectionNumber':
                        self['Num']['subsectionNum'] = int(el.text)
                    elif el.tag == 'EntryNumber':
                        # need to split off the suffix, use regex
                        m = r2.match(el.text)
                        self['Num']['entryNum'] = int(m.group(1))
                        self['Num']['entrySuf'] = m.group(2)
                    else:
                        pass

            if child.tag == 'Title':
                self['Title'] = child.text

            # subTitle and subsubTitle not supported in AJBentry
            if child.tag == 'subTitle':
                self['Title'] += child.text

            if child.tag == 'subsubTitle':
                self['Title'] += child.text

            if child.tag == 'Authors':
                for author in child:
                    for g2 in author:
                        if g2.tag == 'Person':
                            self['Authors'].append(self.HumanNameFmXML(g2))

            if child.tag == 'Editors':
                # PersonInfo or CorporateBody
                for editor in child:
                    for g2 in editor:
                        if g2.tag == 'Person':
                            self['Editors'].append(self.HumanNameFmXML(g2))

            if child.tag == 'Publishers':
                # Place and Name
                for publ in child:
                    publisher = {}
                    for pub in publ:
                        if pub.tag == 'Place':
                            if pub.text is not None:
                                publisher['Place'] = str(pub.text)
                            else:
                                publisher['Place'] = ''
                                
                        elif pub.tag == 'Name':
                            if pub.text is not None:
                                publisher['PublisherName'] = str(pub.text)
                            else:
                                publisher['PublisherName'] = ''

                        else:
                            pass
                    self['Publishers'].append(publisher)
                    del(publisher)

            if child.tag == 'Year':
                self['Year'] = child.text

            if child.tag == 'Edition':
                self['Edition'] = child.text

            if child.tag == 'Pagination':
                self['Pagination'] = child.text

            if child.tag == 'Prices':
                first = True
                self['Price'] = ''
                for price in child:
                    if first:
                       first = False
                    else:
                        self['Price'] += ' and '
                    self['Price'] += price.text
                del first

            if child.tag == 'Reviews':
                for review in child:
                    self['Reviews'].append(review.text)


            if child.tag == 'TranslatedFrom':
                self['TranslatedFrom'] = child.text

            if child.tag == 'Language':
                self['Language'] = child.text

            if child.tag == 'Translators':
                # PersonInfo or CorporateBody
                for trans in child:
                    for g2 in trans:
                        if g2.tag == 'Person':
                            self['Translators'].append(self.HumanNameFmXML(g2))

            if child.tag == 'Compilers':
                # PersonInfo or CorporateBody
                for comp in child:
                    for g2 in comp:
                        if g2.tag == 'Person':
                            self['Compilers'].append(self.HumanNameFmXML(g2))

            if child.tag == 'Contributors':
                # PersonInfo or CorporateBody
                for contr in child:
                    for g2 in contr:
                        if g2.tag == 'Person':
                            self['Contributors'].append(self.HumanNameFmXML(g2))

            if child.tag == 'ReprintOf':
                # Year or AJBnum but only one
                for rp in child:
                    if rp.tag == 'Year':
                        self['Reprint'] = rp.text
                    elif rp.tag == 'Index':
                        self['Reprint'] = self.AJBstringFromIndex_XML(rp)
                

            if child.tag == 'ReferenceOf':
                # AJBnum
                subsectionNum = '0'
                for ell in child:
                    if ell.tag == 'Index':
                        self['Reference'] = self.AJBstringFromIndex_XML(ell)

            if child.tag == 'Comments':
                for comment in child:
                    self['Others'].append(comment.text)

    def AJBstringFromIndex_XML( self, ell):
        '''Return a AJB number as a string "AJB xx.xxx(xx).xx[a]" from 
        an XML Index element.'''

        r2 = re.compile(r'([0-9]+)([A-Za-z]*)', re.ASCII)
        for el in ell:
            if el.tag == 'IndexName':
                aname = el.text
            elif el.tag == 'VolumeNumber':
                volNum = '%02d'%int(el.text)
            elif el.tag == 'SectionNumber':
                sectionNum = '%02d'%int(el.text)
            elif el.tag == 'SubSectionNumber':
                subsectionNum = el.text
            elif el.tag == 'EntryNumber':
                m = r2.match(el.text)
                entryNum = '%02d'%int(m.group(1))
                entrySuf = m.group(2)
        return aname + ' ' + volNum + '.' + sectionNum + '.' + entryNum
        
        
    def HumanNameFmXML(self, ell):
        hn = HumanName()
        for el in ell:
            if el.tag == 'First':
                hn.first = el.text
            elif el.tag == 'Middle':
                hn.middle = el.text
            elif el.tag == 'Last':
                hn.last = el.text
            elif el.tag == 'Title':
                hn.title = el.text
            elif el.tag == 'Suffix':
                hn.suffix = el.text
            elif el.tag == 'NickName':
                hn.nickname = el.text
            else:
                pass

        return hn


#
# Test everything
#
if __name__ == '__main__':

    ajbstr = '4 66.145(1).29 P. W. Hodge, The Physics comma and Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other This is the ajbstr9;'

    ajbstra = '4 66.145(1).29a P. W. Hodge, The Physics comma and Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other This is the ajbstr9;'

    ajbstra1 = '4 66.145.29a P. W. Hodge, The Physics comma and Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other This is the ajbstr9;'

    badajbstrd = '4 66.145.29d P. W. Hodge, The Physics comma and Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other This is the ajbstr9;'

    authorstr = '4 66.145(1).29 P. W. Hodge and I. A. Author and A. N. Other, The Physics comma and Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other This is the authorstr;'

    editorstr = '4 66.145.29 P.-W. Hodge jr. and I. A. Author III and A. Other and A. V. de la Name ed., The Physics comma and Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other a first comment; edited by A. B. Name; translated from Italian into English by A. Trans; also published London: A Publishing Co.; other This is the editor string;'

    allfieldsstr = '4 66.145.29a P.-W. Hodge jr. and I. A. Author III and A. Other and A. V. de la Name, The Physics comma and Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other a first comment; 3rd edition; edited by A. B. Name; translated from Italian into English by A. Trans; also published London: A Publishing Co.; other This is the editor string; contributors A. B. Contrib; compiled by A. B. Compiler; in French; reprint of 1956; reference AJB 59.144.55;'

    allfieldsstr2 = '4 66.145.29 P.-W. Hodge jr. and I. A. Author III and A. Other and A. V. de la Name, The Physics comma and Astronomy of Galaxies and Cosmology, , , , , , Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, reference AJB 59.144.55'

    badajbstr = '27 xx.145(1).309 P. W. Hodge, The Physics comma and Astronomy of Galaxies and Cosmology , New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other This is the badstr;'

    badtitlestr = '27 66.145(1).309 P. W. Hodge, , New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other This is the badstr;'

    try:
        from pprint import pprint
    except:
        print('Pretty Print module unavailable')
        sys.exit(0)

    try:
      badentry = Entry(ajbstr)
    except:
      print("Entry() class fails properly with no read() method.")
      
    allfieldajb = AJBentry(allfieldsstr)
    print('\nThe all fields ajb entry isValid() is %d and looks like:' % allfieldajb.isValid())
    pprint(allfieldajb)

    ajb1 = AJBentry()
    print("\najb.py version:: %s \n" % ajb1.version())
    print('The empty ajb entry isValid() is %d and looks like:' % ajb1.isValid())
    pprint(ajb1)

    ajb2 = AJBentry(ajbstr)
    print("\najb.py version " + ajb2.version())
    print('The good ajb entry isValid() is %d and looks like:' % ajb2.isValid())
    pprint(ajb2)


    ajb2 = AJBentry(ajbstra)
    print('\nThe good ajb entry isValid() is %d and looks like:' % ajb2.isValid())
    pprint(ajb2)

    ajb2 = AJBentry(ajbstra1)
    print('\nThe good ajb entry isValid() is %d and looks like:' % ajb2.isValid())
    pprint(ajb2)

    ajb3 = AJBentry(badajbstr)
    print('\nThe bad ajb entry isValid() is %d and looks like:' % ajb3.isValid())
    
    # This currently throws an error.
    #ajb3 = AJBentry(badajbstrd)
    #print('\nThe bad ajb entry isValid() is %d and looks like:' % ajb3.isValid())
    #pprint(ajb3)

    ajb4 = AJBentry(badtitlestr)
    print('\nThe bad title ajb entry isValid() is %d and looks like:' % ajb4.isValid())
    pprint(ajb4)

    authorajb = AJBentry(authorstr)
    print('\nThe author ajb entry isValid() is %d and looks like:' % authorajb.isValid())
    pprint(authorajb)
    print(authorajb.shortTitle())

    editorajb = AJBentry(editorstr)
    print('\nThe editor ajb entry isValid() is %d and looks like:' % editorajb.isValid())
    pprint(editorajb)
    print(editorajb.shortTitle())

    print(editorajb.numStr())
    eds = editorajb['Editors']
    print(eds[0].full_name)

    print(editorajb._parseAJBNum('AJB 32.45(0).56'))
    print(editorajb._parseAJBNum('32.45(0).56'))

    #
    # test XML routines
    #
    print('\n\nTesting XML routines\n')
    print('allfieldajb as entry:')
    pprint(allfieldajb)

    print('\nallfieldajb as XML')
    et = allfieldajb.write_XML_from_Entry()
    print(etree.tostring(et, pretty_print=True, encoding='unicode'))

    print('\nallfieldajb XML as entry')
    eAll = AJBentry()
    eAll.read_XML_to_Entry(et)
    pprint(eAll)
