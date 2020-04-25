#! /usr/bin/env python3
# -*- mode: Python;-*-
#
# Begin copyright
#
#  /home/jrf/Documents/books/Books20/Tools/python/duptitles
#
#   Part of the Books20 Project
#
#   Copyright 2020 James R. Fowler
#
#   All rights reserved. No part of this publication may be
#   reproduced, stored in a retrival system, or transmitted
#   in any form or by any means, electronic, mechanical,
#   photocopying, recording, or otherwise, without prior written
#   permission of the author.
#
#
# End copyright
#
'''
Check for duplicate titles in a journal file.
'''

import sys
import os
import argparse

import aabooks.journal.journalfile as jf

from pprint import pprint

#
# Parse the command line arguments
#
def getargs():
    '''Get the command line arguments.'''
    
    parser = argparse.ArgumentParser(description='Check for duplicate entries in a journals.xml file. The program looks for duplicate titles.')

    parser.add_argument('-i', '--input', type=str,
                        help='read the file INPUT for entries',
                        default='/home/jrf/Documents/books/Books20/Data/journals.xml')


    args = parser.parse_args()

    return args

def entries_match(entry_I, entry_J):
    '''Decide if two entries are the same or match in some way.'''

    if entry_I['Title'] == entry_J['Title']:
        return True

    return False

#
# Main work
#
if __name__ == '__main__':

    args = getargs()
    
    _JF = jf.JournalFile()

    _JF.read_xml_file(args.input)

    max_entry = _JF.max_entries()

    for i in range(1, max_entry):
        entry_I = _JF.get_entry(i)
        
        for j in range(i+1, max_entry):
            entry_J = _JF.get_entry(j)

            if entries_match(entry_I, entry_J):
                print('Titles for entry {} matches entry {}'.format(i, j))
