#
# python code to read, edit, and write the JSON structures
#  for the table of contents as well as page and entry counts
#

import json
import pprint

# open the file and return the file descriptor
fp = open("ajb_aaa.json")

# read the JSON string from the file and put it
# in the dictionary labeled 'aj'
aj = json.load(fp)

# set the pretty indent to 2 spaces
# and pretty print the dict 'aj'
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(aj)

#
# 'aj' is a dictionary aj["keyword"]
# aj["Parts"] is a list of dictionaries
# aj["Parts"}[0] is a dictionary
# aj["Parts"}[0]["Sections"] is a list of dictionaries
# aj["Parts"}[0]["Sections"][0] dictionary
# aj["Parts"}[0]["Sections"][0] is a list of dictionaries
# aj["Parts"}[0]["Sections"][0] dictionary
#
# Should aj be just a dictionary of dictionaries?
#
