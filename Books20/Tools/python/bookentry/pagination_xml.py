#! /usr/bin/env python3
# -*- mode: Python;-*-
# Begin copyright
#
# /home/jrf/Documents/books/Books20/Tools/python/bookentry/xml/pagination_XML.py
#
# Part of the Books20 Project
#
# Copyright 2018 James R. Fowler
#
# All rights reserved. No part of this publication may be
# reproduced, stored in a retrival system, or transmitted
# in any form or by any means, electronic, mechanical,
# photocopying, recording, or otherwise, without prior written
# permission of the author.
#
#
# End copyright
'''Convert pagination string of the form
<count><code>[+<count><code>[+...]] to XML pagination elements and the
reverse.

Example 12pp+203pm+23AA+3t+34i+12P  converts to

<Pagination>
  <Preface>12</Preface>
  <Main>203</Main>
  <Appendix_A>23</Appendix_A>
  <Tables>3</Tables>
  <Illustrations>34</Illustrations>
  <Plates>12</Plates>
  ...
</Pagination>

'''
import re
from lxml import etree

##
## Local Variables
##

#
# These two dictionaries define the mapping between tags in pagination
# strings and sub-element names in an XML Pagination element. Note
# that tags and XML names must be one to one and unique.
#
# If you make changes to this list, you must also make a change to the
# schema in bookfile.xsd.
#
__TAG_TO_XML_NAME__ = {
    'AA' : 'Appendix_A',
    'AB' : 'Appendix_B',
    'AC' : 'Appendix_C',
    'AD' : 'Appendix_D',
    'AE' : 'Appendix_E',
    'AF' : 'Appendix_F',
    'b'  : 'Models',
    'c'  : 'Charts',
    'D'  : 'Diagrams',
    'd'  : 'Drawings',
    'F'  : 'Frontispiece',
    'f'  : 'Figures',
    'h'  : 'Woodcuts',
    'i'  : 'Illustrations',
    'M'  : 'Maps',
    'n'  : 'Nomograms',
    'bP' : 'BW_Plates',
    'cP' : 'Colour_Plates',
    'P'  : 'Plates',
    'pp' : 'Preface',
    'p'  : 'Main',
    'pa' : 'Afterword',
    # Other unknown sections
    'pa' : 'OtherSec_1',
    'pb' : 'OtherSec_2',
    'pc' : 'OtherSec_3',
    'pd' : 'OtherSec_4',
    'pe' : 'OtherSec_5',
    # Not sure how these last two names are used so I am sticking with
    # the German words for now.
    't'  : 'Tafeln',
    'T'  : 'Tabellen',
}

__XML_NAME_TO_TAG__ = {v: k for k, v in __TAG_TO_XML_NAME__.items()}

#
# The regular expression searches for
# one or more digits  \d+ (the count)
# exactly one or two word character string  \w{1,2} (the tag)
# in a pagination string.
#
__COUNT_TAGS_RE__ = re.compile(r'([0-9]+|[IVXLCDM]+)([a-zA-Z]{1,2})')

# Indices into the regular expression result list
__RE_EXP_COUNT__ = 1
__RE_EXP_TAG__ = 2

##
## Public Functions
##
def pagination_string_to_xml(pagination_string):
    '''Convert a pagination string to a XML pagination element. A
    pagination string is a string of counts and tags separated by '+'
    character.

    '''

    # Create the basic XML element
    pagination_xml = etree.Element('Pagination')

    # return basic element if string is empty
    if pagination_string == '' or pagination_string is None:
        return pagination_xml

    # split the string into it parts (count,tag)
    parts_list = pagination_string.split('+')

    # check each part of the string
    #page_counter = 0
    for p_l in parts_list:
        p_parts = __COUNT_TAGS_RE__.split(p_l.strip())

        p_name = __TAG_TO_XML_NAME__[p_parts[__RE_EXP_TAG__]]
        p_count = p_parts[__RE_EXP_COUNT__]

        part_xml = etree.SubElement(pagination_xml, p_name)
        part_xml.text = str(p_count)

    return pagination_xml


def xml_to_pagination_string(elem):
    '''Convert an XML Pagination element to a pagination string'''

    pagination_string = ''

    if elem is None or elem.tag != 'Pagination':
        return pagination_string

    first = True
    for child in elem:
        count = child.text
        tag = __XML_NAME_TO_TAG__[child.tag]

        if not first:
            pagination_string += '+'
        else:
            first = False

        pagination_string += '{count}{tag}'.format(count=count, tag=tag)

    return pagination_string



##
## Test everything
##
if __name__ == '__main__':

    OLD_STR = '12p+203p+14i+23f+522P+10c'
    NEW_STR = '12pp+203p+45pa+32pb+40AA+32AB+14i+23f+522P+10c'
    ROM_STR = '5D+XIIIpp+203p+40AA+32AB+14i+23f+522P+10c'
    BAD_STR = '12pz+203p+14i+23f+522P+10c'

    def testit(test_string):
        '''test the XML to/from pagination strings'''

        # Test transform from string to xml
        print('Testing string "{}"'.format(test_string))
        p_elem = pagination_string_to_xml(test_string)
        print(etree.tostring(p_elem, pretty_print=True,
                             method='xml', encoding='unicode'))

        # Test transform from xml to string
        p_string = xml_to_pagination_string(p_elem)
        print('and this maps back to:\n', p_string)
        if p_string == test_string:
            print('which matches the test string\n')
        else:
            print('which does not match the test string\n')


    #
    # ok, do the testing now.
    #
    testit('')
    testit(None)
    testit(NEW_STR)

    try:
        testit(OLD_STR)
    except KeyError:
        print('OLD_STR fails as expected with ValueError\n\n')

    try:
        testit(BAD_STR)
    except KeyError:
        print('BAD_STR fails as expected with KeyError\n\n')

    testit(ROM_STR)
