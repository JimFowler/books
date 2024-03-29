#! /usr/bin/env python3
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/lib/search.py
##
##   Part of the Books20 Project
##
##   Copyright 2018 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrieval system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright
'''Search for a string from a list of strings and return some
associated value.

Given a list of strings and return values, we create another set of
sub-strings from the strings and associate the sub-strings and the
return value in a dictionary. The sub-strings are keys to the
dictionary and the values are a list of the various return values that
are associated with the string that the sub-string was created from.

Looking up a the key returns a list of tuples of (title, returnvalue).

The sub-strings and search string are case-sensitive.

Ideally the tuples should be in a weighted order scheme, e.g. the
sub-string is closer to the beginning of the list if the sub-string
appears closer to the start of the string. Alternatively, we can
remove the articles from the string before creating the sub-strings.
This may best be left to the user.

As an example; a dictionary created from the strings

  | ('British Astronomy Journal', retVal1),
  | ('Americal Astronomy Journal', retVal2),
  | ('Astronomy Journal of Pakistan', retVal3),
  | ('The Astronomical Journal', retVal4)
  | ...

would look something like

  | { 'Astr' : [('British Astronomy Journal', retVal1),
  |             ('The Astronomical Journal', retVal4), ...],
  |   'Astro' : [('British Astronomy Journal', retVal1),
  |              ('Astronomy Journal of Pakistan', retVal3), ...],
  |   'Astronomy Jou' : [('British Astronomy Journal', retVal1),
  |                      ('Ameican Astronomy Journal', retVal2), ...],
  |   ...
  | }

'''

def __get_sub_strings__(string, min_length=3, max_length=10):
    '''Gets the set of all contiguous sub-strings of 's' between minN
    and maxN chars in length. If the string is shorter than maxN chars
    we set the maximum to be the length of the string.

    Returns a set of sub-strings.

    '''

    # the length of the input string
    len_string = len(string)
    # the max length substring we will return
    max_length = min(max_length, len_string)

    strset = set() # the temporary sub-string set

    if max_length >= min_length and max_length > 0:
        for length in range(min_length, (max_length + 1)):
            for start in range(0, length):
                end = start + length
                if end <= length:
                    strset.add(string[start:end].strip())
                else:
                    # break out of the inner loop here.
                    break

    if len(string) < min_length:
        # if the length is shorter than the substrings
        # we also add the string itself.
        strset.add(string)

    return strset

def __split_string__(string, value):
    '''Split a string into sub-strings.  Return a list of unique
    tuples of (sub-string, value).
    '''
    substring_list = [(substring, value) for substring in __get_sub_strings__(string)]
    return substring_list


class SearchDict(dict):
    '''SearchDict is a dictionary whose keys are sub-strings of strings
    that have been added to the dictionary.  The sub-strings are
    case-sensitive. The values are a list of retVals associated with
    the original string.

    '''

    def __init__(self):
        '''When a new SeachDict object is created clear() the
        underlying dictionary.'''
        super().__init__()
        self.clear()

    #
    # Public functions
    #
    def search(self, string, max_length=10):
        '''Search for string in self. Return a list of the return_vals
        entered when the strings were added or an empty list if no
        match was found. string is case-sensitive. max_length is the
        maximum length of string we will search for.

        '''

        final_list = []
        try:
            str_list = self[string[:max_length]]
        except KeyError:
            return final_list

        for sub_string in str_list:
            final_list.append(sub_string)
        return final_list

    def add_sub_strings(self, string, return_value):
        '''Given a string, add all unique sub-strings to the
        dictionary. return_value will be in the list returned when a
        particular sub-string matches.  return_value may be any valid
        python type.

        '''

        for substring in __split_string__(string, return_value):
            if substring[0] != '':
                self._add(substring)

    #
    # Local functions
    # (still publicly available but not recommended for public use)
    #
    def _add(self, tstr):
        '''Take a tuple (sub-string, returnVal) and add it to the
        dictionary. If the sub-string already exists in the dictionary,
        then add the returnVal to that key. If the sub-string does
        not exist as a key, then add a new key with the returnVal as the first
        element in the value list.

        '''

        if tstr[0] in self.keys():
            self[tstr[0]].append(tstr[1])
        else:
            self[tstr[0]] = [tstr[1]]


#
# Test everything (I hope)
#
if __name__ == '__main__':

    import unittest
    import aabooks.lib.title_list as tl

    SEARCH_TERMS = [
        ('Journal de', [('Journal des Observateurs', 1)]),
        ("Annales d'", [("Annales d'Astrophysique", 1)]),
        ('Astro', [('Astronomische Abhandlungen', 1),
                   ('Astronomische Blätter', 1),
                   ('Astronomical Herald', 1),
                   ('Astronomical Journal of Soviet Union', 1),
                   ('Astronomische Nachrichten', 1)]),
        ('ApJ', [('ApJ', 1)]),
        ('BZ', [('BZ', 1)]),
        ('apj', []),
        ('Optical', []),
        ]

    class SearchTestCase(unittest.TestCase):
        '''Unit tests for search.py.'''

        def setUp(self):
            '''Set up the unit tests.'''
            self.searchd = SearchDict()

            for title in tl.TITLE_LIST:
                self.searchd.add_sub_strings(title[0], (title[0], title[1]))

        def tearDown(self):
            '''Clean up for the next tests.'''
            del self.searchd

        def test_a_search_astronomy(self):
            '''Test the search terms within the journals.'''

            for search_str, answer in SEARCH_TERMS:
                prelim_answer = self.searchd.search(search_str)
                self.assertEqual(prelim_answer, answer)

        def test_b_colors(self):
            '''Test the color list.'''

            self.searchd.clear()
            for color in tl.COLOR_LIST:
                self.searchd.add_sub_strings(color[0], color[1])

            answer = [('apple', 'blood', 'cherry', 'ferrari'),
                      ('blood', 'apple', 'ferrari')]
            prelim_answer = self.searchd.search('red')
            self.assertEqual(prelim_answer, answer)

            answer = []
            prelim_answer = self.searchd.search('animal')
            self.assertEqual(prelim_answer, answer)

    unittest.main()
