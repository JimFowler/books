#! /usr/bin/env python
#

import datetime as dt

Months = {
    'Jan' : 1,
    'Feb' : 2,
    'Mar' : 3,
    'April' : 4,
    'Apr' : 4,
    'May' : 5,
    'June' : 6,
    'July' : 7,
    'August' : 8,
    'Aug' : 8,
    'Sept' : 9,
    'Oct' : 10,
    'Nov' : 11,
    'Dec' : 12,
    }

def str_to_iso(date_str):

    ret_str = ''
    
    if date_str:
        day, mon_name, year = date_str.split()
        
        udate = dt.date(int(year), Months[mon_name], int(day))
        ret_str = udate.isoformat()

    return ret_str


with open('gotit.csv', 'r') as fp:

    for line in fp.readlines():
        index, voln, year, start, finish, proof, bookentry = line.split(',')

        startISO = str_to_iso(start.strip())
        finishISO = str_to_iso(finish.strip())
        proofISO = str_to_iso(proof.strip())
        bookentryISO = str_to_iso(bookentry.strip())

        print(index, voln, year, startISO, finishISO, proofISO, bookentryISO, sep=', ')
