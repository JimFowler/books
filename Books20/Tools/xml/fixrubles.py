#! python
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

rubles = re.compile(r'(\d)+R')
def fix_price(entry):
    '''Replace a 'nR' strings in Price with 'n Rbl.' '''

    old_price_str = entry['Price']
    if rubles.search(old_price_str):
        entry['Price'] = rubles.sub(r'\g<1> Rbl.', old_price_str)



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

        bookfile = bf.BookFile()
        bookfile.set_filename(ajbfile)
        bookfile.read_file_xml()

        for count, entry in enumerate(bookfile):
            # this mess is because BookFile(entrylist)
            # has the header as the first item in the list
            if count == 0:
                continue

            fix_price(entry)

        bookfile.write_file_xml()

if __name__ == '__main__':

    main()
