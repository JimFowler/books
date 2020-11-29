#!/usr/bin/env python3
# -*- mode: Python;-*-
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/setup.py
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
#
# installation instructions for python install
#
# run as
#   python3 setup.py install --prefix=/home/jrf
#
'''Installation for python tools in Books20'''

from distutils.core import setup

# get the master version number for the module
exec(open('aabooks/version.py').read())

setup(name='aabooks',
      version=__version__,
      description='Books20 Project Tools',
      author='James R. Fowler',
      author_email='jrf12@mac.com',
      url='http://het.as.utexas.edu/jrf/20thCentury.html',
      platforms=['Ubuntu 20.04 LTS'],
      packages=['aabooks', 'aabooks.lib', 'aabooks.ajbbook', 'aabooks.journal'],
      scripts=['scripts/aaaconvert', 'scripts/ajbbooks', 'scripts/journals',
               'scripts/ppxml', 'scripts/validate_xml', 'scripts/verify'],
      package_data={'aabooks.lib': ['symbols.txt']},)
