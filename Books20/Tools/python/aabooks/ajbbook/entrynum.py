#! /usr/bin/env python
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/ajbbook/entrynum.py
##
##   Part of the Books20 Project
##
##   Copyright 2023 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrival system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright
'''Class definition of the ajbentry number.  This number consists
of a catalog name, a volume number, a section number, an optional
sub-section number, an entry number, and a page number.

EntryNums should be able to read and write both strings as well as
XML; indeed they define the XML format for this class.  They
should also be able to decide which EntryNum is bigger than another
for sorting purposes.

'''
import sys
import re
import traceback
from pprint import pprint

from lxml import etree

__REG2__ = re.compile(r'([0-9]+)([A-Za-z]*)', re.ASCII)
__REG3__ = re.compile(r'(\W{0,1}) (\d+)\.(\d+)(\((\d+)\))*\.(\d+)(\W{0,1})', re.UNICODE)

class AJBEntryNum(dict):
    '''The class definition of an AJB entry number'''

    def __init__(self, **kwargs):
        '''Initialize an EntryNum.  **kwargs can include any of 'volName',
        'volNum', 'sectionNum', 'subsectionNum', 'entryNum',
        'entrySuf', 'pageNum' 'ajbxml', or 'ajbstr'. Any other
        keywords are ignored. If 'ajbxml' and 'ajbstr' are given, then
        'ajbxml' will override 'ajbstr'.  The other keywords will
        override any values given by 'ajbxml' or 'ajbstr'.

        '''
        super().__init__()

        self.__keylist__ = ['volName', 'volNum', 'sectionNum', 'subsectionNum',
                            'entryNum', 'entrySuf', 'pageNum']

        self.clear()

        if 'ajbstr' in kwargs:
            self.from_string(kwargs['ajbstr'])
        if 'ajbxml' in kwargs:
            if isinstance(kwargs['ajbxml'], str):
                parser = etree.XMLParser()
                parser.feed(kwargs['ajbxml'])
                ent_xml = parser.close()
            elif isinstance(kwargs['ajbxml'], etree._Element):
                ent_xml = kwargs['ajbxml']
            else:
                # Raise an error here?
                return
            self.from_xml(ent_xml)

        for key in self.__keylist__:
            if key in kwargs:
                self[key] = kwargs[key]

    def clear(self):
        '''Reset all the values to the default, non-valid AJBEntryNum'''
        self['volName'] = ''
        self['volNum'] = -1
        self['sectionNum'] = -1
        self['subsectionNum'] = 0
        self['entryNum'] = -1
        self['entrySuf'] = ''
        self['pageNum'] = 0

    def is_valid(self):
        '''A valid AJB/AAA number has a volume number, section number
        and entry number greater than -1.  The volume name, subsection
        number, entry suffix, and page number may be any value'''

        return bool(self['volNum'] > -1 \
                    and self['sectionNum'] > -1 \
                    and self['entryNum'] > -1)

    def to_string(self):
        '''Return a stringfied version of the Num entry, Note that to
        to_string() method always returns the subsection number even if no
        subsection number was explicitly set.

        ex. 'AJB 68.01(0).20'

        '''

        strnum = str(self['volName'])
        strnum += ' ' + f'{self["volNum"]:02}'
        strnum += '.' + f'{self["sectionNum"]:02}'
        strnum += f'({self["subsectionNum"]})'
        strnum += '.' + f'{self["entryNum"]:02}'
        strnum += str(self['entrySuf'])

        return strnum

    def from_string(self, strnum):
        '''Convert from a string'''

        nums = __REG3__.split(strnum.strip())
        #pprint(nums)
        if len(nums) != 9:
            return

        if not nums[5]: # subsectionNum
            nums[5] = 0

        if not nums[7]: # entrySuf
            nums[7] = ''

        self['volName'] = nums[0].strip()
        self['volNum'] = int(nums[2])
        self['sectionNum'] = int(nums[3])
        self['subsectionNum'] = int(nums[5])
        self['entryNum'] = int(nums[6])
        self['entrySuf'] = nums[8]


    def to_xml(self):
        '''Write an XML version of an AJB number as an index
        element. The self argument must be a dictionary in the format
        of ajbentry['Num']'''

        index_xml = etree.Element('Index')

        try:
            elm = etree.SubElement(index_xml, 'IndexName')
            elm.text = str(self['volName']).strip()

            elm = etree.SubElement(index_xml, 'VolumeNumber')
            elm.text = str(self['volNum'])

            elm = etree.SubElement(index_xml, 'SectionNumber')
            elm.text = str(self['sectionNum'])

            elm = etree.SubElement(index_xml, 'SubSectionNumber')
            elm.text = str(self['subsectionNum'])

            elm = etree.SubElement(index_xml, 'EntryNumber')
            elm.text = str(self['entryNum']) + self['entrySuf']

            if self['pageNum'] != -1:
                elm = etree.SubElement(index_xml, 'PageNumber')
                elm.text = str(self['pageNum'])
        except ValueError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      limit=2, file=sys.stdout)
            print('ERROR entrynum::to_xml: failed')
            return etree.Element('Index')

        return index_xml


    def from_xml(self, child):
        '''Convert from an XML etree'''

        for elm in child:
            if elm.tag == 'IndexName':
                self['volName'] = elm.text
            elif elm.tag == 'VolumeNumber':
                self['volNum'] = int(elm.text)
            elif elm.tag == 'SectionNumber':
                self['sectionNum'] = int(elm.text)
            elif elm.tag == 'SubSectionNumber':
                self['subsectionNum'] = int(elm.text)
            elif elm.tag == 'EntryNumber':
                # need to split off the suffix, use regex
                mreg = __REG2__.match(elm.text)
                self['entryNum'] = int(mreg.group(1))
                self['entrySuf'] = mreg.group(2)
            elif elm.tag == 'PageNumber':
                self['pageNum'] = int(elm.text)
            else:
                pass


    def __str__(self):

        '''Override for the dict.__str__() function'''
        return self.to_string()

    def __eq__(self, enum):
        '''determine equality between self and enum.'''
        return self['volName'] == enum['volName'] \
            and self['volNum'] == enum['volNum'] \
            and self['sectionNum'] == enum['sectionNum'] \
            and self['subsectionNum'] == enum['subsectionNum'] \
            and self['entryNum'] == enum['entryNum'] \
            and self['entrySuf'] == enum['entrySuf']


    def __ne__(self, enum):
        '''Test for non-equility betwwen self and enum'''
        return not self.__eq__(enum)

    def __gt__(self, enum):
        '''Test if self is greater than enum.  Greater than mean that
        '''
        for key in self.__keylist__:
            if 'pageNum' in key:
                continue
            if self[key] > enum[key]:
                return True
        return False

    def __ge__(self, enum):
        '''Test if self is greater than or equal to enum'''
        return self.__gt__(enum) or self.__eq__(enum)


    def __lt__(self, enum):
        '''Test if self is less than enum.  Greater than mean that
        '''
        for key in self.__keylist__:
            if 'pageNum' in key:
                continue
            if self[key] < enum[key]:
                return True
        return False

    def __le__(self, enum):
        '''Test if self is less than or equal to enum'''
        return self.__lt__(enum) or self.__eq__(enum)
