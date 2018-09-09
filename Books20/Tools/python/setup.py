#!/usr/bin/env python3
# -*- mode: Python;-*-
# -*- coding: UTF-8 -*-
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


from distutils.core import setup

setup( name='bookentry',
       version='1.0.0',
       description='AJB BooksEntry tool',
       author='James R. Fowler',
       author_email='jrf12@mac.com',
       url='http://het.as.utexas.edu/jrf/20thCentury.html',
       platforms=['Ubuntu 12.04',
                  'Ubuntu 13',
                  'Ubuntu 14.10 LTS',
                  'Ubuntu 16.10 LTS'],
       packages=['bookentry'],
       scripts=['ajbbooks', 'journals', 'ppxml', 'validateXML'],
       package_data={'bookentry': ['symbols.txt']},
       )

