'''Provide the unittests for ajbook/search.py'''
import unittest

from aabooks.ajbbook import search
from aabooks.ajbbook import bookfile as bf

def mkname(ajbname: str) -> str:
    '''Create the full path name for an Ajb/AAA file'''

    dirloc: str = '/home/jrf/Documents/books/Books20/Data/'
    return dirloc + ajbname

def mk_name_list() -> list[str]:
    '''Make a list for file names'''
    name_list: list[str] = ['Ajb/ajb23_books.xml', 'Ajb/ajb63_books.xml', 'AAA/aaa08_books.xml',
                            'AAA/aaa20_books.xml', 'AAA/aaa33_books.xml'] 
    return [mkname(name) for name in name_list]


class SearchFunctionTestCase(unittest.TestCase):
    '''Test for the AJB/AAA search class'''

    def setUp(self):
        '''Start every test with a fresh of variables'''
        self.search_file: search.SearchFiles = search.SearchFiles(search_terms='',
                                                        header='This is a test header string',
                                                        files=mk_name_list())

    def tearDown(self) -> None:
        del self.search_file
        return super().tearDown()

    def test_search(self) -> None:
        '''Test the search thing'''
        bfile: bf.BookFile = self.search_file.search()
        self.assertEqual(len(bfile), 0)
