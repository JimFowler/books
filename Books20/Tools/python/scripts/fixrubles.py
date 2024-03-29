#! /usr/bin/env python
#
#  open the xml file
#   for each entry
#    if search <Price> for nR
#      replace 'nR' with 'n Rbl.'
#  write file
'''Replace the price signature for Ruble, 'nR', with 'n Rbl.' This is so
we don't confuse Rands or other price signature with Rubles.'''

import argparse
import re

from pprint import pprint

import aabooks.lib.utils as aautils
import aabooks.ajbbook.bookfile as bf

__DESCRIPTION__ = '''Change price in Rubels from R to Rbl'''

def getargs():
    '''Get the command line arguments and files to test.'''

    parser = argparse.ArgumentParser(description=__DESCRIPTION__)

    aautils.standard_parser_args(parser)

    parser.add_argument('ajbfiles',
                        help='a list of files to check',
                        nargs='*',
                        action='append')

    args = parser.parse_known_args()[0]

    return args

rubles = re.compile(r'(\d+[.]?\d*)\s?(R[.]?[\W]+|R[.]?$)')
def fix_price(count, entry):
    '''Replace a 'nR ' strings in Price with 'n Rbl.' '''

    old_price_str = entry['Price'].strip()

    if rubles.search(old_price_str):
            new_price_str = rubles.sub(r'\g<1> Rbl. ', old_price_str)
            entry['Price'] = new_price_str.strip()
            print('{} "{}" : "{}"'.format(count, old_price_str, entry['Price']))


def main():
    '''The main function to update prices in many files.'''
    # get command line
    args = getargs()
    if args.verbose:
        pprint(args)

    # open xml file to bookfile
    # for each entry
    #
    for ajbfile in args.ajbfiles[0]:
        print('working on:', ajbfile)
        bookfile = bf.BookFile()
        bookfile.set_filename(ajbfile)
        bookfile.read_file_xml()

        for count, entry in enumerate(bookfile):
            fix_price(count, entry)

        bookfile.write_file_xml()

if __name__ == '__main__':

    main()
