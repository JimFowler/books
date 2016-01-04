'''Defines the class that handles disk files and entry lists'''
# -*- coding: UTF-8 -*-
# -*- mode: Python;-*-

import fileinput
import os
import traceback
import json
from lxml import etree

import bookentry.journalEntry as journalEntry

__version__ = 0.1

__defaultHeader__ = '''
Default header for journal file
'''
# end of defaultHeader


class JournalFile():
    """The BookFile class handles the disk file and entry list
    for book lists from AJB/AAA. It handles all the translation
    between the disk file format and the AJBentry format."""

    def __init__(self, parent=None):
        self._header = __defaultHeader__
        self._entryList = []

        self._fileName = './document1'
        self._dirName = './'
        self._baseName = 'document1'

        self.curEntryNumber = -1  # 1 <= curEntryNumber <= len(self._entryList)

        self.setFileName('document1')
        self._dirty = False


    # dirty (modified) file
    def isDirty(self):
        """Returns a boolean. The value is True if any of the entries
        or the header has changed since the last read() or write().
        """
        return self._dirty


    # file name
    def setFileName(self, filename):
        """Set the name of the disk file. Thus one can read a file,
        set a new file name, and save the file. No validity checking
        is done at this stage."""
        self._fileName = filename
        self._dirName, self._baseName = os.path.split(filename)
        self._dirty = True

    def getFileName(self):
        """Return the current value of the fileName."""
        return self._fileName

    def getBaseName(self):
        """Returns the basename() of the current filename."""
        return self._baseName

    def getDirName(self):
        """Returns the dirname() of the current filename."""
        return self._dirName


    # header
    def setHeader(self, headerStr):
        """Set the header entry to be headerStr."""
        self._dirty = True
        self._header = headerStr

    def getHeader(self):
        """Return the current header string."""
        return self._header


    # current entry
    def getEntry(self, count=-1):
        """Returns the entry at position count. If count is less than 0
        or greater than the number of entries, 'None' is returned. Note
        that 1 <= count <= len(self._entryList).
        """
        if count < 1 or count > len(self._entryList):
            return None

        self.curEntryNumber = count - 1
        return self._entryList[self.curEntryNumber]

    def setEntry(self, entry, count=-1):

        """Write over the current entry or the entry at position
        'count' if given.  Note that 1 <= count <= len(self._entryList).
        The dirty flag is set for the file."""

        if not entry.isValid():
            print('bookfile().setEntry count %d entry:'%count)
            print(entry)
            return False
    
        if count < 1 or count > len(self._entryList):
            return False

        self.curEntryNum = count - 1
        self._entryList[self.curEntryNum] = entry
        self._dirty = True
        return True

    def setNewEntry(self, entry, count=-1):
        """Append an entry to the list or insert before entry 'count' 
        if that value is given. Note that 1 <= count <= len(self._entryList).
        The dirty flag is set for the file.
        """

        if not entry.isValid():
            return False

        #print('bookfile', count, entry['Num'] )
        if count < 1 or count > len(self._entryList):
            self._entryList.append(entry)
        else:
            self.curEntryNumber = count - 1
            self._entryList.insert(self.curEntryNumber, entry)

        self._dirty = True
        return True

    def deleteEntry(self, entryNum):
        '''Delete the (entryNum - 1) record in the list, if such exists.
        Return the length of the remaining list.'''
        if entryNum > 0 and entryNum <= len(self._entryList):
            self._entryList.pop(entryNum - 1)
            self._dirty = True

        return len(self._entryList)

    def mkShortTitleList(self):
        '''Create a string of short titles from all entries in the list.
        A short title is "count AJBnum Title" and is used to look quickly
        at the list of titles.'''

        shortTitleList = ''
        count = 1
        for e in self._entryList:
            shortTitleList = shortTitleList + str(count) + ' ' + e['Title']
            count += 1

        return shortTitleList
            
    # file I/O
    def readfile_XML(self, filename=None):
        """Open and read the header stuff into _header and the entries
        into the entry list. If filename is not given, we use
        the value set in BookFile.setFileName() if valid. Note that we
        do not care if the entries or header have been modified; that is
        the job of the calling routine.
    
        Return value is the number of record entries read."""
    
        if filename:
            self.setFileName(filename)
        
        if self._fileName == '' or not os.path.isfile(self._fileName):
            return 0 # no records read

        # if we have a good file, then clear the entryList and header
        self._entryList = []
        self._header = ''
        self._dirty = False

        count = 0
    
        # read and validate the XML file
        try:
            bf_schema = etree.XMLSchema(file='/home/jrf/Documents/books/Books20/Tools/bookentry/xml/journalfile.xsd')
            Parser = etree.XMLParser(schema=bf_schema)
        except:
            print('The schema is not well formed')
            return 0
        try:
            bf_xml = etree.parse(self._fileName, parser=Parser)
        except:
            print('The xml file is not well formed or is invalid')
            return 0

        bf = bf_xml.getroot()
        for child in bf:
            if child.tag == 'Header':
                self.setHeader(child.text)

            if child.tag == 'Journals':
                for entry in child:
                    entTemp = journalEntry.journalEntry()
                    entTemp.read_XML_to_Entry(entry)
                    if entTemp.isValid():
                        count += 1
                        self._entryList.append(entTemp)
        
        self._dirty = False

        return count


    def writefile_XML(self, filename=None):
        """Write the entry list and header to a disk file.
        if filename is not given, we use BookEntry._fileName instead.

        Returns True if the file could be written or False otherwise."""

        if filename:
            self.setFileName(filename)
        
        try:
            fd = open(self._fileName, 'w', encoding='UTF8')
        except:
            return False

        # We do something clever here when we know how.
        elBF = etree.Element('JournalFile')
        hdr = etree.SubElement(elBF, 'Header')
        hdr.text = self.getHeader()

        ets = etree.SubElement(elBF, 'Journals')
        for entry in self._entryList:
            ee = entry.write_XML_from_Entry()
            ets.append(ee)

        bStr = etree.tostring(elBF,
                              xml_declaration=True,
                              method='xml', encoding='UTF-8')
        strStr = bStr.decode(encoding='UTF-8')
        fd.write(strStr)

        fd.close()
        self._dirty = False


if __name__ == "__main__":

    from pprint import pprint
    import sys

    bf = JournalFile()
    bf.readfile_XML('./xml/JournalFile.xml')

    print( 'The header for %s' % bf.getFileName())
    print( bf.getHeader() )

    bf.writefile_XML('journalfile_test.xml')
    print('We can read and validate a file with the parse() function')
    try:
        bf_schema = etree.XMLSchema(file='./xml/journalfile.xsd')
        Parser = etree.XMLParser(schema=bf_schema)
        print('The schema is well formed')
    except:
        print('The schema is not well formed')
        sys.exit(1)
    try:
        # etree.parse() returns an Etree rather than an Element
        bf3 = etree.parse('journalfile_test.xml', parser=Parser)
        print('The xml file is well formed and valid')
    except:
        print('The xml file is not well formed or is invalid')


