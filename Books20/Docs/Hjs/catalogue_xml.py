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


TODO:

  really need to make this a class that takes an entry

  pick better font for catalogue entries

  DONE identify bookplates in hjs01_books.xml
  DONE indent year place publisher??
  DONE use \vbox for both entry and comments to prevent page breaks in comments
  DONE add sensible pagination, do not use my codes for page counts
  DONE use Roman numerals for preface page counts
  DONE determine proper order of comments
   edition
   series
   books notes
    laid in, etc.
    dedication
   dust jacket
   binding
   bookplate
   library stamp
   signature/initials
   ISBN
  DONE remove "ownership" words
  DONE print sub-titles
  DONE change 'selbtsverlog' to 'self-published'
  DONE change ' "' to '``' to get TeX quote marks
  DONE add additional space between year and place ?? or add comma

'''
import sys
from pprint import pprint

from aabooks.ajbbook import bookfile as bf
from aabooks.lib import utils as aautils
from aabooks.lib import roman

import configargparse as argp

from nameparser.config import CONSTANTS
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

    '''
    header = protect(r'\newcounter{bksctr}')
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

    authors = entry['Authors']
    editors = entry['Editors']
    ret_str = ''

    if len(authors):
        # first author
        ret_str = r'''\textit{'''
        ret_str += make_name_string(authors[0], name_style='first')
        ret_str += r'}'
        if len(authors) > 2:
            ret_str += ', et.\,al.'
        elif len(authors) == 2:
            ret_str += r' and \textit{'
            ret_str += make_name_string(authors[1], name_style='second')
            ret_str += '}'
    elif len(editors):
        # first editor
        ret_str = r'''\textit{'''
        ret_str += make_name_string(editors[0])
        ret_str += r'}'
        if len(editors) > 2:
            ret_str += ', et.\,al., eds.'
        elif len(editors) == 2:
            ret_str += r' and \textit{'
            ret_str += make_name_string(editors[1], name_style='second')
            ret_str += r'}, eds.'
        else:
            ret_str += ', ed.'

    if ret_str:
        # Only add this comma if the name string is not empty
        # otherwise the title is preceeded by a single comma
        ret_str += ','

    return ret_str

class Comma(object):
    '''Add a comma and a space unless first is True'''
    def __init__(self):
        self.first_comma = True

    def test(self):
        '''Test the value of first_comma and return the
        appropriate string.

        '''
        if self.first_comma:
            self.first_comma = False
            return '\hspace{1em}'
        else:
            return ', '

def make_pagination_str(pagination):
    '''Create a clean and neat pagination string given a string
    of the form 12pp+235p+12P.

    '''

    if not pagination:
        return ''
    
    pages = ''
    page_counts = pagination.split('+')
    comma = Comma()

    for page in page_counts:
        if 'pp' in page:
            pg = int(page.split(r'pp')[0])
            pages += comma.test() + roman.to_roman(pg).lower()
        elif 'p' in page:
            pg = page.split('p')[0]
            pages += comma.test() + str(pg) + '\,pp'
        elif 'P' in page:
            pg = page.split('P')[0]
            pages += comma.test() + str(pg) + '\,plates'
        elif 'c' in page:
            pg = page.split('c')[0]
            pages += comma.test() + str(pg) + '\,charts'
        elif 'I' in page:
            pg = page.split('I')[0]
            pages += comma.test() + str(pg) + 'p index'
        elif 'AA' in page:
            pg = page.split('AA')[0]
            pages += comma.test() + str(pg) + 'p App.\ A'
        elif 'AB' in page:
            pg = page.split('AB')[0]
            pages += comma.test() + str(pg) + 'p App.\ B'
        elif 'AC' in page:
            pg = page.split('AC')[0]
            pages += comma.test() + str(pg) + 'p App.\ C'
        elif page:
            print(page)
        else:
            pass
        
    return pages


