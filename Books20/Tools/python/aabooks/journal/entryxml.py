## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/journal/entryxml.py
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
'''The module contains the functions needed to convert journal entries
into XML format in accordance with the schema defined in journalfile.xsd.
The two main functions are entry_from_xml() and entry_to_xml().  These
functions depend explicitly on the definition of the class JournalEntry
defined in journalentry.py and can not be used with out journalentry.py.

'''

from lxml import etree

# pylint: disable=exec-used,unused-argument

def entry_to_xml(entry):
    '''Create an XML etree element with the root tag Entry from
    the entry.
    '''

    if not entry.is_valid:
        return None

    # Title and Index are required of any entry
    element = etree.Element('Journal')

    sub_element = etree.SubElement(element, 'Title')
    sub_element.text = entry['Title']

    # This ends the required elements.  All further elements
    # may be missing or blank.
    # return the root Entry element
    entry_xml_subtitle(entry, element)
    entry_xml_subsubtitle(entry, element)
    entry_xml_publishers(entry, element)
    entry_xml_abbreviations(entry, element)
    entry_xml_startdate(entry, element)
    entry_xml_enddate(entry, element)
    entry_xml_links(entry, element)
    entry_xml_designators(entry, element)
    entry_xml_comments(entry, element)

    return element

def entry_xml_subtitle(entry, entryxml):
    '''Convert the entry subTitle to XML.'''

    if entry.not_empty('subTitle'):
        sub_element = etree.SubElement(entryxml, 'subTitle')
        sub_element.text = entry['subTitle']

def entry_xml_subsubtitle(entry, entryxml):
    '''Convert the entry subsubTitle to XML.'''

    if entry.not_empty('subsubTitle'):
        sub_element = etree.SubElement(entryxml, 'subsubTitle')
        sub_element.text = entry['subsubTitle']


def entry_xml_publishers(entry, entryxml):
    '''Convert the entry Publishers to XML.'''

    pub_len = len(entry['Publishers'])
    if pub_len > 0:
        sub_element = etree.SubElement(entryxml, 'Publishers')
        for publ in entry['Publishers']:
            publisher_element = etree.SubElement(sub_element, 'Publisher')

            if 'Name' in publ and publ['Name']:
                epp = etree.Element('Name')
                epp.text = publ['Name']
                publisher_element.append(epp)

            if 'Place' in publ and publ['Place']:
                epp = etree.Element('Place')
                epp.text = publ['Place']
                publisher_element.append(epp)

            if 'startDate' in publ and publ['startDate']:
                epp = etree.Element('startDate')
                epp.text = publ['startDate']
                publisher_element.append(epp)

            if 'endDate' in publ and publ['endDate']:
                epp = etree.Element('endDate')
                epp.text = publ['endDate']
                publisher_element.append(epp)

def entry_xml_abbreviations(entry, entryxml):
    '''Convert the entry Abbreviations to XML.'''

    if entry.not_empty('Abbreviations'):
        sub_element = etree.SubElement(entryxml, 'Abbreviations')
        for abrv in entry['Abbreviations']:
            abrv_element = etree.SubElement(sub_element, 'Abbreviation')
            abrv_element.text = abrv

def entry_xml_startdate(entry, entryxml):
    '''Convert the entry startDate to XML.'''

    if entry.not_empty('startDate'):
        sub_element = etree.SubElement(entryxml, 'startDate')
        sub_element.text = entry['startDate']

def entry_xml_enddate(entry, entryxml):
    '''Convert the entry endDate to XML.'''

    if entry.not_empty('endDate'):
        sub_element = etree.SubElement(entryxml, 'endDate')
        sub_element.text = entry['endDate']

def entry_xml_links(entry, entryxml):
    '''Convert the entry links to XML.'''

    if entry.not_empty('linkprevious') or entry.not_empty('linknext'):
        sub_element = etree.SubElement(entryxml, 'Links')
        if entry.not_empty('linkprevious'):
            for link in entry['linkprevious']:
                link_element = etree.SubElement(sub_element, 'linkPrevious')
                link_element.text = link

        if entry.not_empty('linknext'):
            for link in entry['linknext']:
                link_element = etree.SubElement(sub_element, 'linkNext')
                link_element.text = link

def entry_xml_designators(entry, entryxml):
    '''Convert the entry Designators to XML.'''

    if entry.not_empty('Designators'):
        sub_element = etree.SubElement(entryxml, 'Designators')
        for key in entry['Designators'].keys():
            desg_element = etree.SubElement(sub_element, key)
            desg_element.text = entry['Designators'][key]

def entry_xml_comments(entry, entryxml):
    '''Convert the entry Comments to XML'''

    if entry.not_empty('Comments'):
        sub_element = etree.SubElement(entryxml, 'Comments')
        for comment in entry['Comments']:
            comment_element = etree.SubElement(sub_element, 'Comment')
            comment_element.text = comment

#
#
#
def entry_from_xml(entry, element):
    '''Parse an XML element of a Journal Entry and place the information
    into the journalEntry dictionary. '''

    for child in element:
        #print('child is ', child.tag)
        exec('xml_entry_' + child.tag.lower() + '(entry, child)')


def xml_entry_title(entry, child):
    '''Convert the XML Title to entry Title.'''

    entry['Title'] = child.text

def xml_entry_subtitle(entry, child):
    '''Convert XML subTitle to entry subTitle.'''

    entry['subTitle'] = child.text

def xml_entry_subsubtitle(entry, child):
    '''Convert the XML subsubTitle to entry subsubTitle.'''

    entry['subsubTitle'] = child.text

def xml_entry_publishers(entry, child):
    '''Convert the XML Publishers to entry Publishers.'''

    # Place and Name
    for publ in child:
        pub = {}
        for tag in publ:
            if tag.tag == 'Name':
                pub['Name'] = tag.text

            if tag.tag == 'Place':
                pub['Place'] = tag.text

            if tag.tag == 'startDate':
                pub['startDate'] = tag.text

            if tag.tag == 'endDate':
                pub['endDate'] = tag.text

        entry['Publishers'].append(pub)

def xml_entry_abbreviations(entry, child):
    '''Convert the XML Abbreviations to entry Abbreviations.'''

    for abrv in child:
        entry['Abbreviations'].append(abrv.text)

def xml_entry_startdate(entry, child):
    '''Convert the XML startDate to entry startDate.'''

    entry['startDate'] = child.text

def xml_entry_enddate(entry, child):
    '''Convert the XML endDate to entry endDate.'''

    entry['endDate'] = child.text

def xml_entry_links(entry, child):
    '''Convert the XML Links to entry Links.'''

    for link in child:
        if link.tag == 'linkPrevious':
            entry['linkprevious'].append(link.text)
        elif link.tag == 'linkNext':
            entry['linknext'].append(link.text)
        else:
            assert 0, 'journalEntry.read_XML_to_entry() invalid link name'

def xml_entry_designators(entry, child):
    '''Convert the XML Designators to entry Designators.'''

    for desg in child:
        #print('read_XML_to_Entry: (%s) : (%s)' % (desg.tag, desg.text))
        entry['Designators'][desg.tag] = desg.text

def xml_entry_comments(entry, child):
    '''Convert the XML Comments to entry Comments.'''

    for comment in child:
        entry['Comments'].append(comment.text)
