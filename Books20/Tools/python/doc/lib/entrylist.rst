..  Begin copyright
.. 
..   /home/jrf/Documents/books/Books20/Tools/python/doc/lib/entryfile.rst
.. 
..    Part of the Books20 Project
.. 
..    Copyright 2020 James R. Fowler
.. 
..    All rights reserved. No part of this publication may be
..    reproduced, stored in a retrival system, or transmitted
..    in any form or by any means, electronic, mechanical,
..    photocopying, recording, or otherwise, without prior written
..    permission of the author.
.. 
.. 
..  End copyright
 
entrylist
*********

A generic class which contains a list of entries described by entry.py
as well as the metadata associated with the entries.  An EntryFile
consists of a header and a list of entries.  The EntryFile class
should be a sub-class of list with metadata of header, filename,
basename, file extention (indicating the file type), 

Will need to modify ajbbooks/bookfile.py and journal/journalfile.py
to incorporate this functionality

metadate

  * dirty_flag

  * header

  * filename

  * dirname

  * basename

  * extension

Function

  * def __init__(self):

  * def is_dirty(self):
    
  * def set_filename(self, filename):

  * def get_filename(self):

  * def get_dirname(self):

  * def get_basename(self):

  * def get_basename_with_extension(self):

  * def get_extension(self):

  * def set_header(self, headerstr):

  * def get_header(self):

  * def max_entries()
    
  * def get_entry(self, count=-1):

  * def set_entry(self, entry, count=-1):

  * def set_new_entry(self, entry, count=-1):

  * def delete_entry(self, entrynum): # might be able to list operators to code these calls

  * def insert_entry(self, entrynum=-1)

  * def read_file(self, filename=None):

  * def write_file(self, filename=None):

.. automodule:: entrylist
   :members:
   :show-inheritance:



