..  Begin copyright
.. 
..   /home/jrf/Documents/books/Books20/Tools/python/doc/journals/classes.rst
..   
..    Part of the Books20 Project
.. 
..    Copyright 2016 James R. Fowler
.. 
..    All rights reserved. No part of this publication may be
..    reproduced, stored in a retrival system, or transmitted
..    in any form or by any means, electronic, mechanical,
..    photocopying, recording, or otherwise, without prior written
..    permission of the author.
.. 
.. 
..  End copyright


Classes
*******

Entry
_____

Entry provides the basic class for any book entry.  Specific sub-classes
should be created for each type of entry, Journals, AJB or AAA.

Entry is a sub-class of dict so keyword:values may be accessed
directly.  Some entry items are pre-defined but there is nothing to
prevent the program from deleting an item so programs should check for
existence of a list item before appending or extending.

The functions provided in this base class are empty and will need to be over ridden
by your specific class.

.. automodule:: entry
    :members:
    :show-inheritance:

journalEntry
____________

.. automodule:: journalEntry
    :members:
    :show-inheritance:

The journalEntry class provides the specific methods to read and write
the journal entries in XML format.  A blank journalEntry object looks
like:

.. code-block:: python
   :linenos:

   entry = {
        'Title'         = '',
        'subTitle'      = '',
        'subsubTitle'   = '',
        'Publishers'     = [],
        #
        #Publishers is list of dictionaries of the form
        #   {'Name'      : '', # required, all others optional
        #    'Place'     : '',
        #    'startDate' : '',
        #    'endDate'   : ''
        #   }
        #
        'Abbreviations' = [], # a list of strings
        'startDate'     = '', # the start of publishing
        'endDate'       = '', # the end of publishing
        'linknext'      = [], # a list of strings'
        'linkprevious'  = [], # a list of strings
        'Designators'   = {},
        #
        # Designators is a dictionary of catalogue designations
        #   for example 'ISSN' : '9-123456-789-12-3'
        #     and       "ADS_Bibcode' : '....ApJ...'
        #    others can be 
        #               'LCCN', 'DDCN', etc
        #
        'Comments'      = [] # should be a list of strings

	}



journalFile
___________ 

journalFile object provides a link between a disk file and the entry
list.  The class provides methods to read and write DiskFiles, change the
name of the file, and get/set the file header. With repect to the
entry list we can get/replace entries, and add a new entry.

.. automodule:: journalFile
    :members:
    :show-inheritance:


HeaderEntry
___________

The HeaderEntry object provides a graphical text entry window for the
journalFile header information.

.. automodule:: headerWindow
    :members:
    :show-inheritance:

Symbol Table
____________

The Symbol table provides a small dialog window that allows one to insert
special charactors into the current text/line edit object.  This is primarily
used to insert unicode non-ascii charactor encodings. The default table is
./symbols.txt.

.. automodule:: symbol
    :members:
    :show-inheritance:



JournalEntry
____________

The JournalEntry  object is the main  user interface to the  entries in a
file.   It  is  defined  in ``journalWin.py``.   The  JournalEntry  class
contains a journalFile, header entry, and symbol table objects.

.. automodule:: journalWin
    :members:
    :show-inheritance:

