#
# -*- mode: Python;-*-
#
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/ajbbook/entryxml.py
##
##   Part of the Books20 Project
##
##   Copyright 2020 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrival system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright
'''This file contains the functions needed to convert AJB/AAA entries
into XML format in accordance with the schema defined in bookfile.xsd.
The two main functions are entry_from_xml() and entry_to_xml().  These
functions depend explicitly on the definition of the class AJBentry
defined in ajbentry.py and can not be used with out ajbentry.py.

'''

import sys
import traceback
import re
from lxml import etree
from nameparser import HumanName

from aabooks.lib import utils

# pylint: disable=exec-used,unused-argument

__reg2__ = re.compile(r'([0-9]+)([A-Za-z]*)', re.ASCII)

# XML create routines
#
# will need to change bookfile.py as well
#def write_xml_from_entry(self):
def entry_to_xml(entry):
    '''This function converts an Entry dictionary to an XML Entry element.
    The input argument is the Entry and the function returns the XML
    element.

    '''

    if not entry.is_valid():
        return None

    # Title and Index are required of any entry
    entryxml = etree.Element('Entry')

    anum = entry['Num']
    entryxml.append(make_ajbnum_xml(anum))

    elm = etree.SubElement(entryxml, 'Title')
    elm.text = entry['Title']

    # This ends the required elements.  All further elements
    # may be missing or blank.
    entry_xml_subtitles(entry, entryxml)
    entry_xml_authors(entry, entryxml)
    entry_xml_editors(entry, entryxml)
    entry_xml_publishers(entry, entryxml)
    entry_xml_year(entry, entryxml)
    entry_xml_edition(entry, entryxml)
    entry_xml_pagination(entry, entryxml)
    entry_xml_price(entry, entryxml)
    entry_xml_reviews(entry, entryxml)
    entry_xml_translatedfrom(entry, entryxml)
    entry_xml_language(entry, entryxml)
    entry_xml_translators(entry, entryxml)
    entry_xml_translationof(entry, entryxml)
    entry_xml_compilers(entry, entryxml)
    entry_xml_contributors(entry, entryxml)
    entry_xml_reprint(entry, entryxml)
    entry_xml_reference(entry, entryxml)
    entry_xml_others(entry, entryxml)
    entry_xml_keywords(entry, entryxml)

    # return the root Entry element
    return entryxml

def entry_xml_subtitles(entry, entryxml):
    '''Convert the entry subTitles to XML'''
    if entry.not_empty('subTitle'):
        elm = etree.SubElement(entryxml, 'SubTitle')
        elm.text = entry['subTitle']

def entry_xml_authors(entry, entryxml):
    '''Convert the entry Authors to XML'''
    # Create the people list, right now these lists are
    # only HumanNames but we need to add business names
    # in the future.
    if entry['Authors']:
        elm = etree.SubElement(entryxml, 'Authors')
        for author in entry['Authors']:
            autelm = etree.SubElement(elm, 'Author')
            # all authors are humannames right now.
            person = make_person_xml(author)
            autelm.append(person)

def entry_xml_editors(entry, entryxml):
    '''Convert the entry Editor to XML'''
    if entry['Editors']:
        elm = etree.SubElement(entryxml, 'Editors')
        for editor in entry['Editors']:
            edelm = etree.SubElement(elm, 'Editor')
            # all authors are humannames right now.
            person = make_person_xml(editor)
            edelm.append(person)

def entry_xml_publishers(entry, entryxml):
    '''Convert the entry Publishers to XML'''
    if entry['Publishers']:
        elm = etree.SubElement(entryxml, 'Publishers')
        for publ in entry['Publishers']:
            epub = etree.SubElement(elm, 'Publisher')

            eplace = etree.Element('Place')
            eplace.text = publ['Place']
            epub.append(eplace)

            epn = etree.Element('Name')
            epn.text = publ['PublisherName']
            epub.append(epn)

def entry_xml_year(entry, entryxml):
    '''Convert the entry Year (of publication) to XML'''
    if entry.not_empty('Year'):
        elm = etree.SubElement(entryxml, 'Year')
        elm.text = str(entry['Year'])

