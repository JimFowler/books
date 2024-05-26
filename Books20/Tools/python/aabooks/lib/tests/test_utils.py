#! /usr/bin/env python
##
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/lib/tests/test_utils.py
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
'''Provide the unittests for aabooks/lib/utils.py'''
import unittest
from aabooks.lib import utils

class UtilsTestCase(unittest.TestCase):
    '''Test cases for aabooks/lib/utils.py.'''

    def setUp(self):
        '''Set things up for every test.'''
        self.glines = ['AJB 12.34(1).56a J. Russell',
                       ' 12.34(1).56a J. Russell',
                       '12.34.56a J. Russell',
                       ' 12.34(1).56 J. Russell',
                      ]
        self.blines = ['AJB 12.34(1).a J. Russell',
                       ' 12.-1.56a J. Russell',
                       'aa.34.56a J. Russell',
                      ]
        self.ajbnum = {'volume': 'AJB',
                       'volNum': 12,
                       'pageNum': -1,
                       'sectionNum': 34,
                       'subsectionNum': 1,
                       'entryNum': 56,
                       'entrySuf': 'a',
                       }
    def tearDown(self):
        '''Clean up the mess after every test.'''
        del self.glines
        del self.blines

        del self.ajbnum

    def test_a_make_name_func(self):
        '''Test make_name_list().'''
        name_str = '''A. B. Author and C. D. Next sj and D. E. Brother'''
        test_name_list = utils.make_name_list(name_str)
        test_name_str = utils.make_name_str(test_name_list)
        self.assertEqual(test_name_str, name_str)

    def test_b0_good_parse_ajbnum(self):
        '''test the parse_ajb() function.'''
        self.assertEqual(self.ajbnum, utils.parse_ajbnum(self.glines[0]))

    def test_b1_good_parse_ajbnum(self):
        '''Test without volume name. Should default to 'AJB'.'''
        self.assertEqual(self.ajbnum, utils.parse_ajbnum(self.glines[1]))

    def test_b2_good_parse_ajbnum(self):
        '''Test without optional sub-section number. Should
        default to 0.'''
        self.ajbnum['subsectionNum'] = 0
        self.assertEqual(self.ajbnum, utils.parse_ajbnum(self.glines[2]))

    def test_b3_good_parse_ajbnum(self):
        '''Test without option entry suffix. Should default to the empty
        string.

        '''
        self.ajbnum['entrySuf'] = ''
        self.assertEqual(self.ajbnum, utils.parse_ajbnum(self.glines[3]))

    def test_c0_bad_parse_ajbnum(self):
        '''Test a missing entry number. Should get back and empty
        dictionary.

        '''
        self.assertEqual({}, utils.parse_ajbnum(self.blines[0]))

    def test_c1_bad_parse_ajbnum(self):
        '''Test a missing or incorrect section number. Should get back and
        empty dictionary.

        '''
        self.assertEqual({}, utils.parse_ajbnum(self.blines[1]))

    def test_c2_bad_parse_ajbnum(self):
        '''Test a missing section number. Should get back and empty
        dictionary.

        '''
        self.assertEqual({}, utils.parse_ajbnum(self.blines[2]))
