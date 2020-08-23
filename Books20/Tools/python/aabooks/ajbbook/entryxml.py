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
into XML format in accordance with bookfile.xsd.  The two main
functions are entry_from_xml() and entry_to_xml().
'''

import re
from lxml import etree
from nameparser import HumanName

__reg2__ = re.compile(r'([0-9]+)([A-Za-z]*)', re.ASCII)

# XML create routines
#
#def write_xml_from_entry(self):
def entry_to_xml(entry):
    '''This function converts an Entry dictionary to an XML Entry element.
    The input argument is the Entry and the function returns the XML
    element.

    '''

    if not entry.is_valid:
        return None

    # Title and Index are required of any entry
    entryxml = etree.Element('Entry')

    anum = entry['Num']
    entryxml.append(make_ajbnum_xml(anum))

    elm = etree.SubElement(entryxml, 'Title')
    elm.text = entry['Title']

    # This ends the required elements.  All further elements
    # may be missing or blank.

    if entry.not_empty('subTitle'):
        elm = etree.SubElement(entryxml, 'SubTitle')
        elm.text = entry['subTitle']

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

    if entry['Editors']:
        elm = etree.SubElement(entryxml, 'Editors')
        for editor in entry['Editors']:
            edelm = etree.SubElement(elm, 'Editor')
            # all authors are humannames right now.
            person = make_person_xml(editor)
            edelm.append(person)

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

    if entry.not_empty('Year'):
        elm = etree.SubElement(entryxml, 'Year')
        elm.text = str(entry['Year'])

    if entry.not_empty('Edition'):
        elm = etree.SubElement(entryxml, 'Edition')
        elm.text = str(entry['Edition'])

    if entry.not_empty('Pagination'):
        elm = etree.SubElement(entryxml, 'Pagination')
        elm.text = str(entry['Pagination'])

    # The schema defines a price with currency and value
    # but we need to do some intellegent parsing of the prices
    # before we can use this.  For now we just naively use
    # the string.
    if entry.not_empty('Price'):
        elm = etree.SubElement(entryxml, 'Prices')
        for price in entry['Price'].split(' and '):
            priceelm = etree.SubElement(elm, 'Price')
            priceelm.text = price

    if entry['Reviews']:
        elm = etree.SubElement(entryxml, 'Reviews')
        for rev in entry['Reviews']:
            revelm = etree.SubElement(elm, 'Review')
            revelm.text = str(rev)

    if entry.not_empty('TranslatedFrom'):
        elm = etree.SubElement(entryxml, 'TranslatedFrom')
        elm.text = str(entry['TranslatedFrom'])

    if entry.not_empty('Language'):
        elm = etree.SubElement(entryxml, 'Language')
        elm.text = str(entry['Language'])

    if entry['Translators']:
        elm = etree.SubElement(entryxml, 'Translators')
        for trans in entry['Translators']:
            aelm = etree.SubElement(elm, 'Translator')
            # all transltors are humannames right now.
            person = make_person_xml(trans)
            aelm.append(person)

    if entry['Compilers']:
        elm = etree.SubElement(entryxml, 'Compilers')
        for compiler in entry['Compilers']:
            aelm = etree.SubElement(elm, 'Compiler')
            # all compilers are humannames right now.
            person = make_person_xml(compiler)
            aelm.append(person)

    if entry['Contributors']:
        elm = etree.SubElement(entryxml, 'Contributors')
        for contrib in entry['Contributors']:
            aelm = etree.SubElement(elm, 'Contributor')
            # all contributors are humannames right now.
            person = make_person_xml(contrib)
            aelm.append(person)

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
            numdict = entry._parse_ajbnum(entry['Reprint'])
            num = make_ajbnum_xml(numdict)
            elm.append(num)

    if entry.not_empty('Reference'):
        elm = etree.SubElement(entryxml, 'ReferenceOf')
        # parse_ajbnum is defined for the text conversion!
        numdict = entry._parse_ajbnum(entry['Reference'])
        ajbxml = make_ajbnum_xml(numdict)
        elm.append(ajbxml)


    if entry['Others']:
        elm = etree.SubElement(entryxml, 'Comments')
        for comment in entry['Others']:
            com = etree.SubElement(elm, 'Comment')
            com.text = comment

    # return the root Entry element
    return entryxml


def make_ajbnum_xml(ajbnum):
    '''Write an XML version of an AJB number as an index
    element. The ajbnum argument must be a dictionary in the format
    of ajbentry['Num']'''
    
    index_xml = etree.Element('Index')

    elm = etree.SubElement(index_xml, 'IndexName')
    elm.text = str(ajbnum['volume']).strip()

    elm = etree.SubElement(index_xml, 'VolumeNumber')
    elm.text = str(ajbnum['volNum'])

    if ajbnum['pageNum'] != -1:
        elm = etree.SubElement(index_xml, 'PageNumber')
        elm.text = str(ajbnum['pageNum'])

    elm = etree.SubElement(index_xml, 'SectionNumber')
    elm.text = str(ajbnum['sectionNum'])

    elm = etree.SubElement(index_xml, 'SubSectionNumber')
    elm.text = str(ajbnum['subsectionNum'])

    elm = etree.SubElement(index_xml, 'EntryNumber')
    elm.text = str(ajbnum['entryNum']) + ajbnum['entrySuf']

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

#def read_xml_to_entry(self, elxml):
def entry_from_xml(entry, elementxml):
    '''Given an XML Entry element place the information
    into the AJBentry dictionary. The input value is the XML
    element and the function returns a variable of class AJBentry.

    '''

    for child in elementxml:
        #print('child is ', child.tag)

        if child.tag == 'Index':
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

        if child.tag == 'Title':
            entry['Title'] = child.text

        # subTitle and subsubTitle not supported in AJBentry
        if child.tag == 'subTitle':
            entry['Title'] += child.text

        if child.tag == 'subsubTitle':
            entry['Title'] += child.text

        if child.tag == 'Authors':
            for author in child:
                for g2ent in author:
                    if g2ent.tag == 'Person':
                        entry['Authors'].append(person_name_from_xml(g2ent))

        if child.tag == 'Editors':
            # PersonInfo or CorporateBody
            for editor in child:
                for g2ent in editor:
                    if g2ent.tag == 'Person':
                        entry['Editors'].append(person_name_from_xml(g2ent))

        if child.tag == 'Publishers':
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

        if child.tag == 'Year':
            entry['Year'] = child.text

        if child.tag == 'Edition':
            entry['Edition'] = child.text

        if child.tag == 'Pagination':
            entry['Pagination'] = child.text

        if child.tag == 'Prices':
            first = True
            entry['Price'] = ''
            for price in child:
                if first:
                    first = False
                else:
                    entry['Price'] += ' and '
                entry['Price'] += price.text

        if child.tag == 'Reviews':
            for review in child:
                entry['Reviews'].append(review.text)


        if child.tag == 'TranslatedFrom':
            entry['TranslatedFrom'] = child.text

        if child.tag == 'Language':
            entry['Language'] = child.text

        if child.tag == 'Translators':
            # PersonInfo or CorporateBody
            for trans in child:
                for g2ent in trans:
                    if g2ent.tag == 'Person':
                        entry['Translators'].append(person_name_from_xml(g2ent))

        if child.tag == 'Compilers':
            # PersonInfo or CorporateBody
            for comp in child:
                for g2ent in comp:
                    if g2ent.tag == 'Person':
                        entry['Compilers'].append(person_name_from_xml(g2ent))

        if child.tag == 'Contributors':
            # PersonInfo or CorporateBody
            for contr in child:
                for g2ent in contr:
                    if g2ent.tag == 'Person':
                        entry['Contributors'].append(person_name_from_xml(g2ent))

        if child.tag == 'ReprintOf':
            # Year or AJBnum but only one
            for reprint in child:
                if reprint.tag == 'Year':
                    entry['Reprint'] = reprint.text
                elif reprint.tag == 'Index':
                    entry['Reprint'] = ajbstr_from_xml(reprint)


        if child.tag == 'ReferenceOf':
            # AJBnum
            subsectionnum = '0'
            for ell in child:
                if ell.tag == 'Index':
                    entry['Reference'] = ajbstr_from_xml(ell)

        if child.tag == 'Comments':
            for comment in child:
                entry['Others'].append(comment.text)

def ajbstr_from_xml(element):
    '''Return a AJB number as a string "AJB xx.xxx(xx).xx[a]" from
    an XML Index element.'''

    for child in element:
        if child.tag == 'IndexName':
            aname = child.text
        elif child.tag == 'VolumeNumber':
            volnum = '%02d'%int(child.text)
        elif child.tag == 'SectionNumber':
            sectionnum = '%02d'%int(child.text)
        elif child.tag == 'SubSectionNumber':
            subsectionnum = child.text
        elif child.tag == 'EntryNumber':
            mreg = __reg2__.match(child.text)
            entrynum = '%02d'%int(mreg.group(1))
            entrysuf = mreg.group(2)
    return aname + ' ' + volnum + '.' + sectionnum + '.' + entrynum + entrysuf


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

    import aabooks.ajbbook.ajbentry as ajbentry
    from pprint import pprint
    
    entry = ajbentry.AJBentry()

    entry_xml = '''<Entry>
  <Index>
    <IndexName>AJB</IndexName>
    <VolumeNumber>66</VolumeNumber>
    <SectionNumber>145</SectionNumber>
    <SubSectionNumber>0</SubSectionNumber>
    <EntryNumber>29a</EntryNumber>
  </Index>
  <Title>The Physics, and Astronomy of Galaxies and Cosmology</Title>
  <Authors>
    <Author>
      <Person>
        <First>P.</First>
        <Middle>W.</Middle>
        <Last>Hodge</Last>
        <Suffix>jr.</Suffix>
      </Person>
    </Author>
    <Author>
      <Person>
        <First>I.</First>
        <Middle>A. Author</Middle>
        <Last>Other</Last>
      </Person>
    </Author>
    <Author>
      <Person>
        <First>A.</First>
        <Middle>V.</Middle>
        <Last>de la Name</Last>
      </Person>
    </Author>
  </Authors>
  <Editors>
    <Editor>
      <Person>
        <First>A.</First>
        <Middle>B.</Middle>
        <Last>Name</Last>
      </Person>
    </Editor>
  </Editors>
  <Publishers>
    <Publisher>
      <Place>New York</Place>
      <Name>McGraw-Hill Book Company</Name>
    </Publisher>
    <Publisher>
      <Place>London</Place>
      <Name>A Publishing Co.</Name>
    </Publisher>
  </Publishers>
  <Year>1966</Year>
  <Edition>3</Edition>
  <Pagination>179 pp</Pagination>
  <Prices>
    <Price>$2.95 and $4.95</Price>
  </Prices>
  <Reviews>
    <Review>Sci. American 216 Nr 2 142</Review>
    <Review>Sky Tel. 33 164</Review>
  </Reviews>
  <TranslatedFrom>Italian</TranslatedFrom>
  <Language>French</Language>
  <Translators>
    <Translator>
      <Person>
        <First>A.</First>
        <Last>Trans</Last>
      </Person>
    </Translator>
  </Translators>
  <Compilers>
    <Compiler>
      <Person>
        <First>A.</First>
        <Middle>B.</Middle>
        <Last>Compiler</Last>
      </Person>
    </Compiler>
  </Compilers>
  <Contributors>
    <Contributor>
      <Person>
        <First>A.</First>
        <Middle>B.</Middle>
        <Last>Contrib</Last>
      </Person>
    </Contributor>
  </Contributors>
  <ReprintOf>
    <Year>1956</Year>
  </ReprintOf>
  <ReferenceOf>
    <Index>
      <IndexName>AJB</IndexName>
      <VolumeNumber>59</VolumeNumber>
      <SectionNumber>144</SectionNumber>
      <SubSectionNumber>0</SubSectionNumber>
      <EntryNumber>55b</EntryNumber>
    </Index>
  </ReferenceOf>
  <Comments>
    <Comment>a first comment</Comment>
    <Comment>This is the editor string</Comment>
  </Comments>
</Entry>'''

    ent_xml = etree.fromstring(entry_xml)
    #ent_root = ent_xml.getroot()

    entry.entry_from_xml(ent_xml)

    print(etree.tostring(entry.entry_to_xml(), pretty_print=True, encoding='unicode'))
