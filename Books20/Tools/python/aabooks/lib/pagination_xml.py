#! /usr/bin/env python3
# -*- mode: Python;-*-
# Begin copyright
#
# /home/jrf/Documents/books/Books20/Tools/python/aabooks/lib/pagination_XML.py
#
# Part of the Books20 Project
#
# Copyright 2018 James R. Fowler
#
# All rights reserved. No part of this publication may be
# reproduced, stored in a retrieval system, or transmitted
# in any form or by any means, electronic, mechanical,
# photocopying, recording, or otherwise, without prior written
# permission of the author.
#
#
# End copyright
'''
Convert a pagination string of the form

<count><code>[+<count><code>[+...]]

to XML pagination elements and the reverse.

Example 12pp+203pm+23AA+3t+34i+12P  converts to::

  <Pagination>
    <Preface>12</Preface>
    <Main>203</Main>
    <Appendix_A>23</Appendix_A>
    <Tables>3</Tables>
    <Illustrations>34</Illustrations>
    <Plates>12</Plates>
    ...
  </Pagination>


Known text codes and their matching XML tags are::

  __TAG_TO_XML_NAME__ = {
    'AA' : 'Appendix_A',
    'AB' : 'Appendix_B',
    'AC' : 'Appendix_C',
    'AD' : 'Appendix_D',
    'AE' : 'Appendix_E',
    'AF' : 'Appendix_F',
    'AG' : 'Appendix_G',
    'b'  : 'Models',
    'c'  : 'Charts',
    'D'  : 'Diagrams',
    'd'  : 'Drawings',
    'F'  : 'Frontispiece',
    'f'  : 'Figures',
    'i'  : 'Illustrations',
    'I'  : 'Index',
    'h'  : 'Woodcuts',
    'M'  : 'Maps',
    'n'  : 'Nomograms',
    'bP' : 'BW_Plates',
    'cP' : 'Colour_Plates',
    'P'  : 'Plates',
    'pp' : 'Preface',
    'p'  : 'Main',
    'pa' : 'Afterword',
    # Other unknown sections
    'pb' : 'OtherSec_2',
    'pc' : 'OtherSec_3',
    'pd' : 'OtherSec_4',
    'pe' : 'OtherSec_5',
    'pf' : 'OtherSec_6',
    'pg' : 'OtherSec_7',
    'ph' : 'OtherSec_8',
    'pi' : 'OtherSec_9',
    'pj' : 'OtherSec_10',
    # Not sure how these last two names are used so I am sticking with
    # the German words for now.
    't'  : 'Tables (Tabellen)',
    'T'  : 'Tafeln (Plates, tables, boards),
  }


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
# schema in Tools/xml/pagination.xsd.
#
__TAG_TO_XML_NAME__ = {
    'AA' : 'Appendix_A',
    'AB' : 'Appendix_B',
    'AC' : 'Appendix_C',
    'AD' : 'Appendix_D',
    'AE' : 'Appendix_E',
    'AF' : 'Appendix_F',
    'AG' : 'Appendix_G',
    'b'  : 'Models',
    'c'  : 'Charts',
    'D'  : 'Diagrams',
    'd'  : 'Drawings',
    'F'  : 'Frontispiece',
    'f'  : 'Figures',
    'i'  : 'Illustrations',
    'I'  : 'Index',
    'h'  : 'Woodcuts',
    'M'  : 'Maps',
    'n'  : 'Nomograms',
    'bP' : 'BW_Plates',
    'cP' : 'Colour_Plates',
    'P'  : 'Plates',
    'pp' : 'Preface',
    'p'  : 'Main',
    # Other unknown sections
    'pa' : 'OtherSec_1',
    'pb' : 'OtherSec_2',
    'pc' : 'OtherSec_3',
    'pd' : 'OtherSec_4',
    'pe' : 'OtherSec_5',
    'pf' : 'OtherSec_6',
    'pg' : 'OtherSec_7',
    'ph' : 'OtherSec_8',
    'pi' : 'OtherSec_9',
    'pj' : 'OtherSec_10',
    't'  : 'Tables',     # tabelen
    'T'  : 'Tafeln',     # tafeln  need to append plates or change all 'T's
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
    '''
    Convert a pagination string to a XML pagination element. A
    pagination string is a string of counts and tags separated by '+'
    character.

    Returns an lxml.etree.Element with at least::

      <Pagination>
      </Pagination>


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
    '''
    Convert an lml.etree.Element XML Pagination element to a pagination
    string.

    Returns a string

    '''

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
## convert to unit tests
##
if __name__ == '__main__':

    import unittest

    GOOD_STRING = [
        ('', ''),
        (None, ''),
        ('12pp+203p+45pa+32pb+40AA+32AB+14i+23f+522P+10c', \
         '12pp+203p+45pa+32pb+40AA+32AB+14i+23f+522P+10c'),
        ]

    OLD_STR = '12p+203p+14i+23f+522P+10c'
    ROM_STR = '5D+XIIIpp+203p+40AA+32AB+14i+23f+522P+10c'
    BAD_STR = '12pz+203p+14i+23f+522P+10c'
    BAD_STR2 = '12 pp+203p+14i+23f+522P+10c'
    BAD_STR3 = '12pp+203p+14i+23f+522z+10c' # parse a bad character
    
    class PaginationTestCase(unittest.TestCase):
        '''The test suite for pagination_xml.py.'''

        def setUp(self):
            '''Set up for the tests.'''

        def tearDown(self):
            '''Tear down for the next test.'''

        def do_string(self, test_string, final_string):
            '''Convert a pagination string to XML, convert back to a pagination
            string, and compare the answer to the final string.

            '''

            p_elem = pagination_string_to_xml(test_string)
            p_string = xml_to_pagination_string(p_elem)
            self.assertEqual(p_string, final_string)
            #print(etree.tostring(p_elem, pretty_print=True,
            #                     method='xml', encoding='unicode'))

        def test_a_good_strings(self):
            '''Test all the good strings that can be correctly converted.'''

            for t_string, f_string in GOOD_STRING:
                self.do_string(t_string, f_string)

        def test_b_old_string(self):
            '''Test the old format string.'''
            self.do_string(OLD_STR, OLD_STR)

        def test_c_bad_string(self):
            '''Test a bad string that should not convert.'''

            with self.assertRaises(KeyError):
                self.do_string(BAD_STR, BAD_STR)

        def test_d_bad_string(self):
            '''Test a bad string that should not convert.'''

            with self.assertRaises(IndexError):
                self.do_string(BAD_STR2, BAD_STR2)

        def test_e_bad_string(self):
            '''Test a bad string that should not convert.'''

            with self.assertRaises(KeyError):
                self.do_string(BAD_STR3, BAD_STR3)

        def test_f_roman_string(self):
            '''Test the roman string.'''

            self.do_string(ROM_STR, ROM_STR)

    unittest.main()
