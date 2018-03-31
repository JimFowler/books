#! /usr/bin/env python
#
# Create Astronomy and Space Science table list
# from the file of titles.  This allows us to change the table
# if we desire.
#
#
from __future__ import print_function

import table as tb
from asslKluwerList import *

def assl_print_books(book_list):
    for volnum, title_list, year, author_list in book_list:
        len_title = len(title_list)
        len_author = len(author_list)
        max_loops = max(len_title, len_author, 1)

        raw_str = r''
        
        # Do first line
        for index in range(1, max_loops+1):
            if volnum is not None:
                raw_str += r'''  {0} & '''.format(volnum)
                volnum = None
            else:
                raw_str += r'''  & '''

            if len_title >= index:
                raw_str += r'''\bt{}{}{} & '''.format('{', title_list[index-1], '}')
            else:
                raw_str += r''' & '''

            if len_author >= index:
                raw_str += r'''{} & '''.format(author_list[index-1])
            else:
                raw_str += r''' & '''

            if year is not None:
                raw_str += r'''{} \\'''.format(year)
                year = None
            else:
                raw_str += r''' \\'''

            raw_str += '''
'''
        # Clean up for TeX and print() statement
        raw_str2 = raw_str.replace( r'. ', r'.\ ')
        safe_str = tb.protect_str(raw_str2)
        # if more title and/or more authors
        print(safe_str)
    return

def assl_print_table():
    # get table format, caption, label, column headings, continuation headings
    # and possible footers and continuation footers
    # from this list
    #
    tb.print_table_comment(tbl_comment)
    tb.print_table_copyright(tbl_copyright)
    tb.print_table_start( tbl_format)

    tb.print_table_caption( tbl_caption )
    tb.print_table_label( tbl_label )
    tb.print_table_heading( 4, tbl_heading, continue_label)
    tb.print_table_footer(tbl_footer, continue_footer)

    assl_print_books(assl_book_list)
    tb.print_table_end()

if __name__ == '__main__':
    assl_print_table()
    
