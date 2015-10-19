#! /usr/bin/env python
# -*- mode: Python;-*-
'''Validate a set of XML files to a given schema.'''

import sys
import argparse

# lxml has schema validation, pretty print, and is more complete the etree
from lxml import etree

Version = "version v1.0.0"

Usage = '''%(prog)s [options] schemafile.xsd xmlfile.xml [...]
The return values in $? are

 100 - not a failure, the --Version option was called,
 101 - no schema file was given on the command line,
 102 - no XML files were given on the command line,
 103 - the schema file is not well formed,
   0 - the schema is well formed and all xml files successfully validated,
   1, 2, 3... 'n' of the XML files did not validate correctly.
'''

Description='''Validate the XML files against the given schema. The
program may be used stand-alone and provide human readable text output
or in may be used in a script in which case the exit value in $? may
be checked for success or failure.
'''


def getargs():
    parser = argparse.ArgumentParser(
        description=Description,
        usage=Usage)
    
    
    parser.add_argument('-V', '--version',
                        help='provide version info,',
                        action='store_true')
    parser.add_argument('-v', '--verbose',
                        help='provide user readable output.',

                        action='store_true')

    parser.add_argument('schemafile', nargs="?", default="")
    parser.add_argument('xmlfiles', nargs=argparse.REMAINDER)

    args = parser.parse_args()
    
    return args, parser
#
# Main Action
#

args, parser = getargs()

if args.version:
    print(Version)
    sys.exit(100)

if args.schemafile != '':
    if args.verbose:
        print('Schema file: %s\n' % (args.schemafile))
else:
    if args.verbose:
        print('No schema file given.')
    sys.exit(101)

if len(args.xmlfiles) == 0:
    if args.verbose:
        print('No XML files given.')
    sys.exit(102)
else:
    if args.verbose:
        print('XML files:')
        for f in args.xmlfiles:
            print("   %s" % (f))
        print('\n')

#
# we have a Schema file and at least one XML file
#
#
try:
    schema = etree.XMLSchema(file=args.schemafile)
    Parser = etree.XMLParser(schema=schema)
    if args.verbose:
        print('The schema in file %s is well formed' % (args.schemafile))
except:
    if args.verbose:
        print('The schema is not well formed')
    sys.exit(103)

returnCount = 0
for f in args.xmlfiles:
    try:
        bf2 = etree.parse( f, parser=Parser)
        if args.verbose:
            print('The XML file %s is valid against the schema' % (f))
    except:
        if args.verbose:
            print('The XML file %s is NOT valid against the schema' % (f))
            returnCount += 1

sys.exit(returnCount)

