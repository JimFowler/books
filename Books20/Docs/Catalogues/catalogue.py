#! /usr/bin/env python
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Data/HJS/catalogue.py
##
##   Part of the Books20 Project
##
##   Copyright 2022 James R. Fowler
##
##   All rights reserved. No part of this publ
##   reproduced, stored in a retrival system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright
"""Create a catalog of books from a BookFile XML list
"""
import os
import configargparse as argp

from pprint import pprint

from aabooks.ajbbook import bookfile as bf
import aabooks.lib.utils as aautils


__DESCRIPTION__ = '''Create a TeX catalogue of entries from a BookFile'''

def get_args():
    """Parse the command line arguments."""
    parser = argp.ArgumentParser(description=__DESCRIPTION__,
                                 default_config_files=['~/.config/Books20/ajbbooks.conf'])
                                 
    aautils.standard_parser_args(parser)
    
    parser.add_argument('-f', '--format', type=str,
                        choices = ['short', 'long'],
                        help='use this as the format, choices "short" or "long")')

    parser.add_argument('input', type=str,
                        help='read the file INPUT for entries')

    return parser.parse_known_args()[0]


def protect_str(raw_str):
    '''Make a TeX string with \ and {} safe for
    python print().

    '''

    raw_str.replace(r"\\", r'\\\\')
    raw_str.replace(r'&', r'\\&')
    
    return raw_str


def add_commands():
    '''The definition of the book entry TeX command..'''
        
    command = r'''%% A counter to keep track of the books
\newcounter{bksctr}

%%
%% The short title bibliography entry
%%    problems with long title, multiple authors, and multiple publishers
%%
%%  \shrtentry{Author}{Title}{Place}{Publisher}{Year}
%%
\newcommand{\shrtentry}[5]{
\stepcounter{bksctr}
\noindent
{\bf\arabic{bksctr}} #1 {\itshape #2} #3: #4 #5\newline
}

%%
%% \bkentry{year}{author}  #1 #2
%% {title}       #3
%% {publishing}  #4
%% {description} #5
%% {references}  #6
%%
\newcommand{\bkentry}[4]{
\stepcounter{bksctr}
\vspace*{1 cm}
\noindent
\hbox{{\bf\arabic{bksctr}  #2, }}
\hbox{{\itshape \large #3\hfil}}\newline
\hbox{#4, #1 \hfil}\newline
\hbox{Comments:\hfil}\newline
}

%%\hbox{#5\hfil}\newline
%%\hbox{#6\hfil}\newline

\setcounter{bksctr}{0}
'''
    safe_str = protect_str(command)
    #print(command)
    print(safe_str)




def print_short_entry(entry):
    '''Print the TeX string for an entry'''

    try:
        year = entry['Year']
    except:
        year = ''

    title = entry['Title']
    title = title.split(';')[0] + ','

    pub = entry['Publishers'][0]
    #pprint(pub[0])
    try:
        place = pub['Place']
        publisher = pub['PublisherName'] +','
    except:
        pub = ''
        place = ''
        publisher = ''

        # Generate Author or Editor (or both?)
    if entry.not_empty('Authors'):
        name = entry['Authors'][0]
        aux_name = r','
    elif entry.not_empty('Editors'):
        name = entry['Editors'][0]
        aux_name = r' ed.,'
    else:
        author = r''
        name = r''
        aux_name = r''

    if name and name.last:
        author = name.last
        if name.first:
            author = r'' + author + ', ' + name.first
        if name.middle:
            author = r'' + author + ' ' + name.middle
        if name.suffix:
            author = r'' + author + ' ' + name.suffix
    
    author = protect_str(author + aux_name)
    
    # need one { to escape the TeX { and a final third { for the format string
    print('\n\\',  end='')
    print(f'shrtentry{{{author}}}{{{title}}}{{{place}}}{{{publisher}}}{{{year}}}')



def print_long_entry(entry):
    '''Print the TeX string for an entry'''
    
    year = entry['Year']
    title = protect_str(entry['Title'])
    pagination = protect_str(entry['Pagination'])
    
    # Generate Author or Editor (or both?)
    if entry.not_empty('Authors'):
        name = entry['Authors'][0]
        aux_name = r''
    elif entry.not_empty('Editors'):
        name = entry['Editors'][0]
        aux_name = r' ed.'
    else:
        author = r''
        name = r''
        aux_name = r''

    if name and name.last:
        author = name.last
        if name.first:
            author = r'' + author + ', ' + name.first
        if name.middle:
            author = r'' + author + ' ' + name.middle
        if name.suffix:
            author = r'' + author + ' ' + name.suffix
    
    author = protect_str(author + aux_name)
    
    print('\n\\',  end='')

    # need one { to escape the TeX { and a final third { for the format string
    print(f'bkentry{{{year}}}{{{author}}}{{{title}}}{{{pagination}}}')


def main():
    '''Create a ?_books.tex file of \bkentry lines. This
    file will be included in some catalogue.tex file.'''
    
    args = get_args()

    BookF = bf.BookFile()
    # expect args.input to be a comma separated list later on
    BookF.set_filename(args.input)
    BookF.read_file()

    add_commands()

    for entry in BookF:

        print_short_entry(entry)

            
#
# Main Work
#
if __name__ == '__main__':

    main()
