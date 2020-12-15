#! /usr/bin/env python3
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Docs/Series/journals.py
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

  journals.py

  Table listing of my journal collection and the missing journals
  from that collection

  The file created is in the LaTeX longtable format
  journals.tex
'''
import table as tb
from pprint import pprint

TBL_COMMENT = '''%%
%%
%% journals.tex
%%
%%   Table listing of the the journals in my collection along
%%   with a listing (in boldface) of the missing journals.
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

TBL_CAPTION = r'\bfseries Sky \& Telescope Magazine'
TBL_FORMAT = r'[p]{l l l l l l l l c l l l l l l l}'
TBL_LABEL = r'skytel:1'
#TBL_HEADING = r''
TBL_HEADING = r'''Vol & Year & & & & & & & & Vol & & & & & &'''
CONTINUE_LABEL = r'''Continuation of \bt{Sky \& Telescope}'''
TBL_PREAMBLE = r'''\setlength\LTleft{0pt}'''
TBL_FOOTER = r''
CONTINUE_FOOTER = r''

def st_print_table():

    year_jump = 14
    volume_jump = 30
    
    year = 1960
    volume = 19
    for volume in range(volume, 145, 2):
        raw_str = r''
        raw_str += r'''\bf{Vol '''
        raw_str += r'''{}'''.format(volume)
        raw_str += r'''} & \bf{''' + r'''{}'''.format(year)
        raw_str += r'''} & Jan & Feb & Mar & Apr & May & Jun &'''
        raw_str += r'''\hfill & \bf{Vol ''' + '''{}'''.format(volume + 1)
        raw_str += r'''}''' + r''' & Jul & Aug & Sep & Oct & Nov & Dec \\[5pt]'''
        safe_str = tb.protect_str(raw_str)
        print(safe_str)
        year += 1

if __name__ == '__main__':

    tb.print_table_comment(TBL_COMMENT)
    tb.print_table_copyright(TBL_COPYRIGHT)
    tb.print_table_preamble(TBL_PREAMBLE)
    tb.print_table_start(TBL_FORMAT)

    tb.print_table_caption(TBL_CAPTION)
    tb.print_table_label(TBL_LABEL)
    tb.print_table_heading(16, TBL_HEADING, CONTINUE_LABEL)
    tb.print_table_footer(TBL_FOOTER, CONTINUE_FOOTER)

    st_print_table()
    tb.print_table_end()
