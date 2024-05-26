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
'''Make a catalogue entry from an ajbentry. We can create a number of
different catalogue entries.

'''
from aabooks.lib import roman

class Comma():
    '''Add a comma and a space unless first_comma is True'''

    def __init__(self, first_text='', other_text=', '):
        '''Initialize the class variables.'''
        self.first_comma = True
        self.first_text = first_text
        self.other_text = other_text

    def test(self):
        '''Test the value of first_comma and return the
        appropriate string.

        '''
        if self.first_comma:
            self.first_comma = False
            ret_str = self.first_text
        else:
            ret_str = self.other_text

        return ret_str

    def reset_first(self):
        '''Reset the value of first_comma.'''
        self.first_comma = True


class CatEntry():
    '''A generic class to create a catalogue entry from an AJBEntry (see
    ajbbook/ajbentry.py). This is used as a base class for specific
    catalogue entry formats.

    This generic class may be unnecessary as it does not provide anything
    in common with the child classes except a definition.

    '''
    def __init__(self):
        '''Set up the class variables.'''

    def protect(self, raw_str):
        '''Protect the LaTeX special characters that we want to print.

        '''

        new_str = raw_str.replace(r'&', r'\&')
        new_str = new_str.replace(r'$', r'\$')
        return new_str

    def make_name_string(self, hname, name_style='first'):
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

    def get_author_string(self, entry):
        '''Create an author/editor string from an entry.

        '''

        authors = entry['Authors']
        editors = entry['Editors']
        ret_str = ''

        if len(authors):
            # first author
            ret_str = r'''\textit{'''
            ret_str += self.make_name_string(authors[0], name_style='first')
            ret_str += r'}'
            if len(authors) > 2:
                ret_str += r', et.\,al.'
            elif len(authors) == 2:
                ret_str += r' and \textit{'
                ret_str += self.make_name_string(authors[1], name_style='second')
                ret_str += '}'
        elif len(editors):
            # first editor
            ret_str = r'''\textit{'''
            ret_str += self.make_name_string(editors[0])
            ret_str += r'}'
            if len(editors) > 2:
                ret_str += r', et.\,al., eds.'
            elif len(editors) == 2:
                ret_str += r' and \textit{'
                ret_str += self.make_name_string(editors[1], name_style='second')
                ret_str += r'}, eds.'
            else:
                ret_str += ', ed.'

        if ret_str:
            # Only add this comma if the name string is not empty
            # otherwise the title is preceeded by a single comma
            ret_str += ','

        return ret_str

    def make_edition(self, edition):
        '''Create a proper string for the edition number.  i.e. 1^{st},
        2^{nd}, 11^{th}, 101^{st}, etc. This should be able to handle
        any edition number. 'edition' may be a string, int, or float.

        '''

        ed_num = int(edition)
        end_digit = str(ed_num)[-1]
        #if ed_num == 11 or ed_num == 12 or ed_num == 13:
        if ed_num in (11, 12, 13):
            suffix = 'th'
        elif '1' in end_digit:
            suffix = 'st'
        elif '2' in end_digit:
            suffix = 'nd'
        elif '3' in end_digit:
            suffix = 'rd'
        else:
            suffix = 'th'

        return r'\Ord{' + str(ed_num) + '}{' + suffix + '} ' + 'edition'

    def make_pagination_str(self, pagination):
        '''Create a clean and neat pagination string given a string
        of the form 12pp+235p+12P+... as defined in pagination_xml.py

        '''
        pages = ''
        page_counts = pagination.split('+')
        comma = Comma(first_text=r'\hspace{1em}', other_text=', ')

        for page in page_counts:
            if 'pp' in page:
                pg_count = int(page.split('pp')[0])
                pages += comma.test() + roman.to_roman(pg_count).lower()
            elif 'p' in page:
                # there should alway be one of these page counts
                pg_count = page.split('p')[0]
                pages += comma.test() + str(pg_count) + r'\,pp'
            elif 'P' in page:
                pg_count = page.split('P')[0]
                pages += comma.test() + str(pg_count) + r'\,plates'
            elif 'c' in page:
                pg_count = page.split('c')[0]
                pages += comma.test() + str(pg_count) + r'\,charts'
            elif 'I' in page:
                pg_count = page.split('I')[0]
                pages += comma.test() + str(pg_count) + r'p\,index'
            elif 'AA' in page:
                pg_count = page.split('AA')[0]
                pages += comma.test() + str(pg_count) + r'p\,app.\,A'
            elif 'AB' in page:
                pg_count = page.split('AB')[0]
                pages += comma.test() + str(pg_count) + r'p\,app.\,B'
            elif 'AC' in page:
                pg_count = page.split('AC')[0]
                pages += comma.test() + str(pg_count) + r'p\,app.\,C'
            elif page:
                print(page)
            else:
                pass

        return pages

    def clean_comment(self, comment):
        '''Clean up the quotes in my comments from the XML files with
        good LateX quotes.

        Should this be added to self.protect()?

        '''
        cleaned = comment.replace(' "', ' ``')

        return cleaned
