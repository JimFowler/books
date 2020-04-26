## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Docs/Series/intersci_table.py
##
##   Part of the Books20 Project
##
##   Copyright 2020 James R. Fowler
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
  intersci_table.py

  Table listing of the book series Interscience Tracts on Physics
  and Astronomy published by Interscience Publishers.

  This file created the LaTeX longtable format
  interscience_table.tex.
'''
import table as tb
from pprint import pprint

TBL_COMMENT = '''%%
%%
%% intersciencetable.tex
%%
%%   Table listing of the book series Interscience Tracts on Physics
%%   and Astronomy published Interscience Publishers. This is information
%%   userd with the book project "Some Important Books in Astronomy
%%   and Astrophysics in the 20th Century"
%%
'''

TBL_COPYRIGHT = r'''%%   Copyright 2020 James R. Fowler
%%
%%   All rights reserved. No part of this publication may be
%%   reproduced, stored in a retrival system, or transmitted
%%   in any form or by any means, electronic, mechanical,
%%   photocopying, recording, or otherwise, without prior written
%%   permission of the author.
%%
%%
%%
'''

TBL_CAPTION = r'\bfseries \bt{Interscience Tracts on Physics and Astronomy}'
TBL_FORMAT = r'[p]{l l l l}'
TBL_LABEL = r'interscience:1'
TBL_HEADING = r'Vol & Title & Author/Editor(s) & Date'
CONTINUE_LABEL = r'Continuation of \bt{Tracts on Physics and Astronomy}'
TBL_PREAMBLE = r'''\setlength\LTleft{0pt}'''
TBL_FOOTER = r''
CONTINUE_FOOTER = r''

INTERSCI_BOOK_LIST = [
    #(volnum, [title_list], 'copyright',
    # [authors/editors list],
    #'E|A', 'ISBN'),
    (1, ['Neutron Optics'], '1954',
     ['D. J. Hughes'],
     'A', None),

    (2, ['High-Energy Accelerators'], '1954',
     ['M. S. Livingston'],
     'A', None),

    (3, ['Physics of Fully Ionized Gases'], '1956 *',
     ['L. Spitzer jr.'],
     'A', None),

    (4, ['Magnetohydrodynamics'], '1957',
     ['T. G. Cowling'],
     'A', None),

    (5, ['Introduction to the Physics', 'of Many-Body Systems'], '1958',
     ['D. ter Haar'],
     'A', None),

    (6, ['Physics of Meteor Flight in the Atmosphere'], '1958 *',
     ['E. J. Öpik'],
     'A', None),

    (7, ['Cryophysics'], '1960',
     ['K. Mendelssohn'],
     'A', None),

    (8, ['Introduction to the Theory of Ionized Gases'], '',
     ['J. L. Deleroix'],
     'A', None),

    (9, ['An Introduction to Celestial Mechanics'], '1960',
     ['T. E. Sterne'],
     'A', None),

    (10, ['General Relativity and Gravitational Waves'], '1961',
     ['J. Weber'],
     'A', None),

    (11, ['Introduction to Elemetary Particle Physics'], '1961',
     ['R. E. Marshak', 'E. C. G. Sudarshan'],
     'A', None),

    (12, ['Electron Transport in Metals'], '1962',
     ['J. L. Olsen'],
     'A', None),

    (13, ['Modern Applications of Physical Optics'], '1963',
     ['M. Francon'],
     'A', None),

    (14, ['The Optical Model in Nuclear', 'and Particle Physics'], '',
     ['P. B. Jones'],
     'A', None),

    (15, ['Strange Particles'], '',
     ['R. K. Adair', 'E. C. Fowler'],
     'A', None),

    (16, ['The Nucleon-Nucleon Interaction:',
          'Experimental and Phenomenological',
          'Aspects'], '1963',
     ['R. Wilson'],
     'A', None),

    (17, ['Plasma Waves'], '1963',
     ['J. F. Denisse', 'J. L .Decroix'],
     'A', None),

    (18, ['Micromagnetics'], '',
     ['W. F. Brown jr.'],
     'A', None),

    (19, ['Concepts in Photoconductivity',
          'and Allied Problems'], '1963',
     ['A. Rose'],
     'A', None),

    (20, ['X-ray Studies of Materials'], '',
     ['A. Guinier', 'D. L. Dexter'],
     'A', None),

    (21, ['The Adiabatic Motion of Charged Particles'], '',
     ['T. G. Northrup'],
     'A', None),

    (22, ['Introduction to Advanced Field Theory'], '',
     ['G. Barton'],
     'A', None),

    (23, ['Dynamic Nuclear Orientation'], '',
     ['C. D. Jeffries'],
     'A', None),

    (24, ['Magnetic Resonance at High Pressure'], '1963',
     ['G. B. Benedek'],
     'A', None),

    (25, ['Excitons'], '1965',
     ['D. L. Dexter', 'R. S. Knox'],
     'A', None),

    (26, ['Radiative Contributions to Energy',
          'and Momentum Transport in a Gas'], '1965',
     ['D. H. Sampson'],
     'A', None),

    (27, ['Introduction to Unitary Symmetry'], '1966',
     ['P. Carruthers'],
     'A', None),

    (28, ['Diffuse Matter in Space'], '1968 *',
     ['L. Spitzer jr.'],
     'A', None),

    ( 'nn', ['High-energy Electromagnetic Processes?',
             'in Condensed Media'], '1972',
      ['M. L. Ter-Mikaelian'],
      'A', '0471851906'),
]

def intersci_print_books(book_list):
    '''Print the book list in interscience_table in long table format.'''

    for volnum, title_list, year, author_list, ae_flag, isbn in book_list:
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
                raw_str += r'''{} '''.format(author_list[index-1])
                if ae_flag == 'E' and index == 1:
                    raw_str += r'''eds. & '''
                else:
                    raw_str += r'''& '''
            else:
                raw_str += r''' & '''

            if year is not None:
                raw_str += r'''{}'''.format(year)
                year = None

            if isbn is not None:
                isbn = None


            if index == max_loops:
                # at the end of a book allow a break and add spacing
                raw_str += r''' \\[5pt]'''
            else:
                raw_str += r''' \\*'''

            raw_str += '''
'''
        # Clean up for TeX and print(), statement
        raw_str = raw_str.replace(r'. ', r'.\ ')
        safe_str = tb.protect_str(raw_str)
        # if more title and/or more authors
        print(safe_str)

if __name__ == '__main__':

    tb.print_table_comment(TBL_COMMENT)
    tb.print_table_copyright(TBL_COPYRIGHT)
    tb.print_table_preamble(TBL_PREAMBLE)
    tb.print_table_start(TBL_FORMAT)

    tb.print_table_caption(TBL_CAPTION)
    tb.print_table_label(TBL_LABEL)
    tb.print_table_heading(4, TBL_HEADING, CONTINUE_LABEL)
    tb.print_table_footer(TBL_FOOTER, CONTINUE_FOOTER)

    intersci_print_books(INTERSCI_BOOK_LIST)
    tb.print_table_end()

