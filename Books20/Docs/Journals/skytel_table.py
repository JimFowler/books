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



st_missing = {
  '17' : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],  '18' : ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],  # 1959
  '19' : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],  '20' : [                                        ],  # 1960
  '21' : [       'Feb', 'Mar',        'May', 'Jun'],  '22' : ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],  # 1961
  '23' : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],  '24' : ['Jul', 'Aug', 'Sep', 'Oct',        'Dec'],  # 1962
  '25' : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],  '26' : ['Jul',        'Sep', 'Oct', 'Nov', 'Dec'],  # 1963
  '27' : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],  '28' : ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],  # 1964
  '29' : ['Jan',        'Mar', 'Apr', 'May', 'Jun'],  '30' : [       'Aug', 'Sep', 'Oct', 'Nov',      ],  # 1965
  '31' : [],  '32' : [],  # 1966
  '33' : [],  '34' : [],  # 1967
  '35' : [],  '36' : [],  # 1968
  '37' : [],  '38' : [],  # 1969
  '39' : [],  '40' : ['Oct'],  # 1970
  '41' : [],  '42' : [],  # 1971
  '43' : [],  '44' : [],  # 1972
  '45' : [],  '46' : [],  # 1973
  '47' : [],  '48' : [],  # 1974
  '49' : [],  '50' : [],  # 1975
  '51' : [],  '52' : [],  # 1976
  '53' : [],  '54' : [],  # 1977
  '55' : [],  '56' : [],  # 1978
  '57' : [],  '58' : [],  # 1979
  '59' : [],  '60' : [],  # 1980
  '61' : [],  '62' : [],  # 1981
  '63' : [],  '64' : [],  # 1982
  '65' : [],  '66' : [],  # 1983
  '67' : [],  '68' : [],  # 1984
  '69' : [],  '70' : [],  # 1985
  '71' : [],  '72' : [],  # 1986
  '73' : [],  '74' : [],  # 1987
  '75' : [],  '76' : [],  # 1988
  '77' : [],  '78' : [],  # 1989
  '79' : [],  '80' : [],  # 1990
  '81' : [],  '82' : [],  # 1991
  '83' : [],  '84' : [],  # 1992
  '85' : [],  '86' : [],  # 1993
  '87' : [],  '88' : [],  # 1994
  '89' : ['Feb'],  '90' : [],  # 1995
  '91' : ['Jun'],  '92' : [],  # 1996
  '93' : ['May'],  '94' : ['Sep'],  # 1997
  '95' : [],  '96' : [],  # 1998
  '97' : [],  '98' : ['Dec'],  # 1999
  '99' : [],  '100' : [],  # 2000
 '101' : [],  '102' : ['Sep'],  # 2001
 '103' : [],  '104' : [],  # 2002
 '105' : [],  '106' : [],  # 2003
 '107' : [],  '108' : [],  # 2004
 '109' : [],  '110' : [],  # 2005
 '111' : [],  '112' : [],  # 2006
 '113' : [],  '114' : [],  # 2007
 '115' : ['Jan'],  '116' : [],  # 2008
 '117' : ['Feb'],  '118' : [],  # 2009
 '119' : [],  '120' : [],  # 2010
 '121' : [],  '122' : [],  # 2011
 '123' : ['Feb'],  '124' : ['Jul', 'Aug'],  # 2012
 '125' : [],  '126' : ['Jul', 'Oct'],  # 2013
 '127' : [],  '128' : [],  # 2014
 '129' : [],  '130' : [],  # 2015
 '131' : [],  '132' : ['Aug', 'Oct', 'Nov'],  # 2016
 '133' : ['Jan', 'Feb',        'Apr', 'May', 'Jun'],  '134' : ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],  # 2017
 '135' : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],  '136' : ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],  # 2018
 '137' : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],  '138' : ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],  # 2019
 '139' : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],  '140' : ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],  # 2021
 '141' : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],  '142' : ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],  # 2022
 '143' : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],  '144' : ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],  # 2023
}

    
TBL_CAPTION = r'\bfseries Sky \& Telescope Magazine'
TBL_FORMAT = r'[p]{l l l l l l l l c l l l l l l l}'
TBL_LABEL = r'skytel:1'
#TBL_HEADING = r''
TBL_HEADING = r'''Vol & Year & & & & & & & & Vol & & & & & &'''
CONTINUE_LABEL = r'''Continuation of \bt{Sky \& Telescope}'''
TBL_PREAMBLE = r'''\setlength\LTleft{0pt}'''
TBL_FOOTER = r''
CONTINUE_FOOTER = r''

def print_month(volume, month):
    '''Pretty print a month name depending on whether
    it is missing from my collection or not.

    '''
    raw_str = ' & '
    
    if month in st_missing[str(volume)]:
        # if the volume is missing
        raw_str += str(month)
    else:
        raw_str += r'''\bf{''' + str(month) + r'''}'''
        
    return raw_str

def st_print_table():

    year_jump = 14
    volume_jump = 30
    
    year = 1960
    volume = 19
    for volume in range(volume, 145, 2):
        raw_str = r''
        raw_str += r'''\bf{''' + r'''{}'''.format(year)
        raw_str += r'''} & \bf{Vol ''' + r'''{}'''.format(volume) + r'''}'''
        for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']:
            raw_str += print_month(volume, month)
        raw_str += r''' & '''
        raw_str += r'''\hfill & \bf{Vol ''' + '''{}'''.format(volume + 1) + r'''}'''

        for month in ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            raw_str += print_month(volume, month)
            
        raw_str += r''' \\[5pt]'''
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
