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
##   reproduced, stored in a retrival system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright

'''
.. py:module:: aaroman

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

In the fields of astronomical writing, publishing, and reading the use
of Roman numberals is still common. For example, they are used in
preface or front matter page numbering and page counts. They are used
in suffixes of names or titles. They are also used in numbering
planetary satellites, eg, Titan is also called Saturn VI.

This module utilizes the 'modern' interpretation of Roman
numerals. Numbers are restricted to between 1-3999 inclusive; we use
IV instead of IIII and CD instead of CCCC. This may be expanded to
alternate usage styles in the future if we find publishers or authors
who use such alternate styles.


This regular expression for finding Roman numerals was taken from
`stackoverflow.com <https://stackoverflow.com/questions/267399/how-do-you-match-only-valid-roman-numerals-with-a-regular-expression>`_.

.. code-block:: python

  import re

  Roman_Match = """
      ^                # beginning of string
      (?=[MDCLXVI])    # must contain one or all of these characters,
                       # no empty strings
      M{0,3}           # thousands -  3999 is the largest Roman number in use
      (C[MD]|D?C{0,3}) # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 C's),
                       #            or 500-800 (D, followed by 0 to 3 C's)
      (X[CL]|L?X{0,3}) # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 X's),
                       #        or 50-80 (L, followed by 0 to 3 X's)
      (I[XV]|V?I{0,3}) # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 I's),
                       #        or 5-8 (V, followed by 0 to 3 I's)
      $                # end of string
  """
  RomanNumeral_match = re.compile(Roman_Pattern, re.VERBOSE|re.IGNORECASE)

'''

import re

Roman_Match = '''
    ^                # beginning of string
    (?=[MDCLXVI])    # must contain one or all of these characters,
                     # no empty strings
    M{0,3}           # thousands -  3999 is the lagest Roman number in use
    (C[MD]|D?C{0,3}) # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 C's),
                     #            or 500-800 (D, followed by 0 to 3 C's)
    (X[CL]|L?X{0,3}) # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 X's),
                     #        or 50-80 (L, followed by 0 to 3 X's)
    (I[XV]|V?I{0,3}) # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 I's),
                     #        or 5-8 (V, followed by 0 to 3 I's)
    $                # end of string
'''

# Doesn't work yet...
Roman_Find = '''
    (^               # beginning of string
    (?=[MDCLXVI])    # must contain one or all of these characters,
                     # no empty strings
    M{0,3}           # thousands -  3999 is the lagest Roman number in use
    (C[MD]|D?C{0,3}) # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 C's),
                     #            or 500-800 (D, followed by 0 to 3 C's)
    (X[CL]|L?X{0,3}) # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 X's),
                     #        or 50-80 (L, followed by 0 to 3 X's)
    (I[XV]|V?I{0,3}) # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 I's),
                     #        or 5-8 (V, followed by 0 to 3 I's)
    $)               # end of string
'''

RomanNumeral_match = re.compile(Roman_Match, re.VERBOSE|re.IGNORECASE)
RomanNumeral_find = re.compile(Roman_Find, re.VERBOSE|re.IGNORECASE)


NUMERAL_MAP = tuple(zip(
    (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
    ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
))


def is_roman_numeral(test_str):
    '''Return True if 'test_str' matches the Roman Numeral regular
    expression given above.'''
    if RomanNumeral_match.match(test_str):
        return True

    return False

def find_roman_numerals(test_str):
    '''Find a list of all the Roman Numerals in the test_str. If there are
    none, then an empty list is returned.

    '''
    print('''find_roman_numerals: input string '{}' '''.format(test_str))
    return RomanNumeral_find.finditer(test_str)


''' The conversion between Arabic and Roman numerals was found at
`activestate.com <http://code.activestate.com/recipes/81611-roman-numerals/>`_
submitted by din385. Last read on 30 May 2016
'''
def int_to_roman(i):
    '''Convert an integer to a Roman numeral string'''
    result = []
    for integer, numeral in NUMERAL_MAP:
        count = i // integer
        result.append(numeral * count)
        i -= integer * count
    return ''.join(result)


def roman_to_int(roman):
    '''Convert a string of Roman numerals to an integer.'''

    if not is_roman_numeral(roman):
        return None
    
    i = result = 0
    for integer, numeral in NUMERAL_MAP:
        while roman[i:i + len(numeral)] == numeral:
            result += integer
            i += len(numeral)
    return result



if __name__ == '__main__':

    from pprint import pprint
    import argparse

    parser = argparse
    
    def convert(input_numeral):
        '''Converts an integer to a Roman numeral and back again.
        We print all the values so the user can check for validity'''

        roman_numeral = int_to_roman(input_numeral)
        arabic_numeral = roman_to_int(roman_numeral)

        print('%4d, %9s, %4d' % (input_numeral, roman_numeral, arabic_numeral))

    def test_conversion():
        for test_number in range(1,4000):
            roman_numeral = int_to_roman(test_number)
            arabic_number = roman_to_int(roman_numeral)
            if arabic_number != test_number:
                print('Conversion failed: {} does not match {} or {}'.format(test_number, arabic_number, roman_numeral))


            
    '''
    print('   i,     Roman,  Arabic')
    for d in range(1, 21):
        convert(d)

    for d in range(88, 132):
        convert(d)

    convert(932)

    print('This is one of the longest Roman numbers...')
    convert(8888)
    print('...obviously numbers above 4000 or so do not work well in the Roman system.')
    '''
    
    print('\nTrying to convert a floating point number like 10.4 should fail...')
    try:
        int_to_roman(10.4)
    except TypeError as exc:
        print('...and it does with TypeError:', str(exc))
    else:
        print('...but it does not!')


    # Test non-Roman characters
    print('''\nThe function roman_to_int() fails if it finds a non-Roman character,
    as in {0} which could be read as 110 but perhaps 113 if we ignore
    the 'AAA' string\n    roman_to_int({0}) returns: {1}'''.format('CXAAAIII', roman_to_int('CXAAAIII')))

    print('''\nNote that roman_to_int() will not accept an 'illegal' roman
    numeral such as MDDCXI which returns as '{}' although it might be 
    interpreted in some system as 2111.'''.format(roman_to_int('MDDCXI')))

    print(RomanNumeral_match.match(''))
    print(RomanNumeral_match.match('MMCCXV'))
    print(RomanNumeral_match.match('mcX'))

    
    print('\nTesting the find function')
    r = find_roman_numerals('MCCXXIII')
    pprint(r)
    for r in  find_roman_numerals('MCCXXIII'):
        pprint(r)

    test_conversion()

