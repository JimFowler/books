Theory of Operation
*******************

Overview
======== 

**ajbbooks** was written primarily to facilitate user input of entries
and to facilitate review of entries (proofreading) by letting the user
concentrate on the content of the entry rather than the formatting. In
addition, it needed to be able to read the already existing book lists
that had been produced with Word. Finally, it needed to write
out the text files in a consistent format so that all files are
similar in format and structure. This later point is particularly
important for files that would later be read into a database. The
older method, of formatting the files manually, was sure to introduce
inconsistencies between files.

The list of book entries created by **ajbbooks** will be used by other
programs to generate the database for the project.  Thus **ajbbooks**
doesn't care much about the actual content of fields. It just needs to know
how to parse and write the fields.


Internal BookFile Object
========================

The internal class BookFile is defined in bookfile.py. 

=================== == ======================================
=================== == ======================================
self._header        =  __defaultHeader__
self._entryList     =  []

self._volumeNumber  =  -1
self._fileName      =  './document1'
self._dirName       =  './'
self._baseName      =  'document1'

self.curEntryNumber =  -1
self._dirty         =  False
=================== == ======================================


The primary internal variables are ``_header`` and ``_entryList``,
which contain the header of the external disk file and the list of
entries respectively.  Entries are of the Class AJBentry, defined in
AJBentry.py.  Secondary variables are ``_volumeNumber``, the value to
outfall the volume number in a new entry; ``_fileName``, the pathname
for the disk file as passed to BookFile via the command line or menu item;
``_dirName``, the directory portion of _filename; ``_baseName``, the
base name of ``_fileName``; ``_curEntryNumber``, the number of the
current active entry in ``_entryList``, restricted to the range 1 <=
``_curEntryNumber`` <= len(``_entryList``); and ``_dirty``, indicating
that the internal BookFile has been modified since the last write to
disk. The class functions are detailed in the Classes section of this
manual.
 
The default header is

.. parsed-literal::

   '''
   Entry format

   Num AJB_ID Author [and author [and …]] [ed.|comp.], Title, Place,
   Publisher, year, description, price, review [and review [and …]],
   comments

   AJB_ID   volume.section[(subsection)].entry, for example 68.144(1).25
   would be volume 68, section 144, subsection 1, and entry number 25.

   Commas are field separators for automatic parsing.  Use the word
   ‘comma’ if you want the character in field string. We will use global
   search and replace after parsing into fields.

   Save as Unicode UTF-8 text encoding. Skip section 4 in Part 1

   For volume AJB ?? Index to the Literature of ????, started, finished,
   proofread
   '''


Reading and Writing Text Files
------------------------------

The BookFile class knows how to insert/delete/replace entries in the
``_entryList``, how to open/read/write disk files, how to read the
header of a disk file, and how to recognize an entry in the disk file.
When ever it needs to read/write an entry to/from the ``_entryList``,
it calls on the entry itself to handle this action.  Entries are of type
``Class AJBentry`` defined in AJBentry.py.

AJB Entries
-----------

The ``Class AJBentry`` is a subclass of ``Entry`` which is defined in
entry.py. A generic entry object is a python dictionary with the following
fields and default values.

======================== ===== ======================
 Entry[ 'Index']          =    -1                   
 Entry[ 'Num']            =    {'volNum' : -1,         
 \                       \     'sectionNum' : -1,      
 \                       \     'subsectionNum' : -1,   
 \                       \     'entryNum' :- 1,        
 \                       \     'entrySuf' : '',
 \                       \     'volume' : ''}         
 Entry[ 'Authors']        =     []                  
 Entry[ 'Editors']        =     []                        
 Entry[ 'Compilers']      =     []                  
 Entry[ 'Contributors']   =     []                  
 Entry[ 'Translators']    =     []                  
 Entry[ 'Others']         =     []                  
 Entry[ 'Title']          =     ''                  
 Entry[ 'Publishers']     =     []                  
 Entry[ 'Year']           =     ''                  
 Entry[ 'Pagination']     =     ''                  
 Entry[ 'Price']          =     ''                  
 Entry[ 'Reviews']        =     []                  
 Entry[ 'Comments']       =     ''                  
 Entry[ 'OrigStr']        =     ''                  
