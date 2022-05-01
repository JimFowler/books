#! /usr/bin/env python
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/lib/roman.py
##
##   Part of the Books20 Project
##
##   Copyright 2018 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrieval system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright

'''.. py:module:: aaroman

Introduction
____________

Roman numerals are a numbering system, developed in ancient Rome,
which were used extensively until the late middle ages at which time
they were gradually replaced by Arabic numbers. Roman numerals are
still used today although there is no standardized methodology for
their use and never has been, even in ancient Rome.  Usage today has
been established by general practice over a number of centuries
although there are still multiple usages in place today. A good
introduction with many additional references can be found in the
`Wikepedia <https://en.wikipedia.org/wiki/Roman_numerals>`_ on Roman
Numerals.

In the fields of writing, publishing, and reading the use
of Roman numberals is still common. For example, they are used in
preface or front matter page numbering and page counts. They are used
in suffixes of names or titles. They are also used in numbering
planetary satellites, eg, Titan is also called Saturn VI.

This module utilizes the 'modern' interpretation of Roman
numerals. Numbers are restricted to between 1-4999 inclusive; we use
IV instead of IIII and CD instead of CCCC. This may be expanded to
alternate usage styles in the future if we find publishers or authors
who use such alternate styles.

Description
___________

A regular expression shown below is used to determine if a string is a valid
Roman numeral.

.. code-block:: python

  import re

  romanNumeralPattern = re.compile("""
    ^                   # beginning of string
    M{0,4}              # thousands - 0 to 4 M's
    (CM|CD|D?C{0,3})    # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 C's),
                        #            or 500-800 (D, followed by 0 to 3 C's)
    (XC|XL|L?X{0,3})    # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 X's),
                        #        or 50-80 (L, followed by 0 to 3 X's)
    (IX|IV|V?I{0,3})    # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 I's),
                        #        or 5-8 (V, followed by 0 to 3 I's)
    $                   # end of string
    """ ,re.VERBOSE)

In addition three exception classes are defined and returned by
``toRoman()`` and ``fromRoman()`` in the event of an error.  These
exceptions are ``OutOfRangeError`` returned from ``toRoman()`` if the
argument is not between 1 and 4999 inclusive, ``NotIntegerError``
returned by ``toRoman()`` if the argument is not an integer type, and
``InvalidRomanNumeralError`` returned by ``fromRoman()`` if the string
is not a valid Roman numeral.

The function ``isRoman()`` returns True or False.

Original Source
_______________

This code was lifted from the roman.py package, v3.2, maintained by
Mark Pilgim and available on `PyPi <https://pypi.org/project/roman>`_.
I have added the ``isRoman()`` function.

The original header from his file is given below.


  This program is part of "Dive Into Python", a free Python tutorial for
  experienced programmers.  Visit http://diveintopython.org/ for the
  latest version.  [NOTE: the diveintopython.org domain no longer exists
  as of 2020-04-28 when I last checked.]

  This program is free software; you can redistribute it and/or modify
  it under the terms of the Python 2.1.1 license, available at
  http://www.python.org/2.1.1/license.html


Functions and Exceptions
________________________

'''

import re


class RomanError(Exception):
    '''The base class for the Roman numeral conversion module.'''

class OutOfRangeError(RomanError):
    '''The argument passed in is not between 1 and 4999 inclusive.'''

class NotIntegerError(RomanError):
    '''The argument passed in is not an integer.'''

class InvalidRomanNumeralError(RomanError):
    '''The string argument is not a valid Roman numeral.'''


