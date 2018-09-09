## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/bookentry/bookfile.py
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
"""Defines the class that handles disk files and entry lists"""

import fileinput
import os, sys
import traceback
import json
from lxml import etree

import bookentry.AJBentry as AJBentry

__version__ = 0.1

__defaultHeader__ = """Entry format

Num AJB_ID Author [and author [and …]] [ed.|comp.], Title, Place, Publisher, year, description, price, review [and review [and …]], comments

AJB_ID   volume.section[(subsection)].entry, for example 68.144(1).25 would be volume 68, section 144, subsection 1, and entry number 25.

Commas are field separators for automatic parsing.  Use the word ‘comma’ if you want the character in field string. We will use global search and replace after parsing into fields.

Save as Unicode UTF-8 text encoding. Skip section 4 in Part 1

For volume AJB ?? Index to the Literature of ????, started, finished, proofread


"""
# end of defaultHeader


class BookFile():
    """The BookFile class handles the disk file and entry list
    for book lists from AJB/AAA. It handles all the translation
    between the disk file format and the AJBentry format."""

    def __init__(self, parent=None):
        self._header = __defaultHeader__
        self._entryList = []

        self._volumeNumber = -1
        self._fileName = './document1'
        self._dirName = './'
        self._baseName = 'document1'
        self._extension = '.txt'

        self.curEntryNumber = -1  # 1 <= curEntryNumber <= len(self._entryList)

        self.setFileName('document1')
        self._dirty = False


    # dirty (modified) file
    def isDirty(self):
        """Returns a boolean. The value is True if any of the entries
        or the header has changed since the last read() or write().
        """
        return self._dirty

    # volume number
    def setVolumeNumber( self, vol ):
        self._volumeNumber = vol

    def getVolumeNumber(self):
        return self._volumeNumber


    # file name
    def setFileName(self, filename):
        """Set the name of the disk file. Thus one can read a file,
        set a new file name, and save the file. No validity checking
        is done at this stage."""
        self._fileName = filename
        self._dirName, _baseName = os.path.split(filename)
        self._baseName, self._extension = os.path.splitext(_baseName)
        self._dirty = True

    def getFileName(self):
        """Return the current value of the fileName."""
        return self._fileName

    def getDirName(self):
        """Returns the dirname() of the current filename."""
        return self._dirName

    def getBaseName(self):
        """Returns the basename() of the current filename."""
        return self._baseName

    def getBaseNameWithExtension(self):
        """Returns the baseName().extension() of the current filename."""
        return self._baseName + self._extension

    def getExtension(self):
        """Returns the extension() of the current filename."""
        return self._extension


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
            shortTitleList = shortTitleList + str(count) + ' ' + e.shortTitle()
            count += 1

        return shortTitleList
            
    # file I/O
    def readFile(self, filename=None):
        '''Select a reader function depending on the filename
        extension.  Return the number of entries read.'''
        if filename:
            self.setFileName(filename)

        if self._fileName == '' or not os.path.isfile(self._fileName):
            return 0 # no records read

        if self._extension == '.txt':
            return self.readFile_Text()
        elif self._extension == '.xml':
            return self.readFile_XML()
        else:
            # return error to caller who should know about Qt message boxes.
            print('Invalid file extension for %s' % self._fileName)
            return 0


    def writeFile(self, filename=None):
        '''Select a writer function depending on the filename
        extension. If filename is not given, we use BookEntry._fileName
        instead.

        Returns True if the file could be written or False otherwise.'''
        if filename:
            self.setFileName(filename)

        if self._extension == '.txt':
            return self.writeFile_Text()
        elif self._extension == '.xml':
            return self.writeFile_XML()
        else:
            # return error to caller who should know about Qt message boxes.
            print('Invalid file extension for %s' % self._fileName)
            return 0


    # Specific file type I/O
    def readFile_Text(self, filename=None ):
        """Open and read a .txt file and put the header stuff into
        _header and the entries into the entry list. The header is
        defined as everything before the first valid entry. If
        filename is not given, we use the value set in
        BookFile.setFileName() if valid. Note that we do not care if
        the entries or header have been modified; that is the job of
        the calling routine.

        Return value is the number of record entries read."""

        # if we have a good file, then clear the entryList and header
        self._entryList = []
        self._header = ''
        self._dirty = False

        entTemp = AJBentry.AJBentry()
        count = 0
        
        for line in fileinput.input([self._fileName]):
            line = line.strip()
            try:
                if not entTemp.read_Text_to_Entry(line) and not count:
                    self._header = self._header + line + '\n'
            except:
                print(line + '\n')
                traceback.print_exc()
                print('\n\n')
         
            if entTemp.isValid():
                count += 1
                self._entryList.append(entTemp)
                entTemp = AJBentry.AJBentry()
         
        self.curEntryNumber = 1

        return count


    def writeFile_Text(self):
        """Write the entry list and header to a .txt disk file.
        if filename is not given, we use BookEntry._fileName instead.

        Returns True if the file could be written or False otherwise."""

        try:
            fd = open(self._fileName, 'w', encoding='UTF8')
        except:
            return False

        if fd.newlines:
            newline = fd.newlines + fd.newline
        else:
            newline = '\n\n'


        fd.write(self._header)
        count = 1
        for ent in self._entryList:
            fd.write(str(count) + ' ' + ent.write_Text_from_Entry() + newline)
            count += 1

        fd.close()
        self._dirty = False


    def readFile_XML(self):
        """Open and read the header stuff into _header and the entries
        into the entry list. If filename is not given, we use
        the value set in BookFile.setFileName() if valid. Note that we
        do not care if the entries or header have been modified; that is
        the job of the calling routine.
    
        Return value is the number of record entries read."""
    
        if self._fileName == '' or not os.path.isfile(self._fileName):
            return 0 # no records read

        # if we have a good file, then clear the entryList and header
        self._entryList = []
        self._header = ''
        self._dirty = False

        count = 0
    
        # read and validate the XML file
        try:
            bf_schema = etree.XMLSchema(file='/home/jrf/Documents/books/Books20/Tools/python/bookentry/xml/bookfile.xsd')
            Parser = etree.XMLParser(schema=bf_schema)
        except:
            print('The schema is not well formed or can not be found')
            return 0
        try:
            bf_xml = etree.parse(self._fileName, parser=Parser)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                               limit=2, file=sys.stdout)
            print('The xml file is not well formed or is invalid')
            return 0

        bf = bf_xml.getroot()
        for child in bf:
            if child.tag == 'Header':
                self.setHeader(child.text)

            if child.tag == 'Entries':
                for entry in child:
                    entTemp = AJBentry.AJBentry()
                    entTemp.read_XML_to_Entry(entry)
                    if entTemp.isValid():
                        count += 1
                        self._entryList.append(entTemp)
                        entTemp = AJBentry.AJBentry()
        
        self._dirty = False

        return count


    def writeFile_XML(self, filename=None):
        """Write the entry list and header to a .xml disk file.
        if filename is not given, we use BookEntry._fileName instead.

        Returns True if the file could be written or False otherwise."""

        try:
            if filename is not None:
                fd = open(filename, 'w', encoding='UTF8')
                # only set _filename if we are successful in opening
                self._filename = filename
            else:
                fd = open(self._fileName, 'w', encoding='UTF8')
        except:
            # really should print the exception here
            return False


        # We do something clever here when we know how.
        elBF = etree.Element('BookFile')
        hdr = etree.SubElement(elBF, 'Header')
        hdr.text = self.getHeader()

        ets = etree.SubElement(elBF, 'Entries')
        for entry in self._entryList:
            # entry is of Class AJBentry
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

    bf = BookFile()
    print( "%d entries found\n" % bf.readFile("/home/jrf/Documents/books/Books20/Data/Ajb/ajb58_books.txt"))

    print( 'The header for %s' % bf.getFileName())
    print( bf.getHeader() )

    bf.writeFile("testfile.txt")

    bf.readFile('testfile.txt')
    bf.writeFile('testfile2.txt')
    print(' run "diff testfile2.txt testfile.txt"')

    ent = AJBentry.AJBentry('500 58.04.05 , An Amazing Book')
    ent2 = AJBentry.AJBentry('500 58.04.06 , An Amazing Book Too')
    bf.setNewEntry(ent) # append
    bf.setNewEntry(ent2, 0) # append
    bf.setNewEntry(ent, 1) # insert as entry 1
    bf.setNewEntry(ent2, 5) # insert as entry 5
    bf.setEntry(ent, 4) # replace entry 4
    bf.writeFile('testfile3.txt')
    bf.setNewEntry(ent, 5)
    bf.deleteEntry(22)
    bf.deleteEntry(0)
    bf.deleteEntry(5)
    print('testfile3.txt should have new entry 1 and 5 and replaced entry 4')
    print('\n\n')
    bf.writeFile_XML('ajb58_books.xml')
    print('We can read and validate a file with the parse() function')
    try:
        bf_schema = etree.XMLSchema(file='/home/jrf/Documents/books/Books20/Tools/python/bookentry/xml/bookfile.xsd')
        Parser = etree.XMLParser(schema=bf_schema)
        print('The schema is well formed')
    except:
        print('The schema is not well formed')
        sys.exit(1)
    try:
        # etree.parse() returns an Etree rather than an Element
        bf3 = etree.parse('ajb58_books.xml', parser=Parser)
        print('The xml file is well formed and valid')
    except:
        print('The xml file is not well formed or is invalid')


