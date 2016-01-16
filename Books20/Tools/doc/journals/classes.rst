Classes
*******

Entry
_____

Entry provides the basic class for any book entry.  Specific sub-classes
should be created for each type of entry, AJB or AAA.

Entry is a sub-class of dict so keyword:values may be accessed
directly.  Some entry items are pre-defined but there is nothing to
prevent the program from deleting an item so programs should check for
existence of a list item before appending or extending. A blank Entry
objects look like:

.. code-block:: python
   :linenos:

   entry = {
	'Index' :     -1            # file index number
	'Num' :       {'volNum':-1,       # bibliography entry num
                       'sectionNum':-1,
                       'subsectionNum':-1,
                       'entryNum':-1,
                      'volume': ''}
        'Authors' :   []   # list of nameparser::HumanName objects
	'Editors' :   []   # list of nameparser::HumanName objects
	'Compilers' : []   # list of nameparser::HumanName objects
	'Contributors' : [] # list of nameparser::HumanName objects
	'Translators'] : []   # list of nameparser::HumanName objects
	'Others' ] :  []   # list strings from the comments that we can't parse
	'Title' :      ''   # the title of the work
	'Publishers' : []   # list of tuples (Place, PublisherName)
	'Year' :       ''   # year of publication, if known
	'Pagination' : ''   # page count, if known
	'Price' :      ''   # publishers price, if known
	'Reviews'] :   []   # bibliographic list of reviews, strings
	'Comments' :   ''   # the original comment string
	'OrigStr' :    ''   # the original book entry string if read from a string
	}


.. automodule:: entry
    :members:
    :show-inheritance:

journalEntry
____________

The journalEntry class provides the specific methods for read and write
journal entries.

.. automodule:: journalEntry
    :members:
    :show-inheritance:


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

