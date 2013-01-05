"""Defines the class that handles disk files and entry lists
"""
# -*- mode: Python;-*-

import fileinput
import os
import traceback

from AJBentry import *

__version__ = 0.1

__defaultHeader__ = """Entry format

Num AJB_ID Author [and author [and…]] [ed.|comp.], Title, Place, Publisher, year, description, price, review [and review [and …]], comments

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
        self._entryList = []
        self._volumeNumber = -1
        self._fileName = ''
        self._baseName = ''
        self._dirty = False
        self._header = __defaultHeader__
        self.setFileName('document1')


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
        self._baseName = os.path.basename(filename)

    def getFileName(self):
        """Return the current value of the fileName."""
        return self._fileName


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
        or greater than the number of entries, 'None' is returned.
        """
        if count < 0 or count >= self._entryList.__len__():
            return None

        self.curEntryNumber = count
        return self._entryList[count]


    def setEntry(self, entry, count=-1):
        self._dirty = True
        pass

    def addEntry(self, entry):
        pass


    # file I/O
    def readFile(self, filename=None ):
        """Open and read the header stuff into _header and the entries
        into the entry list. The header is defined as everything
        before the first valid entry. If filename is not given, we use
        the value set in BookFile.setFileName().

        Return value is the number of record entries read."""

        if filename:
            self.setFileName(filename)

        if not os.path.isfile(self._fileName):
            # error dialog ?
            printf('Invalid file')
            return 0

        # if we have a good file, then clear the entryList and header
        self._entryList = []
        self._header = ''
        self._dirty = False

        entTemp = AJBentry()
        count = 0
        
        for line in fileinput.input([self._fileName]):
            line = line.strip()
            try:
                if not entTemp.read(line) and not count:
                    self._header = self._header + line + '\n'
            except:
                print(line + '\n')
                traceback.print_exc()
                print('\n\n')
         
            if entTemp.isValid():
                count += 1
                self._entryList.append(entTemp)
                entTemp = AJBentry()
         
        self.maxRecord = count

        return count

    def writeFile(self, filename=None):
        """Write the entry list and header to a disk file.
        if filename is not given, we use BookEntry._fileName instead.

        Returns True if the file could be written or False otherwise."""
 
        if filename:
            self.setFileName(filename)

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
            fd.write(str(count) + ' ' + ent.write() + newline)
            count += 1

        fd.close()
        self._dirty = False


if __name__ == "__main__":

    bf = BookFile()
    print( "%d entries found\n" % bf.readFile("ajb58_books.txt"))

    print( 'The header for %s' % bf.getFileName())
    print( bf.getHeader() )

    bf.writeFile("testfile.txt")
    # run diff ajb58_books.txt and testfile.txt after we get AJBentry.write()

    bf.readFile('testfile.txt')
    bf.writeFile('testfile2.txt')
