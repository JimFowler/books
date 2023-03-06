#! /usr/bin/env python3
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Data/HJS/make94.py
##
##   Part of the Books20 Project
##
##   Copyright 2023 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrival system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright
from pprint import pprint

from aabooks.ajbbook import bookfile as bf
from aabooks.lib import utils

bf01 = bf.BookFile()
bf01.set_filename('hjs01_books.xml')
bf01.read_file_xml()

# entries in hjs01 with a comment listing an HJS 94 entrynum
bf94 = bf.BookFile()

# entries in hjs01_books.xml without a comment listing an HJS 94 entrynum
bf00 = bf.BookFile()

first = True
for entry in bf01:
    no_94 = True
    # for each comment, check for 'HJS 94'
    for comment in entry['Others']:
        if 'HJS 94' in comment:
            # swap hjs01 num and hjs94 num
            #if first:
            #    pprint(entry['Num'])
            entry['Others'].append(entry.num_str())
            entry['Num'] = utils.parse_ajbnum(comment[comment.index('HJS'):])
            entry['Num']['pageNum'] = 1
            #if first:
            #    pprint(entry['Num'])
            #    first = False
            entry['Others'].remove(comment)
            bf94.append(entry)
            no_94 = False
    if no_94:
        bf00.append(entry)

#pprint(bf94[0])
bf94.set_filename('hjs94_books.xml')
bf94.sort_by('num')
bf94.write_file_xml()

bf00.set_filename('hjs00_books.xml')
bf00.write_file_xml()


        
