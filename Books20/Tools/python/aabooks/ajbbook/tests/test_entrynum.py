# /usr/bin/env python3
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/ajbbook/test_entrynum.py
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

from lxml import etree
import unittest
import aabooks.ajbbook.entrynum as en

TEST_XML = '<Index><IndexName>AJB</IndexName><VolumeNumber>98</VolumeNumber>'
TEST_XML += '<SectionNumber>21</SectionNumber><SubSectionNumber>5</SubSectionNumber>'
TEST_XML += '<EntryNumber>32c</EntryNumber><PageNumber>52</PageNumber></Index>'

def compare_enum(enum, name, volnum, secnum, subsecnum, entnum, entsuf, page):
    '''Compare and en.AJBEntryNum with a set of descrete values'''
    return enum.enum['volName'] == name \
        and enum.enum['volNum'] == volnum \
        and enum.enum['sectionNum'] == secnum \
        and enum.enum['subsectionNum'] == subsecnum \
        and enum.enum['entryNum'] == entnum \
        and enum.enum['entrySuf'] == entsuf \
        and enum.enum['pageNum'] == page


class AJBEntryNumTestCase(unittest.TestCase):
    '''The unittest class to test the entrynum class'''

    def setUp(self):
        '''Set up for each test'''
        self.full_str = 'AJB 98.21(5).32c'
        self.short_str = 'AJB 98.21.32'
        self.enum = en.AJBEntryNum()

    def tearDown(self):
        '''Clean up after each test'''
        del self.enum

    def test_a_(self):
        '''test the creation of an en.AJBEntryNum'''
        self.assertFalse(self.enum.is_valid())

    def test_b_from_string(self):
        '''test the from_string() method'''
        self.enum.from_string('AJB 98.01.32')
        self.assertTrue(self.enum.is_valid())
        self.assertTrue(compare_enum(self, 'AJB', 98, 1, 0, 32, '', 0))

        self.enum.clear()
        self.enum.from_string('AJB 98.01(3).32F')
        self.assertTrue(self.enum.is_valid())
        self.assertTrue(compare_enum(self, 'AJB', 98, 1, 3, 32, 'F', 0))

        self.enum.clear()
        self.enum.from_string('AJB98.01(3).32F')
        # from_string() needs a space between volName and volNum
        self.assertFalse(self.enum.is_valid())

        self.enum.clear()
        self.enum.from_string('HJS 98.100000.32')
        self.assertTrue(self.enum.is_valid())
        self.assertTrue(compare_enum(self, 'HJS', 98, 100000, 0, 32, '', 0))

        self.enum.clear()
        self.enum.from_string('ABCDEFGHI 98.01.32')
        self.assertTrue(self.enum.is_valid())
        self.assertTrue(compare_enum(self, 'ABCDEFGHI', 98, 1, 0, 32, '', 0))

        self.enum.clear()
        self.enum.from_string('ABCDEFGHI 98.1.32')
        self.assertTrue(self.enum.is_valid())
        self.assertTrue(compare_enum(self, 'ABCDEFGHI', 98, 1, 0, 32, '', 0))

        self.enum.clear()
        self.enum.from_string('AJB .01.32')
        self.assertFalse(self.enum.is_valid())

        self.enum.clear()
        self.enum.from_string('AJB 98..32')
        self.assertFalse(self.enum.is_valid())

        self.enum.clear()
        self.enum.from_string(' 98.01.32')
        self.assertFalse(self.enum.is_valid())

        self.enum.clear()
        self.enum.from_string('AJB 98.-1.32')
        self.assertFalse(self.enum.is_valid())

    def test_c_to_string(self):
        '''Test the to_string() method'''
        ajbstr = 'AJB 98.21(0).32c'
        self.enum.from_string(ajbstr)
        self.assertTrue(self.enum.is_valid())
        self.assertEqual(self.enum.to_string(), ajbstr)

        self.enum.clear()
        ajbstr = 'AJB 98.21.32'
        self.enum.from_string(ajbstr)
        self.assertTrue(self.enum.is_valid())
        self.assertNotEqual(self.enum.to_string(), ajbstr)
        self.assertEqual(self.enum.to_string(), 'AJB 98.21(0).32')

    def test_d_from_xml(self):
        '''Test the from_xml() method'''
        parser = etree.XMLParser()
        parser.feed(TEST_XML)
        ent_xml = parser.close()
        self.enum.from_xml(ent_xml)
        self.assertEqual(self.enum.to_string(), 'AJB 98.21(5).32c')
        self.assertEqual(self.enum['pageNum'], 52)


    def test_e_to_xml(self):
        '''Test the to_xml() method'''
        self.enum.from_string(self.full_str)
        self.enum['pageNum'] = 52
        ajbxml = self.enum.to_xml()
        bstr = etree.tostring(ajbxml,
                              xml_declaration=False,
                              method='xml', encoding='UTF-8')
        strstr = bstr.decode(encoding='UTF-8')
        self.assertEqual(strstr, TEST_XML)

    def test_f_str(self):
        '''Test the __str__() function'''
        self.enum.from_string(self.full_str)
        self.assertEqual(f'{self.enum}', self.full_str)

    def test_g_kwargs(self):
        '''Test the use of kwargs in the constructor'''
        del self.enum
        self.enum = en.AJBEntryNum(ajbstr=self.full_str)
        self.assertEqual(self.enum.to_string(), self.full_str)

        del self.enum
        self.enum = en.AJBEntryNum(ajbstr=self.full_str, volName='HJS')
        self.assertEqual(self.enum.to_string(), 'HJS 98.21(5).32c')

        del self.enum
        self.enum = en.AJBEntryNum(ajbstr=self.full_str, sectionNum=12)
        self.assertEqual(self.enum.to_string(), 'AJB 98.12(5).32c')

        del self.enum
        self.enum = en.AJBEntryNum(ajbstr=self.full_str, subsectionNum=2)
        self.assertEqual(self.enum.to_string(), 'AJB 98.21(2).32c')

        del self.enum
        self.enum = en.AJBEntryNum(ajbstr=self.full_str, entryNum=12)
        self.assertEqual(self.enum.to_string(), 'AJB 98.21(5).12c')

        del self.enum
        self.enum = en.AJBEntryNum(ajbstr=self.full_str, entrySuf='a')
        self.assertEqual(self.enum.to_string(), 'AJB 98.21(5).32a')

        self.enum = en.AJBEntryNum(ajbstr=self.full_str, pageNum=62)
        self.assertEqual(self.enum.to_string(), 'AJB 98.21(5).32c')
        self.assertEqual(self.enum['pageNum'], 62)

        del self.enum
        self.enum = en.AJBEntryNum(ajbstr=self.full_str, bogon='none')
        self.assertEqual(self.enum.to_string(), self.full_str)

        del self.enum
        self.enum = en.AJBEntryNum(ajbxml=TEST_XML)
        self.assertEqual(self.enum.to_string(), self.full_str)
        self.assertEqual(self.enum['pageNum'], 52)

        del self.enum
        parser = etree.XMLParser()
        parser.feed(TEST_XML)
        ent_xml = parser.close()
        self.enum = en.AJBEntryNum(ajbxml=ent_xml)
        self.assertEqual(self.enum.to_string(), self.full_str)
        self.assertEqual(self.enum['pageNum'], 52)

        del self.enum
        self.enum = en.AJBEntryNum(ajbxml=5)
        self.assertFalse(self.enum.is_valid())

    def test_h_eq_(self):
        '''Test the equals (==) operator.'''
        self.enum.from_string(self.full_str)
        enum = en.AJBEntryNum(ajbstr=self.full_str)
        self.assertTrue(self.enum == enum)
        enum['pageNum'] = 3
        self.assertTrue(self.enum == enum)

    def test_i_gt_(self):
        '''Test the __gt__() (>) operator'''
        self.enum.from_string(self.full_str)
        enum = en.AJBEntryNum(ajbstr=self.full_str)
        self.assertTrue(self.enum == enum)

        self.enum['volName'] = 'HJS'
        self.assertTrue(self.enum > enum, msg='Fail on volName')

        self.enum.from_string(self.full_str)
        self.enum['volNum'] = 100
        self.assertTrue(self.enum > enum, msg='Fail on volNum')

        self.enum.from_string(self.full_str)
        self.enum['sectionNum'] = 22
        self.assertTrue(self.enum > enum, msg='Fail on sectionNum')

        self.enum.from_string(self.full_str)
        self.enum['subsectionNum'] = 6
        self.assertTrue(self.enum > enum, msg='Fail on subsectionNum')

        self.enum.from_string(self.full_str)
        self.enum['entryNum'] = 42
        self.assertTrue(self.enum > enum, msg='Fail on entryNum')

        self.enum.from_string(self.full_str)
        self.enum['entrySuf'] = 'd'
        self.assertTrue(self.enum > enum, msg='Fail on entrySuf')

        self.enum.from_string(self.full_str)
        self.enum['pageNum'] = 3
        self.assertFalse(self.enum > enum, msg='Fail on pageNum')

    def test_i_lt_(self):
        '''Test the __gt__() (>) operator.  The initial value is

        'AJB 98.21(5).32c'

        '''
        self.enum.from_string(self.full_str)
        enum = en.AJBEntryNum(ajbstr=self.full_str)
        self.assertTrue(self.enum ==enum)
        self.assertFalse(self.enum < enum)

        self.enum['volName'] = 'AAB'
        self.assertTrue(self.enum < enum, msg='Fail on volName')

        self.enum.from_string(self.full_str)
        self.enum['volNum'] = 97
        self.assertTrue(self.enum < enum, msg='Fail on volNum')

        self.enum.from_string(self.full_str)
        self.enum['sectionNum'] = 1
        self.assertTrue(self.enum < enum, msg='Fail on sectionNum')

        self.enum.from_string(self.full_str)
        self.enum['subsectionNum'] = 3
        self.assertTrue(self.enum < enum, msg='Fail on subsectionNum')

        self.enum.from_string(self.full_str)
        self.enum['entryNum'] = 12
        self.assertTrue(self.enum < enum, msg='Fail on entryNum')

        self.enum.from_string(self.full_str)
        self.enum['entrySuf'] = 'a'
        self.assertTrue(self.enum < enum, msg='Fail on entrySuf')

        self.enum.from_string(self.full_str)
        enum['pageNum'] = 5
        self.enum['pageNum'] = 4
        self.assertFalse(self.enum < enum, msg='Fail on pageNum')


##
## Unit tests
##
if __name__ == '__main__':

    unittest.main()
