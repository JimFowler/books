#!/usr/bin/python
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
import fileinput
import re
import pprint
#
#  Parse out the relevent fields from a line
#    into an Entry Dictionary
# 
#
#  A line looks like:
#   Index AJB_Num Author, Title, Place, Publisher, Year,
#   Pagination, Price, Reviews, Comments
#
#
#   Field 1 Index AJB_Num Author has format
#
#    Index AJB_Num [I. A. Author [ and H. E. Another [and ...]]] \
#     [ed.|comp.|something else]
#
#   Field 2 Title
#
#   Field 3 Place
#
#     [name | name-name[-name[-...]] Name may contain spaces
#
#   Field 4 Publisher
#
#   Field 5 Year
#
#   Field 6 Pagination
#
#   Field 7 Price
#
#   Field 8 Reviews
#
#     [Journal vol page [and Journal vol page [and ...]]]
#
#     Need to pull the Journal and reference from here
#
#   Field 9 Comment
#
#     Need to do something with these contains editions, editors,
#      translators, and other people
#
#  Returns
#    
# Authors, Editors, Translators, and Other are lists of people.
#   Each list entry will be a dictionary
#         {'FirstName' : '', 
#          'MiddleNames' : '',
#          'LastName' : '',
#          'Suffix' : '',
#         }
#
# Publishers is a list of dictionarys
#         { 'Place' : '',
#           'PublisherName' : ''
#         }
#     
#
entryDict = {
    'Index' : -1,
    'AJBNum' : '-1.-1.-1',
    'Authors' : [],   # array of author(s) in priority order
    'Editors' : [],   # array of editor(s)
    'Translators' : [], # array of translators
    'Others' : [],    # array of other people associated with this expression
    'Title' : '',
    'Publishers' : [], # array of publishers 
    'Year' : -1,
    'Pagination' : '',
    'Price' : '',
    'Reviews' : [],
    'Comments' : '',
    }



def parseField0( line ) : 

    # split out the authors/editors
    fields = line.split( ' ', 2)
    entryDict['Index'] = fields[0].strip()
    entryDict['AJBNum'] = fields[1].strip()
    fields[2] = fields[2].strip()
    return





#
# Loop through every line putting the data in the database.
#
linecount = 0
r1 = re.compile(r'^[0-9]+')

for line in fileinput.input() : 
    line = line.strip()
    if (line and r1.match(line)):  # Skip blank lines and non-index lines i.e. leading comments
        linecount += 1
        if (linecount < 5) :
            fields = line.split(',')
            fieldNum = -1
            for field in fields :
                fieldNum += 1
                if (0 == fieldNum):
                    parseField0( field )
                elif (1 == fieldNum ):
                    entryDict['Title'] = field.strip()
                elif (2 == fieldNum):
                    Place = field.strip()
                elif (3 == fieldNum):
                    entryDict['Publishers']= [ {'Place' : Place, 'PublisherName' : field.strip(),}]
                elif (4 == fieldNum):
                    entryDict['Year'] = field.strip()
                elif (5 == fieldNum):
                    entryDict['Pagination'] = field.strip()
                elif (6 == fieldNum):
                    entryDict['Price'] = field.strip()
                elif (7 == fieldNum):
                    entryDict['Reviews'] = field.strip()
                elif (8 == fieldNum):
                    entryDict['Comments'] = field.strip()
                    


            pprint.pprint( entryDict )

exit


