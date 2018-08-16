#! /usr/bin/env python3
# -*- mode: Python;-*-
"""The version number for Books20 python programs.

Store the version here so:
 1) we don't load dependencies by storing it in __init__.py
 2) we can import it in setup.py for the same reason
 3) we can import it into your module module
"""

__version_info__ = ('8', '16', '56')
__major__ = __version_info__[0]
__minor__ = __version_info__[1]
__micro__ = __version_info__[2]

__version__ = '.'.join(__version_info__)


