#! /usr/bin/env python
# -*- mode: Python;-*-
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/scripts/searchbooks.py
##
##   Part of the Books20 Project
##
##   Copyright 2024 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrival system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright
'''Search the ajb??_books.xml and aaa??_books.xml files for
a particular string

'''
from pprint import pprint
import configargparse as argp


__VERSION__ = 'v1.0.0'

__DESCRIPTION__ = '''Search AJB or AAA XML files for a particular search
term and return an XML file with the found entries'''

#
# Parse the command line arguments
#
def getargs():
    '''Parse the command line arguments.'''
    parser = argp.ArgumentParser(description=__DESCRIPTION__,
                                 default_config_files=['~/.config/Books20/searchbooks.conf'])
                                 
    aautils.standard_parser_args(parser)

    parser.add_argument('--search-term', '-s',
                        help='a logical string',
                        type=str,
                        default='Title.contains="stars"')
    
    parser.add_argument('files',
                        nargs='*')

    return parser.parse_known_args()[0]


def main():
    '''Search the files'''

    args = getargs()
    pprint(args)

##
## Do the work
##
if __name__ == '__main__':

    main()

