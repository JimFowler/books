'''Tests for XML version of bookfile.  Ultimately need to read an XML file
into a bookfile class and write a bookfile class to an XML file.

 We might also consider transforming the BookFile class, defined in
bookfile.py, into an ElementTree and work 1n 'pure' XML.
'''
# -*- coding: UTF-8 -*-
# -*- mode: Python;-*-

import sys

# lxml has schema validation, pretty print, and is more complete the etree
from copy import deepcopy
from lxml import etree

# Building an etree
BF = etree.XML('''<?xml version="1.0"?>
<BookFile>
</BookFile>''')
HDR = etree.SubElement(BF, 'Header')
ETS = etree.SubElement(BF, 'Entries')
ET = etree.SubElement(ETS, 'Entry')
ET.text = 'Entry 0'
ET = etree.SubElement(ETS, 'Entry')
ET.text = 'Entry 1'
ET = etree.SubElement(ETS, 'Entry')
ET.text = 'Entry 2'
ET = etree.SubElement(ETS, 'Entry')
ET.text = 'Entry 3'
ET = etree.SubElement(ETS, 'Entry')
ET.text = 'Entry 4'
ET = etree.SubElement(ETS, 'Entry')
ET.text = 'Entry 5'

print()
print('This is a byte stream with UTF-8 encoding and an xml header')
print(etree.tostring(BF, pretty_print=False,
                     method='xml', encoding='UTF-8',
                     xml_declaration=True))

print()
print('Entry subelement 1 is', ETS[1].tag)
print('bookfile has', len(BF), 'subelements')
print('Entries has', len(ETS), 'subelements')

print()
print('Insert Entries[3] before Entries[5]')
ETS.insert(5, deepcopy(ETS[3]))
AEL = etree.Element('Entry')
AEL.text = 'Appended entry 8'
ETS.append(AEL)
print(etree.tostring(BF, pretty_print=True,
                     method='xml', encoding='unicode'))

print()
print('Elements have getnext() and getprevious() functions')
print('ets[1] is ets[0].getnext()', ETS[1] is ETS[0].getnext())
print('ets[2] is ets[3].getprevious()', ETS[2] is ETS[3].getprevious())

print()
HDR.text = 'This is the bookfile header.'
print(etree.tostring(HDR, pretty_print=True,
                     method='xml', encoding='unicode'))

print()
print('Get all the Entry elements')
for el in BF.iter('Entry'):
    print(el.text)

print()
print('We can read and validate a file with the parse() function')
try:
    BF_SCHEMA = etree.XMLSchema(file='bookfile.xsd')
    PARSER = etree.XMLParser(schema=BF_SCHEMA)
    print('The schema is well formed')
except etree.XMLSchemaParseError:
    print('The schema is not well formed')
    sys.exit(1)

try:
    print('Validating minimal bookfile ajbtest_books.xml')
    BF2 = etree.parse('ajbtest_books.xml', parser=PARSER)
    print('ajbtest_books.xml is well formed and valid')
    print()
    print(etree.tostring(BF2, pretty_print=True,
                         method='xml', encoding='unicode'))
except etree.XMLSyntaxError:
    print('The xml file is not well formed or xxx is invalid')

try:
    print('Validating the full entry file ajbtest3_books.xml')
    BF3 = etree.parse('ajbtest3_books.xml', parser=PARSER)
    print('ajbtest3_books.xml is well formed and valid')
except etree.XMLSyntaxError:
    print('The xml file is not well formed or is invalid')
    sys.exit(0)

BF_ROOT = BF3.getroot()
print('BF_ROOT[0] is ', BF_ROOT[0].tag)
print('BF_ROOT[1] is ', BF_ROOT[1].tag)
