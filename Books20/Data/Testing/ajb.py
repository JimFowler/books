#! python
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
#
import fileinput


#
# parse_line
# 
#  Parse out the relevent fields from a line.
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
#   expressions
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
#     
#
def parse_line( line ):
    lineList = line.split(',')

    # split out the authors/editors
    field01 = lineList[0].split( " ", 2)
    print field01[0], field01[2], field01[1]
    return





#
# Loop through every line putting the data in the database.
#
linecount = 0

for line in fileinput.input():
    linecount += 1
    if(13 < linecount):
        parse_line( line )
    else:
        print line

exit


