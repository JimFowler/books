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
client programs. It utilizes the standard ``argparse`` and
``configparser`` packages to work out what configuraton variables are
needed and the primary object returned by ``get_config()`` is of
type ``configparser.ConfigParser()``

Program configuration may be done through a configuration file in a
standard location, an alternate configuration file in a non-standard
or standard location, or via the command line.  All configuration
variable available in a configuration file are also available via the
command line.  One may also specify default values in the event that
the variable is not listed in a configuration file or on the command
line. 

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
  cf.create_config(description)
  cf.add_parameter('verbose', help='Be noisy about our actions',
                   default=True)
  cf.add_parameter('volume', help='The default volume number',
                   default=68)
  cf.add_parameter('symbols', help='location of symbol table', default='')
  cf.add_parameter('input', help='the input file to use', default='')

  config = cf.read_config(config_file_name='configname.conf')
  defaultconf = config['DEFAULT']
  # config is of type configparser.ConfigParser()

  with open(defaultconf['input'], 'w') as infile:
      # do something with the file
  ...
  cf.save_config(config_file_name='configfilename')
  
Then the configuration file for `prog` will be `prog.conf` which would
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

.. automodule:: config
    :members:
    :show-inheritance:
