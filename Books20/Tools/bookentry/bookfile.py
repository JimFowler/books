"""Defines the class that handles disk files and entry lists"""
# -*- coding: UTF-8 -*-
# -*- mode: Python;-*-

import fileinput
import os
import traceback

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
        self._entryList = []
        self._volumeNumber = -1
        self._fileName = 'document1'
        self._dirName = './'
        self._baseName = './'
        self.curEntryNumber = -1  # 1 <= curEntryNumber <= len(self._entryList)
        self._header = __defaultHeader__
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


    # file I/O
    def readFile(self, filename=None ):
        """Open and read the header stuff into _header and the entries
        into the entry list. The header is defined as everything
        before the first valid entry. If filename is not given, we use
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

        entTemp = AJBentry.AJBentry()
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
                entTemp = AJBentry.AJBentry()
         
        self.curEntryNumber = 1
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
    print( "%d entries found\n" % bf.readFile("./ajb58_books.txt"))

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
    print('testfile3.txt should have new entry 1 and 5 and replaced entry 4')
