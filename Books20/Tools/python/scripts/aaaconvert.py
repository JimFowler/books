#! /usr/bin/env python3
# -*- mode: Python;-*-
#
# Begin copyright
#
#  /home/jrf/Documents/books/Books20/Tools/python/aaaconvert.py
#
#   Part of the Books20 Project
#
#   Copyright 2020 James R. Fowler
#
#   All rights reserved. No part of this publication may be
#   reproduced, stored in a retrival system, or transmitted
#   in any form or by any means, electronic, mechanical,
#   photocopying, recording, or otherwise, without prior written
#   permission of the author.
#
#
# End copyright
#
"""Convert aaannsmm.txt files to aaann_books.xml files for use
with ajbbooks.py and other xml parsers.
"""
import sys
import os
import argparse
import itertools

from aabooks.ajbbook import bookfile
from aabooks.ajbbook import ajbentry

from pprint import pprint

__version__ = '1.0'

#
# Parse the command line arguments
#
def getargs():
    """Parse the command line arguments."""
    
    parser = argparse.ArgumentParser(description='''Convert an aaa??s??.txt to an aaa??_books.xml file''')

    parser.add_argument('-V', '--version',
                        help='provide version info,',
                        action='store_true')

    parser.add_argument('--verbose',
                        help='provide useful info,',
                        action='store_true')

    parser.add_argument('filename',
                        type=str,
                        action='store',
                        help='read the file INPUT for entries')

    args = parser.parse_args()


    return args


def aaanum(num, numstr):
    pass


#
# The main body
#

def main():
    """Set up the windows and start the event loop for aaacovert."""
    args = getargs()

    if args.verbose:
        pprint(args)

    # set up required data structures and variables
    bf = bookfile.BookFile()
    tmp_entry = ajbentry.AJBentry()
    with open(args.filename, 'r', encoding='ISO-8859-1') as f:
        lines = f.readlines()
        count = 0
        for l in lines:
            count += 1
            elements = l.strip().split('|')


            # convert the list of elements to a dictionary
            del elements[0]
            element_dict = dict(itertools.zip_longest(*[iter(elements)] * 2, fillvalue=""))

            # convert element dictionary to a AJBentry
            tmp_entry.blank_entry()

            try:
                tmp_entry['Year'] = element_dict['y']
            except KeyError:
                pass
            
            try:
                tmp_entry['Title'] = element_dict['t']
            except KeyError:
                pass
            
            try:
                tmp_entry._parse_ajbnum(element_dict['n'])
            except KeyError:
                pass
                
            if count < 10:
                pass
                #print('printing elements dict')
                #print(element_dict)
                #pprint(elements)
                #pprint(tmp_entry)


    print('length of bookfile', len(bf._entry_list))
#
# Main work
#
if __name__ == '__main__':

    main()

def temp():
    elements = ['a',
                'G._A._Partel (ed.)',
                't',
                '''Space engineering. Proceedings of the Second International Conference on Space Engineering, held at the Fondazione Giorgio Cini, Isola di San Giorgio, Venice, Italy, May 7_-_10, 1969.''',
                's',
                'Astrophys. Space Sci. Libr. (Dordrecht (Netherlands): D. Reidel), Vol._15, '
                '11_+_728_p.',
                'y',
                '1970',
                'k',
                'Proceedings, Colloquia, Congresses, Meetings, Symposia',
                'n',
                'AAA003.012.007']


    pprint(elements)
    pprint([iter(elements)])
    pprint(*[iter(elements)])
    pprint(zip(*[iter(elements)] * 2))
    for z1, z2 in zip(*[iter(elements)] * 2):
        print(z1, z2)
