## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/lib/utils.py
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
'''Utility functions that may be used in various programs.'''

from nameparser import HumanName
from nameparser.config import CONSTANTS

# add SJ Suffix list
CONSTANTS.suffixes.add('sj')

def make_name_list(line, sep=' and '):
    """Returns a list of object of class HumanName. See the package
    nameparser for full info. The names have the following possible keys
    "Title", "First", "Middle", "Last", and "Suffix"
    """
    name_list = []
    names = line.split(sep)

    for name in names:
        clean_name = HumanName(name.strip())
        name_list.append(clean_name)

    return name_list

def make_name_str(name_list, sep=' and '):
    """Returns a string built from a list of HumanName objects.
    See the package nameparser for details about HumanName.
    """
    name_str = ''
    if not name_list:
        return name_str

    first = True
    for name in name_list:
        if not first:
            name_str += sep
        first = False
        name_str += str(name)

    return name_str

if __name__ == '__main__':
    print('No tests available yet')
