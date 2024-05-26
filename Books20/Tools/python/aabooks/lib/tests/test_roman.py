#! /usr/bin/env python
##
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/lib/test/test_roman.py
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
'''Run the unit tests for roman.py'''
import unittest
from aabooks.lib import roman

__TEST_MAP__ = ((1, 'I'), (3, 'III'), (4, 'IV'), (9, 'IX'), (10, 'X'),
            (14, 'XIV'), (19, 'XIX'), (24, 'XXIV'), (40, 'XL'),
            (49, 'XLIX'), (90, 'XC'), (99, 'XCIX'), (100, 'C'),
            (400, 'CD'), (490, 'CDXC'), (499, 'CDXCIX'), (500, 'D'),
            (900, 'CM'), (990, 'CMXC'), (998, 'CMXCVIII'),
            (999, 'CMXCIX'), (1000, 'M'), (2013, 'MMXIII'))

__NOT_ROMAN__ = ('AA', 'mxvi', 'MMaVI', '', 'SPQR', 'MMXiii', 'MXCD')


#
# Unit tests also taken from Mark Pilgrim
#

class RomanNumberTestCase(unittest.TestCase):
    '''Run the unit tests for Roman number functions.'''

    def test_is_roman(self):
        '''Test valid strings in is_roman().'''
        for _, num_roman in __TEST_MAP__:
            self.assertTrue(roman.is_roman(num_roman),
                            f'"{num_roman}" should be a valid Roman')

    def test_is_roman_errors(self):
        '''Test invalid strings in is_roman().'''
        for bad_string in __NOT_ROMAN__:
            self.assertFalse(roman.is_roman(bad_string),
                             f'"{bad_string}" should not be Roman')

    def test_to_roman(self):
        '''Test valid numbers in to_roman().'''
        for num_arabic, num_roman in __TEST_MAP__:
            self.assertEqual(roman.to_roman(num_arabic), num_roman,
                             f'{num_arabic} should be {num_roman}')

    def test_to_roman_errors(self):
        '''Test invalid numbers in to_roman().'''
        self.assertRaises(roman.OutOfRangeError, roman.to_roman, 100000)
        self.assertRaises(roman.NotIntegerError, roman.to_roman, '1')

    def test_from_roman(self):
        '''Test valid Roman numerals from_roman().'''
        for num_arabic, num_roman in __TEST_MAP__:
            self.assertEqual(roman.from_roman(num_roman), num_arabic,
                             f'{num_roman} should be {num_arabic}')

    def test_from_roman_errors(self):
        '''Test invalid strings in from_roman().'''
        for bad_string in __NOT_ROMAN__:
            self.assertRaises(
                roman.InvalidRomanNumeralError, roman.from_roman, bad_string)
