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


def parse_authors(author_str):
    pass

def parse_title(title_str):
    pass

def parse_publishing(pub_str):
    pass

def parse_year(year_str):
    pass

def parse_keywords(keyword_str):
    pass

def parse_aaanum(numstr):
    pass

def parse_j_key(j_str):
    pass

def parse_m_key(m_str):
    pass

def parse_b_key(b_str):
    pass

def parse_l_key(l_str):
    pass

def parse_plus_key(plus_str):
    pass


#
# The main body
#

def main():
    '''For every line in the file, create a dictionary of key - keyvalue.
    Then parse the dictionary and convert the fields to an AJBentry type.
    Added the temporary entry to a bookfile list. Finally write the bookfile
    as an XML file of the form aaaXXXsYYY.xml.

    '''
    
    args = getargs()

    if args.verbose:
        pprint(args)

    # set up required data structures and variables
    # generate the output file name and add to bf.
    bf = bookfile.BookFile()
    tmp_entry = ajbentry.AJBentry()
    
    with open(args.filename, 'r', encoding='ISO-8859-1') as f:
        lines = f.readlines()
        count = 0
        for l in lines:
            count += 1

            # convert the line to a dictionary
            elements = l.strip().split('|')


            # convert the list of elements to a dictionary
            del elements[0]
            element_dict = dict(itertools.zip_longest(*[iter(elements)] * 2, fillvalue=""))

            # convert element dictionary to a AJBentry
            tmp_entry.blank_entry()

            # Parse the elements of the dictionary
            for key in element_dict.keys():
                #print('key is', key)

                if key == 'a':
                    parse_authors(element_dict['a'])

                elif key == 't':
                    parse_title(element_dict['t'])
            
                elif key == 's':
                    parse_publishing(element_dict['s'])

                elif key == 'y':
                    parse_year(element_dict['y'])
                    
                elif key == 'k':
                    parse_keywords(element_dict['k'])
                                   
                elif key == 'n':
                    parse_aaanum(element_dict['n'])

                elif key == 'j':
                    parse_j_key(element_dict['j'])
                    
                elif key == 'm':
                    parse_m_key(element_dict['m'])
                    
                elif key == 'b':
                    parse_b_key(element_dict['b'])
                    
                elif key == 'l':
                    parse_l_key(element_dict['l'])
                    
                elif key == '+':
                    parse_plus_key(element_dict['+'])
                    
                else:
                    print('Unknown key: {}'.format(key))
                    print(l)
                    


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
