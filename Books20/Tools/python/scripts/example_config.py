#! /usr/bin/env python
#
#  A test for configuration with config
#  file, default values, and command line values
#
# TODO:
#   Merge master with aabooks
#   in Tools/python/aabooks/lib
#    delete configuration.py and any other config files
#    add standard_parser_args() to utils
#   Add example_conf.py and example_conf.conf to scripts but don't install
#   Modify programs to use configargparse and utils.standard_parser_args()
#   Remove .conf files from .gitignore
#   What else??
#

# This example program can use argparse or configargparse
#import argparse as argp
import configargparse as argp

from pprint import pprint

#
# Library Function
#
def standard_parser_args(parser):
    '''The configuration flags that every program should use.  This
    function is in the Books20 library and should be called after
    creating the parser.  This function may be used with either
    the argparse or configargparse packages.

    '''
    
    parser.add_argument('-V',
                        help='show the version information and exit',
                        default=False,
                        action='store_true')
    try:
        # use only with configargparser
        parser.add_argument('-c', '--config-path',
                            is_config_file=True,
                            metavar='CONF',
                            help='path to the alternate configuration file.')
    except TypeError:
        pass
    
    parser.add_argument('--verbose',
                        help='be noisy about our actions',
                        default=False,
                        action='store_true')
    
    parser.add_argument('--debug',
                        help='turn on debugging information',
                        default=False,
                        action='store_true')
    

    return parser


#
# Specific function
#
__description='''Test the config and command line overrides'''

def getargs():
    '''Get the command line arguments or the configuration file values.
    Add any unique flags or arguments for the specific program.  This
    function should be written for each of the programs in Books20.

    '''

    try:
        parser = argp.ArgumentParser(description=__description,
                                    default_config_files=['~/.config/Books20/ajbbooks.conf'])
    except TypeError:
        parser = argp.ArgumentParser(description=__description)

    standard_parser_args(parser)

    parser.add_argument('-i', '--input', type=str,
                        help='read the file INPUT for entries')
    
    parser.add_argument('-s', '--symbols', type=str,
                        default='~/.config/Books20/symbols.txt',
                        help='use alternate symbol table,')
    
    parser.add_argument('-v', '--volume', type=int,
                        default=-1,
                        help='default volume number,')
    
    return parser.parse_known_args()


    
if __name__ == '__main__':

    args = getargs()

    print('\nFinal results')
    pprint(args)