def entry_xml_edition(entry, entryxml):
    '''Convert the entry Edition to XML'''
    if entry.not_empty('Edition'):
        elm = etree.SubElement(entryxml, 'Edition')
        elm.text = str(entry['Edition'])

def entry_xml_pagination(entry, entryxml):
    '''Convert the entry Pagination to XML'''
    if entry.not_empty('Pagination'):
        elm = etree.SubElement(entryxml, 'Pagination')
        elm.text = str(entry['Pagination'])

def entry_xml_price(entry, entryxml):
    '''Convert the entry Price to XML'''
    # The schema defines a price with currency and value
    # but we need to do some intellegent parsing of the prices
    # before we can use this.  For now we just naively use
    # the string.
    if entry.not_empty('Price'):
        elm = etree.SubElement(entryxml, 'Prices')
        for price in entry['Price'].split(' and '):
            priceelm = etree.SubElement(elm, 'Price')
            priceelm.text = price

def entry_xml_reviews(entry, entryxml):
    '''Convert the entry Reviews to XML'''
    if entry['Reviews']:
        elm = etree.SubElement(entryxml, 'Reviews')
        for rev in entry['Reviews']:
            revelm = etree.SubElement(elm, 'Review')
            revelm.text = str(rev)

def entry_xml_translatedfrom(entry, entryxml):
    '''Convert the entry TranslatedFrom to XML'''
    if entry.not_empty('TranslatedFrom'):
        elm = etree.SubElement(entryxml, 'TranslatedFrom')
        elm.text = str(entry['TranslatedFrom'])

def entry_xml_language(entry, entryxml):
    '''Convert the entry Language to XML'''
    if entry.not_empty('Language'):
        elm = etree.SubElement(entryxml, 'Language')
        elm.text = str(entry['Language'])

def entry_xml_translators(entry, entryxml):
    '''Convert the entry Translators to XML'''
    if entry['Translators']:
        elm = etree.SubElement(entryxml, 'Translators')
        for trans in entry['Translators']:
            aelm = etree.SubElement(elm, 'Translator')
            # all transltors are humannames right now.
            person = make_person_xml(trans)
            aelm.append(person)

def entry_xml_translationof(entry, entryxml):
    '''Convert the entry TranslationOf to XML'''
    # Sometimes the translationof can be just a year number rather than
    # an AJBnum.  An AJBnum should have decimal points in it and
    # Years should not, so we look for a decimal point to determine
    # which it is.
    if entry.not_empty('TranslationOf'):
        elm = etree.SubElement(entryxml, 'TranslationOf')
        if len(entry['TranslationOf'].split('.')) == 1:
            # Must be a year
            eyear = etree.SubElement(elm, 'Year')
            eyear.text = entry['TranslationOf']
        else:
            # parse_ajbnum is defined for the text conversion!
            numdict = utils.parse_ajbnum(entry['TranslationOf'])
            num = make_ajbnum_xml(numdict)
            elm.append(num)

def entry_xml_compilers(entry, entryxml):
    '''Convert the entry Compilers to XML'''
    if entry['Compilers']:
        elm = etree.SubElement(entryxml, 'Compilers')
        for compiler in entry['Compilers']:
            aelm = etree.SubElement(elm, 'Compiler')
            # all compilers are humannames right now.
            person = make_person_xml(compiler)
            aelm.append(person)

def entry_xml_contributors(entry, entryxml):
    '''Convert the entry Contributors to XML'''
    if entry['Contributors']:
        elm = etree.SubElement(entryxml, 'Contributors')
        for contrib in entry['Contributors']:
            aelm = etree.SubElement(elm, 'Contributor')
            # all contributors are humannames right now.
            person = make_person_xml(contrib)
            aelm.append(person)

