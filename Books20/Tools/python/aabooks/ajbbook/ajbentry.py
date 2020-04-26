#
# -*- mode: Python;-*-
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/ajbbook/AJBentry.py
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
"""AJBentry provides a class which can convert between a unicode text
entry and a representation in python, typically a dictionary entry of
the form Entry.py.entry()."""


import re
from lxml import etree

from nameparser import HumanName
from aabooks.lib import entry
from aabooks.lib import utils
from aabooks.ajbbook import AJBcomments as comments

#
# Don't build the regular expression compilers everytime
#  we build and entry.
#
__reg1__ = re.compile(r'\A\d+ +\d+\.\d+', re.UNICODE)
__reg2__ = re.compile(r'([0-9]+)([A-Za-z]*)', re.ASCII)
__reg3__ = re.compile(r'([AJB]{0,1})(\d+)\.(\d+)(\((\d+)\))*\.(\d+)([a-c]{0,1})',
                      re.UNICODE)

class AJBentry(entry.Entry):

    """Read the information from a string and put the data in the
    AJBentry dictionary. The entry is valid if there was a valid AJB
    number (vol.section.index) and a title.

    A line looks like:

    Index AJB_Num Author, Title, Place, Publisher, Year, \
    Pagination, Price, Reviews, Comments]

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

    def __init__(self, _entry_str=None):

        super(AJBentry, self).__init__()

        self.blank_entry()

        if _entry_str:
            self.read_text_to_entry(_entry_str)

    def blank_entry(self):
        """Initialize a blank entry by setting known fields to
        null values and deleting all other fields.
        """
        keys = list(self.keys())
        for k in keys:
            del self[k]

        self['Index'] = -1
        self['Num'] = {'volNum':-1,
                       'sectionNum':-1,
                       'subsectionNum':-1,
                       'entryNum':-1,
                       'entrySuf':'',
                       'volume': ''}
        self['Authors'] = []
        self['Editors'] = []
        self['Compilers'] = []
        self['Contributors'] = []
        self['Translators'] = []
        self['Others'] = []
        self['Title'] = ''
        self['Publishers'] = []
        self['Year'] = ''
        self['Pagination'] = ''
        self['Price'] = ''
        self['Reviews'] = []
        self['Comments'] = ''
        self['OrigStr'] = ''


    def num_str(self):
        """Return a stringfied version of the Num entry,
        ex. 'AJB 68.01(0).20'
        """
        anum = self['Num']
        if anum:
            strnum = str(anum['volume'])
            strnum = strnum + ' ' + '%02d'%anum['volNum']
            strnum = strnum + '.' + '%02d'%anum['sectionNum']
            if anum['subsectionNum'] > -1:
                strnum = strnum + '(' + str(anum['subsectionNum']) + ')'
            strnum = strnum + '.' + '%02d'%anum['entryNum']
            strnum = strnum + '%1s'%anum['entrySuf']
            return strnum

        return None

    def short_title(self):
        """Create a short title string for the entry. A short title
        is 'AJBnum 1stAuthor_lastname Title'."""
        string = self.num_str() + ' '
        if self.not_empty('Authors'):
            name = self['Authors'][0].last
        elif self.not_empty('Editors'):
            name = self['Editors'][0].last
        else:
            name = 'noAuthor'

        string = string + name + ', ' + self['Title'] + '\n'
        return string

    def is_valid(self):
        """AJB entries are valid if they have a valid AJB num
        and a Title."""
        return bool(self.is_valid_ajbnum() and self['Title'] != '')

    def not_empty(self, key):
        """Return the truth value of, 'key' existing
        in the entry and the key value is not empty."""
        if self.__contains__(key) and self[key]:
            return True
        return False

    #
    # Ascii comma separated variable file, read/write functions
    #
    def write_text_from_entry(self):
        """Write an AJBentry back into the string format that it came from.
        It should be the case that write(read(ajbstr)) == ajbstr up to
        the order of the comments and that read(write(ajbent)) == ajbent."""

        if not self.is_valid():
            return ''

        entrystr = self.num_str()[4:] + ' '

        if self.not_empty('Authors'):
            entrystr += utils.make_name_str(self['Authors'])
        elif self.not_empty('Editors'):
            entrystr += utils.make_name_str(self['Editors'])
            entrystr += ' ed.'

        entrystr = entrystr + ', ' + self['Title'].replace(', ', ' comma ')

        if self.not_empty('Publishers'):
            entrystr += ', '
            if self['Publishers'][0]['Place']:
                entrystr += self['Publishers'][0]['Place']

            entrystr += ', '
            if self['Publishers'][0]['PublisherName']:
                name = self['Publishers'][0]['PublisherName']
                name = name.replace(', ', ' comma ')
                entrystr += name
        else:
            entrystr += ', , '

        entrystr += ', '
        if self.not_empty('Year'):
            entrystr += str(self['Year'])

        entrystr += ', '
        if self.not_empty('Pagination'):
            entrystr += str(self['Pagination'])

        entrystr += ', '
        if self.not_empty('Price'):
            entrystr += str(self['Price'])

        entrystr += ', '
        if self.not_empty('Reviews'):
            first = True
            for review in self['Reviews']:
                if not first:
                    entrystr += ' and '
                first = False
                entrystr += review

        # comments
        entrystr += ', '
        if self.not_empty('Edition'):
            entrystr += str(self['Edition'])
            num = int(self['Edition'])
            if  num == 1:
                entrystr += 'st'
            elif num == 2:
                entrystr += 'nd'
            elif num == 3:
                entrystr += 'rd'
            else:
                entrystr += 'th'
            entrystr += ' edition;'

        if self.not_empty('Reprint'):
            entrystr += 'reprint of '
            entrystr += str(self['Reprint'])
            entrystr += ';'

        if self.not_empty('Compilers'):
            entrystr += 'compiled by '
            entrystr += utils.make_name_str(self['Compilers'])
            entrystr += ';'


        if self.not_empty('Contributors'):
            entrystr += 'contributors '
            entrystr += utils.make_name_str(self['Contributors'])
            entrystr += ';'

        # translated from by
        if self.not_empty('Translators') or self.not_empty('TranslatedFrom'):
            entrystr += 'translated '
            if self.not_empty('TranslatedFrom'):
                entrystr += 'from '
                entrystr += self['TranslatedFrom']
            if self.not_empty('Translators'):
                entrystr += ' by '
                entrystr += utils.make_name_str(self['Translators'])
            entrystr += ';'

        # additional editors
        if self.not_empty('Authors') and self.not_empty('Editors'):
            # need to include editors in comments
            entrystr += 'edited by '
            entrystr += utils.make_name_str(self['Editors'])
            entrystr += ';'

        # additional publishers
        if self['Publishers'].__len__() > 1:
            extrapubl = self['Publishers'][1:]
            entrystr += 'also published '
            first = True
            for publ in extrapubl:
                if not first:
                    entrystr += ' and '
                first = False
                entrystr += '%s: %s' % (publ['Place'].replace(', ', ' comma '),
                                        publ['PublisherName'].replace(', ', ' comma '))
            entrystr += ';'

        if self.not_empty('Language'):
            entrystr += 'in '
            entrystr += self['Language']
            entrystr += ';'

        # others
        if self.not_empty('Others'):
            for other in self['Others']:
                entrystr += 'other %s' % str(other).replace(', ', ' comma ')
                entrystr += '; '

        if self.not_empty('Reference'):
            entrystr += 'reference '
            entrystr += self['Reference']
            entrystr += ';'


        return entrystr

    def read_text_to_entry(self, line):
        """Parse a line with an AJB entry in it placing the values in the
        Entry dictionary. Returns True if this is a parsable line and
        false if it is not."""

        place = ""
        publishername = ""

        #
        # This regular expression is used to check the beginning of a line
        # for an item number, volnum and section number. If no numbers are
        # seen, then we reject the line.
        #

        if line and __reg1__.match(line):
            self['OrigStr'] = line
            #print(line)
            fields = line.split(',')
            fieldnum = -1
            for field in fields:

                fieldnum += 1
                field = field.replace(' comma ', ', ')
                field = field.strip()
                if fieldnum == 0:  # AJBnum and Authors
                    self._parse_field0(field)

                elif fieldnum == 1:  # Title
                    self['Title'] = field

                elif fieldnum == 2:  # place of publication
                    place = "" + field

                elif fieldnum == 3:  # Publisher
                    publishername = "" + field
                    self['Publishers'] = [{'Place' : place,
                                           'PublisherName' : publishername}]

                elif fieldnum == 4:   # Publication Year
                    self['Year'] = field

                elif fieldnum == 5:   # Page Count
                    self['Pagination'] = field

                elif fieldnum == 6:   # Price
                    self['Price'] = field

                elif fieldnum == 7:   # Reviews
                    if field:
                        self['Reviews'] = field.split(' and ')

                elif fieldnum == 8:   # Comments and other material
                    self['Comments'] = field
                    self._parse_comments(field)
                    continue

            return True

        return False

    def is_valid_ajbnum(self):
        """A valid AJB number has a volume number between 1-68
        and a section number between 1-150
        and an entry number > 0"""
        num = self['Num']

        return bool(num['volNum'] > 0 and num['volNum'] < 69 \
                    and num['sectionNum'] > 0 and num['sectionNum'] < 150 \
                    and num['entryNum'] > 0 \
                    and (num['entrySuf'] == '' or num['entrySuf'] == 'a' \
                         or num['entrySuf'] == 'b' or num['entrySuf'] == 'c'))



    #
    # Private functions
    #
    def _parse_field0(self, line):

        fields = line.split(' ', 2)

        self._parse_index(fields[0])

        self['Num'] = self._parse_ajbnum(fields[1])

        if len(fields) > 2:
            self._parse_authors(fields[2].strip())



    def _parse_index(self, line):
        """
        Get the file Index value (i.e. what number is this entry
        in the file.)
        """
        self['Index'] = line.strip()


    def _parse_ajbnum(self, line):
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

        nums = __reg3__.split(line.strip())

        if len(nums) != 9:
            print('Bad AJB number {}\n'.format(line))
            return
            
        if not nums[0]: # volume
            nums[0] = 'AJB'

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


    def _parse_authors(self, line):
        """split out the authors/editors
        """
        edt = False
        comp = False

        if line.endswith('ed.'):
            edt = True
            line = line.replace('ed.', '   ')
        elif line.endswith('comp.'):
            comp = True
            line = line.replace('comp.', '    ')

        names = utils.make_name_list(line)

        if edt:
            self['Editors'] = names
        elif comp:
            self['Compilers'] = names
        else:
            self['Authors'] = names



    def _parse_comments(self, field):
        """comment"""
        cparser = comments.Comment.parser()
        results = cparser.parse_text(field, reset=True, multi=True)
        #
        # Look for translators, language, edition, and other publishers
        #
        if results:
            for result in results:
                grammar_name = result.elements[0].grammar_name
                if grammar_name == 'Edition':
                    self['Edition'] = result.elements[0].edition_num

                elif grammar_name == 'Reference':
                    self['Reference'] = str(result.find(comments.AJBNum)).strip()

                elif grammar_name == 'Reprint':
                    tmp = result.find(comments.AJBNum)
                    if tmp:
                        self['Reprint'] = str(tmp).strip()
                    tmp = result.find(comments.Year)
                    if tmp:
                        self['Reprint'] = str(tmp).strip()

                elif grammar_name == 'Editors':
                    line = str(result.find(comments.NameList))
                    name = utils.make_name_list(line)
                    if self.not_empty('Editors'):
                        self['Editors'].extend(name)
                    else:
                        self['Editors'] = name

                elif grammar_name == 'Contributors':
                    line = str(result.find(comments.NameList))
                    name = utils.make_name_list(line)
                    if self.not_empty('Contributors'):
                        self['Contributors'].extend(name)
                    else:
                        self['Contributors'] = name

                elif grammar_name == 'Compilers':
                    line = str(result.find(comments.NameList))
                    name = utils.make_name_list(line)
                    if self.not_empty('Compilers'):
                        self['Compilers'].extend(name)
                    else:
                        self['Compilers'] = name

                elif grammar_name == 'Translation':
                    tmp = result.find(comments.FromLanguage)
                    if tmp:
                        self['TranslatedFrom'] = str(tmp.elements[1]).strip()

                    tmp = result.find(comments.ToLanguage)
                    if tmp:
                        self['Language'] = str(tmp.elements[1]).strip()

                    tmp = result.find(comments.NameList)
                    if tmp:
                        name = utils.make_name_list(str(tmp))
                        if self.not_empty('Translators'):
                            self['Translators'].extend(name)
                        else:
                            self['Translators'] = name

                elif grammar_name == 'Publishers':
                    tmp = str(result.find(comments.PublisherList))
                    # the space chars in the split avoids problems with
                    # e.g. Rand McNally & Sons
                    tlist = tmp.split(' and ')
                    for pub in tlist:
                        parts = pub.split(':')
                        self['Publishers'].append({'Place' : parts[0].strip(),
                                                   'PublisherName': parts[1].strip()})

                elif grammar_name == 'Language':
                    self['Language'] = str(result.find(comments.uWord)).strip()

                elif grammar_name == 'Other':
                    name = str(result.find(comments.uWords)).strip()
                    if not self.not_empty('Others'):
                        self['Others'] = []
                    self['Others'].append(name)

                else:
                    print('Unknown grammer name %s' % grammar_name)

    #
    # XML create routines
    #
    def write_xml_from_entry(self):
        '''Create an XML etree element with the root tag Entry from
        the entry.'''

        if not self.is_valid:
            return None

        # Title and Index are required of any entry
        entryxml = etree.Element('Entry')

        anum = self['Num']
        entryxml.append(self.make_ajbnum_xml(anum))

        elm = etree.SubElement(entryxml, 'Title')
        elm.text = self['Title']

        # This ends the required elements.  All further elements
        # may be missing or blank.

        if self.not_empty('subTitle'):
            elm = etree.SubElement(entryxml, 'SubTitle')
            elm.text = self['subTitle']

        # Create the people list, right now these lists are
        # only HumanNames but we need to add business names
        # in the future.
        if self['Authors']:
            elm = etree.SubElement(entryxml, 'Authors')
            for author in self['Authors']:
                autelm = etree.SubElement(elm, 'Author')
                # all authors are humannames right now.
                person = self.make_person_xml(author)
                autelm.append(person)

        if self['Editors']:
            elm = etree.SubElement(entryxml, 'Editors')
            for editor in self['Editors']:
                edelm = etree.SubElement(elm, 'Editor')
                # all authors are humannames right now.
                person = self.make_person_xml(editor)
                edelm.append(person)

        if self['Publishers']:
            elm = etree.SubElement(entryxml, 'Publishers')
            for publ in self['Publishers']:
                epub = etree.SubElement(elm, 'Publisher')

                eplace = etree.Element('Place')
                eplace.text = publ['Place']
                epub.append(eplace)

                epn = etree.Element('Name')
                epn.text = publ['PublisherName']
                epub.append(epn)

        if self.not_empty('Year'):
            elm = etree.SubElement(entryxml, 'Year')
            elm.text = str(self['Year'])

        if self.not_empty('Edition'):
            elm = etree.SubElement(entryxml, 'Edition')
            elm.text = str(self['Edition'])

        if self.not_empty('Pagination'):
            elm = etree.SubElement(entryxml, 'Pagination')
            elm.text = str(self['Pagination'])

        # The schema defines a price with currency and value
        # but we need to do some intellegent parsing of the prices
        # before we can use this.  For now we just naively use
        # the string.
        if self.not_empty('Price'):
            elm = etree.SubElement(entryxml, 'Prices')
            for price in self['Price'].split(' and '):
                priceelm = etree.SubElement(elm, 'Price')
                priceelm.text = price

        if self['Reviews']:
            elm = etree.SubElement(entryxml, 'Reviews')
            for rev in self['Reviews']:
                revelm = etree.SubElement(elm, 'Review')
                revelm.text = str(rev)

        if self.not_empty('TranslatedFrom'):
            elm = etree.SubElement(entryxml, 'TranslatedFrom')
            elm.text = str(self['TranslatedFrom'])

        if self.not_empty('Language'):
            elm = etree.SubElement(entryxml, 'Language')
            elm.text = str(self['Language'])

        if self['Translators']:
            elm = etree.SubElement(entryxml, 'Translators')
            for trans in self['Translators']:
                aelm = etree.SubElement(elm, 'Translator')
                # all translators are humannames right now.
                person = self.make_person_xml(trans)
                aelm.append(person)

        if self['Compilers']:
            elm = etree.SubElement(entryxml, 'Compilers')
            for compiler in self['Compilers']:
                aelm = etree.SubElement(elm, 'Compiler')
                # all compilers are humannames right now.
                person = self.make_person_xml(compiler)
                aelm.append(person)

        if self['Contributors']:
            elm = etree.SubElement(entryxml, 'Contributors')
            for contrib in self['Contributors']:
                aelm = etree.SubElement(elm, 'Contributor')
                # all contributors are humannames right now.
                person = self.make_person_xml(contrib)
                aelm.append(person)

        # Sometimes the reprint can be just a year number rather than
        # an AJBnum.  An AJBnum should have decimal points in it and
        # Years should not, so we look for a decimal point to determine
        # which it is.
        if self.not_empty('Reprint'):
            elm = etree.SubElement(entryxml, 'ReprintOf')
            if len(self['Reprint'].split('.')) == 1:
                # Must be a year
                eyear = etree.SubElement(elm, 'Year')
                eyear.text = self['Reprint']
            else:
                numdict = self._parse_ajbnum(self['Reprint'])
                num = self.make_ajbnum_xml(numdict)
                elm.append(num)

        if self.not_empty('Reference'):
            elm = etree.SubElement(entryxml, 'ReferenceOf')
            numdict = self._parse_ajbnum(self['Reference'])
            ajbxml = self.make_ajbnum_xml(numdict)
            elm.append(ajbxml)


        if self['Others']:
            elm = etree.SubElement(entryxml, 'Comments')
            for comment in self['Others']:
                com = etree.SubElement(elm, 'Comment')
                com.text = comment

        # return the root Entry element
        return entryxml


    def make_ajbnum_xml(self, ajbnum):
        '''Write an XML version of an AJB number as an index
        element. The index argument must be a dictionary'''
        index_xml = etree.Element('Index')

        elm = etree.SubElement(index_xml, 'IndexName')
        elm.text = str(ajbnum['volume']).strip()

        elm = etree.SubElement(index_xml, 'VolumeNumber')
        elm.text = str(ajbnum['volNum'])

        elm = etree.SubElement(index_xml, 'SectionNumber')
        elm.text = str(ajbnum['sectionNum'])

        elm = etree.SubElement(index_xml, 'SubSectionNumber')
        elm.text = str(ajbnum['subsectionNum'])

        elm = etree.SubElement(index_xml, 'EntryNumber')
        elm.text = str(ajbnum['entryNum']) + ajbnum['entrySuf']

        return index_xml


    def make_person_xml(self, hname):
        '''Create a Person element from a HumanName object. Returns the Person
        element.

        '''

        person_xml = etree.Element('Person')

        if hname.title:
            elm = etree.SubElement(person_xml, 'Prefix')
            elm.text = hname.title

        if hname.first:
            elm = etree.SubElement(person_xml, 'First')
            elm.text = hname.first

        if hname.middle:
            elm = etree.SubElement(person_xml, 'Middle')
            elm.text = hname.middle

        if hname.last:
            elm = etree.SubElement(person_xml, 'Last')
            elm.text = hname.last

        if hname.suffix:
            elm = etree.SubElement(person_xml, 'Suffix')
            elm.text = hname.suffix

        return person_xml

    def read_xml_to_entry(self, elxml):
        '''Parse an XML element of an Entry and place the information
        into the AJBentry dictionary. This is a bit tricky.  XML entries
        contain more information than the AJBentry does.'''

        for child in elxml:
            #print('child is ', child.tag)

            if child.tag == 'Index':
                for elm in child:
                    if elm.tag == 'IndexName':
                        self['Num']['volume'] = elm.text
                    elif elm.tag == 'VolumeNumber':
                        self['Num']['volNum'] = int(elm.text)
                    elif elm.tag == 'SectionNumber':
                        self['Num']['sectionNum'] = int(elm.text)
                    elif elm.tag == 'SubSectionNumber':
                        self['Num']['subsectionNum'] = int(elm.text)
                    elif elm.tag == 'EntryNumber':
                        # need to split off the suffix, use regex
                        mreg = __reg2__.match(elm.text)
                        self['Num']['entryNum'] = int(mreg.group(1))
                        self['Num']['entrySuf'] = mreg.group(2)
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
                    for g2ent in author:
                        if g2ent.tag == 'Person':
                            self['Authors'].append(self.person_name_from_xml(g2ent))

            if child.tag == 'Editors':
                # PersonInfo or CorporateBody
                for editor in child:
                    for g2ent in editor:
                        if g2ent.tag == 'Person':
                            self['Editors'].append(self.person_name_from_xml(g2ent))

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
                    for g2ent in trans:
                        if g2ent.tag == 'Person':
                            self['Translators'].append(self.person_name_from_xml(g2ent))

            if child.tag == 'Compilers':
                # PersonInfo or CorporateBody
                for comp in child:
                    for g2ent in comp:
                        if g2ent.tag == 'Person':
                            self['Compilers'].append(self.person_name_from_xml(g2ent))

            if child.tag == 'Contributors':
                # PersonInfo or CorporateBody
                for contr in child:
                    for g2ent in contr:
                        if g2ent.tag == 'Person':
                            self['Contributors'].append(self.person_name_from_xml(g2ent))

            if child.tag == 'ReprintOf':
                # Year or AJBnum but only one
                for reprint in child:
                    if reprint.tag == 'Year':
                        self['Reprint'] = reprint.text
                    elif reprint.tag == 'Index':
                        self['Reprint'] = self.ajbstr_from_xml(reprint)


            if child.tag == 'ReferenceOf':
                # AJBnum
                subsectionnum = '0'
                for ell in child:
                    if ell.tag == 'Index':
                        self['Reference'] = self.ajbstr_from_xml(ell)

            if child.tag == 'Comments':
                for comment in child:
                    self['Others'].append(comment.text)

    def ajbstr_from_xml(self, ell):
        '''Return a AJB number as a string "AJB xx.xxx(xx).xx[a]" from
        an XML Index element.'''

        for elm in ell:
            if elm.tag == 'IndexName':
                aname = elm.text
            elif elm.tag == 'VolumeNumber':
                volnum = '%02d'%int(elm.text)
            elif elm.tag == 'SectionNumber':
                sectionnum = '%02d'%int(elm.text)
            elif elm.tag == 'SubSectionNumber':
                subsectionnum = elm.text
            elif elm.tag == 'EntryNumber':
                mreg = __reg2__.match(elm.text)
                entrynum = '%02d'%int(mreg.group(1))
                entrysuf = mreg.group(2)
        return aname + ' ' + volnum + '.' + sectionnum + '.' + entrynum + entrysuf


    def person_name_from_xml(self, ell):
        '''Create a person mane from an XML element.'''
        hname = HumanName()
        for elm in ell:
            if elm.tag == 'First':
                hname.first = elm.text
            elif elm.tag == 'Middle':
                hname.middle = elm.text
            elif elm.tag == 'Last':
                hname.last = elm.text
            elif elm.tag == 'Title':
                hname.title = elm.text
            elif elm.tag == 'Suffix':
                hname.suffix = elm.text
            elif elm.tag == 'NickName':
                hname.nickname = elm.text
            else:
                pass

        return hname


#
# Test everything
#
if __name__ == '__main__':

    from pprint import pprint

    TESTENT = {
        'ajbstr': '''4 66.145(1).29 P. W. Hodge, The Physics comma and Astronomy of
Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179
pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216
Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other This is the ajbstr;''',

        'ajbstra' : '''4 66.145(1).29a P. W. Hodge, The Physics comma and Astronomy of
Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179
pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216
Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other This is the ajbstr;''',

        'ajbstra1' : '''4 66.145.29a P. W. Hodge, The Physics comma and
Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company,
1966, 179 pp, $2.95 and $4.95,
Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144
and Sky Tel. 33 109 and Sky Tel. 33 164, other This is the ajbstr;''',

        'badajbstrd' : '''4 66.145.29d P. W. Hodge,
The Physics comma and Astronomy of Galaxies and Cosmology,
New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95
and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144
and Sky Tel. 33 109 and Sky Tel. 33 164, other This is the ajbstr;''',

        'authorstr' : '''4 66.145(1).29 P. W. Hodge and I. A. Author and A. N. Other,
The Physics comma and Astronomy of Galaxies and Cosmology, New York,
McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American
216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and
Sky Tel. 33 164, other This is the authorstr;''',

        'editorstr' : '''4 66.145.29 P.-W. Hodge jr. and I. A. Author III
and A. Other and A. V. de la Name ed.,
The Physics comma and Astronomy of Galaxies and
Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and
$4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and
Sky Tel. 33 109 and Sky Tel. 33 164, other a first comment;
edited by A. B. Name; translated from Italian into English by A. Trans;
also published London: A Publishing Co.; other This is the editor string;''',

        'allfieldsstr' : '''4 66.145.29a P.-W. Hodge jr. and I. A. Author III
and A. Other and A. V. de la Name, The Physics comma and Astronomy of Galaxies and
Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and
$4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and
Sky Tel. 33 109 and Sky Tel. 33 164, other a first comment;
3rd edition;
edited by A. B. Name; translated from Italian into English by A. Trans;
also published London: A Publishing Co.;
other This is the editor string;
contributors A. B. Contrib; compiled by A. B. Compiler;
in French; reprint of 1956; reference AJB 59.144.55b;''',

        'allfieldsstr2' : '''4 66.145.29 P.-W. Hodge jr. and I. A. Author III
and A. Other and A. V. de la Name,
The Physics comma and Astronomy of Galaxies and Cosmology, , , , , ,
Sci. American 216 Nr 2 142 and Sci. American 216
Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, reference AJB 59.144.55''',

        'badajbstr' : '''27 xx.145(1).309 P. W. Hodge,
The Physics comma and Astronomy of Galaxies and Cosmology ,
New York, McGraw-Hill Book Company, 1966, 179 pp,
$2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216
Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164,
other This is the badstr;''',

        'badtitlestr' : '''27 66.145(1).309 P. W. Hodge, , New York,
McGraw-Hill Book Company,
1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and
Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164,
other This is the badstr;''',
        }


    try:
        entry.Entry(TESTENT['ajbstr'])
    except NotImplementedError:
        print("Entry() class fails properly with no read() method.")

    ENT = AJBentry()
    print('The empty ajb entry is_valid() is %d and looks like:' % ENT.is_valid())
    pprint(ENT)

    ENT = AJBentry(TESTENT['ajbstr'])
    print('The good ajb entry is_valid() is %d and looks like:' % ENT.is_valid())
    pprint(ENT)


    ENT = AJBentry(TESTENT['ajbstra'])
    print('\nThe good ajb entry is_valid() is %d and looks like:' % ENT.is_valid())
    pprint(ENT)

    ENT = AJBentry(TESTENT['ajbstra1'])
    print('\nThe good ajb entry is_valid() is %d and looks like:' % ENT.is_valid())
    pprint(ENT)

    ENT = AJBentry(TESTENT['badajbstr'])
    print('\nThe bad ajb entry is_valid() is %d and looks like:' % ENT.is_valid())

    ENT = AJBentry(TESTENT['badtitlestr'])
    print('\nThe bad title ajb entry is_valid() is %d and looks like:' % ENT.is_valid())
    pprint(ENT)

    ENT = AJBentry(TESTENT['authorstr'])
    print('\nThe author ajb entry is_valid() is %d and looks like:' % ENT.is_valid())
    pprint(ENT)
    print(ENT.short_title())

    ENT = AJBentry(TESTENT['editorstr'])
    print('\nThe editor ajb entry is_valid() is %d and looks like:' % ENT.is_valid())
    pprint(ENT)
    print(ENT.short_title())

    print(ENT.num_str())
    EDS = ENT['Editors']
    print(EDS[0].full_name)

    ENT = AJBentry(TESTENT['allfieldsstr'])
    print('\nThe all fields ajb entry is_valid() is %d and looks like:' % ENT.is_valid())
    pprint(ENT)

    print(ENT._parse_ajbnum('AJB 32.45(0).56'))
    print(ENT._parse_ajbnum('32.45(0).56'))

    #
    # test XML routines
    #
    print('\n\nTesting XML routines\n')
    print('allfieldajb as entry:')
    pprint(ENT)

    print('\nallfieldajb as XML')
    XMLENT = ENT.write_xml_from_entry()
    print(etree.tostring(XMLENT, pretty_print=True, encoding='unicode'))

    print('\nallfieldajb XML as entry')
    ENT = AJBentry()
    ENT.read_xml_to_entry(XMLENT)
    print('entry.is_valid is %d' % (ENT.is_valid()))
    pprint(ENT)
