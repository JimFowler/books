#! /usr/bin/env python
#
# Definition for generic table printing
# function using the LaTeX style longtable
#
#
from __future__ import print_function

import re

def protect_str(raw_str):
    '''Make a TeX string with \ and {} safe for
    python print().

    '''
    
    raw_str.replace(r"\\", r'\\\\')
    return raw_str


def print_table_comment(tbl_comment):
    raw_comment = r'''{}'''.format(tbl_comment)
    safe_comment = protect_str(raw_comment)
    print(safe_comment)
    
def print_table_copyright(tbl_copyright):
    raw_copyright = r'''{}'''.format(tbl_copyright)
    safe_copyright = protect_str(raw_copyright)
    print(safe_copyright)    

def print_table_start(tbl_format):
    raw_format = r'\begin{}{}'.format('{longtable}', tbl_format) 
    safe_format = protect_str(raw_format)
    print( safe_format )

def print_table_caption(tbl_caption):
    raw_caption = r'  \caption{}{}{} \\'.format('{', tbl_caption, '}')
    safe_caption = protect_str(raw_caption)
    print( safe_caption )

def print_table_label(tbl_label):
    raw_label = r'  \label{}{}{} \\'.format('{', tbl_label, '}')
    safe_label = protect_str(raw_label)
    print( raw_label )
    
def print_table_heading(numcol, tbl_heading, continue_label):
    raw_heading = r''' {0} \\
  \hline\hline
  \endfirsthead

  \multicolumn{1}{2}{3}{4}{5}{6}{7} \\
  {8} \\
  \hline\hline
  \endhead

'''.format(tbl_heading, '{', numcol, '}', '{c}', '{', continue_label, '}', tbl_heading)
    safe_heading = protect_str(raw_heading)
    print('\n', safe_heading)
    
def print_table_footer(tbl_footer, continue_footer):
    raw_footer = r'''  \hline
  {0}
  \endfoot
  
  \hline\hline
  {1}
  \endlastfoot

'''.format(tbl_footer, continue_footer)
    safe_footer = protect_str(raw_footer)
    print(safe_footer)

def print_table_end():
    raw_end = r'''\end{}

%%
%%
%%
'''.format('{longtable}')
    safe_end = protect_str(raw_end)
    print('\n', safe_end)
