## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/journal/journalentry.py
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

'''journalEntry provides a class which can convert between a an XML
entry and a representation in python, typically a dictionary entry of
the form Entry.entry().'''
# -*- coding: UTF-8 -*-
# -*- mode: Python;-*-


from lxml import etree

import aabooks.lib.entry as entry

__version__ = 'class JournalEntry(Entry) v1.0.0 dtd 3 Jan 2015'

class JournalEntry(entry.Entry):

    """Read the information from an XML string and put the data in the
    journalEntry dictionary. The entry is valid if there is a valid
    title.

    The JournalEntry XML definition can be found in journalfile.xsd
    """

    def blankEntry(self):
        """Hack until I can rewrite entry.py and AJBentry.py"""
        self.blank_entry()

    def blank_entry(self):
        """Initialize a blank entry by setting known fields to
        null values and deleting all other fields.
        """
        keys = list(self.keys())
        for k in keys:
            del self[k]

        self['Title'] = ''
        self['subTitle'] = ''
        self['subsubTitle'] = ''
        self['Publishers'] = []
        #
        #Publishers is list of dictionaries of the form
        #   {'Name'      : '', # required, all others optional
        #    'Place'     : '',
        #    'startDate' : '',
        #    'endDate'   : ''
        #   }
        #
        self['Abbreviations'] = [] # a list of strings
        self['startDate'] = '' # the start of publishing
        self['endDate'] = '' # the end of publishing
        self['linknext'] = [] # a list of strings'
        self['linkprevious'] = [] # a list of strings
        self['Designators'] = {}
        #
        # Designators is a dictionary of catalogue designations
        #   for example 'ISSN' : '9-123456-789-12-3'
        #     and       "ADS_Bibcode' : '....ApJ...'
        #    others can be
        #               'LCCN', 'DDCN', etc
        #
        self['Comments'] = [] # should be a list of strings



    def version(self):
        return __version__ + ": " + super(JournalEntry, self).version()


    def is_valid(self):
        """journal entries are valid if they have a valid Title."""
        return self['Title'] != ''

    def not_empty(self, key):
        """Return the truth value of, 'key' existing
        in the entry and the key value is not empty."""
        if self.__contains__(key) and self[key]:
            return True
        return False

    #
    # XML create routines
    #
    def write_xml_from_entry(self):
        '''Create an XML etree element with the root tag Entry from
        the entry.
        '''

        if not self.isValid:
            return None

        # Title and Index are required of any entry
        element = etree.Element('Journal')

        sub_element = etree.SubElement(element, 'Title')
        sub_element.text = self['Title']

        # This ends the required elements.  All further elements
        # may be missing or blank.

        if self.not_empty('subTitle'):
            sub_element = etree.SubElement(element, 'subTitle')
            sub_element.text = self['subTitle']

        if self.not_empty('subsubTitle'):
            sub_element = etree.SubElement(element, 'subsubTitle')
            sub_element.text = self['subsubTitle']

        pub_len = len(self['Publishers'])
        if pub_len > 0:
            sub_element = etree.SubElement(element, 'Publishers')
            for publ in self['Publishers']:
                publisher_element = etree.SubElement(sub_element, 'Publisher')

                if publ.__contains__('Name') and publ['Name']:
                    epp = etree.Element('Name')
                    epp.text = publ['Name']
                    publisher_element.append(epp)

                if publ.__contains__('Place') and publ['Place']:
                    epp = etree.Element('Place')
                    epp.text = publ['Place']
                    publisher_element.append(epp)

                if publ.__contains__('startDate') and publ['startDate']:
                    epp = etree.Element('startDate')
                    epp.text = publ['startDate']
                    publisher_element.append(epp)

                if publ.__contains__('endDate') and publ['endDate']:
                    epp = etree.Element('endDate')
                    epp.text = publ['endDate']
                    publisher_element.append(epp)

        # abbreviations
        if self.not_empty('Abbreviations'):
            sub_element = etree.SubElement(element, 'Abbreviations')
            for abrv in self['Abbreviations']:
                abrv_element = etree.SubElement(sub_element, 'Abbreviation')
                abrv_element.text = abrv

        # startDate
        if self.not_empty('startDate'):
            sub_element = etree.SubElement(element, 'startDate')
            sub_element.text = self['startDate']

        # endDate
        if self.not_empty('endDate'):
            sub_element = etree.SubElement(element, 'endDate')
            sub_element.text = self['endDate']

        # Links
        if self.not_empty('linkprevious') or self.not_empty('linknext'):
            sub_element = etree.SubElement(element, 'Links')
            if self.not_empty('linkprevious'):
                for link in self['linkprevious']:
                    link_element = etree.SubElement(sub_element, 'linkPrevious')
                    link_element.text = link

            if self.not_empty('linknext'):
                for link in self['linknext']:
                    link_element = etree.SubElement(sub_element, 'linkNext')
                    link_element.text = link


        # Designators is a dictionary
        if self.not_empty('Designators'):
            sub_element = etree.SubElement(element, 'Designators')
            for key in self['Designators'].keys():
                desg_element = etree.SubElement(sub_element, key)
                desg_element.text = self['Designators'][key]

        # Comments
        if self.not_empty('Comments'):
            sub_element = etree.SubElement(element, 'Comments')
            for comment in self['Comments']:
                comment_element = etree.SubElement(sub_element, 'Comment')
                comment_element.text = comment

        # return the root Entry element
        return element


    def read_xml_to_entry(self, element):
        '''Parse an XML element of a Journal Entry and place the information
        into the journalEntry dictionary. '''

        for child in element:
            #print('child is ', child.tag)

            if child.tag == 'Title':
                self['Title'] = child.text

            # subTitle and subsubTitle
            elif child.tag == 'subTitle':
                self['subTitle'] = child.text

            elif child.tag == 'subsubTitle':
                self['subsubTitle'] = child.text

            # Publishers
            elif child.tag == 'Publishers':
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

                    self['Publishers'].append(pub)

            # Abbreviations known for this journal
            elif child.tag == 'Abbreviations':
                for abrv in child:
                    self['Abbreviations'].append(abrv.text)

            # Starting Date of journal
            elif child.tag == 'startDate':
                self['startDate'] = child.text

            # Ending Date of journal
            elif child.tag == 'endDate':
                self['endDate'] = child.text

            # Links
            elif child.tag == 'Links':
                for link in child:
                    if link.tag == 'linkPrevious':
                        self['linkprevious'].append(link.text)
                    elif link.tag == 'linkNext':
                        self['linknext'].append(link.text)
                    else:
                        assert 0, 'journalEntry.read_XML_to_entry() invalid link name'

            # Designators is a dictionary
            #   This should be valid for any entry
            elif child.tag == 'Designators':
                for desg in child:
                    #print('read_XML_to_Entry: (%s) : (%s)' % (desg.tag, desg.text))
                    self['Designators'][desg.tag] = desg.text

            # Comments is a list of strings
            elif child.tag == 'Comments':
                for comment in child:
                    self['Comments'].append(comment.text)

            else:
                assert 0, 'JournalEntry.read_xml_to_entry() invalid tag name %s' % (child.tag)



