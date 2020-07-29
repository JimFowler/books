#! /usr/bin/env python3
# -*- mode: Python;-*-
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/lib/version.py
##
##   Part of the Books20 Project
##
##   Copyright 2018 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrieval system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright

"""The version number for the aabooks lib module.

Store the version here so:
 1) we don't load dependencies by storing it in __init__.py
 2) we can import it in setup.py for the same reason
 3) we can import it into your module module

Found this at
https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package
"""

__version_info__ = ('2', '2', '0')
__major__ = __version_info__[0]
__minor__ = __version_info__[1]
__micro__ = __version_info__[2]

__version__ = '.'.join(__version_info__)
