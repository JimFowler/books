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

    name_list: list[str] = ['Ajb/ajb63_books.xml', 'AAA/aaa33_books.xml']
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

    def test_a(self) -> None:
        '''Test the search thing'''
        bfile: bf.BookFile = self.search_file.search()
        self.assertEqual(len(bfile), 0)

    def test_b_AnyPerson(self) -> None:
        '''Test the AnyPerson search'''
        search_file: search.SearchFiles = search.SearchFiles(search_terms='Abetti in AnyPerson',
                                                        header='This is a test header string',
                                                        files=mk_name_list())
        bfile: bf.BookFile = search_file.search()
        del search_file
        self.assertEqual(len(bfile), 3)

    def test_c_Author(self) -> None:
        '''Test a specifc field for person'''
        search_file: search.SearchFiles = search.SearchFiles(search_terms='Abetti in Authors',
                                                        header='This is a test header string',
                                                        files=mk_name_list())
        bfile: bf.BookFile = search_file.search()
        del search_file
        self.assertEqual(len(bfile), 3)

    def test_d_Editor(self) -> None:
        '''Test a specifc field for person'''
        search_file: search.SearchFiles = search.SearchFiles(search_terms='Abetti in Editors',
                                                        header='This is a test header string',
                                                        files=mk_name_list())
        bfile: bf.BookFile = search_file.search()
        del search_file
        self.assertEqual(len(bfile), 0)
