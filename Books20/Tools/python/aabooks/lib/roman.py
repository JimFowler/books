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

'''Roman numerals are a numbering system, developed in ancient Rome,
which were used extensively until the late middle ages at which time
they were gradually replaced by Arabic numbers. Roman numerals are
still used today although there is no standardized methodology for
their use and never has been, even in ancient Rome.  Usage today has
been established by general practice over a number of centuries
although there are still multiple usages in place today. A good
introduction with many additional references can be found at
`Wikepedia <https://en.wikipedia.org/wiki/Roman_numerals>`_.

In the fields of astronomical writing, publishing, and reading the use
of Roman numberals is still common. For example, they are used in
preface or front matter page numbering and page counts. They are used
in suffixes of names or titles. They are also used in numbering
planetary satellites, eg, Titan is also called Saturn VI.

This module utilizes the 'modern' interpretation of Roman
numerals. Numbers are restricted to between 1-3999 inclusive; we use
IV instead of IIII and CD instead of CCCC. This may be expanded to
alternate usage styles if we find publishers or authors who use
such alternate styles

'''

import re


'''
The regular expression for finding Roman numerals was taken from
http://pages.cs.wisc.edu/~zeyuan/projects/notes/diveintopython/chap7.html

pattern = """
    ^                 # beginning of string
    M{0,4}            # thousands - 0 to 4 M's
    (CM|CD|D?C{0,3})  # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 C's),
                      #            or 500-800 (D, followed by 0 to 3 C's)
    (XC|XL|L?X{0,3})  # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 X's),
                      #        or 50-80 (L, followed by 0 to 3 X's)
    (IX|IV|V?I{0,3})  # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 I's),
                      #        or 5-8 (V, followed by 0 to 3 I's)
    $                 # end of string
"""
This regular expression for finding Roman numerals was taken from
https://stackoverflow.com/questions/267399/how-do-you-match-only-valid-roman-numerals-with-a-regular-expression
'''
Roman_Pattern = '''
    (^               # beginning of string
    (?=[MDCLXVI])    # must contain one or all of these characters,
                     # no empty strings
    M*               # thousands - however many you want,
                     #             though 4000 is the lagest Roman number in use
    (C[MD]|D?C{0,3}) # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 C's),
                     #            or 500-800 (D, followed by 0 to 3 C's)
    (X[CL]|L?X{0,3}) # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 X's),
                     #        or 50-80 (L, followed by 0 to 3 X's)
    (I[XV]|V?I{0,3}) # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 I's),
                     #        or 5-8 (V, followed by 0 to 3 I's)
    $)                # end of string
'''
RomanNumeral_re = re.compile(Roman_Pattern, re.VERBOSE|re.IGNORECASE)


NUMERAL_MAP = tuple(zip(
    (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
    ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
))

def is_roman_numeral(test):
    '''Return True if 'test' matches the regular expression'''
    if RomanNumeral_re.match(test):
        return True

    return False

def find_roman_numerals(instr):
    return []

'''

Found at http://code.activestate.com/recipes/81611-roman-numerals/
submitted by din385

Last read on 30 May 2016
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

    def convert(input_numeral):
        '''Converts an integer to a Roman numeral and back again.
        We print all the values so the user can check for validity'''

        roman_numeral = int_to_roman(input_numeral)
        arabic_numeral = roman_to_int(roman_numeral)

        print('%4d, %9s, %4d' % (input_numeral, roman_numeral, arabic_numeral))

    def test_convert():
        for test_number in range(1,4000):
            roman_numeral = int_to_roman(test_number)
            arabic_number = roman_to_int(roman_numeral)
            if arabic_number != test_number:
                print('Conversion failed: {} does not match {} or {}'.format(test_number, arabic_number, roman_numeral))


            

    print('   i,     Roman,  Arabic')
    for d in range(1, 21):
        convert(d)

    for d in range(88, 132):
        convert(d)

    convert(932)

    print('This is one of the longest Roman numbers...')
    convert(8888)
    print('...obviously numbers above 4000 or so do not work well in the Roman system.')

    # test floating point values (should fail)
    print('\nUsing a floating point number like 10.4 should fail...')
    try:
        convert(10.4)
    except TypeError as exc:
        print('...and it does with error:', str(exc))
    else:
        print('...but it does not.')


    # Test non-Roman characters
    print('''\nroman_to_int() quits after finding a non-Roman character
    as in CXAAAIII which could be read as 110 but perhaps 113 if we ignore
    the 'AAA' string''')
    print('roman_to_int() returns:', roman_to_int('CXAAAIII'))

    print('''Note that roman_to_int() will accept an 'illegal' roman
    numeral such as MDDCXI which returns as''', roman_to_int('MDDCXI'))

    print(RomanNumeral_re.match(''))
    print(RomanNumeral_re.match('AMCX'))
    print(RomanNumeral_re.match('mcX'))
    print(RomanNumeral_re.match(int_to_roman(8888)))
    for r in RomanNumeral_re.finditer('MCX CX'):
        print(r)

    test_convert()

