#! /usr/bin/env python
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/lib/isbn.py
##
##   Part of the Books20 Project
##
##   Copyright 2021 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrival system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright
'''Some useful utility functions for working with ISBN numbers
that are not supplied in the module isbnlib.

https://isbnsearch.com/search?s=0-667-02340-5
  will return the book's information if this is a valid ISBN
'''

from math import fmod
import isbnlib as isbn

#
# for ISBN-10 the checksum is calculated by
# ISBN-10 is of the form a-bcd-efghi-j
# checksum is j =  remainder of ([abcdefghi] x [123456789]) MOD 11
# Valid results are '0'-'9' and 'X'
#
isbn10_mults = [1, 2, 3, 4, 5, 6, 7, 8, 9]
def checksum_10(isbnlike):
    '''Calculate the proper ISBN-10 check sum for a test ISBN 10
    string. The input string must be 10 legal characters with or
    without dashes but the checksum character need not be valid.

    Return a string character of the checksum digit or 'X'

    '''

    isbndigits = isbn.canonical(isbnlike)

    tmp_sum = 0
    for num, value in zip(isbn10_mults, isbndigits[:9]):
        tmp_sum += num * int(value)

    chksum = int(fmod(tmp_sum, 11))

    if chksum == 10:
        return 'X'
    return str(chksum)


#
# ISBN-13 is of the form abc-def-ghijkl-m (where abc will usually be 978 or 979)
# checksum is m = 10 - the remainder of ([abcdefghiklm] x [131313131313]) MOD 10
# Valid results are '0'-'9'
#
isbn13_mults = [1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3]
def checksum_13(isbnlike):
    '''Calculate the proper ISBN-13 check sum for a test ISBN 13
    string. The input string must have 13 legal characters with or
    without dashes but the checksum character need not be valid.

    Return a string character of the checksum digit.

    '''

    isbndigits = isbn.canonical(isbnlike)

    tmp_sum = 0
    for num, value in zip(isbn13_mults, isbndigits[:12]):
        tmp_sum += num * int(value)
    return str(int(10 - fmod(tmp_sum, 10)))

#
# Generate a checksum for either a 10 or 13 digit ISBN
#
def checksum(isbnlike):
    '''Calculate the proper ISBN-check sum for a test ISBN
    string. The input string must have 10 or 13 legal characters with or
    without dashes but the checksum character need not be valid.

    Return a string character of the checksum digit.

    '''
    isbndigits = isbn.canonical(isbnlike)
    isbnlen = len(isbndigits)
    # get length, choose 10 or 13 checksum
    if isbnlen == 10:
        chksum = checksum_10(isbndigits)
    elif isbnlen == 13:
        chksum = checksum_13(isbndigits)
    else:
        return None

    return chksum


#
#
#
if __name__ == '__main__':

    import sys
    import argparse

    # check for command line argument.  Run checksum rather
    # than unit tests

    parser = argparse.ArgumentParser(description='parse and validate ISBN values')
    parser.add_argument('isbn',
                        type=str,
                        help='''An ISBN value to test''',
                        default='',
                        nargs='?')

    args = parser.parse_args()

    if args.isbn:
        cksum = checksum(args.isbn)
        if cksum is None:
            print('This ISBN value', args.isbn, 'does not seem to be a proper value')
        else:
            print('The proper ISBN checksum is', cksum)
    sys.exit()
