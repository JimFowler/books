#! /usr/bin/env python3
# -*- mode: Python;-*-
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/scripts/catalogue_xml.py
##
##   Part of the Books20 Project
##
##   Copyright 2022 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrival system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright
'''Make a catalogue from an XML bookfile.  Choose what order to list
the books.  Create a LaTeX file for processing. Catalogue should look like

'''
import sys
from pprint import pprint

import configargparse as argp
from nameparser.config import CONSTANTS

from aabooks.lib import utils as aautils
from aabooks.ajbbook import bookfile as bf
import hjsentry

CONSTANTS.initials_format='{first}{middle}'

__VERSION__ = '2.0'

__DESCRIPTION__ = 'Create or edit an ajb??_books.xml file'
#
# Parse the command line arguments
#
def get_args():
    """Parse the command line arguments."""

    parser = argp.ArgumentParser(description=__DESCRIPTION__,
                                 default_config_files=['~/.config/Books20/ajbbooks.conf'])

    aautils.standard_parser_args(parser)

    sort_choices = ['Title', 'Author', 'Year', 'Place', 'Publisher']
    parser.add_argument('-s', '--sort', type=str,
                        metavar='SORT_FLAG',
                        choices= sort_choices,
                        default='',
                        help=f'sort the bookfile, (default None) Available choices {sort_choices}')

    parser.add_argument('-o', '--output', type=str,
                        default=sys.stdout,
                        metavar='OUTPUT',
                        help='write the file OUTPUT for entries  (default stdout)')

    parser.add_argument('input', type=str,
                        help='read the file INPUT for entries')

    return parser.parse_known_args()[0]


def sort_bookfile(bookfile, sort_flag):
    '''Use the sort flag to determine how to sort the bookfile.

    '''

    if sort_flag:
        # sort the bookfile
        print(f'sorting bookfile by {sort_flag}')
        bookfile.sort(sort_name=sort_flag)

def main():
    '''Do all the work here

    '''
    args = get_args()
    if args.verbose:
        pprint(args)

    hjs_entry = hjsentry.HjsEntry()

    with open(args.output, 'w', encoding = 'UTF8') as filep:
        authp = open('author2.idx', 'w', encoding = 'UTF8')
        bookf = bf.BookFile()
        bookf.read_file(args.input)

        # sort bookfile
        if args.sort:
            bookf.sort_by(args.sort)

        hjs_entry.print_header(outf=filep)
        for count, ent in enumerate(bookf, start=1):
            try:
                hjs_entry.print_entry(count, ent, authp, outf=filep)
            except [KeyError, ValueError] as exp:
                pprint(exp)
                print('problem with entry:', count)
                pprint(ent)
        hjs_entry.print_closing()

    filep.close()

#
#
#
if __name__ == '__main__':

    main()
