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
'''

from math import fmod
import isbnlib as isbn

#
# for ISBN-10 the checksum is calculated by
# ISBN-10 is of the form a-bcd-efgh-i
# checksum is i =  remainder of ([abcdefghi] x [123456789]) MOD 11
# Valid results are '0'-'9' and 'X'
#
def checksum_10(isbnlike):
    '''Calculate the proper ISBN-10 check sum for a test ISBN 10
    string. The input string must be 10 legal characters with or
    without dashes but the checksum character need not be valid.

    Return a string character of the checksum digit or 'X'

    '''

    isbndigits = isbn.canonical(isbnlike)

    tmp_sum = 0
    for num, value in enumerate(isbndigits[:9]):
        tmp_sum += (num + 1) * int(value)

    chksum = int(fmod(tmp_sum, 11))

    if chksum == 10:
        return 'X'
    return str(chksum)


#
# ISBN-13 is of the form abc-def-ghiklm-n (where abc will usually be 978 or 979)
# checksum is n = 10 - the remainder of ([abcdefghiklm] x [131313131313]) MOD 10
# Valid results are '0'-'9'
#
isbn13mults = [1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3]
def checksum_13(isbnlike):
    '''Calculate the proper ISBN-13 check sum for a test ISBN 13
    string. The input string must have 13 legal characters with or
    without dashes but the checksum character need not be valid.

    Return a string character of the checksum digit.

    '''

    isbndigits = isbn.canonical(isbnlike)

    tmp_sum = 0
    for num, value in zip(isbn13mults, isbndigits[:12]):
        tmp_sum += num * int(value)
    return str(10 - fmod(tmp_sum, 10))

#
#
#
if __name__ == '__main__':

    import unittest

    # missing a checksum of 8 still
    isbn10_list = [
    ('0-8357-0331', '2'),
    ('0-08-024620', '6'),
    ('3-540-09830', '5'),
    ('0-387-09830', '5'),
    ('3-540-09831', '3'),
    ('0-387-09831', '3'),
    ('0-292-75507', '4'),
    ('0-8243-0917', '0'),
    ('0-521-22285', '0'),
    ('0-262-02137', '4'),
    ('0-471-04492', 'X'),
    ('0-7167-1006', '4'),
    ('0-7167-1062', '5'),
    ('3-12-983890', '2'),
    ('3-12-983840', '6'),
    ('0-442-30215', '0'),
    ('0-442-30216', '9'),
    ('0-89490-027', '7'),
    ('0-7188-2433', '4'),
    ('3-519-02346', '6'),
    ('90-277-1001', '5'),
    ('90-277-1044', '9'),
    ('90-277-0957', '2'),
    ('90-277-0997', '1'),
    ('0-85264-244', 'X'),
    ('0-201-05674', '7'),
    ('0-444-85115', '1'),
    ('0-444-85266', '2'),
    ('0-444-85267', '0'),
    ('0-19-851462', 'X'),
    ('0-387-90369', '0'),
    ('3-540-90369', '0'),
    ('0-19-857553', 'X'),
    ('0-471-04815', '1'),
    ('3-411-01570', '5'),
    ('3-528-17236', '3'),
    ('3-528-17214', '2'),
    ('3-211-81430', '2'),
    ('0-387-81430', '2'),
    ('3-211-81475', '2'),
    ('0-387-81475', '2'),
    ('0-86008-258', 'X'),
    ('2-01-003860', '6'),
    ('0-86961-109', '7'),
    ('0-444-41802', '4'),
    ('0-444-41803', '2'),
    ]

    # check valid and invalid checksum values
    class ISBNTestCase(unittest.TestCase):
        '''The test suite for isbn.py.'''

        def setUp(self):
            '''Set up for the tests.'''

        def tearDown(self):
            '''Tear down for the next test.'''

        def test_a_checksum_10(self):
            '''Test checksum_10() function.'''

            for isbntest, chksum in isbn10_list:
                self.assertEqual(checksum_10(isbntest + '0'), chksum)

        def test_b_checksum_13(self):
            '''Test checksum_13() function.'''

            self.skipTest('checksum_13() tests are not defined yet.')

    unittest.main()