#Define digit mapping
__roman_numeral_map = tuple(zip(
    ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I'),
    (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
))


#Define pattern to detect valid Roman numerals
roman_numeral_pattern = re.compile("""
    ^                   # beginning of string
    M{0,4}              # thousands - 0 to 4 M's
    (CM|CD|D?C{0,3})    # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 C's),
                        #            or 500-800 (D, followed by 0 to 3 C's)
    (XC|XL|L?X{0,3})    # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 X's),
                        #        or 50-80 (L, followed by 0 to 3 X's)
    (IX|IV|V?I{0,3})    # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 I's),
                        #        or 5-8 (V, followed by 0 to 3 I's)
    $                   # end of string
    """, re.VERBOSE)


def is_roman(roman_str):
    """test to verify if a string is a roman numeral."""

    if not roman_str or not roman_numeral_pattern.search(roman_str):
        return False

    return True


def to_roman(number):
    """convert integer to Roman numeral"""

    if not isinstance(number, int):
        raise NotIntegerError("decimals can not be converted")
    if not -1 < number < 5000:
        raise OutOfRangeError("number out of range (must be 0..4999)")

    # special case
    if number == 0:
        return 'N'

    result = ""
    for numeral, integer in __roman_numeral_map:
        while number >= integer:
            result += numeral
            number -= integer
    return result


def from_roman(roman_str):
    """convert Roman numeral to integer"""
    if not roman_str:
        raise InvalidRomanNumeralError('Input can not be blank')

    # special case
    if roman_str == 'N':
        return 0

    if not roman_numeral_pattern.search(roman_str):
        raise InvalidRomanNumeralError(f'Invalid Roman numeral: {roman_str}')

    result = 0
    index = 0
    for numeral, integer in __roman_numeral_map:
        while roman_str[index:index+len(numeral)] == numeral:
            result += integer
            index += len(numeral)
    return result


#
# Unit tests also taken from Mark Pilgrim
#
if __name__ == '__main__':

    import unittest

    TEST_MAP = ((1, 'I'), (3, 'III'), (4, 'IV'), (9, 'IX'), (10, 'X'),
                (14, 'XIV'), (19, 'XIX'), (24, 'XXIV'), (40, 'XL'),
                (49, 'XLIX'), (90, 'XC'), (99, 'XCIX'), (100, 'C'),
                (400, 'CD'), (490, 'CDXC'), (499, 'CDXCIX'), (500, 'D'),
                (900, 'CM'), (990, 'CMXC'), (998, 'CMXCVIII'),
                (999, 'CMXCIX'), (1000, 'M'), (2013, 'MMXIII'))

    NOT_ROMAN = ('AA', 'mxvi', 'MMaVI', '', 'SPQR', 'MMXiii', 'MXCD')

    class RomanNumberTestCase(unittest.TestCase):
        '''Run the unit tests for Roman number functions.'''

        def test_is_roman(self):
            '''Test valid strings in is_roman().'''
            for _, num_roman in TEST_MAP:
                self.assertTrue(is_roman(num_roman),
                                f'"{num_roman}" should be a valid Roman')

        def test_is_roman_errors(self):
            '''Test invalid strings in is_roman().'''
            for bad_string in NOT_ROMAN:
                self.assertFalse(is_roman(bad_string),
                                 f'"{bad_string}" should not be Roman')

        def test_to_roman(self):
            '''Test valid numbers in to_roman().'''
            for num_arabic, num_roman in TEST_MAP:
                self.assertEqual(to_roman(num_arabic), num_roman,
                                 f'{num_arabic} should be {num_roman}')

        def test_to_roman_errors(self):
            '''Test invalid numbers in to_roman().'''
            self.assertRaises(OutOfRangeError, to_roman, 100000)
            self.assertRaises(NotIntegerError, to_roman, '1')

        def test_from_roman(self):
            '''Test valid Roman numerals from_roman().'''
            for num_arabic, num_roman in TEST_MAP:
                self.assertEqual(from_roman(num_roman), num_arabic,
                                 f'{num_roman} should be {num_arabic}')

        def test_from_roman_errors(self):
            '''Test invalid strings in from_roman().'''
            for bad_string in NOT_ROMAN:
                self.assertRaises(
                    InvalidRomanNumeralError, from_roman, bad_string)


    unittest.main()
