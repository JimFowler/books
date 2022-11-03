#! /usr/bin/env python3

from aabooks.ajbbook import bookfile as bf

bf1 = bf.BookFile()
bf1.set_filename('./hjs01_books.xml')
bf1.read_file_xml()

bf2 = bf.BookFile()
bf2.set_filename('./hjs02_books.xml')
bf2.read_file_xml()

bf3 = bf.BookFile()
bf3.set_filename('./hjs03_books.xml')
bf3.read_file_xml()

bf4 = bf.BookFile()
bf4.set_filename('./hjs04_books.xml')
bf4.read_file_xml()

bf_all = bf1 + bf2 + bf3 + bf4
bf_all.sort_by('Author')
bf_all.sort_by('Year')
bf_all.set_filename('./hjs_all.xml')
bf_all.write_file_xml()

