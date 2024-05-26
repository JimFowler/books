#! /usr/bin/env python3
# -*- mode: Python;-*-
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/lib/tests/test_pagination_xml.py
##
##   Part of the Books20 Project
##
##   Copyright 2024 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrival system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright
'''The unittests for aabooks/lib/pagination_xml.py'''
import unittest
from aabooks.lib import pagination_xml as pg

__GOOD_STR__ = [
    ('', ''),
    (None, ''),
    ('12pp+203p+45pa+32pb+40AA+32AB+14i+23f+522P+10c+2m', \
     '12pp+203p+45pa+32pb+40AA+32AB+14i+23f+522P+10c+2m'),
    ]

__OLD_STR__ = '12p+203p+14i+23f+522P+10c'
__ROM_STR__ = '5D+XIIIpp+203p+40AA+32AB+14i+23f+522P+10c'
__BAD_STR__ = '12pz+203p+14i+23f+522P+10c'
__BAD_STR2__ = '12 pp+203p+14i+23f+522P+10c'
__BAD_STR3__ = '12pp+203p+14i+23f+522z+10c' # parse a bad character

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

        p_elem = pg.pagination_string_to_xml(test_string)
        p_string = pg.xml_to_pagination_string(p_elem)
        self.assertEqual(p_string, final_string)

    def test_a_good_strings(self):
        '''Test all the good strings that can be correctly converted.'''

        for t_string, f_string in __GOOD_STR__:
            self.do_string(t_string, f_string)

    def test_b_old_string(self):
        '''Test the old format string.'''
        self.do_string(__OLD_STR__, __OLD_STR__)

    def test_c_bad_string(self):
        '''Test a bad string that should not convert.'''

        with self.assertRaises(KeyError):
            self.do_string(__BAD_STR__, __BAD_STR__)

    def test_d_bad_string(self):
        '''Test a bad string that should not convert.'''

        with self.assertRaises(IndexError):
            self.do_string(__BAD_STR2__, __BAD_STR2__)

    def test_e_bad_string(self):
        '''Test a bad string that should not convert.'''

        with self.assertRaises(KeyError):
            self.do_string(__BAD_STR3__, __BAD_STR3__)

    def test_f_roman_string(self):
        '''Test the roman string.'''

        self.do_string(__ROM_STR__, __ROM_STR__)
