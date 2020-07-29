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

# pylint: disable=invalid-name

class RomanError(Exception):
    '''The base class for the Roman numeral conversion module.'''

class OutOfRangeError(RomanError):
    '''The argument passed in is not between 1 and 4999 inclusive.'''

class NotIntegerError(RomanError):
    '''The argument passed in is not an integer.'''

class InvalidRomanNumeralError(RomanError):
    '''The string argument is not a valid Roman numeral.'''


#Define digit mapping
__romanNumeral_Map = tuple(zip(
    ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I'),
    (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
))


#Define pattern to detect valid Roman numerals
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
    """, re.VERBOSE)


def isRoman(s):
    """test to verify is a string is a roman numeral."""

    if not s or not romanNumeralPattern.search(s):
        return False

    return True


def toRoman(n):
    """convert integer to Roman numeral"""

    if not isinstance(n, int):
        raise NotIntegerError("decimals can not be converted")
    if not -1 < n < 5000:
        raise OutOfRangeError("number out of range (must be 0..4999)")

    # special case
    if n == 0:
        return 'N'

    result = ""
    for numeral, integer in __romanNumeral_Map:
        while n >= integer:
            result += numeral
            n -= integer
    return result


def fromRoman(s):
    """convert Roman numeral to integer"""
    if not s:
        raise InvalidRomanNumeralError('Input can not be blank')

    # special case
    if s == 'N':
        return 0

    if not romanNumeralPattern.search(s):
        raise InvalidRomanNumeralError('Invalid Roman numeral: %s' % s)

    result = 0
    index = 0
    for numeral, integer in __romanNumeral_Map:
        while s[index:index+len(numeral)] == numeral:
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

    class TestRoman(unittest.TestCase):
        '''Run the unit tests for Roman number functions.'''

        def test_isRoman(self):
            '''Test valid strings in isRoman().'''
            for _, num_roman in TEST_MAP:
                self.assertTrue(isRoman(num_roman),
                                '"%s" should be a valid Roman' % (num_roman))

        def test_isRoman_errors(self):
            '''Test invalid strings in isRoman().'''
            for s in NOT_ROMAN:
                self.assertFalse(isRoman(s),
                                 '"%s" should not be Roman' % (s))

        def test_toRoman(self):
            '''Test valid numbers in toRoman().'''
            for num_arabic, num_roman in TEST_MAP:
                self.assertEqual(toRoman(num_arabic), num_roman,
                                 '%s should be %s' % (num_arabic, num_roman))

        def test_toRoman_errors(self):
            '''Test invalid numbers in toRoman().'''
            self.assertRaises(OutOfRangeError, toRoman, 100000)
            self.assertRaises(NotIntegerError, toRoman, '1')

        def test_fromRoman(self):
            '''Test valid Roman numerals fromRoman().'''
            for num_arabic, num_roman in TEST_MAP:
                self.assertEqual(fromRoman(num_roman), num_arabic,
                                 '%s should be %s' % (num_roman, num_arabic))

        def test_fromRoman_errors(self):
            '''Test invalid strings in fromRoman().'''
            for s in NOT_ROMAN:
                self.assertRaises(
                    InvalidRomanNumeralError, fromRoman, s)


    unittest.main()
