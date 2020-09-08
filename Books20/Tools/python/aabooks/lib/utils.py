## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/lib/utils.py
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
'''Utility functions that may be used in various programs.'''

import re

from nameparser import HumanName

__reg3__ = re.compile(r'([AJB]{0,1})(\d+)\.(\d+)(\((\d+)\))*\.(\d+)([a-c]{0,1})', re.UNICODE)

# Should use namesparser here
def make_name_list(line, sep=' and '):
    """Returns a list of object of class HumanName. See the package
    nameparser for full info. The names have the following possible keys
    "Title", "First", "Middle", "Last", and "Suffix"
    """
    name_list = []
    names = line.split(sep)

    for name in names:
        clean_name = HumanName(name.strip())
        name_list.append(clean_name)

    return name_list

def make_name_str(name_list, sep=' and '):
    """Returns a string built from a list of HumanName objects.
    See the package nameparser for details about HumanName.
    """
    name_str = ''
    if not name_list:
        return name_str

    first = True
    for name in name_list:
        if not first:
            name_str += sep
        first = False
        name_str += str(name)

    return name_str

def standard_parser_args(parser):
    '''The configuration flags that every program should use.  This
    function is in the Books20 library utils.py and should be called
    after creating the parser.  This function may be used with either
    the argparse or configargparse packages.

    '''

    parser.add_argument('--version',
                        help='show the version information and exit',
                        default=False,
                        action='store_true')
    try:
        # use only with configargparser
        parser.add_argument('-c', '--config-path',
                            is_config_file=True,
                            metavar='CONF',
                            help='path to the alternate configuration file.')
    except TypeError:
        pass

    parser.add_argument('--verbose',
                        help='be noisy about our actions',
                        default=False,
                        action='store_true')

    parser.add_argument('--debug',
                        help='turn on debugging information',
                        default=False,
                        action='store_true')

    return parser

def parse_ajbnum(line):
    """Get the Volume, Section, any possible subSection, and the
    section entry number.  The subSection defaults to zero
    if no subSection value exists. Returns a dictionary with the
    AJB number elements {'volume': 'AJB', 'volNum': int, 'sectionNum': int,
    'subsectionNum': int, 'entryNum': int, 'entrySuf': ''}.
    """
    #
    # This regular expression is used to parse the AJB number
    # which is of the form
    # [AJB ]volNum.sectionNum[(subsectionNum)].entryNum[entrySuf], where
    # the AJB, subsectionNum, and entrySuf are optional
    # e.g. 66.18(1).25a. It returns the list [empty, empty, 66,
    # 18, (1), 1, 25, 'a', empty].  Note
    # that the subsectionNum may not be there in which case both
    # item 4 and 5 will be empty strings and the subsection number defaults
    # to zero.
    #

    nums = __reg3__.split(line.strip())

    if len(nums) != 9:
        print('Bad AJB number {}\n'.format(line))
        return {}

    if not nums[0]: # volume
        nums[0] = 'AJB'

    if not nums[5]: # subsectionNum
        nums[5] = 0

    if not nums[7]: # entrySuf
        nums[7] = ''

    return {'volume': nums[0],
            'volNum': int(nums[2]),
            'pageNum': -1,
            'sectionNum': int(nums[3]),
            'subsectionNum': int(nums[5]),
            'entryNum': int(nums[6]),
            'entrySuf': nums[7],
            }



if __name__ == '__main__':

    import unittest

    class UtilsTestCase(unittest.TestCase):
        '''Test cases for aabooks/lib/utils.py.'''

        def setUp(self):
            '''Set things up for every test.'''

        def tearDown(self):
            '''Clean up the mess after every test.'''

        def test_a_make_name_func(self):
            '''Test make_name_list().'''

            name_str = '''A. B. Author and C. D. Next sj and D. E. Brother'''
            test_name_list = make_name_list(name_str)
            test_name_str = make_name_str(test_name_list)
            self.assertEqual(test_name_str, name_str)

        def test_b_parse_ajbnum(self):
            '''test the parse_ajb() function.'''

            # test a good value
            # testa bad value
            # test AAA value?


    unittest.main()
