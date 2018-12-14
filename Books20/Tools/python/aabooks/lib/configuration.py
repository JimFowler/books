#! /usr/bin/env python3
##
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

"""A configuration file and command line parser for all python
programs. This parser contains the minimum required variable for all
python programs that are part of the Books20 project.

"""
import sys
import argparse
import configparser


# XXXXX
# need to getenv HOME and use in place of ~
# possible configure or make variable to set at config time
#
CONFIG_SEARCH_PATHS = ['/opt/local/config', '~/.config', '~/config', './']

__VERSION__ = '1.0.0'

#
# Private Functions
#
def __standard_flags__(pars):
    """Provides a standard parser that should be used by all python
    programs that are part of the Books20 project.  This parser
    provides the minimum required command line flags as defined in the
    Books20 style guide.  These command line flags are not stored in the
    ConfigParams() class.

    """
    pars.add_argument('-c', '--config', type=str,
                      help='alternate configuration file name.',
                      default='{}.conf'.format(sys.argv[0]))

    pars.add_argument('--version',
                      help='display the program version information string and exit',
                      action='store_true')

    return pars

def __extra_flags__(pars):
    """Add extra recommended flags to a parser.

    convert all of these to add_param() calls

    """


    pars.add_argument('--verbose',
                      help='provide extra info,',
                      action='store_true')

    pars.add_argument('-i', '--input', type=str,
                      action='append',
                      help='read the file INPUT for entries')

    pars.add_argument('-s', '--symbols', type=str,
                      help='use alternate symbol table,')

    pars.add_argument('-V', '--volume', type=str,
                      help='default volume number,')

    return pars


#
# Public classes and functions
#
class ConfigParams():
    """The ConfigParams class keeps track of the configuration file,
    command line arguments, and the configuration parameters.  It
    provides a mechanism to build and read a configuration file as
    well as to override the configuration parameters via the command
    line arguments.

    'description' is used as the description variable in
    argparse.ArgumentParser() for use with the '--help' flag.

    """

    def __init__(self, description):
        super(ConfigParams, self).__init__()

        self._config_file_name = ''
        self._version_flag = False
        self._config_parser = configparser.ConfigParser()
        self._cmd_line_parser = argparse.ArgumentParser(description=description)

        # add the non-configuration flags to the command line parser
        __standard_flags__(self._cmd_line_parser)
        
    #
    # Public Functions
    #
    def add_parameter(self, name, section='DEFAULT', **kwords):
        """Add a new parameter to the empty _config_parser and _cmd_line_parser
        objects.

        'name' is the name of the variable and will be the name in the
        configuration file as well as the command line flag as --name.

        'section' is the section of the INI file that the parameter
        will be stored in.  The usual place is the DEFAULT section.

        'kwords' may be any valid keyword available in the
        ArgumentParser.add_argument() function.  Both 'help' and
        'default' are strongly recommended.

        'help' is the help string that is used by ArgumentParser()
        when the '--help' flag is requested.

        'default' is the default value for the parameter.  It will be
        stored as a string in the ConfigParser() object but will be the type()
        that is pass in for the ArgumentParser() object.

        """
        pass

    def read_config(self, config_file_name=None):
        """Read the configuration file give by 'config_file_name' or the
        config_file specified on the command line or the default if
        'config_file_name' is None of empty

        Returns the ConfigParser() object.

        """
        args = self._cmd_line_parser.parse_args()
        self._version_flag = args.version

        # Do something here
        return self._config_parser


    def write_config(self, config_file_name=None):
        '''Save  the current  configuration in  the file  'configfilename'. If
        'configfilename' is empty  or None, save the  configuration in the
        file that was previously opened to read the file.  If that is also
        None or empty, then we toss an exception.

        '''
        pass

    def version_flag(self):
        """Return the state of the --version flag from the command line."""
        return self._version_flag
    

if __name__ == '__main__':

    from pprint import pprint

    CONFP = ConfigParams('''Test configuration.py library file''')

    CONFIG = CONFP.read_config()

    if CONFP.version_flag():
        print('{} version {}'.format(sys.argv[0], '1.0.0'))

    pprint(CONFIG.sections())
