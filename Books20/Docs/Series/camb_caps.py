#! /usr/bin/env python3
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Docs/Series/camb_cas.py
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
  camb_caps.py

  Table listing of the book series Cambridge Astrophysics Series
  published by Cambridge University Press.

  This file creates the LaTeX longtable format
  cambCAPStable.tex.
'''
import table as tb
from pprint import pprint

TBL_COMMENT = '''%%
%%
%% camb_cas_table.tex
%%
%%   Table listing of the book series Cambridge Astrophysics Series
%%   published by Cambridge Unversity Press. This is information used
%%   with the book project "Some Important Books in Astronomy
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

TBL_CAPTION = r'\bfseries CUPS \bt{Cambridge Astrophysics Series}'
TBL_FORMAT = r'[p]{l l l l}'
TBL_LABEL = r'caps:1'
TBL_HEADING = r'Vol & Title & Author/Editor(s) & Date'
CONTINUE_LABEL = r'Continuation of \bt{Cambridge Astrophysics Series}'
TBL_PREAMBLE = r'''\setlength\LTleft{0pt}'''
TBL_FOOTER = r''
CONTINUE_FOOTER = r''

CAS_BOOK_LIST = [
    #(volnum, [title_list], 'copyright',
    # [authors/editors list],
    #'E|A', 'ISBN'),
    ( 1, ['Active Galactic Nuclei'], '',
     ['C. Hazard', 'S. Mitton'],
      'E', None),

    ( 2, ['Globular Clusters'], '',
     ['D. A. Hanes', 'B. F. Madore'],
      'E', None),

    ( 3, ['Low Light-level Detectors in Astronomy'], '',
     ['M. J. Eccles', 'M. E. Sim', 'K. P. Tritton'],
      'A', None),

    ( 4, ['Accretion-driven Stellar X-ray Sources['], '',
     ['W. H. G. Lewin', 'E. P. J. van den Heuvel'],
      'E', None),

    ( 5, ['The Solar Granulation'], '',
     ['R. J. Bray', 'R. E. Loughhead', 'C. J. Durrant'],
      'A', None),

    ( 6, ['Interacting Binary Stars'], '',
     ['J. E. Pringle', 'R. A. Wade'],
      'E', None),
    
    ( 7, ['Spectroscopy of Astrophysical Plasmas'], '*',
     ['A. Dalgarno', 'D. Layzer'],
      'A', None),
    
    ( 8, ['Accretion Power in Astrophysics'], '',
     ['J. Frank', 'A. R. King', 'D. J. Raine'],
      'A', None),
    
    ( 9, ['Gamma-ray Astronomy'], '',
     ['P. V. Ramana Murthy', 'A. W. Wolfendale'],
      'A', None),
    
    (10, ['Quaser Astronomy'], '',
     ['D. W. Weedman'],
      'A', None),
    
    (11, ['X-ray Emission from Clusters of Galaxies'], '',
     ['C. L. Sarazin'],
      'A', None),
    
    (12, ['The Symbiotic Stars'], '',
     ['S. J. Kenyon'],
      'A', None),
    
    (13, ['High Speed Astronomical Photometry'], '',
     ['B. Warner'],
      'A', None),
    
    (14, ['The Physics of Flare Stars'], '',
     ['E. Tandvberg-Hanssen', 'A. G. Emslie'],
      'A', None),
    
    (15, ['X-ray Detectors in Astronomy'], '',
     ['G. W. Fraser'],
      'A', None),
    
    (16, ['Pulsar Astronomy'], '',
     ['A. Lyne', 'F. Graham-Smith'],
      'A', None),
    
    (17, ['Molecular Collision in the Interstellar Medium'], '1990*',
     ['D. Flower'],
      'A', '0-521-32032-1'),
]


def cas_print_books(book_list):
    '''Print the book list in aal_table in long table format.'''
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
    tb.print_table_heading(3, TBL_HEADING, CONTINUE_LABEL)
    tb.print_table_footer(TBL_FOOTER, CONTINUE_FOOTER)

    cas_print_books(CAS_BOOK_LIST)
    tb.print_table_end()

