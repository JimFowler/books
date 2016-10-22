'''journalEntry provides a class which can convert between a an XML
entry and a representation in python, typically a dictionary entry of
the form Entry.entry().'''
# -*- coding: UTF-8 -*-
# -*- mode: Python;-*-


from lxml import etree

import bookentry.entry as entry

__version__ = 'class journalEntry(Entry) v1.0.0 dtd 3 Jan 2015'

class journalEntry(entry.Entry):

    """Read the information from an XML string and put the data in the
    journalEntry dictionary. The entry is valid if there is a valid
    title.

    The journalEntry XML definition can be found in journalfile.xsd
    """

    def blankEntry(self):
        """Initialize a blank entry by setting known fields to
        null values and deleting all other fields.
        """
        keys = list(self.keys())
        for k in keys :
            del(self[k])

        self[ 'Title']         = ''
        self[ 'subTitle']      = ''
        self[ 'subsubTitle']   = ''
        self[ 'Publishers']     = []
        #
        #Publishers is list of dictionaries of the form
        #   {'Name'      : '', # required, all others optional
        #    'Place'     : '',
        #    'startDate' : '',
        #    'endDate'   : ''
        #   }
        #
        self[ 'Abbreviations'] = [] # a list of strings
        self[ 'startDate']     = '' # the start of publishing
        self[ 'endDate']       = '' # the end of publishing
        self[ 'linknext']      = [] # a list of strings'
        self[ 'linkprevious']  = [] # a list of strings
        self[ 'Designators']   = {}
        #
        # Designators is a dictionary of catalogue designations
        #   for example 'ISSN' : '9-123456-789-12-3'
        #     and       "ADS_Bibcode' : '....ApJ...'
        #    others can be 
        #               'LCCN', 'DDCN', etc
        #
        self[ 'Comments']      = [] # should be a list of strings



    def version(self):
        return __version__ + ": " + super(journalEntry, self).version()


    def isValid(self):
        """journalEntries are valid if they have a valid Title."""
        if self['Title'] != '':
            return True
        else:
            return False

    def notEmpty(self, key ):
        """Return the truth value of, 'key' existing
        in the entry and the key value is not empty."""
        if self.__contains__(key) and self[key]:
            return True
        return False

    #
    # XML create routines
    #
    def write_XML_from_Entry(self):
        '''Create an XML etree element with the root tag Entry from
        the entry.
        '''

        if not self.isValid:
            return None

        # Title and Index are required of any entry
        entryXML = etree.Element('Journal')
    
        el = etree.SubElement(entryXML, 'Title')
        el.text = self['Title']

        # This ends the required elements.  All further elements
        # may be missing or blank.
        
        if self.notEmpty('subTitle'):
            el = etree.SubElement(entryXML, 'subTitle')
            el.text = self['subTitle']

        if self.notEmpty('subsubTitle'):
            el = etree.SubElement(entryXML, 'subsubTitle')
            el.text = self['subsubTitle']
            
        if 0 < len(self['Publishers']):
            el = etree.SubElement(entryXML, 'Publishers')
            for publ in self['Publishers']:
                ep = etree.SubElement(el, 'Publisher')

                if publ.__contains__('Name') and publ['Name']:
                    epp = etree.Element('Name')
                    epp.text = publ['Name']
                    ep.append(epp)

                if publ.__contains__('Place') and publ['Place']:
                    epp = etree.Element('Place')
                    epp.text = publ['Place']
                    ep.append(epp)

                if publ.__contains__('startDate') and publ['startDate']:
                    epp = etree.Element('startDate')
                    epp.text = publ['startDate']
                    ep.append(epp)

                if publ.__contains__('endDate') and publ['endDate']:
                    epp = etree.Element('endDate')
                    epp.text = publ['endDate']
                    ep.append(epp)

        # abbreviations
        if self.notEmpty('Abbreviations'):
            el = etree.SubElement(entryXML, 'Abbreviations')
            for abrv in self['Abbreviations']:
                ep = etree.SubElement(el, 'Abbreviation')
                ep.text = abrv
                
        # startDate
        if self.notEmpty('startDate'):
            el = etree.SubElement(entryXML, 'startDate')
            el.text = self['startDate']

        # endDate
        if self.notEmpty('endDate'):
            el = etree.SubElement(entryXML, 'endDate')
            el.text = self['endDate']

        # Links
        if self.notEmpty('linkprevious') or self.notEmpty('linknext'):
            el = etree.SubElement(entryXML, 'Links')
            if self.notEmpty('linkprevious'):
                for link in self['linkprevious']:
                    ep = etree.SubElement(el, 'linkPrevious')
                    ep.text = link

            if self.notEmpty('linknext'):
                for link in self['linknext']:
                    ep = etree.SubElement(el, 'linkNext')
                    ep.text = link


        # Designators is a dictionary
        if self.notEmpty('Designators'):
            el = etree.SubElement(entryXML, 'Designators')
            for key in self['Designators'].keys():
                #key = key.strip()
                #print('write_XML_from_Entry: (%s) : (%s)' % (key, self['Designators'][key] ))
                cl = etree.SubElement(el, key)
                cl.text = self['Designators'][key]

        # Comments
        if self.notEmpty('Comments'):
            el = etree.SubElement(entryXML, 'Comments')
            for comment in self['Comments']:
                cl = etree.SubElement(el, 'Comment')
                cl.text = comment

        # return the root Entry element
        return entryXML


    def read_XML_to_Entry(self, elXML):
        '''Parse an XML element of a Journal Entry and place the information
        into the journalEntry dictionary. '''

        for child in elXML:
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
                assert 0, 'journalEntry.read_XML_to_entry() invalid tag name'
                


#
# Test everything
#
if __name__ == '__main__':

    try:
        from pprint import pprint
    except:
        print('Pretty Print module unavailable')
        sys.exit(0)

    allFields = journalEntry()
    allFields['Title'] = 'First Test Journal'
    allFields['subTitle'] = 'A journal of First Things'
    allFields['subsubTitle'] = 'and a pot full of honey'
    publ1 = { 'Name' : 'Publisher_1',
              'Place' : 'Place_1'}
    publ2 = { 'Name' : 'Publisher_2',
              'Place' : 'Place_2',
              'startDate' : '1968-10-21',
              'endDate' : '1972-12-31' }
    allFields['Publishers'] = [publ1, publ2]
    allFields['Abbreviations'] = ['Fj', 'F Journal']
    allFields['startDate'] = '1960-01-01'
    allFields['endDate'] = '2010-01-01'
    allFields['linkprevious'] = ['The Sky', 'The Telescope']
    allFields['linknext'] = ['Sky and Telescope']
    allFields['Designators'] = {'ISSN' :'9-01234-567-890-12',
                                'ADSdesignator' : 'U...ApJ..'}
    allFields['Comments'] = ['This is a comment.',
                            'This is a second comment']

    #
    # test XML routines
    #
    print('\n\nTesting Journal Entry XML routines\n')
    print('allFields as entry:')
    pprint(allFields)

    print('\nallFields as XML from entry')
    et = allFields.write_XML_from_Entry()
    print(etree.tostring(et, pretty_print=True, encoding='unicode'))

    print('\nallFields as entry read from XML')
    eAll = journalEntry()
    eAll.read_XML_to_Entry(et)
    pprint(eAll)
