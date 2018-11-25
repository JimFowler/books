#! /usr/bin/env python3
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/lib/parser.py
##
##   Part of the Books20 Project
##
##   Copyright 2018 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrival system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright

"""A standard parser for all python programs. This parser
contains the minimum required flags for all python programs
that are part of the Books20 project.

To Do:
  Combine with config file parser

  Consider proper use of extra flags. Do we need them all?
"""
import argparse

def standard_parser(pars):
    """Provides a standard parser that should be used by all python programs
    that are part of the Books20 project.  This parser provides the minimum
    required command line flags as defined in the Books20 style guide.

    """
    pars.add_argument('-v', '--version',
                      help='provide version information',
                      action='store_true')

    pars.add_argument('--verbose',
                      help='provide extra info,',
                      action='store_true')

    return pars

def extra_flags(pars):
    """Add extra recommended flags to a parser."""

    pars.add_argument('-i', '--input', type=str,
                      action='append',
                      help='read the file INPUT for entries')

    pars.add_argument('-s', '--symbols', type=str,
                      help='use alternate symbol table,')

    pars.add_argument('-V', '--volume', type=str,
                      help='default volume number,')

    pars.add_argument('-c', '--config', type=str,
                      help='alternate configuration file name.',
                      default='./ajbbooks.conf')

    return pars



if __name__ == '__main__':

    from pprint import pprint

    print('argparse v{}'.format(argparse.__version__))

    DESCRIPTION = '''Test parser.py'''

    PARSER = argparse.ArgumentParser(description=DESCRIPTION)
    standard_parser(PARSER)

    extra_flags(PARSER)

    ARGS = PARSER.parse_args()

    pprint(ARGS)
