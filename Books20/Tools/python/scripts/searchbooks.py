#! /usr/bin/env python
# -*- mode: Python;-*-
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/scripts/searchbooks.py
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
'''Search the ajb??_books.xml and aaa??_books.xml files for
a particular string


Class inputs:
   a bookfile
   search categories
   search parameters
     and, or, not  ?

Class output
   a bookfile


Fields

HumanName (last, first, middle, 
author
editors
AuthorEditor
translator
compiler
contributers
AllPeople

Strings
ajbnum
title
comments
place
publisher
keywords

Date
publication date (year)

tasks
  contains  # strings 'contain' other strings
  numeric       # numbers|dates can be = != >= > <= <
  date

Field.task='string' [logical 


Command Line/Config file Arguments
standard arg
AJB/AAA locations
search string  area=string

output  a bookfile object, use ajbbooks to display

what if the entry is a reference
    print both? need to search for an AJBnum


reverse lookup to catch references
for every file in AAA and AJB
  search fields
  if found or reference
     add to book file
'''
from pprint import pprint
import configargparse as argp

import aabooks.lib.utils as aautils
from aabooks.ajbbook import bookfile as bf

__VERSION__ = 'v1.0.0'

__DESCRIPTION__ = '''Search AJB or AAA XML files for a particular search
term and return an XML file with the found entries'''

#
# Parse the command line arguments
#
def getargs():
    '''Parse the command line arguments.'''
    parser = argp.ArgumentParser(description=__DESCRIPTION__,
                                 default_config_files=['~/.config/Books20/searchbooks.conf'])
                                 
    aautils.standard_parser_args(parser)

    parser.add_argument('--search-term', '-s',
                        help='a logical string',
                        type=str,
                        default='Title.contains="stars"')
    
    parser.add_argument('files',
                        nargs='*')

    return parser.parse_known_args()[0]

class SearchBooks():
    '''A class to consolidate the search functions to search book files
    with AJB and AAA entries.'''

    def __init__(self, **kwargs):
        '''Set up the class structure'''

        self.bookfile = bf.BookFile()
        self.search = ''
        self.files = []

        self.set_header()

    def set_header(self):
        '''Write all relevant information to the books file header,
        date/time
        files
        search terms

        '''
    def clear_file(self):
        '''Clear self.bookfile of previous entries.

        '''
    def search(self):
        '''Perform the search with the search terms on the files'''

        for afile in self.files:
            new_entries = self.search_file(afile, self.search)
            
def main():
    '''Search the files'''

    args = getargs()
    pprint(args)

##
## Do the work
##
if __name__ == '__main__':

    main()

