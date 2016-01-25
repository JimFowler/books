#! /usr/bin/env python3
# -*- coding: utf-8 -*-
''' Searching for a Title

Want to look for a sub-string within a list of sub-strings formed from
the title and abbreviation. If we find a match, we return a list of
titles and indicies to the relevant entires.

The sub-strings are keys to a dictionary.  Looking up a the key
returns a list of tuples of (title, index). The list of tuples should
be alphabetized by title. Alternatively, the tuples should be in a
weighted order scheme, e.g. the title appears closer to the begining
of the list if the sub-string appears closer to the start of the
title. But this later feature is harder to implement.

The dictionary looks like

{ 'astr' : [('title1', index1), ('title2', index2), ...],
  'astro' : [('title1', index1), ('title3', index3), ...],
  'astronomy jou' : [('title1', index1), ('title4', index4), ...],
  ...
}
'''

class SearchDict(dict):
    '''SearchDict is a dictionary whose keys are sub-strings of
    strings that have been added to the dictionary.  The values are
    a dictionary of the original string as well as an index into
    something else.'''

    def __init__(self):
        self.clear()
        return

    def _valkey(self, s):
        return s[2]

    def search(self, ss1):
        '''Search for sub-string ss1 in self. Compute the distance of
        the sub-string for the start of title string. Return a list of
        (title, index) sorted by the start distance.'''

        final = []
        try:
            sl = self[ss1[:10]]
        except:
            return final

        for s in sl:
            sdist = s[0].find(ss1)
            if sdist != -1:
                final.append((s[0], s[1], sdist))

        final.sort(key=self._valkey)

        return final

    def addSubStrings(self, string, index):
        '''Given a string, add all unique sub-strings to
        the dictionary'''
        for t in self._splitString(string, index):
            if t[0] != '':
                self._add(t)

    def _splitString(self, string, index):
        '''Split a string into sub-strings, return a sorted list of
        unique tuples of (sub-string, string, index). '''
        front = [(sstring, string, index) for sstring in self._getSubStrings(string)]
        return front

    def _getSubStrings(self, s, minN=3, maxN=10):
        '''Gets the set of all contiguous sub-strings of 's' between minN
        and maxN chars in length. If the string is shorter than maxN chars
        we set the maximum to be the length of the string. Returns a set
        of sub-strings.'''

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
        '''Take a tuple (sub-string, string, index) and add to the
        dictionary. If the sub-string already exists in the dictionary,
        then add the (title, index) to that key. If the sub-string does
        not exist as a key, then add a new key with the tuple as the first
        element in the value list.'''
        if tstr[0] in self.keys():
            self[tstr[0]].append((tstr[1], tstr[2]))
        else:
            self[tstr[0]] = [(tstr[1], tstr[2])]


if __name__ == '__main__':

    from fuzzywuzzy import fuzz
    from pprint import pprint
    from titleList import titleList



    #titleList = [('Astronomical Journal', 1), ('The Astrophysical Journal', 2),
    #             ('ApJ', 2), ('Aj', 1),
    #             ('Monthly Notices of the Royal Astronomical Society', 3)]

    d = SearchDict()

    for title in titleList:
        d.addSubStrings(title[0], title[1])

    pprint(d.search('Journal devo'))

    pprint(d.search('Astrop'))
    pprint(d.search('Optical'))
    pprint(d.search('Astro'))
    '''
    print('\nsearching for "Astro"')
    pprint(d['Astro'])
    print('\nsearching for "Astrop"')
    pprint(d['Astrop'])
    print('\nsearching for "ApJ"')
    pprint(d['ApJ'])
    print('\nsearching for "Monthly"')
    pprint(d['Monthly'])
    '''
