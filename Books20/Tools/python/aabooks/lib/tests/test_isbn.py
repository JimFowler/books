#! /usr/bin/env python
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/lib/test/test_isbn.py
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
'''Test the isbn.py module for consistence'''
import unittest
from aabooks.lib import isbn


# still missing a checksum of 8
__ISBN10_LIST__ = [
    ('0-8357-0331', '2'), ('0-08-024620', '6'), ('3-540-09830', '5'),
    ('0-387-09830', '5'), ('3-540-09831', '3'), ('0-387-09831', '3'),
    ('0-292-75507', '4'), ('0-8243-0917', '0'), ('0-521-22285', '0'),
    ('0-262-02137', '4'), ('0-471-04492', 'X'), ('0-7167-1006', '4'),
    ('0-7167-1062', '5'), ('3-12-983890', '2'), ('3-12-983840', '6'),
    ('0-442-30215', '0'), ('0-442-30216', '9'), ('0-89490-027', '7'),
    ('0-7188-2433', '4'), ('3-519-02346', '6'), ('90-277-1001', '5'),
    ('90-277-1044', '9'), ('90-277-0957', '2'), ('90-277-0997', '1'),
    ('0-85264-244', 'X'), ('0-201-05674', '7'), ('0-444-85115', '1'),
    ('0-444-85266', '2'), ('0-444-85267', '0'), ('0-19-851462', 'X'),
    ('0-387-90369', '0'), ('3-540-90369', '0'), ('0-19-857553', 'X'),
    ('0-471-04815', '1'), ('3-411-01570', '5'), ('3-528-17236', '3'),
    ('3-528-17214', '2'), ('3-211-81430', '2'), ('0-387-81430', '2'),
    ('3-211-81475', '2'), ('0-387-81475', '2'), ('0-86008-258', 'X'),
    ('2-01-003860', '6'), ('0-86961-109', '7'), ('0-444-41802', '4'),
    ('0-08-026341', '0'), ('0-08-026342', '9'),
]

__ISBN13_LIST__ = [
    ('978-1-62040-593-', '2'), ('978-0-691-15271-', '4'),
    ('978-0-521-38200-', '7'), ('978-1-137-28008-', '4'),
    ('978-0-262-04318-', '2'), ('978-0-06-236359-', '6'),
    ('978-0-375-42429-', '8'), ('978-0-670-01695-', '2'),
    ('978-1-61614-739-', '6'), ('978-1-61636-023-', '8'),
    ('978-1-250-09896-', '2'), ('978-0-684-83252-', '4'),
    ('978-0-8229-4552-', '9'), ('978-1-108-47154-', '1'),
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

        for isbntest, csum in __ISBN10_LIST__:
            err_msg = f'{isbntest + "0"} should have checksum {csum}'
            self.assertEqual(isbn.checksum_10(isbntest + '0'), csum, err_msg)

    def test_b_checksum_13(self):
        '''Test checksum_13() function.'''

        for isbntest, csum in __ISBN13_LIST__:
            err_msg = f'{isbntest + "0"} should have checksum {csum}'
            self.assertEqual(isbn.checksum_13(isbntest + '0'), csum, err_msg)
