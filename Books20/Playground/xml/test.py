#! /usr/bin/env python3
# -*- coding: utf-8; -*-
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/bookentry/xml/bookxml.py
##  
##   Part of the Books20 Project
##
##   Copyright 2018 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrival system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright

'''Tests for XML version of bookfile.  Ultimately need to read an XML file
into a bookfile class and write a bookfile class to an XML file.

 We might also consider transforming the BookFile class, defined in
bookfile.py, into an ElementTree and work 1n 'pure' XML.
'''

import sys

from pprint import pprint

# lxml has schema validation, pretty print, and is more complete the etree
from lxml import etree

XSI = "http://www.w3.org/2001/XMLSchema-instance"
XS = '{http://www.w3.org/2001/XMLSchema}'


SCHEMA_TEMPLATE = r"""<?xml version="1.0" ?>
<xs:schema xmlns="https://dummy.libxml2.validator"
targetNamespace="https://dummy.libxml2.validator"
xmlns:xs="http://www.w3.org/2001/XMLSchema"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
version="1.0"
elementFormDefault="unqualified"
attributeFormDefault="unqualified">
</xs:schema>"""

def validate_XML(tree):
    """Validate an XML file represented as string. Follow all schemaLocations.
    :param xml: XML represented as string.
    :type xml: str

    https://gist.github.com/mloesch/5255230
    """

    schema_tree = etree.XML(SCHEMA_TEMPLATE)
    # Find all unique instances of 'xsi:schemaLocation="<namespace> <path-to-schema.xsd> ..."'
    schema_locations = set(tree.xpath("//*/@xsi:schemaLocation", namespaces={'xsi': XSI}))
    for schema_location in schema_locations:
        # Split namespaces and schema locations ; use strip to remove leading
        # and trailing whitespace.
        namespaces_locations = schema_location.strip().split()
        pprint(namespaces_locations)
        # Import all found namspace/schema location pairs
        for namespace, location in zip(*[iter(namespaces_locations)] * 2):
            print(namespace, location)
            xs_import = etree.Element(XS + "import")
            xs_import.attrib['namespace'] = namespace
            xs_import.attrib['schemaLocation'] = location
            schema_tree.append(xs_import)
    # Construct the schema
    schema = etree.XMLSchema(schema_tree)
    print(etree.tostring(schema_tree, pretty_print=True,
                     method='xml', encoding='unicode'))

    # Validate!
    schema.assertValid(tree)

if __name__ == '__main__':
    
    bf = etree.parse('ajbtest4_books.xml')

    validate_XML(bf)