def entry_xml_reprint(entry, entryxml):
    '''Convert the entry Reprint to XML'''
    # Sometimes the reprint can be just a year number rather than
    # an AJBnum.  An AJBnum should have decimal points in it and
    # Years should not, so we look for a decimal point to determine
    # which it is.
    if entry.not_empty('Reprint'):
        elm = etree.SubElement(entryxml, 'ReprintOf')
        if len(entry['Reprint'].split('.')) == 1:
            # Must be a year
            eyear = etree.SubElement(elm, 'Year')
            eyear.text = entry['Reprint']
        else:
            # parse_ajbnum is defined for the text conversion!
            numdict = utils.parse_ajbnum(entry['Reprint'])
            num = make_ajbnum_xml(numdict)
            elm.append(num)

def entry_xml_reference(entry, entryxml):
    '''Convert the entry Reference to XML'''
    if entry.not_empty('Reference'):
        elm = etree.SubElement(entryxml, 'ReferenceOf')
        # parse_ajbnum is defined for the text conversion!
        numdict = utils.parse_ajbnum(entry['Reference'])
        ajbxml = make_ajbnum_xml(numdict)
        elm.append(ajbxml)

def entry_xml_others(entry, entryxml):
    '''Convert the entry Others (comments) to XML'''
    if entry.not_empty('Others'):
        elm = etree.SubElement(entryxml, 'Comments')
        for comment in entry['Others']:
            com = etree.SubElement(elm, 'Comment')
            com.text = comment

def entry_xml_keywords(entry, entryxml):
    '''Convert the entry Keywords to XML'''
    if entry['Keywords']:
        elm = etree.SubElement(entryxml, 'Keywords')
        for keyword in entry['Keywords']:
            key = etree.SubElement(elm, 'Keyword')
            key.text = str(keyword)

def make_ajbnum_xml(ajbnum):
    '''Write an XML version of an AJB number as an index
    element. The ajbnum argument must be a dictionary in the format
    of ajbentry['Num']'''

    index_xml = etree.Element('Index')

    try:
        elm = etree.SubElement(index_xml, 'IndexName')
        elm.text = str(ajbnum['volume']).strip()

        elm = etree.SubElement(index_xml, 'VolumeNumber')
        elm.text = str(ajbnum['volNum'])

        elm = etree.SubElement(index_xml, 'SectionNumber')
        elm.text = str(ajbnum['sectionNum'])

        elm = etree.SubElement(index_xml, 'SubSectionNumber')
        elm.text = str(ajbnum['subsectionNum'])

        elm = etree.SubElement(index_xml, 'EntryNumber')
        elm.text = str(ajbnum['entryNum']) + ajbnum['entrySuf']

        if ajbnum['pageNum'] != -1:
            elm = etree.SubElement(index_xml, 'PageNumber')
            elm.text = str(ajbnum['pageNum'])
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  limit=2, file=sys.stdout)
        print('ERROR entryxml::make_ajbnum_xml: failed')
        return etree.Element('Index')
    
    return index_xml


def make_person_xml(hname):
    '''Create a Person element from a HumanName object. Returns the Person
    element.

    '''

    person_xml = etree.Element('Person')

    if hname.title:
        elm = etree.SubElement(person_xml, 'Prefix')
        elm.text = hname.title

    if hname.first:
        elm = etree.SubElement(person_xml, 'First')
        elm.text = hname.first

    if hname.middle:
        elm = etree.SubElement(person_xml, 'Middle')
        elm.text = hname.middle

    if hname.last:
        elm = etree.SubElement(person_xml, 'Last')
        elm.text = hname.last

    if hname.suffix:
        elm = etree.SubElement(person_xml, 'Suffix')
        elm.text = hname.suffix

    return person_xml

#
#def read_xml_to_entry(self, elxml):
#
def entry_from_xml(entry, elementxml):
    '''Given an XML Entry element place the information into the AJBentry
    dictionary. The input arguments are the entry to put the
    information into and the XMLelement to be parsed.

    '''

    for child in elementxml:
        #print('child is ', child.tag)
        exec('xml_entry_' + child.tag.lower() + '(entry, child)')

