..  Begin copyright
.. 
..   /home/jrf/Documents/books/Books20/Tools/python/doc/journals/theory.rst
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


Theory of Operation
*******************

Overview
======== 

**journals** was written primarily to facilitate user input of entries
and to facilitate review of entries (proofreading) by letting the user
concentrate on the content of the entry rather than the formatting. In
addition, it needed to be able to read the already existing book lists
that had been produced with Word. Finally, it needed to write
out the text files in a consistent format so that all files are
similar in format and structure. This later point is particularly
important for files that would later be read into a database. The
older method, of formatting the files manually, was sure to introduce
inconsistencies between files.

The list of journal entries created by **journals** will be used by other
programs to generate the database for the project.  Thus **journals**
doesn't care much about the actual content of fields. It just needs to know
how to parse and write the fields.


Internal JournalFile Object
===========================

The internal class JournalFile is defined in bookfile.py. 

=================== == ======================================
=================== == ======================================
self._header        =  __defaultHeader__
self._entryList     =  [] # a list of journalEntry objects

self._fileName      =  './document1'
self._dirName       =  './'
self._baseName      =  'document1'

self.curEntryNumber =  -1
self._dirty         =  False
self.schemaName     =  None
self._dirty         =  False
=================== == ======================================


The primary internal variables are ``_header`` and ``_entryList``,
which contain the header of the external disk file and the list of
entries respectively.  Entries are of the class journalEntry, defined in
journalEntry.py.  Secondary variables  ``_fileName``, the pathname
for the disk file as passed to JournalFile via the command line or menu item;
``_dirName``, the directory portion of _filename; ``_baseName``, the
base name of ``_fileName``; ``_curEntryNumber``, the number of the
current active entry in ``_entryList``, restricted to the range 1 <=
``_curEntryNumber`` <= len(``_entryList``); and ``_dirty``, indicating
that the internal JournalFile has been modified since the last write to
disk. The class functions are detailed in the Classes section of this
manual.
 


Journal Entries
---------------

The ``class journalEntry`` is a subclass of ``Entry`` which is defined in
entry.py. A generic entry object is a python dictionary with the following
fields and default values.

=============== === ======================
'Title'          =   ''
'subTitle'       =   ''
'subsubTitle'    =   ''
'Publishers'     =   []
'Abbreviations'  =   [] # a list of strings
'startDate'      =   '' # the start of publishing
'endDate'        =   '' # the end of publishing
'linknext'       =   [] # a list of strings'
'linkprevious'   =   [] # a list of strings
'Designators'    =   {}
'Comments'       =   [] # should be a list of strings
=============== === ======================

``Publishers`` is list of dictionaries of the form::

  {'Name'      : '', # required, all others optional
   'Place'     : '',
   'startDate' : '',
   'endDate'   : ''
  }

where ``startDate`` and ``endDate`` are the dates when the publisher
started/ended publication of the particular journal. A number of journals
changed publishers during their lifetime.

``startDate`` and ``endDate`` in the journalEntry itself refer to the
starting/ending dates of publication.  A journal ends publication when it
merges with another journal or ceases operations all together.

``linnext`` and ``linkprevious`` are for journals that have merged or are
the result of a merge.  ``linknext`` lists the journals that merged to form
this journal.  ``linkprevious`` is the name of the journal that this one
merged into.

``Designators`` is a dictionary of catalogue designations for example::

  { 'ISSN' : '9-123456-789-12-3',
    'ADS_Bibcode' : '....ApJ...'
  }

others can be 'LCCN', 'DDCN', etc.

``Comments`` are any other information about the journal that is not
included in the above fields.


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
indicated the start of a new row in the window display. The action of
the button when it is clicked is to send the signal
``sigClicked(QString)`` with the character as the parameter in the
signal.

This signal in turn is caught in the main window defined in
JournalWindow class (journalWin.py) and is connected to the
insertChar() function.  This insertion function changes on the fly
whenever the focus changes in the BookEntry window between the various
LineEdit and TextEdit items.

Search Dialog
-------------

The search dialog
