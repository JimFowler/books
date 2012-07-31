"""Parse line entries for the books abstracted from the
Astronomische Jahrbericht series.

Classes
--------

ajbEntry()
    Takes a unicode string with comma separated fields
    and returns an entDict object.

Functions
---------

Some of the parsing functions may be public so that folks can
use them outside of the class object.

  A line looks like:
   Index AJB_Num Author, Title, Place, Publisher, Year, \
   Pagination, Price, Reviews, Comments

  No field need be present except Index and AJB_Num.

   Field 1 Index AJB_Num Author has format

    Index AJB_Num [I. A. Author [jr.|III|...] [ and H. E. Another [and ...]]] \
     [ed.|comp.|something else]

   Field 2 Title

   Field 3 Place

     [name | name-name[-name[-...]] Name may contain spaces

   Field 4 Publisher

   Field 5 Year

   Field 6 Pagination

   Field 7 Price

   Field 8 Reviews

     [Journal vol page [and Journal vol page [and ...]]]

     Need to pull the Journal and reference from here

   Field 9 Comment

     Need to do something with these. They contains editions, editors,
      translators, and other people as well as references and language.

  An ajbEntry object will return

  EntryDict = {
    'Index' : -1,
    'AJBNum' : {'volNum':-1, 'sectionNum':-1,
                'subsectionNum':-1, "entryNum":-1},
    'Authors' : [],   # array of author(s) in priority order
    'Editors' : [],   # array of editor(s)
    'Translators' : [], # array of translator(s)
    'Others' : [],    # array of other people associated with this expression
    'Title' : '',
    'Publishers' : [], # array of publishers 
    'Year' : -1,
    'Pagination' : '',
    'Price' : '',
    'Reviews' : [],
    'Comments' : '',
    }

    where Authors, Editors, Translators, and Other are lists of people.
    Each list entry will be a dictionary
         {'FirstName' : '', 
          'MiddleNames' : '',
          'LastName' : '',
          'Suffix' : '',
         }

    Publishers is also a list of dictionarys
         { 'Place' : '',
           'PublisherName' : ''
         }
"""     

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
import re

class AJBentry():
    """Class that manages an AJB entry and associated information

    Functions:
    __init__(ajbstr=NONE) -- creates a new, empty AJBentry with the values
          listed below as predfined in the dictionary
      extract(line) -- extracts values from a text entry.
      getVal(ValueName:) -- get the value of one of the entries
      setVal("ValueName") -- set an existing value or a new value
          Possibly set reference data based on existing data values
          in the database.
    """

  _entryDict = {}
  
  def __init__(ajbstr=NONE):
    """Alloc entry dictionaru
    if string in nonempty, parse string and add to entry
    use self.setparam()
    """

    
    _EntryDict = {
        'Index' : -1,
        'AJBNum' : {'volNum':-1, 'sectionNum':-1,
                    'subsectionNum':-1, "entryNum":-1},
        'Authors' : [],   # array of author(s) in priority order
        'Editors' : [],   # array of editor(s)
        'Translators' : [], # array of translator(s)
        'Others' : [],    # array of other people associated with this expression
        'Title' : '',
        'Publishers' : [], # array of publishers 
        'Year' : -1,
        'Pagination' : '',
        'Price' : '',
        'Reviews' : [],
        'Comments' : '',
        }

#
#  Parse out the relevent fields from a line
#    into an Entry Dictionary
# 
#

def parseFileIndex( line ):
    """
    Get the file Index value (i.e. what number is this entry
    in the file.
    """

    entryDict['Index'] = line.strip()

    
def parseAJBNum( line ):
    """
    Get the Volume, Section, any possible subSection and the
    section entry number.  The subSection defaults to zero
    if no subSection value exists.
    """
    #
    # This regular expression is used to parse the AJB number
    # which is  of the form volNum.sectionNum[(subsectionNum)].entryNum,
    # where the subseectionNum is optional e.g. 66.18(1).25. It returns the list
    # [empty, volNum, sectionNum, string, subsectionNum, itemNum, empty].
    # Note that the subsectionNum may not be there in which case both 
    # item 3 and 4 will be NONE and the subsection number defaults to zero.
    #
    r2 = re.compile(r'(\d+)\.(\d+)(\((\d+)\))*\.(\d+)')

    nums = r2.split(line.strip())

    if not nums[4]:
        nums[4] = 0

    return {'volNum':nums[1],
            'sectionNum':nums[2],
            'subsectionNum':nums[4],
            'entryNum':nums[5],
            }


def parseField0( line ) : 

    # split out the authors/editors
    fields = line.split( ' ', 2)

    parseFileindex( fields[0] )

    fields[2] = fields[2].strip()
    entryDict['Authors'] = fields[2].split(' and ')
    return


def parseComments( field ):

    entryDict['Comments'] = field


if __name__ == '__main__':

    import fileinput
    import pprint

    #
    # Loop through every line putting the data in the database.
    #
    linecount = 0
    
    #
    # This regular expression is used to check the beginning of a line
    # for an item number. If no item number is seen we skip the line.
    r1 = re.compile(r'\A\d+')
    
    
    #
    # The main work
    #
    for line in fileinput.input() : 

        line = line.strip()

        # Skip blank lines and non-index lines i.e. leading comments
        if line and r1.match(line):
            linecount += 1
            if linecount < 5:
                fields = line.split(',')
                fieldNum = -1
                for field in fields :
                    
                    fieldNum += 1
                    field = field.strip()
                    
                    if 0 == fieldNum:
                        parseField0( field )
                        
                    elif 1 == fieldNum:
                        entryDict['Title'] = field
                        
                    elif 2 == fieldNum:
                        Place = field
                        
                    elif 3 == fieldNum:
                        entryDict['Publishers'] =
                        [ {'Place' : Place,
                           'PublisherName' : field.strip(),}]
                        
                    elif 4 == fieldNum:
                        entryDict['Year'] = field
                        
                    elif 5 == fieldNum:
                        entryDict['Pagination'] = field
                        
                    elif 6 == fieldNum:
                        entryDict['Price'] = field
                        
                    elif 7 == fieldNum:
                        entryDict['Reviews'] = field.split(' and ')
                        
                    elif 8 == fieldNum:
                        parseComment( field )
                        
                        

                        pprint.pprint( entryDict )

exit


