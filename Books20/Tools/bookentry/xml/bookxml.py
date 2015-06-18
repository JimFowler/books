"""Tests for XML version of bookfile.  Ultimately need to read an XML file
into a bookfile class and write a bookfile class to an XML file.

 We might also consider transforming the BookFile class, defined in 
bookfile.py, into an ElementTree and work 1n 'pure' XML.
"""
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
bf = etree.Element('Bookfile')
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
print('We can read a file with the parse() function')
bf2 = etree.parse('ajbtest_books.xml')
print(etree.tostring(bf2, pretty_print=True,
                     method='xml', encoding='unicode'))

'''
import xml.etree.ElementTree as ET
import xml.dom.minidom as md

def prettify(elem, indent='  '):
    """Return a pretty-printed XML string for the Element.
    But if Element is was read in as a pretty string, this will
    further indent it. Use this to create human readable version??
    """
    _indent = indent

    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = md.parseString(rough_string)
    return reparsed.toprettyxml(_indent)


__version__ = 1.0

tree = ET.parse('ajbtest2_books.xml') # an ElementTree instance
root = tree.getroot() # an Element instance

print('root tag:', root.tag)

# Gets all the elements of an Entry
for child in root.findall('./Entries/Entry'):
    for el in child:
        print(el.tag)


for child in root.findall('./Entries/Entry'):
    for el in child:
        if el.tag == 'Title':
            print('Title:', el.text)
        elif el.tag == 'subTitle':
            print('SubTitle:', el.text)

# Either one of these procedures builds elements and subelements
pub = ET.Element('Publisher')
place = ET.SubElement(pub, 'Place')
place.text='London'
publ = ET.SubElement(pub, 'Name')
publ.text='My Publishing Co.'
root.append(pub)

tbuild = ET.TreeBuilder()
prices = tbuild.start('Prices')
price = tbuild.start('Price')
tbuild.start('Amount')
tbuild.data('12.5')
tbuild.end('Amount')
tbuild.start('Currency')
tbuild.data('$')
tbuild.end('Currency')
tbuild.end('Price')
tbuild.end('Prices')
root.append(prices)

# Write out the tree
ET.register_namespace('',"http://het.as.utexas.edu/jrf/ns")
tree.write('test.out', encoding='UTF-8', xml_declaration=True,
           method='xml', short_empty_elements=False)

# but tree.write() does not pretty print the XML unless the
# original XML file was pretty printed.

#print(prettify(root))
'''
