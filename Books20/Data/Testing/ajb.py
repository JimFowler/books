
#
# Parse the file of books enteries from Astronomischer Jahresbericht.
# The entries are found in the ajb??_books.txt file. Once we have the
# relevant data put the values into the database.  I don't know what the
# database final form is but is will most likely consist of data tables
# and relationship tables.
#
# created 6 July 2012
#
# usage: python ajb.py file1 [file2 [...]]
#
#   Work
#     (new or previously defined)
#     work attributes ???
#     general bibliography entries including AJB/AAA entries
#
#   Person/Corporation
#     Authors
#     Translations
#     Editors
#     Publishers
#      their relationship to the expression
#
#   Expressions
#    bibliography number (AJB num)
#    Year
#    Place
#    Pagination
#    Cost
#    Reviews
#    Relationship
#       e.g. translation, new edition, Dover release, etc.
#
# Parse comments for additional Person/Corporation
#
# To Do:
#  subsitute ',' for ' comma '
#  check authors string for editors, drop the ' ed.|comp.'
#  check comments for translators, editions, other publishers
#      reference link, languages from/to,
#  what to do about error checking?
#
import sys
import os
import fileinput

from entry import *

if __name__ == '__main__':

    del sys.argv[0]
    for file in sys.argv:
        if not os.path.isfile(file):
            print('%s is an invalid file' % file)
        else:
            entTemp = AJBentry()

            for line in fileinput.input([file]):
                line = line.strip()
                entTemp.blankEntry()
                entTemp.extract(line)
                
                if entTemp.isValid():
                    index = entTemp.getval('Index')
                    comment = entTemp.getval('Comments')
                    if comment:
                        #print('Index %s: %s' % index, comment)
                        print( 'Index ' + index + ':  ' + comment) 

            
            
