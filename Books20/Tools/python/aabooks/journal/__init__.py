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
'''Import the version string for everybody.'''
from .version import __version__
#
# __sort_dict__ is used by the Sort By menu item chain
#   to determine what key should be used in sorting journalentries
#   in JournalFile objects.
#
# The menu_key is the word used in the Edit->Sort By menu.
# sort_word is the value use in JournalFile.sort_by() as the key
#   in journalentry.sort_key() that the list object journalfile will
#   use when sorting the journalentries.
#
__sort_dict__ = {
# menu_key : sort_word,
    'Start Year' : 'year',
    'Title' : 'title',
    'Place' : 'place',
    'Publisher' : 'publisher',
    'Restore Orig Order' : 'orig',
}