def xml_entry_index(entry, child):
    '''Convert XML Index to entry Num'''

    for elm in child:
        if elm.tag == 'IndexName':
            entry['Num']['volume'] = elm.text
        elif elm.tag == 'VolumeNumber':
            entry['Num']['volNum'] = int(elm.text)
        elif elm.tag == 'SectionNumber':
            entry['Num']['sectionNum'] = int(elm.text)
        elif elm.tag == 'SubSectionNumber':
            entry['Num']['subsectionNum'] = int(elm.text)
        elif elm.tag == 'EntryNumber':
            # need to split off the suffix, use regex
            mreg = __reg2__.match(elm.text)
            entry['Num']['entryNum'] = int(mreg.group(1))
            entry['Num']['entrySuf'] = mreg.group(2)
        elif elm.tag == 'PageNumber':
            entry['Num']['pageNum'] = int(elm.text)
        else:
            pass

def xml_entry_title(entry, child):
    '''Convert XML Title to entry Title'''

    entry['Title'] = child.text

# subTitle and subsubTitle not supported in AJBentry
def xml_entry_subtitle(entry, child):
    '''Convert XML subTitle to entry Title'''

    entry['Title'] += child.text

def xml_entry_subsubtitle(entry, child):
    '''Convert XML subsubTitle to entry Title'''

    entry['Title'] += child.text

def xml_entry_authors(entry, child):
    '''Convert XML Authors to entry Authors'''

    for author in child:
        for g2ent in author:
            if g2ent.tag == 'Person':
                entry['Authors'].append(person_name_from_xml(g2ent))

def xml_entry_editors(entry, child):
    '''Convert XML Editors to entry Editors'''

    # PersonInfo or CorporateBody
    for editor in child:
        for g2ent in editor:
            if g2ent.tag == 'Person':
                entry['Editors'].append(person_name_from_xml(g2ent))

def xml_entry_publishers(entry, child):
    '''Convert XML Publishers to entry Publishers'''

    # Place and Name
    for publ in child:
        publisher = {}
        for pub in publ:
            if pub.tag == 'Place':
                if pub.text is not None:
                    publisher['Place'] = str(pub.text)
                else:
                    publisher['Place'] = ''
            elif pub.tag == 'Name':
                if pub.text is not None:
                    publisher['PublisherName'] = str(pub.text)
                else:
                    publisher['PublisherName'] = ''
            else:
                pass
        entry['Publishers'].append(publisher)

def xml_entry_year(entry, child):
    ''' Convert XML Year to entry Year'''

    entry['Year'] = child.text

def xml_entry_edition(entry, child):
    '''Convert XML Edition to entry Edition'''

    entry['Edition'] = child.text

def xml_entry_pagination(entry, child):
    '''Convert XML Pagination to entry Pagination'''

    entry['Pagination'] = child.text

def xml_entry_prices(entry, child):
    '''Convert XML Prices to entry Price'''

    first = True
    entry['Price'] = ''
    for price in child:
        if first:
            first = False
        else:
            entry['Price'] += ' and '
        entry['Price'] += price.text

def xml_entry_reviews(entry, child):
    '''Convert XML Reviews to entry Reviews'''

    for review in child:
        entry['Reviews'].append(review.text)

def xml_entry_translatedfrom(entry, child):
    '''Convert XML TranslatedFrom to entry TranslatedFrom'''

    entry['TranslatedFrom'] = child.text

def xml_entry_language(entry, child):
    '''Convert XML Language to entry Language'''

    entry['Language'] = child.text

def xml_entry_translators(entry, child):
    '''Convert XML Translators to entry Transltors'''

    # PersonInfo or CorporateBody
    for trans in child:
        for g2ent in trans:
            if g2ent.tag == 'Person':
                entry['Translators'].append(person_name_from_xml(g2ent))

def xml_entry_translationof(entry, child):
    '''Convert XML TranslationOf to entry TranslationOf'''

    # Year or AJBnum but only one
    for transof in child:
        if transof.tag == 'Year':
            entry['TranslationOf'] = transof.text
        elif transof.tag == 'Index':
            entry['TranslationOf'] = ajbstr_from_xml(transof)

def xml_entry_compilers(entry, child):
    '''Convert XML Compilers to entry Compilers'''

    # PersonInfo or CorporateBody
    for comp in child:
        for g2ent in comp:
            if g2ent.tag == 'Person':
                entry['Compilers'].append(person_name_from_xml(g2ent))

