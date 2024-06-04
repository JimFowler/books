#! /usr/bin/env python3

from aabooks.ajbbook import bookfile as bf

bfhjs = bf.BookFile()
bfhjs.set_filename('./hjs_all.xml')
bfhjs.read_file_xml()

total_count = 0
isbn_count = 0

for ent in bfhjs:
    total_count += 1
    for comment in ent['Others']:
        if 'ISBN' in comment:
            isbn_count += 1

print(f'total: {total_count}, isbn_count: {isbn_count}')

