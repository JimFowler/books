#! /usr/bin/env python
#
#  Plot information in ./Data/Ajb/ajb_dates.csv
#
# read csv files
# number, volume, lityear, started, finished, proofread, other1, other2
#
# for each entry
#     plot startd-finished, number color=red
#     plot finished-proofread, number color=blue
#     plot proofread-other1, number color=green
#     plot other1-other2, number color=yellow, label=volume

import argparse
import datetime as dt
import csv
import matplotlib.pyplot as plt

from pprint import pprint

def getargs():

    parser = argparse.ArgumentParser(description='plot the Books20 timeline')

    parser.add_argument('-verbose',
                       help='be noisy about our activity',
                       default=False,
                       action='store_true')

    parser.add_argument('date_file',
                        help='the file of timeline dates',
                        action='store')

    args = parser.parse_args()

    return args


def get_date(date_str):
    '''Convert an ISO8601 date string to a datetime.datetime structure.
    Returns a datetime.datetime() or None.

    '''
    d = date_str.strip()
    if d:
        return dt.datetime.fromisoformat(d)
    else:
        return None


def plot_line(gca, level, time_list, style, name):

    l = [level for i in range(0, len(time_list))]
    gca.plot(time_list, l, style, label=name)


def annotate(gca, a):
    '''a is a 3-element tuple with a date, a level 1-68, and a note.'''

    d = dt.datetime.fromisoformat(a[0])
    x = [d, d]
    y = [a[1], a[1] + 2]
    gca.plot(x, y, 'b')
    gca.text(d, a[1] + 4, a[2])

def plot_ajb_dates(gca, date_filename):
    
    with open(date_filename, 'r') as ajbfile:

        ajb_reader = csv.reader(ajbfile, delimiter=',')
        
        first = True
        for row in ajb_reader:

            if first:
                first = False
                column_names = row
                continue

            # get dates
            vol_num = int(row[0])
            vol_name = str(row[1]).strip()
            index_year = str(row[2]).strip()
            start_date = get_date(row[3])
            finish_date = get_date(row[4])
            proof_date = get_date(row[5])
            other1_date = get_date(row[6])
            other2_date = get_date(row[7])

            if start_date and finish_date:
                #plot start finish line
                plot_line(gca, vol_num, [start_date, finish_date], 'r', '')
                if proof_date:
                    # plot finish proof line
                    plot_line(gca, vol_num, [finish_date, proof_date], 'b', '')
                    '''
                    if other1_date:
                        # plot proof other1 line
                        plot_line(gca, vol_num, [proof_date, other1_date], 'g', '')
                        if other2_date:
                            # plot other1 other2 line
                            plot_line(gca, vol_num, [other1_date, other2_date], 'p', '')
                    '''

def main():

    args = getargs()
    if args.verbose:
        pprint(args)
        
    fig = plt.figure()
    gca = fig.add_subplot(1,1,1)

    plot_ajb_dates(gca, args.date_file)

    # annotate the plot with interesting events
    annotate_list = [
        ('2007-07-25', 80, 'stroke'),
        ('2008-11-09', 75, 'begin project'),
        ('2010-09-28', 70, 'begin AJB catalogue'),
        ('2012-07-20', 70, 'start bookentry'),
        ('2012-08-04', 70, 'test bookentry, proof ajb65/66'),
        ('2012-08-23', 70, 'python 3'),
        ('2013-02-11', 70, 'ajbbooks fully functional'),
        ('2016-04-11', 45, 'v2.0 convert to XML'),
        ('2017-07-30', 38, 'journals v1.0'),
        ('2020-03-16', 10, 'COVID-19'),
    ]
    
    for a in annotate_list:
        annotate(gca, a)

    gca.set_ylim(0, 100)
    gca.set_xlabel('Date')
    gca.set_ylabel('AJB Num')
    fig.autofmt_xdate()
    plt.title('Books20 Project Timeline')
    plt.show()

#
# Main work
#
if __name__ =='__main__':

    main()
    
