Classes
*******

mainWindow
__________

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


.. automodule:: mainWindow
    :members:
    :show-inheritance:


Select Dialog
_____________

The selectDialog class provides generic dialog and functions for
making selection for a list.  This class is used for the specific
book, author, project, etc., selections

.. automodule:: selectDialog
    :members:
    :show-inheritance:


Symbol Table
____________

The Symbol table provides a small dialog window that allows one to insert
special charactors into the current text/line edit object.  This is primarily
used to insert unicode non-ascii charactor encodings. The Symbol table class
is taken from bookentry.symbols.




Menus
_____

.. automodule:: menus
    :members:
    :show-inheritance:

DataBase
________


.. automodule:: database
    :members:
    :show-inheritance:


Sql
___


.. automodule:: sql
    :members:
    :show-inheritance:

