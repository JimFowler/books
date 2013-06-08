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

AJBentry
________

The AJBentry class provides the specific methods for read and write
entries from the Astronomische Jahresbericht.

.. automodule:: AJBentry
    :members:
    :show-inheritance:


AJB Comments
____________

.. automodule:: AJBcomments
    :members:
    :show-inheritance:


AJB entries have much common information however there are entries
that have additional information that is not common enough to have an
additional field in the Book Entry. For this additional information
there is a comment field defined. The comment infomation does have
enough common features that we have defined a grammer to allow for
automatic parsing of the field but have also allowed a grammer that allow
one to put anything in the field.  The grammer is defined as:

.. productionlist:: AJBcomments
  Comment       : ( Edition | Compilers | Contributors | Reference | Reprint |
                : Editors | Translation | Publishers | Language | Other );
  Edition       : ( Digit | TwoDigit ), ( 'nd' | 'rd' | 'st' | 'th' ), [(
                : 'facsimile' | 'revised' )], 'edition', ';';
  Compilers     : 'compiled by', NameList, ';';
  Contributors  : 'contributors', NameList, ';';
  Reference     : 'reference', AJBNum, ';';
  Reprint       : 'reprint of', ( AJBNum | Year ), ';';
  Editors       : 'edited by', NameList, ';';
  Translation   : 'translated', [FromLanguage], [ToLanguage], ['by', NameList], ';';
  Publishers    : 'also published', PublisherList, ';';
  Language      : 'in', LanguageList, ['with', uWords, 'references'], ';';
  Other         : 'other', uWords, ';';
  Digit         : ? WORD('0-9') ?;
  TwoDigit      : ? WORD('0-9') ?;
  NameList      : Name, {Name};
  AJBNum        : 'AJB', Volume, '.', Section, '.', Item;
  Year          : ? WORD('0-9') ?;
  FromLanguage  : 'from', uWord;
  ToLanguage    : 'into', uWord;
  PublisherList : Publisher, {Publisher};
  LanguageList  : uWords, {uWords};
  uWords        : uWord, {uWord};
  Name          : [Initial, ['-', Initial]], [( Initial, ['-', Initial] ),
                : {Initial, ['-', Initial]}], uWords;
  Volume        : TwoDigit;
  Section       : ? <RE> ?;
  Item          : ? <RE> ?;
  uWord         : ? <RE> ?;
  Publisher     : uWords, ':', uWords;
  Initial       : ? <RE> ?, '.';


BookFile
________ 

BookFile object provides a link between a disk file and the entry
list.  The class provides methods to read/write diskfile, change the
name of the file, and get/set the file header. With repect to the
entry list we can get/replace entries, and add a new entry.

.. automodule:: bookfile
    :members:
    :show-inheritance:


HeaderEntry
___________

The HeaderEntry object provides a graphical text entry window for the
bookfile header information.

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


Original String 
_______________

Displays the original file string if the entry came from an existing file.

.. automodule:: origstrWindow
    :members:
    :show-inheritance:


BookEntry
_________

The BookEntry object is the main user interface to the entries in a file.
It contains a bookfile, header entry, and symbol table objects.

.. automodule:: mainWindow
    :members:
    :show-inheritance:

