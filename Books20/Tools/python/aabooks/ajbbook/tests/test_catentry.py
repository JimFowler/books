#! /usr/bin/env python3
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/ajbbook/tests/test_catentry.py
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
'''Provide the unit tests for aabooks/ajbbook/catentry.py.  This test are
incomplete right now.
'''
import unittest
from aabooks.ajbbook import catentry as ce

class CatEntryTestCase(unittest.TestCase):
    '''Run the unit tests for the class CatEntry.'''

    def setUp(self):
        '''Set things up for every test.'''
        self.cat_entry = ce.CatEntry()

    def tearDown(self):
        '''Clean up the mess after every test.'''
        del self.cat_entry

    def test_a_make_edition(self):
        '''test the self.cat_entry.make_edition() function.'''
        self.assertEqual(self.cat_entry.make_edition(1), r'\Ord{1}{st} edition')
        self.assertEqual(self.cat_entry.make_edition(2), r'\Ord{2}{nd} edition')
        self.assertEqual(self.cat_entry.make_edition(3), r'\Ord{3}{rd} edition')
        self.assertEqual(self.cat_entry.make_edition(4), r'\Ord{4}{th} edition')
        self.assertEqual(self.cat_entry.make_edition(11), r'\Ord{11}{th} edition')
        self.assertEqual(self.cat_entry.make_edition(12), r'\Ord{12}{th} edition')
        self.assertEqual(self.cat_entry.make_edition(13), r'\Ord{13}{th} edition')
        self.assertEqual(self.cat_entry.make_edition(14), r'\Ord{14}{th} edition')
        self.assertEqual(self.cat_entry.make_edition(101), r'\Ord{101}{st} edition')
        self.assertEqual(self.cat_entry.make_edition(102), r'\Ord{102}{nd} edition')
        self.assertEqual(self.cat_entry.make_edition(103), r'\Ord{103}{rd} edition')
        self.assertEqual(self.cat_entry.make_edition(104), r'\Ord{104}{th} edition')
