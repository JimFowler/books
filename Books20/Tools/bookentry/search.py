#! /usr/bin/env python3
# -*- coding: utf-8 -*-
'''Search for a sub-string from a list of string and return some
associated value.

Given a list of strings and return values, we create another set of
sub-strings from the strings and associate the sub-strings and the
return value in a dictionary. The sub-strings are keys to the dictionary
and the values are a list of the various return values that are associated
with the string that the sub-string was created from.

Looking up a the key returns a list of tuples of (title, returnvalue).

Ideally the tuples should be in a weighted order scheme, e.g. the
sub-string is closer to the beginning of the list if the sub-string
appears closer to the start of the string. Alternatively, we can remove
the articles from the string before creating the sub-strings.  This may
best be left to the user.

For example; a dictionary created from the strings
('British Astronomy Journal', retVal1),
('Americal Astronomy Journal', retVal2),
('Astronomy Journal of Pakistan', retVal3),
('The Astronomical Journal', retVal4)
...

would look something like

{ 'astr' : [('title1', retVal1), ('title4', retVal4), ...],
  'astro' : [('title1', retVal1), ('title3', retVal3), ...],
  'astronomy jou' : [('title1', retVal1), ('title2', retVal2), ...],
  ...
}

'''
from pprint import pprint

class SearchDict(dict):
    '''SearchDict is a dictionary whose keys are sub-strings of
    strings that have been added to the dictionary.  The values are
    a list of retVals associated with the original string.'''

    def __init__(self):
        '''When a new SeachDict object is created we clear() the
        underlying dictionary.'''
        self.clear()
        return

    #
    # Public functions
    #
    def search(self, SubString, maxLen=10):
        '''Search for SubString in self. Return a list of the returnVals
        entered when the sub-strings were added or an None if no
        match was found.
        '''
        
        final = []
        try:
            sl = self[SubString[:maxLen]]
        except KeyError:
            return None

        for s in sl:
            final.append(s)
        print('search.py;', sl)
        return final

    def addSubStrings(self, string, retVal):
        '''Given a string, add all unique sub-strings to the
        dictionary. retVal will be in the list returned when a
        particular substring matches.  retVal may be any valid
        python type.
        '''
        for t in self._splitString(string, retVal):
            if t[0] != '':
                self._add(t)

    #
    # Local functions
    # (still publicly available but not recommended for public use)
    #
    def _splitString(self, string, retVal):
        '''Split a string into sub-strings.  Return a list of unique
        tuples of (sub-string, retVal).
        '''
        front = [(sstring, retVal) for sstring in self._getSubStrings(string)]
        return front

    def _getSubStrings(self, s, minN=3, maxN=10):
        '''Gets the set of all contiguous sub-strings of 's' between minN
        and maxN chars in length. If the string is shorter than maxN chars
        we set the maximum to be the length of the string.

        Returns a set of sub-strings.
        '''

        lenS = len(s) # the length of the input string
        maxN = min(maxN, lenS) # the max length substring we will return
        
        strset = set() # the temporary sub-string set
        
        if maxN >= minN and 0 < maxN:
            for sLen in range(minN, (maxN + 1)):
                for start in range(0, lenS):
                    end = start + sLen
                    if end <= lenS:
                        strset.add(s[start:end].strip())
                    else:
                        # break out of the inner loop here.
                        break
        return strset

    def _add(self, tstr):
        '''Take a tuple (sub-string, returnVal) and add it to the
        dictionary. If the sub-string already exists in the dictionary,
        then add the returnVal to that key. If the sub-string does
        not exist as a key, then add a new key with the returnVal as the first
        element in the value list.'''
        if tstr[0] in self.keys():
            self[tstr[0]].append(tstr[1])
        else:
            self[tstr[0]] = [tstr[1]]


#
# Test everything (I hope)
#
if __name__ == '__main__':
    from pprint import pprint
    import titleList as tl

    d = SearchDict()

    for title in tl.titleList:
        d.addSubStrings(title[0], (title[0],title[1]))

    print('\n\nsearching for "Journal devo"')
    pprint(d.search('Journal devo'))

    print('\n\nsearching for "Astro"')
    pprint(d.search('Astro'))

    print('\n\nsearching for "Astrop"')
    pprint(d.search('Astrop'))

    print('\n\nsearching for "ApJ"')
    pprint(d.search('ApJ'))

    print('\n\nsearching for "Optical"')
    pprint(d.search('Optical'))

    # test with the color list
    # we first clear the existing SearchDict
    #  and reloaded it with the color sub-strings
    d.clear()
    for color in tl.colorList:
        d.addSubStrings(color[0], color[1])


    print('\n\nsearching for "red"')
    pprint(d.search('red'))