def make_edition(edition):
    '''Create a proper string for the edition number.
    i.e. 1^{st}, 2^{nd}, etc. This should be able to handle
    any edition number. edition may be a string, int, or float.
    '''

    ed_num = int(edition)
    ed_digit = str(ed_num)[-1]
    if 11 == ed_num or 12 == ed_num or 13 == ed_num:
        suffix = 'th'
    elif '1' in ed_digit:
        suffix = 'st'
    elif '2' in ed_digit:
        suffix = 'nd'
    elif '3' in ed_digit:
        suffix = 'rd'
    else:
        suffix = 'th'

        
    return '\Ord{' + str(edition) + '}{' + suffix + '} ' + 'edition'

def clean_comment(comment):
    '''Clean up my parsable comments in the XML files
    with good LateX comments.

    These steps will missing quotes at the begining or end
    of a line or followed by a period or comma. Should use a regex.

    '''
    cleaned = comment.replace(' "', ' ``')
    cleaned = cleaned.replace('" ', "'' ")

    return cleaned
    
def print_entry(count, entry, authidx, outf=sys.stdout):
    '''Print an entry as number 'count' for the catalogue. These are
    expected to be of the form AJBEntry.

    '''

    tex_entry = protect(r'''\stepcounter{bksctr}
\vbox{%
  \vspace*{0.5 cm}
  \noindent
  \label{entry:''' + f'{count}' +r'''}
''')

    # add reference label
    # make the Author, Title line
    author = get_author_string(entry)
    
    title = entry['Title']

    tex_entry += r'''  \hypertarget{entry:''' + str(count) + r'''}{\footnotesize\arabic{bksctr}} ''' + author
    tex_entry += r''' \textsc{\bfseries ''' + title + r'''}'''

    print(protect(tex_entry), file=outf)
    print(file=outf)

    # Create author index entries here
    if entry['Authors']:
        for author in entry['Authors']:
            #print(r'\index[author]{' + make_name_string(author) + r'}', file=outf)
            #print(r'\index[author]{' + make_name_string(author) + r'|myentry}', file=outf)
            print(r'\indexentry{' + make_name_string(author) + r'|myhref}{' + f'{count}' + r'}', file=authidx)
    if entry['Editors']:
        for author in entry['Editors']:
            #print(r'\index[author]{' + make_name_string(author) + r'}', file=outf)
            #print(r'\index[author]{' + make_name_string(author) + r'|myentry}', file=outf)
            print(r'\indexentry{' + make_name_string(author) + r'|myhref}{' f'{count}' + r'}', file=authidx)
    # make the Year, Place, Publisher line
    # Get only the first publisher, if there is one listed.
    try:
        place = entry['Publishers'][0]['Place'].split('-')[0]
        if place:
            place += ','
    except IndexError:
        place = ''

    try:
        publisher = entry['Publishers'][0]['PublisherName']
        publisher = publisher.replace('selbstverlag', 'self-published')
    except IndexError:
        publisher = ''

    try:
        year = str(entry['Year'])
    except ValueError:
        year = ''

    try:
        pagination = entry['Pagination']
        pages = make_pagination_str(pagination)
    except KeyError:
        pages = ''
        
    if year or place or publisher or pages:
        if not year:
            year=r'\hspace{3em}'
        else:
            year += '\hspace{0.5em}'
        if not place:
            place = r'\hspace{5em}'
        if publisher and pages:
            page_comma = ','
        else:
            page_comma = ''
        
        year_pub_entry = ' '.join([year, place, publisher]) + page_comma + pages

        print(protect(year_pub_entry), file=outf)
        print(file=outf)

    try:
        edition = entry['Edition']
        if edition:
            print(protect(make_edition(edition)), file=outf)
            print(file=outf)
    except KeyError:
        pass
    
    for comment in entry['Others']:
        clean_com = clean_comment(comment)
        print(protect(clean_com), file=outf)
        print(file=outf)

    print(entry.num_str(), file=outf)
    print(r'''}

''', file=outf)
    
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
        authp = open('author2.idx', 'w')
        bookf = bf.BookFile()
        bookf.read_file(args.input)

        # sort bookfile
        if args.sort:
            bookf.sort_by(args.sort)

        print_header(bookf, outf=filep)
        for count, ent in enumerate(bookf, start=1):
            try:
                print_entry(count, ent, authp, outf=filep)
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
