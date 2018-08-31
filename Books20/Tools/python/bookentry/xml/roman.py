#! /usr/bin/env python
'''roman.py - convert integers to/from Roman numerals

Utilize the 'modern' interpretation of Roman numerals. There is much
inconsistency in the use of Roman numberal well into the late Middle
Ages.

Found at http://code.activestate.com/recipes/81611-roman-numerals/
submitted by din385

30 May 2016

'''


NUMERAL_MAP = tuple(zip(
    (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
    ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
))

def int_to_roman(i):
    '''Convert an integer to a Roman numeral string'''
    result = []
    for integer, numeral in NUMERAL_MAP:
        count = i // integer
        result.append(numeral * count)
        i -= integer * count
    return ''.join(result)


def roman_to_int(num):
    '''Convert a string of Roman numerals to an integer.'''
    i = result = 0
    for integer, numeral in NUMERAL_MAP:
        while num[i:i + len(numeral)] == numeral:
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


    print('   i,     Roman,  Arabic')
    for d in range(1, 21):
        convert(d)

    for d in range(88, 132):
        convert(d)

    convert(932)

    print('This is one of the longest Roman numbers...')
    convert(8888)
    print('...obviously numbers above 4000 or so do not work well in the Roman sytem.')

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
    as in CXAAAIII which could be read as 110 or perhaps 113''')
    print('roman_to_int() returns:', roman_to_int('CXAAAIII'))

