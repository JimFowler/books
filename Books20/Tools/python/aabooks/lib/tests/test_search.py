#! /usr/bin/env python3
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/lib/tests/test_search.py
##
##   Part of the Books20 Project
##
##   Copyright 2024 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrival system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright
'''The unittests for aabooks/lib/search.py'''
import unittest
from aabooks.lib import search as sr
import aabooks.lib.title_list as tl


__SEARCH_TERMS__ = [
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
        self.searchd = sr.SearchDict()

        for title in tl.TITLE_LIST:
            self.searchd.add_sub_strings(title[0], (title[0], title[1]))

    def tearDown(self):
        '''Clean up for the next tests.'''
        del self.searchd

    def test_a_search_astronomy(self):
        '''Test the search terms within the journals.'''

        for search_str, answer in __SEARCH_TERMS__:
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
