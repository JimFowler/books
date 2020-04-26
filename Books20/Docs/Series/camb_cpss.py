#! /usr/bin/env python3
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Docs/Series/camb_cpss.py
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
  camb_cpss.py

  Table listing of the book series Cambridge Planetary Science Series
  published by Cambridge University Press.

  This file creates the LaTeX longtable format
  cambCPSStable.tex.
'''
import table as tb
from pprint import pprint

TBL_COMMENT = '''%%
%%
%% camb_cas_table.tex
%%
%%   Table listing of the book series Cambridge Planetary Science Series
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

TBL_CAPTION = r'\bfseries CUPS \bt{Cambridge Planetary Science Series}'
TBL_FORMAT = r'[p]{l l l l}'
TBL_LABEL = r'cpss_camb:1'
TBL_HEADING = r'Vol & Title & Author/Editor(s) & Date'
CONTINUE_LABEL = r'Continuation of \bt{Cambridge Planetary Science Series}'
TBL_PREAMBLE = r'''\setlength\LTleft{0pt}'''
TBL_FOOTER = r''
CONTINUE_FOOTER = r''

CAS_BOOK_LIST = [
    #(volnum, [title_list], 'copyright',
    # [authors/editors list],
    #'E|A', 'ISBN'),

    (1, ['Meteorites:',
         'A Petrologic, Chemical', 'and Isotopic Synthesis'], '01/2007',
     ['Robert Hutchison'],
     'A', '9780521035392'),

    (2, ['Jupiter:', 'The Planet, Satellites and Magnetosphere'], '03/2007',
     ['Fran Bagenal', 'Timothy E. Dowling', 'Wiliam B. McKinnon'],
     'E', '9780521035453'),

    (3, ['The Martian Surface:',
         'Composition, Mineralogy and Physical Properties'], '07/2008',
     ['Jim Bell'],
     'E', '9780521866989'],

    (4, ['Planetary Crusts:',
         'Their Composition, Origin and Evolution'], '04/2010',
     ['S. Ross Taylor', 'Scott McLennan'],
     'A', '9780521142014'),

    (5, ['The Geology of Mars:',
         'Evidence from Earth-Based Analogs'], '08/2011',
     ['Mary Chapman'],
     'A', '9780521206594'),

    (6, ['Planetary Surface Properties'], '10/2011',
     ['H. Jay Melosh'],
     'A', '9780521514187'),

    (7, ['The Origin of Chondrules and Chondrites'], '11/2011',
     ['Derek W. G. Sears'],
     'A', '9781107402850'),

    (8, ['Planetary Tectonics'], '05/2012',
     ['Thomas R. Watters', 'Richard A. Schultz'],
     'E', '9780521749923'),

    (9, ['Protoplanetary Dust:',
     'Astrophysical and Cosmochemical Perspectives'], '02/2014',
    ['Daniel Apai', 'Dante S. Lauretta'],
     'E', '9781107629424'),

    (10, ['Titan:', 'Interior, Surface, Atmosphere',
          'and Space Enviroment'], '02/2014',
     ['Ingo Müller', 'Caitlin A. Griffith', 'Emmanuel Lellouch',
      'Thomas E. Cravens'],
     'E', '9780521199926'),

    (11, ['Mars:', 'An Introduction to its Interior',
          'Surface and Atmosphere'], '05/2014',
     ['Nadine Barlow'],
     'A', '9781107644878'),

    (12, ['Volcanism on Io:',
     'A Comparison with Earth'], '07/2014',
    ['Ashley Gerard Davies'],
    'A', '9781107665408'),

    (13, ['Asteriods:',
          'Astronomical and Geological Bodies'], '02/2017',
     ['Thomas H. Burbine'],
     'A', '9781107096844'),

    (14, ['Planetesimals:',
     'Early Differentiation and Consequences for Planets'], '03/2017',
    ['Linda T. Elkins-Tanton', 'Benjamin P. Weiss'],
    'E', '9781107118485'),

    (15, ['The Atmosphere and Climate of Mars'], '08/2017',
     ['Robert M. Haberle', 'R. Todd Clancy', 'François Forget',
      'Michael D. Smith', 'Richard W. Zurek'],
     'E', '9781107016187'),

    (16, ['The Surface of Mars'], '03/2018',
     ['Michael H. Carr'],
     'A', ''),

    

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

