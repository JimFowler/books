#! /usr/bin/env python3
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Docs/Wjm/convert_cvs.py
##
##   Part of the Books20 Project
##
##   Copyright 2023 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrival system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright
'''Convert the WJ_McDonald_library_sorted.csv file to wjm_books.xml
file.  This is in preparation for creating a LaTeX/pdf catalogue for
the William J. McDonald book collection in the McDonald library.

'''
import sys
from pprint import pprint

import csv

import configargparse as argp
from nameparser.config import CONSTANTS

from aabooks.lib import utils as aautils
from aabooks.ajbbook import bookfile as bf
from aabooks.ajbbook import ajbentry as ajbent

__VERSION__ = '1.0'

__DESCRIPTION__ = 'Create an ajb??_books.xml file from a *.csv file'

#
# Parse the command line arguments
#
def get_args():
    """Parse the command line arguments."""

    parser = argp.ArgumentParser(description=__DESCRIPTION__,
                                 default_config_files=['~/.config/Books20/wjm.conf'])

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

def main():
    '''The main() function does all the work of converting the CSV file to
    an XML file.

    '''

    args = get_args()
    if args.verbose:
        pprint(args)

    bookf = bf.BookFile()
    bookf.set_header('''The William J. McDonald Book collection
at the McDonald Observatory.

Save as Unicode UTF-8 encoding

''')
    # open csv file and create a reader
    with open(args.input) as csvfile:
        creader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # for each row in csv
        for row in creader:
            if creader.line_num < 2:
                continue
            #
            myid, shelf, mid, title, authors, city, publ, cdate, edition, prt, page, comments = row
            #   convert to ajbentry
            aent = ajbent.AJBentry()
            aent['Num']['volume'] = 'WJM'
            aent['Num']['volNum'] = 1
            aent['Num']['sectionNum'] = 1
            aent['Num']['entryNum'] = int(myid)
            aent['Num']['pageNum'] = 1
            if title:
                aent['Title'] = title
            else:
                aent['Title'] = 'previous entry'
            aent['Year'] = str(cdate)
            aent['Pagination'] = page
            aent['Edition'] = edition
            aent['Publishers'].append({'Place': str(city), 'PublisherName': str(publ)})
            if comments:
                aent['Others'].append(comments)
            aent['Others'].append('Authors: ' + authors)
            aent['Others'].append('shelf mark: ' + str(shelf))
            aent['Others'].append('M num: ' + str(mid))
            if prt:
                aent['Others'].append('printing: ' + str(prt))
            
            #   add to bookf
            bookf.set_new_entry(aent)
        csvfile.close()

    # write bookf
    bookf.set_filename(args.output)
    bookf.write_file_xml()
        
##
## Do the main work
##
if __name__ == '__main__':

    main()
