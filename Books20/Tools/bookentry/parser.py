#! /usr/bin/env python3
# -*- mode: Python;-*-

"""A standard parser for all python programms. This parser
contains the minimum required flags for all python programs
that are part of the Books20 project
"""

import argparse

def standard_parser(pars):
    """Provides a standard parser that should be used by all python programs
    that are part of the Books20 project.  This parser provided the minimum
    required command line flags as defined in the Books20 style guide.

    """

    pars.add_argument('-v', '--version', action='version',
                      version='%(prog)s v{version}'.format(version=version))

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
    from version import __version__

    print('argparse v{}'.format(argparse.__version__))

    parser = argparse.ArgumentParser(description=description,
                                     version=__version__)
    standard_parser(parser)

    extra_flags(parser)

    args = parser.parse_args()

    pprint(args)
