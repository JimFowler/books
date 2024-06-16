#
# search AJB or AAA books
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/ajbbook/search.py
##
##   Part of the Books20 Project
##
##   Copyright 2024 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrival system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright
'''
Search AJB or AAA book files for a set of charateristics.

Would be easier to put all this in a database and do an SQL lookup

Class inputs:
   a list of AJB/AAA bookfiles
   search categories
   search parameters
     and, or, not  ?

Class output
   a bookfile of matching entries


Fields

HumanName (last, first, middle, 
author
editors
AuthorEditor
translator
compiler
contributers
AllPeople

Strings
ajbnum
title
comments
place
publisher
keywords

Date
publication date (year)

tasks
  contains  # strings 'contain' other strings
  numeric       # numbers|dates can be = != >= > <= <
  date

Field.task='string' [logical 


Command Line/Config file Arguments
standard arg
AJB/AAA locations
search string  area=string

output  a bookfile object, use ajbbooks to display

what if the entry is a reference
    print both? need to search for an AJBnum


reverse lookup to catch references
for every file in AAA and AJB
  search fields
  if found or reference
     add to book file
'''
from aabooks.ajbbook import bookfile as bf
from aabooks.ajbbook import ajbentry

'''
We parse the search_terms into a set of these tuples

field - Author, Editor, Translator, Compiler, Contributer
        AnyPerson convert to the tuples Author, Editor, Translator, etc.
    All need to loop over multiple entries.
    Also need AnyPerson.LastName, AnyPerson.FirstName
    AnyPerson without a modifier will search all names
        Title, Publisher, Place
        Year -- numeric
action -- 'in' 'not in', '==', '!=', '<>'

(object: str, action: str, field: str)

object -- the thing we are looking for
action -- the relationship between the fields and the object
field -- the dictionary key in the entry
 ex. Lowell in Author.LastName or Lowell in AnyPerson
'''
__PERSON_LIST__: list = ['Authors', 'Editors', 'Translators', 
                                  'Compilers', 'Contributors']

def search_people(entry: ajbentry.AJBentry, object: str,
                  action: 'str', field: str) -> bool:
    '''Check for object 'action' in the given entry fields'''
    print(f'{object = }, {action = }, {field = }')
    final_result: bool = False
    if field == 'AnyPerson':
        slist: list = __PERSON_LIST__
    else:
        slist: list = [field] # need to deal with multiple fields here as well

    for name_field in slist:
        final_result |= any([object in hname.full_name for hname in entry[name_field]])

    return final_result

class SearchEntry():
    '''Given the search terms decide if the entry matches the
    search terms.

    '''
    def __init__(self, search_terms: str) -> None:
        '''Set up the search terms for this particular search.'''

        self.search_list: list = []
        self.set_search(search_terms)

    def set_search(self, search_terms) -> None:
        '''Set up the search structure (what ever that is) for
        this search.

        start with 'name in AnyPerson'
           expand some day to further tests and logical connections
        '''
        if search_terms:
            terms: list = search_terms.split()
            self.search_list = [(f'{terms[0]}', 'in', terms[2])]

    def search(self, entry: ajbentry.AJBentry) -> bool:
        '''Search an AJB/AAA entry against the search structure.
        Return True/False if search term is/not found.

        '''
        final_result: bool = False
        #print('Search entry:')
        for object, action, field in self.search_list:
            #print(f'{object = }, {action = }, {field = }')
            if field == 'AnyPerson' or field in __PERSON_LIST__:
                final_result |= search_people(entry, object, action, field)
        #print(f' final_result: {final_result}')
        return final_result


class SearchFiles():
    '''A class to consolidate the search functions to search book files
    containing AJB and/or AAA entries.

    You can not change the search terms after initialization but
    you can search additional files.

    Return a bookfile object with the matching entries or a bookfile
    object with no entries if no entries match.  The header will still
    contain the date, the list of files searched, and the search terms.

    '''

    def __init__(self, search_terms: str = '',
                 files: list[str] = [''],
                 header: str = '') -> None:
        '''Set up the class structure, kwargs can be a list of
        file to search, the search terms (in some format TBD),'''

        self._bookfile: bf.BookFile = bf.BookFile()
        self._files: list[str] = files
        self._search_entry: SearchEntry = SearchEntry(search_terms=search_terms)

        self.set_header(header)

    def set_header(self, header: str = '') -> None:
        '''Write all relevant information to the books file header,
        date/time
        files
        search terms

        '''
        self._bookfile.set_header(header)

    def search(self) -> bf.BookFile:
        '''Perform the search with the search terms on the files'''

        for afile in self._files:
            # read afile into a bookfile
            bfile = bf.BookFile()
            bfile.set_filename(afile)
            bfile.read_file_xml()
            for entry in bfile:
                if self._search_entry.search(entry):
                    self._bookfile.append(entry)
            del bfile
        return self._bookfile

    def search_more_files(self, files: list[str]):
        '''Add additional files to the search list'''
        self._files = files

        return self.search()
