## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/ajbbook/inv94entry.py
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
'''
A class definition for the HJS 1994 inventory entry. The class was
modified from the HjsEntry class

'''
import sys
from nameparser.config import CONSTANTS
from aabooks.ajbbook import catentry

CONSTANTS.initials_format='{first} {middle}'

class InvEntry(catentry.CatEntry):
    '''A class to create a HJS 1994 inventoryentry from an AJBEntry (see
    ajbbook/ajbentry.py). An inventory entry is for the Harlan
    J. Smith catalogue in the McDonald Observatory Library.

    '''
    def __init__(self):
        '''Set up the class entities if any.'''
        super().__init__()

    def print_header(self, outf=sys.stdout):
        '''Print the leading material for the catalogue.

        '''
        header = self.protect(r'\newcounter{invctr}')
        print(header, file=outf)


    def print_closing(self, outf=sys.stdout):
        '''Print any closing material for the catalogue.

        '''
        print('Printing the closing material for the catalogue', file=outf)

    def print_entry(self, count, entry, authidx, outf=sys.stdout):
        '''Print an entry as number 'count' for the catalogue. These are
        expected to be of the form AJBEntry.

        '''

        tex_entry = self.protect(r'''\stepcounter{invctr}
\vbox{%
  \vspace*{0.5 cm}
  \noindent
 ''')

        # add reference label
        # make the Author, Title line
        author = self.get_author_string(entry)

        title = entry['Title']

        tex_entry += r''' \hypertarget{entry94:''' + str(count)
        tex_entry += r'''}{\footnotesize \theinvctr} ''' + author
        tex_entry += r''' \textsc{\bfseries ''' + title + r'''}'''

        print(self.protect(tex_entry), file=outf)
        print(file=outf)

        # Create author index entries here
        if entry['Authors']:
            for author in entry['Authors']:
                output = r'\indexentry{' + self.make_name_string(author)
                output += r'|myhref}{' + f'{count}' + r'}'
                print(self.protect(output), file=authidx)
        if entry['Editors']:
            for author in entry['Editors']:
                output = r'\indexentry{' + self.make_name_string(author)
                output += r'|myhref}{' f'{count}' + r'}'
                print(self.protect(output), file=authidx)
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
            pages = self.make_pagination_str(pagination)
        except KeyError:
            pages = ''

        if year or place or publisher or pages:
            if not year:
                year=r'\hspace{3em}'
            else:
                year += r'\hspace{0.5em}'
            if not place:
                place = r'\hspace{5em}'
            if publisher and pages:
                page_comma = ','
            else:
                page_comma = ''

            year_pub_entry = ' '.join([year, place, publisher]) + page_comma + pages

            print(self.protect(year_pub_entry), file=outf)
            print(file=outf)

        try:
            edition = entry['Edition']
            if edition:
                print(self.protect(self.make_edition(edition)), file=outf)
                print(file=outf)
        except KeyError:
            pass

        for comment in entry['Others']:
            if 'HJS 01' in comment or \
               'missing' in comment or \
               'series' in comment:
                clean_com = self.clean_comment(comment)
                print(self.protect(clean_com), file=outf)
                print(file=outf)
        print(r'''}

''', file=outf)
