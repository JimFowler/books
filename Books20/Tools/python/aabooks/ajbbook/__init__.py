## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/bookentry/__init__.py
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
'''Import the version string.'''
from .version import __version__
#
# __sort_dict__ is used by the Sort By menu item chain
#   to determine what key should be used in sorting ajbentries
#   in BookFile objects.
#
# The menu_key is the word used in the Edit->Sort By menu.
# sort_word is the value use in bookfile.sort_by() as the key
#   in ajbentry.sort_key() that the list object bookfile will
#   use when sorting the ajbentries.
#
__sort_dict__ = {
    # menu_key : sort_word,
    'Year' : 'year',
    'Title' : 'title',
    'AJB/AAA Num' : 'num',
    'Place' : 'place',
    'Publisher' : 'publisher',
    'Language' : 'language',
    'Author/Editor' : 'author',
    'Restore Orig Order' : 'orig',
}
