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
import os
import argparse
import configparser

# Define as True to get debugging print
__DEBUG__ = True

# The search path list for the configuration files
__HOME__ = os.environ['HOME']
CONFIG_SEARCH_PATH = ['/opt/local/config',
                      __HOME__ + '/.config',
                      __HOME__ + '/config',
                      './']
del __HOME__

# The version number of configuration.py
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
                      help='alternate configuration file name.')

    pars.add_argument('--version',
                      help='display the program version information string and exit',
                      action='store_true')

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
        self._default_config_file_name = '{}.conf'.format(sys.argv[0])
        self._version_flag = False
        self._config_parser = configparser.ConfigParser()
        self._cmd_line_parser = argparse.ArgumentParser(description=description)

        # add the non-configuration flags to the command line parser
        __standard_flags__(self._cmd_line_parser)

    #
    # Public Functions
    #
    def add_parameter(self, name, section, **kwargs):
        """Add a new parameter to the empty _config_parser and _cmd_line_parser
        objects.

        'name' is the name of the variable and will be the name in the
        configuration file as well as the command line flag as --name.

        'section' is the section of the INI file that the parameter
        will be stored in.

        'kwargs' may be any valid keyword available in the
        ArgumentParser.add_argument() function.  Both 'help' and
        'default' are strongly recommended.

        'help' is the help string that is used by ArgumentParser()
        when the '--help' flag is requested.

        'default' is the default value for the parameter.  It will be
        stored as a string in the configuration file's [DEFAULT]
        section but will be the type() that is pass in for the
        ArgumentParser() object.

        """
        # add section to config file if needed
        if section not in self._config_parser.sections():
            print('adding parser section "{}"'.format(section))
            self._config_parser[section] = {}

        # add default value to DEFAULT section and add name to DEFAULT and section
        if 'default' in kwargs.keys():
            defval =  str(kwargs['default'])
            self._config_parser['DEFAULT'][name] = defval
            self._config_parser[section][name] = defval
        else:
            self._config_parser[section][name] = ''

        if __DEBUG__:
            print('set "{}" "{}" to {}'.format(section, name,
                                               self._config_parser[section][name]))
        #
        # add --name and kwargs to parser
        #
        self._cmd_line_parser.add_argument('--{}'.format(name), **kwargs)

    def read_config(self, config_file_name=None):
        """Read the configuration file specified on the command line or the
        file give by 'config_file_name' or the default if
        'config_file_name' is None of empty.

        Command line flags override the parameters specified in the
        configuration file.

        Returns the ConfigParser() object.

        """
        args = self._cmd_line_parser.parse_args()
        self._version_flag = args.version

        if args.config:
            # read configuration file specified on the command line.
            conf_file = args.config
        elif config_file_name:
            # read the configuration file name passed in.
            conf_file = config_file_name
        else:
            # read the default configuration file.
            conf_file = '{}.conf'.format(self._default_config_file_name)

        if __DEBUG__:
            print("""\n\nConfigParams.read_config():
            args.config = {}
            config_file_name = {}
            default is {}
            
            read_config: reading config file '{}'""".format(args.config,\
                                                config_file_name,\
                                                self._default_config_file_name,\
                                                conf_file))

        # parse conf_file for dirname and basename
        dirname, basename = os.path.split(conf_file)
        if dirname:
            # open directly
            self._config_parser.read(conf_file)
            self._config_file_name = conf_file
        else:
            # use the search the path and read the first one we find
            for dirname in CONFIG_SEARCH_PATH:
                filepath = os.path.join(dirname, basename)
                if os.path.isfile(filepath):
                    print('\nConfigParams.read: found file {}'.format(filepath))
                    self._config_parser.read(filepath)
                    self._config_file_name = filepath
                    break


        # parse the command line and update config parameters
        for k, v in vars(args).items():
            pass

        return self._config_parser


    def write_config(self, config_file_name=None):
        '''Save  the current  configuration in  the file  'configfilename'. If
        'configfilename' is empty  or None, save the  configuration in the
        file that was previously opened to read the file.  If that is also
        None or empty, then we toss an exception.

        '''
        if config_file_name:
            conf_file = config_file_name
        elif self._config_file_name:
            conf_file = self._config_file_name
        else:
            conf_file = self._default_config_file_name

        if __DEBUG__:
            print("""\n\nConfigParams.write_config():
            writing to file '{}'""".format(conf_file))

        with open(conf_file, 'w') as cf_p:
            self._config_parser.write(cf_p)


    def version_flag(self):
        """Return the state of the --version flag from the command line."""
        return self._version_flag

if __name__ == '__main__':

    from pprint import pprint

    print('\n\nconfig search path:')
    pprint(CONFIG_SEARCH_PATH)

    CPARAMS = ConfigParams('''Test configuration.py library file''')

    # add parameter to config and command line
    CPARAMS.add_parameter('thing1', 'conftest',
                          help='The value of thing1',
                          default=22)

    CPARAMS.add_parameter('thing2', 'conftest',
                          help='The value of thing2',
                          default=44)

    CPARAMS.add_parameter('verbose', 'conftest',
                          help='provide extra info,',
                          default=False,
                          action='store_true')

    CPARAMS.add_parameter('input',  'conftest',
                          type=str,
                          action='append',
                          help='read the file INPUT for entries')

    CPARAMS.add_parameter('symbols', 'conftest',
                          type=str,
                          help='use alternate symbol table,')

    CPARAMS.add_parameter('volume', 'conftest',
                          type=str,
                          help='default volume number,')

    # read the config file and command line
    CONFIG = CPARAMS.read_config('configtest1.conf')

    if CPARAMS.version_flag():
        print('\n\nCPARAMS.version_flag()')
        print('{} version {}'.format(sys.argv[0], '1.0.0'))

    print('\n\nCONFIG sections:')
    pprint(CONFIG.sections())

    # test write_config()
    CPARAMS.write_config()

    try:
        CPARAMS.write_config('/conftest.conf')
        print('...opps, we can write in this directory!')
    except PermissionError as ex:
        pprint(ex)
        print('...as expected')
    else:
        pprint(ex)
        print("...but we didn't expect that error")
