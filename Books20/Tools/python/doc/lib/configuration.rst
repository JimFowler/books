..  Begin copyright
.. 
..   /home/jrf/Documents/books/Books20/Tools/python/doc/lib/configuration.rst
.. 
..    Part of the Books20 Project
.. 
..    Copyright 2018 James R. Fowler
.. 
..    All rights reserved. No part of this publication may be
..    reproduced, stored in a retrival system, or transmitted
..    in any form or by any means, electronic, mechanical,
..    photocopying, recording, or otherwise, without prior written
..    permission of the author.
.. 
.. 
..  End copyright

Configuration
*************

The ``configuration`` package provide a configuration mechanism for
client programs. It utilizes the standard `argparse
<https://docs.python.org/3/library/argparse.html>`_ and `configparser
<https://docs.python.org/3/library/configparser.html>`_ packages to
work out what configuraton variables are needed. The primary object
returned by is of type ``configparser.ConfigParser()``.

Program configuration may be done through a configuration file in a
standard location, an alternate configuration file in a non-standard
or standard location, or via the command line.  All configuration
variables available in a configuration file may also be available via
the command line.  Specified default values are listed when building
the ConfigParams object in the event that the variable is not listed
in a configuration file or on the command line.

Configuration Files
===================

All configuration variables can be set in the configuration file or on
the command line.  The ``--config-path`` and ``--version`` flags are only
available on the command line.

Configuration file locations are searched in the following order. If
the ``config-path`` flag is set and the path is a full or relative
path with a directory name, then the file is read from that path only.
If the path is just a basename, then the following directories are
searched in order, ``~/.config/``, ``~/config/``, ``./``.  If the file
is not found or can not be read, the program will throw an exception.
It is possible to have no configuration file in which case only the
command line parser is used. The default name of the configuration file
is `"{}.conf".format(sys.argv[0])`

Example
=======

.. parsed-literal::
   
  from aabooks.lib import configuration as cf

  description = '''This is a short or long description of the program'''
  cf.ConfigParams(description)
  # cf.CONFIG_SEARCH_PATH is a list and may be added to
  cf.CONFIG_SEARCH_PATH.append('mydirectory')
  cf.add_parameter('verbose', help='Be noisy about our actions',
                   default=True)
  cf.add_parameter('volume', help='The default volume number',
                   default=68)
  cf.add_parameter('symbols', help='location of symbol table', default='')
  cf.add_parameter('input', help='the input file to use', default='')

  config = cf.read_config(config_file_name='configname.conf')
  defaultconf = config['DEFAULT']
  # config is of type configparser.ConfigParser()
  # defaultconf is a dictionary of keyword/value from the DEFAULT
  #   section of the configuration file

  # do something with these configuration parameters
  ...
  # save the configuration parameters in a config file
  cf.save_config(config_file_name='configfilename')
  
The configuration file for `prog` will be `prog.conf` which would
look like this:

.. parsed-literal::

   [DEFAULT]
   verbose = false
   volume = 68
   symbols = ''
   input = ''

The `configparser` package supports a structure similar to Microsoft
INI files which may have multiple sub-categories.  The `configure`
package does not support this multi-depth capability at this time. 

configuration.py
================

.. automodule:: configuration
    :members:
    :show-inheritance:
