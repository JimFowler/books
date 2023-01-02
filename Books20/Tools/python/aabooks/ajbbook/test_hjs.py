#! /usr/bin/env python3
# -*- mode: Python;-*-
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Docs/Hjs/test_hjs.py
##
##   Part of the Books20 Project
##
##   Copyright 2022 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrival system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright
'''Test the HjsEntry() class in cat_entry.py.  This will also test
the CatEntry() class as well.  Should produce the test_books.tex
file from the test_hjs.xml file.

'''

from aabooks.ajbbook import bookfile as bf
import cat_entry as ce

# Create test_books.xml
hjs_entry = ce.HjsEntry()
with open('test_books.tex', 'w', encoding='UTF8') as filep:
    bookf = bf.BookFile()
    bookf.read_file('../../Data/HJS/hjs_jrf.xml')

    for test_count, test_entry in enumerate(bookf):
        test_count += 1
        hjs_entry.print_entry(test_count, test_entry, outf=filep)
