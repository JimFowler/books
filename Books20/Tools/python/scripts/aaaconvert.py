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
import re

from nameparser import HumanName

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


def parse_authors(entry, author_str):
    '''Parse the author/editor string and place the result in the AJBentry
    entry. If this is a single editor, then (ed.) will be at the end
    of the string. If there are multiple editors, then (eds.) will be
    at the end of the string. Names are separated by spaces with all
    but the last name having a trailing comma. Initials and last names
    are separated by an underbar.  These names need to go in the
    Author or Editor field of the AJBentry.

    '''

    names = author_str.split(' ')

    if names[-1] == '(ed.)' or names[-1] == '(eds.)':
        field = entry['Editors']
        names.pop(-1)
    else:
        field = entry['Authors']
        
    namelist = []
    for name in names:
        rname = name.replace('_', ' ').strip(',')
        namelist.append(HumanName(rname))

    field.extend(namelist)
        
def parse_title(entry, title_str):
    '''Parse the title string and add to entry['Title'].

    '''

    entry['Title'] = title_str.replace('.', ';').rstrip(';')
    
def parse_publishing(entry, pub_str):
    '''Place the source information in the comment field
    for now.  Parse by hand unless we can work out how to
    parse this string automatically.

    '''
    entry['Others'].append(pub_str)
    

def parse_year(entry, year_str):
    '''Parse the copyright year from the year string and
    put in entry['Year'].

    '''

    entry['Year'] = int(year_str)

    
def parse_keywords(entry, keyword_str):
    '''Parse the keywords from the keyword_str and
    put into the new entry['keywords'].  Need to add keywords
    to the definition of AJBentry.

    '''

    entry['keywords'] = [] # XXX removed this when keywords added to AJBentry
    keywords = keyword_str.split(' ')
    for k in keywords:
        entry['keywords'].append(k.strip(','))

aaa_re = re.compile(r'^AAA(\d+)\.(\d+)\.(\d+)([a-c]{0,1})$')
def parse_aaanum(entry, num_str):
    '''Parse the AAA number out of numstr and put the parts
    into entry['Num'].

    '''

    items = aaa_re.split(num_str)
    num = entry['Num']
    num['volume'] = 'AAA'
    num['volNum'] = int(items[1])
    num['sectionNum'] = int(items[2])
    num['subsectionNum'] = 0
    num['entryNum'] = int(items[3])
    num['entrySuf'] = items[4]

def parse_j_key(entry, j_str):
    pass

def parse_m_key(entry, m_str):
    entry['Others'].append(m_str)

def parse_b_key(entry, b_str):
    entry['Others'].append(b_str)

def parse_l_key(entry, l_str):
    entry['Others'].append(pub_str)

def parse_plus_key(entry, plus_str):
    entry['Others'].append(plus_str)


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
    
    
    with open(args.filename, 'r', encoding='ISO-8859-1') as f:
        lines = f.readlines()
        count = 0
        for l in lines:
            count += 1
            tmp_entry = ajbentry.AJBentry()
            tmp_entry['OrigStr'] = l
            
            # convert the line to a dictionary
            elements = l.strip().split('|')

            # convert the list of elements to a dictionary
            del elements[0]
            element_dict = dict(itertools.zip_longest(*[iter(elements)] * 2, fillvalue=""))

            # convert element dictionary by keys to an AJBentry
            for key in element_dict.keys():
                #print('key is', key)

                if key == 'a':
                    parse_authors(tmp_entry, element_dict['a'])

                elif key == 't':
                    parse_title(tmp_entry, element_dict['t'])
            
                elif key == 's':
                    parse_publishing(tmp_entry, element_dict['s'])

                elif key == 'y':
                    parse_year(tmp_entry, element_dict['y'])
                    
                elif key == 'k':
                    parse_keywords(tmp_entry, element_dict['k'])
                                   
                elif key == 'n':
                    parse_aaanum(tmp_entry, element_dict['n'])

                elif key == 'j':
                    parse_j_key(tmp_entry, element_dict['j'])
                    
                elif key == 'm':
                    parse_m_key(tmp_entry, element_dict['m'])
                    
                elif key == 'b':
                    parse_b_key(tmp_entry, element_dict['b'])
                    
                elif key == 'l':
                    parse_l_key(tmp_entry, element_dict['l'])
                    
                elif key == '+':
                    parse_plus_key(tmp_entry, element_dict['+'])
                    
                else:
                    print('Unknown key: {}'.format(key))
                    print(l)
                    
            bf.set_new_entry(tmp_entry)


    bname = os.path.basename(args.filename)
    fname, ext = os.path.splitext(bname)
    bf.write_file_xml(fname + '.xml')
    
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