def xml_entry_contributors(entry, child):
    '''Convert XML Contributors to entry Contributors'''

    # PersonInfo or CorporateBody
    for contr in child:
        for g2ent in contr:
            if g2ent.tag == 'Person':
                entry['Contributors'].append(person_name_from_xml(g2ent))

def xml_entry_reprintof(entry, child):
    '''Convert XML ReprintOf to entry Reprint'''

    # Year or AJBnum but only one
    for reprint in child:
        if reprint.tag == 'Year':
            entry['Reprint'] = reprint.text
        elif reprint.tag == 'Index':
            entry['Reprint'] = ajbstr_from_xml(reprint)

def xml_entry_referenceof(entry, child):
    '''Convert XML RefereceOf to entry Reference'''

    # AJBnum
    for ell in child:
        if ell.tag == 'Index':
            entry['Reference'] = ajbstr_from_xml(ell)

def xml_entry_comments(entry, child):
    '''Convert XML Comments to entry Other'''

    for comment in child:
        entry['Others'].append(comment.text)

def xml_entry_keywords(entry, child):
    '''Convert XML Keywords to entry Keywords'''

    for keyword in child:
        entry['Keywords'].append(keyword.text)

def ajbstr_from_xml(element):
    '''Return a AJB number as a string "AJB xx.xx(x).xx[a]" from
    an XML Index element.'''

    aname = ''
    volnum = ''
    sectionnum = ''
    subsectionnum = ''
    entrynum = ''
    entrysuf = ''
    
    try:
        for child in element:
            if child.tag == 'IndexName':
                aname = child.text
            elif child.tag == 'VolumeNumber':
                volnum = '%02d'%int(child.text)
            elif child.tag == 'SectionNumber':
                sectionnum = '%02d'%int(child.text)
            elif child.tag == 'SubSectionNumber':
                subsectionnum = '(%02d)'%int(child.text)
            elif child.tag == 'EntryNumber':
                mreg = __reg2__.match(child.text)
                entrynum = '%02d'%int(mreg.group(1))
                entrysuf = mreg.group(2)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  limit=2, file=sys.stdout)
        print('ERROR entryxml::ajbstr_from_xml: failed')
        return ''

    return aname + ' ' + volnum + '.' + sectionnum + subsectionnum + '.' + entrynum + entrysuf


def person_name_from_xml(ell):
    '''Create a person mane from an XML element.'''

    hname = HumanName()
    for elm in ell:
        if elm.tag == 'First':
            hname.first = elm.text
        elif elm.tag == 'Middle':
            hname.middle = elm.text
        elif elm.tag == 'Last':
            hname.last = elm.text
        elif elm.tag == 'Title':
            hname.title = elm.text
        elif elm.tag == 'Suffix':
            hname.suffix = elm.text
        elif elm.tag == 'NickName':
            hname.nickname = elm.text
        else:
            pass

    return hname



#
# Test these functions
#
if __name__ == '__main__':

    import unittest

    from pprint import pprint
    
    import aabooks.ajbbook.ajbentry as ajbentry
    import aabooks.ajbbook.testentryxml as testentry

    class EntryTestCase(unittest.TestCase):
        '''Set up the unit tests'''

        def setUp(self):
            '''Initialize local stuff. We start with a fresh Entry object
            for every test.'''

            self.test_str = testentry.ENTRY_XML_STR
            self.test_entry = ajbentry.AJBentry()
            self.ent_xml = etree.fromstring(self.test_str)

        def tearDown(self):
            '''Dispose of the Entry object at the end of every test.'''

            del self.test_str
            del self.test_entry
            del self.ent_xml

        def test_read_write(self):
            '''Test that we can read/write the XML string to an AJBentry'''

            self.test_entry.read_xml_to_entry(self.ent_xml)
            new_str = etree.tostring(self.test_entry.write_xml_from_entry(),
                                     pretty_print=True, encoding='unicode')

            self.assertEqual(len(self.test_str), len(new_str))
            locs = [i for i in range(len(self.test_str)) if self.test_str[i] != new_str[i]]

            # locs should be an empty list
            self.assertFalse(locs, msg='input and output strings differ')

    unittest.main()