======================== ===== ======================

The AJBentry adds the following items to this dictionary to add
fields that are normally in the comments.

========================= ===== ======================
 Entry[ 'TranslatedFrom']  =     ''                  
 Entry[ 'Language']        =     ''                  
 Entry[ 'Reprint']         =     ''                  
 Entry[ 'Reference']       =     ''                  
========================= ===== ======================

Index is the entry number within the individual BookFiles. It is 
simply a running count of the number of books.

designer
--------

QtDesigner 4.8 is used to build the window interfaces.  The ``ui`` files are
in the directory ``bookentry/designer``.

.. _symbol-table-theory:

symbol table
------------

The *AJB* covers the entire international field of astronomer and
astrophysics and therefore has titles and names in multiple languages
which many additional characters beyond the standard ASCII
codes. The internal and external formats are encoded
in UTF-8 rather than plain ASCII in order to deal with this issue.

Standard keyboards do not have all these additional characters and I did
not want to learn a large number of keyboard tricks in order to enter
these characters.  The solution was to build a symbol table modeled after
similar tables in advanced text editing programs.

The table was based on the charpicker.py package developed by Rich
Griswold. I found it at his blog
`http://richgriswold.wordpress.com/2009/10/17/character-picker/
<http://richgriswold.wordpress.com/2009/10/17/character-picker/>`_ but
that URL no longer appears to be valid. My symbol table code is
located in bookentry/symbol.py

Every time the symbol table is opened it reads the file
symbols.txt. The location of the symbols.txt file is found in
mainWindow.py by looking at the file name of the imported file
symbol.py. The string ``symbols.txt`` is appended to the directory
portion of this name and the resulting name is opened. This is not the
proper pythonic way of doing thing but it works for the time being.

The symbols.txt file is simply a list of characters with tool tips
separated by a comma.  The format of a file look like::

  #
  #
  # symbols.txt
  #  A symbol table for the symbol.py package under the BookEntry program
  #  6 Feb 2013 James R Fowler
  #
  #
  Ä, Capital letter A with diaeresis
  ä, Small letter a with diaeresis
  Å, Capital letter A with ring above
  å, Small letter a with ring above
  à, small letter a with grave
  á, small letter a with acute
  ç, Small letter c with cedilla
  Č, Capital letter C with caron
  č, Small letter c with caron
  ć, Small letter c with acute

  Ë, Capital letter E with diaeresis
  ë, Small letter e with diaeresis
  È, Capital letter E with grave
  É, Capital letter E with acute
  è, Small letter e with grave
  é, Small letter e with acute
  ě, Small letter e with caron
  ę, Small letter e with cedilla
  Ï, Capital letter I with diaeresis
  ï, Small letter i with diaeresis
  ì, Small letter i with grave
  í, Small letter i with acute
  î, Small letter i with caron

  Ň, Capital letter N with caron
  ň, Small letter n with caron
  Ö, Capital letter O with diaeresis
  ö, Small letter o with diaeresis
  ø, Small letter o with stroke
  ô, Small letter o with circumflex
  ò, Small letter o with grave
  ó, Small letter o with acute

  #
  # The End
  #

Comment lines begin with '#' and are ignored by the software.  Each
character is then used as the text image for a Qt button object with
the tip added as the tool tip.  A blank line in the symbols.txt
indicated the start of a new line in the window display. The action of
the button when it is clicked is to send the signal
``sigClicked(QString)`` with the character as the parameter in the
signal.

This signal in turn is caught in the BookEntry class (mainWindow.py)
and is connected to the insertChar() function.  This insertion
function changes on the fly whenever the focus changes in the
BookEntry window between the various LineEdit and TextEdit items.

