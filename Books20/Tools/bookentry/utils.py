'''Utility functions that may be used in various programs.'''

from nameparser import HumanName
from nameparser.constants import SUFFICES

# add SJ and second, third, etc to Suffix list
suffixes_c = SUFFICES | set(['sj', 'ii', 'iii', 'iv', 'v'])

def makeNameList( line, sep=' and ' ) :
    """Returns a list of object of class HumanName. See the package
    nameparser for full info. The names have the following possible keys
    "Title", "First", "Middle", "Last", and "Suffix"
    """
    name_list = []
    names = line.split(sep)
    
    for name in names :
        nm = HumanName( name.strip(), suffixes_c=suffixes_c )
        name_list.append(nm)

    return name_list

def makeNameStr( namelist, sep=' and '):
    """Returns a string built from a list of HumanName objects.
    See the package nameparser for details about HumanName.
    """

    nameStr = ''
    if not namelist:
        return nameStr
    
    first = True
    for nm in namelist:
        if not first:
            nameStr += sep
        first = False
        nameStr += nm.full_name
        
    return nameStr