#
# Test everything
#
if __name__ == '__main__':

    from pprint import pprint

    def test():
        '''The main test function'''
        all_fields = JournalEntry()
        all_fields['Title'] = 'First Test Journal'
        all_fields['subTitle'] = 'A journal of First Things'
        all_fields['subsubTitle'] = 'and a pot full of honey'
        publ1 = {'Name' : 'Publisher_1',
                 'Place' : 'Place_1'}
        publ2 = {'Name' : 'Publisher_2',
                 'Place' : 'Place_2',
                 'startDate' : '1968-10-21',
                 'endDate' : '1972-12-31'}
        all_fields['Publishers'] = [publ1, publ2]
        all_fields['Abbreviations'] = ['Fj', 'F Journal']
        all_fields['startDate'] = '1960-01-01'
        all_fields['endDate'] = '2010-01-01'
        all_fields['linkprevious'] = ['The Sky', 'The Telescope']
        all_fields['linknext'] = ['Sky and Telescope']
        all_fields['Designators'] = {'ISSN' :'9-01234-567-890-12',
                                     'ADSdesignator' : 'U...ApJ..'}
        all_fields['Comments'] = ['This is a comment.',
                                  'This is a second comment']

        #
        # test XML routines
        #
        print('\n\n Testing Journal EntryXML routines\n')
        print('all_fields as entry:')
        pprint(all_fields)

        print('\n all_fields as XML from entry')
        entry_xml = all_fields.write_xml_from_entry()
        print(etree.tostring(entry_xml, pretty_print=True, encoding='unicode'))

        print('\n all_fields as entry read from XML')
        entries = JournalEntry()
        entries.read_xml_to_entry(entry_xml)
        pprint(entries)

    #
    # Run it
    #
    test()
