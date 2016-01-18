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
  'astronoomy jou' : [('title1', index1), ('title4', index4), ...],
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

    def addSubStrings(self, string, index):
        '''Given a string, add all unique sub-strings to
        the dictionary'''
        for t in self._splitString(string, index):
            if t[0] != '':
                self._add(t)

    def _splitString(self, string, index):
        '''Split a string into sub-strings, return a sorted list of
        unique tuples of (sub-string, string, index). '''
        front = [(string[:i].strip(), string, index) for i in range(len(string) + 1)]
        back  = [(string[i:].strip(), string, index) for i in range(len(string) + 1)]
        front.extend(back)
        return sorted(set(front))

    def _add(self, tstr):
        '''Take a tuple (sub-string, string, index) and add to the
        dictionary. If the sub-string already exists in the dictionary,
        then add the (title, index) to that key. If the sub-string does
        not exist as a key, then add a new key with the tuple as the first
        element in the value list.'''
        if tstr[0] in self.keys():
            self[tstr[0]][tstr[1]] = tstr[2]
        else:
            self[tstr[0]] = {tstr[1] : tstr[2]}


if __name__ == '__main__':

    from pprint import pprint

    titleList = [('Astronomical Journal', 1), ('Astrophysical Journal', 2),
                 ('ApJ', 2), ('Aj', 1),
                 ('Monthly Notices of the Royal Astronomical Society', 3)]

    d = SearchDict()

    for title in titleList:
        d.addSubStrings(title[0], title[1])

    print('searching for "Journal"')
    pprint(d['Journal'])
    print('\nsearching for "Astro"')
    pprint(d['Astro'])
    print('\nsearching for "Astrop"')
    pprint(d['Astrop'])
    print('\nsearching for "ApJ"')
    pprint(d['ApJ'])
    print('\nsearching for "Monthly"')
    pprint(d['Monthly'])
