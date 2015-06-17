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

# lxml has schema validation and is more complete the etree
from lxml import etree
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
