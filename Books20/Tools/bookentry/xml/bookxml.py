'''Tests for XML version of bookfile.  Ultimately need to read an XML file
into a bookfile class and write a bookfile class to an XML file.

 We might also consider transforming the BookFile class, defined in 
bookfile.py, into an ElementTree and work 1n 'pure' XML.
'''
# -*- coding: UTF-8 -*-
# -*- mode: Python;-*-

import sys
import fileinput
import os
import traceback
import json

# lxml has schema validation, pretty print, and is more complete the etree
from lxml import etree
from copy import deepcopy

# Building an etree
bf = etree.XML('''<?xml version="1.0"?>
<BookFile>
</BookFile>''')
hdr = etree.SubElement(bf, 'Header')
ets = etree.SubElement(bf, 'Entries')
et = etree.SubElement(ets, 'Entry')
et.text = 'Entry 0'
et = etree.SubElement(ets, 'Entry')
et.text = 'Entry 1'
et = etree.SubElement(ets, 'Entry')
et.text = 'Entry 2'
et = etree.SubElement(ets, 'Entry')
et.text = 'Entry 3'
et = etree.SubElement(ets, 'Entry')
et.text = 'Entry 4'
et = etree.SubElement(ets, 'Entry')
et.text = 'Entry 5'

print()
print('This is a byte stream with UTF-8 encoding and an xml header')
print(etree.tostring(bf, pretty_print=False,
                     method='xml', encoding='UTF-8',
                     xml_declaration=True))

print()
print('Entry subelement 1 is', ets[1].tag)
print('bookfile has', len(bf), 'subelements')
print('Entries has', len(ets), 'subelements')

print()
print('Insert Entries[3] before Entries[5]')
ets.insert( 5, deepcopy(ets[3]) )
ael = etree.Element('Entry')
ael.text = 'Appended entry 8'
ets.append(ael)
print(etree.tostring(bf, pretty_print=True,
                     method='xml', encoding='unicode'))

print()
print('Elements have getnext() and getprevious() functions')
print('ets[1] is ets[0].getnext()', ets[1] is ets[0].getnext())
print('ets[2] is ets[3].getprevious()', ets[2] is ets[3].getprevious())

print()
hdr.text = 'This is the bookfile header.'
print(etree.tostring(hdr, pretty_print=True,
                     method='xml', encoding='unicode'))

print()
print('Get all the Entry elements')
for el in bf.iter('Entry'):
    print(el.text)

print()
print('We can read and validate a file with the parse() function')
try:
    bf_schema = etree.XMLSchema(file='bookfile.xsd')
    Parser = etree.XMLParser(schema=bf_schema)
    print('The schema is well formed')
except:
    print('The schema is not well formed')
    sys.exit(1)

try:
    print('Validating minimal bookfile ajbtest_books.xml')
    bf2 = etree.parse('ajbtest_books.xml', parser=Parser)
    print('ajbtest_books.xml is well formed and valid')
    print()
    print(etree.tostring(bf2, pretty_print=True,
                         method='xml', encoding='unicode'))
except:
    print('The xml file is not well formed or xxx is invalid')

try:
    print('Validating the full entry file ajbtest3_books.xml')
    bf3 = etree.parse('ajbtest3_books.xml', parser=Parser)
    print('ajbtest3_books.xml is well formed and valid')
except:
    print('The xml file is not well formed or is invalid')
    sys.exit(0)

bf_root = bf3.getroot()
print('bf_root[0] is ', bf_root[0].tag)
print('bf_root[1] is ', bf_root[1].tag)
