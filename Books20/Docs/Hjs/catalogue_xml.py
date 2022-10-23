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

Intro
  Who, what, where, when, how

\bkentry{1930}{Eddington, Arthur}
{The Internal Constitution of Stars}
{Cambridge, Cambridge University Press}
{18 x 26.25 cm, x, 407 pp, 5 figs, 48 tables}
{BEA 134; DSB 2:337; DeV 1140}

TODO:

  indent year place publisher
  pick better font for catalogue entries
  use \vbox for both entry and comments to prevent page breaks in comments
  add sensible page count, do not use my codes for page counts
  use Roman numerals for preface page counts
  determine proper order of comments
   series
   books notes
    laid in, edition, etc.
   binding
   dedication
   bookplate
   library stamp
   signature/initials
   ISBN
  remove "ownership" words

'''
import sys
from pprint import pprint

from aabooks.ajbbook import bookfile as bf
from aabooks.lib import utils as aautils

import configargparse as argp

from nameparser.config import CONSTANTS
CONSTANTS.initials_format='{first} {middle}'

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


def protect(raw_str):
    '''Protect the LaTeX special characters that we want to print.

    '''

    new_str = raw_str.replace(r"&", r'\&')
    return new_str

def sort_bookfile(bookfile, sort_flag):
    '''Use the sort flag to determine how to sort the bookfile.

    '''

    if sort_flag:
        # sort the bookfile
        print(f'sorting bookfile by {sort_flag}')
        bookfile.sort(sort_name=sort_flag)

def print_header(bookfile, outf=sys.stdout):
    '''Print the leading material for the catalogue.

    drop the \newcommand and write the commands out directly
    in a \vbox so we don't get a page break in the middle of
    a listing.

    Alternatively have a 5 entry for comments
    '''
    header = protect(r'''%%
%% \bkentry{year}{author}  #1 #2
%% {title}       #3
%% {publishing}  #4
%%
\newcounter{bksctr}

\newcommand{\bkentry}[4]{%
 \stepcounter{bksctr}
 \vbox{%
  \vspace*{0.5 cm}
  \noindent
  \hbox{{\footnotesize\arabic{bksctr}} {\it #2} {\bf #3}\hfil}\\
  \hbox{ #1  #4 \hfil}
 }
}

''')
    print(header, file=outf)

def make_name_string(hname, name_style='first'):
    '''Make the name string in the desired style from a HumanName
    object. There are two forms of each style determine by the
    presence of a first name or a first initial.  The different is the
    ~ tie for LaTeX.

    first -- Last, First MI.
    first -- Last, FI.~MI.

    second -- First MI., Last
    second -- FI.~MI., Last

    '''

    initials = hname.initials()

    if 'first' in name_style:
        name = f'{hname.last}'
        if initials:
            name += f', {initials}'
    elif 'second' in name_style:
        name = f'{initials} {hname.last}'
    else:
        name = r''


    return name.strip()


def get_author_string(entry):
    '''Create an author/editor string from an entry.

    '''

    #return 'Author, A.~N.~and A.~N.~Editor'

    authors = entry['Authors']
    editors = entry['Editors']
    ret_str = ''

    if len(authors):
        # first author
        ret_str = make_name_string(authors[0], name_style='first')
        if len(authors) > 2:
            ret_str += ', et.~al.'
        elif len(authors) == 2:
            ret_str += ' and ' + make_name_string(authors[1], name_style='second')
    elif len(editors):
        # first editor
        ret_str = make_name_string(editors[0])
        if len(editors) > 2:
            ret_str += ', et.~al., eds'
        elif len(editors) == 2:
            ret_str += ' and ' + make_name_string(editors[1], name_style='second') + ', eds.'
        else:
            ret_str += ', ed.'

    if ret_str:
        # Only add this comma if the name string is not empty
        # otherwise the title is preceeded by a single comma
        ret_str += ','
    return ret_str


def print_entry(count, entry, outf=sys.stdout):
    '''Print an entry as number 'count' for the catalogue. These are
    expected to be of the form AJBEntry.

    '''
    year = str(entry['Year'])
    title = entry['Title'].split(';')[0]
    # Get only the first publisher, if there is one listed.
    try:
        place = entry['Publishers'][0]['Place'].split('-')[0]
    except IndexError:
        place = ''
    try:
        publisher = ', ' + entry['Publishers'][0]['PublisherName']
    except IndexError:
        publisher = ''

    if not year and publisher:
        year = r''

    author = get_author_string(entry)

    tex_entry = protect(r'\bkentry{' + year + r'}{' + author + '}{' \
        + title + '}{' \
        + place + publisher + '}')

    print(tex_entry, file=outf)
    print(file=outf)
    for comment in entry['Others']:
        print(protect(comment), file=outf)
        print(file=outf)

    print(entry.num_str(), file=outf)
    print(file=outf)

def print_closing(bookfile, outf=sys.stdout):
    '''Print any closing material for the catalogue.

    '''
    print('Printing the closing material for the catalogue', file=outf)


def main():
    '''Do all the work here

    '''
    args = get_args()
    if args.verbose:
        pprint(args)

    with open(args.output, 'w') as filep:

        bookf = bf.BookFile()
        bookf.read_file(args.input)

        # sort bookfile
        if args.sort:
            bookf.sort_by(args.sort)

        print_header(bookf, outf=filep)
        for count, ent in enumerate(bookf):
            try:
                print_entry(count+1, ent, outf=filep)
            except Exception as e:
                pprint(e)
                print('problem with entry:', count + 1)
                pprint(ent)
        print_closing(bookf)

    filep.close()

#
#
#
if __name__ == '__main__':

    main()
