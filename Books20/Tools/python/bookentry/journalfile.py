'''Defines the class that handles disk files and entry lists'''
# -*- coding: UTF-8 -*-
# -*- mode: Python;-*-

import os
from lxml import etree

import bookentry.journalentry as journalentry

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
        # a list of JournalEntry objects
        self._entry_list = []

        self._file_name = './document1'

        # 1 <= current_entry_number <= len(self._entry_list)
        self.current_entry_number = -1

        self.schema_name = None
        self._dirty = False

        self.set_file_name('document1')

    # dirty (modified) file
    def is_dirty(self):
        """Returns a boolean. The value is True if any of the entries
        or the header has changed since the last read() or write().
        """
        return self._dirty


    # file name
    def set_file_name(self, filename):
        """Set the name of the disk file. Thus one can read a file,
        set a new file name, and save the file. No validity checking
        is done at this stage."""
        self._file_name = filename
        self._dirty = True

    def get_file_name(self):
        """Return the current value of the fileName."""
        return self._file_name

    def get_base_name(self):
        """Returns the basename() of the current filename."""
        dirname, basename = os.path.split(self._file_name)
        return basename

    def get_dir_name(self):
        """Returns the dirname() of the current filename."""
        dirname, basename = os.path.split(self._file_name)
        return dirname


    # header
    def set_header(self, header_string):
        """Set the header entry to be header_string."""
        self._dirty = True
        self._header = header_string
    def setHeader(self, header_string):
        '''temporary hack until headerWindow.py is converted to PEP 8'''
        self.set_header( header_string)

    def get_header(self):
        """Return the current header string."""
        return self._header
    def getHeader(self):
        '''temporary hack until headerWindow.py is converted to PEP 8'''
        self.get_header()

    # current entry
    def get_entry(self, count=-1):
        """Returns the entry at position count. If count is less than 0
        or greater than the number of entries, 'None' is returned. Note
        that 1 <= count <= len(self._entry_list).
        """
        if count < 1 or count > len(self._entry_list):
            return None

        self.current_entry_number = count - 1
        return self._entry_list[self.current_entry_number]

    def set_entry(self, entry, count=-1):

        """Write over the current entry or the entry at position
        'count' if given.  Note that 1 <= count <= len(self._entry_list).
        The dirty flag is set for the file."""

        if not entry.is_valid():
            print('bookfile().set_entry count %d entry:'%count)
            print(entry)
            return False

        if count < 1 or count > len(self._entry_list):
            return False

        self.current_entry_number = count - 1
        self._entry_list[self.current_entry_number] = entry
        self._dirty = True
        return True

    def set_new_entry(self, entry, count=-1):
        """Append an entry to the list or insert before entry 'count'
        if that value is given. Note that 1 <= count <= len(self._entry_list).
        The dirty flag is set for the file.
        """

        if not entry.is_valid():
            return False

        #print('bookfile', count, entry['Num'] )
        if count < 1 or count > len(self._entry_list):
            self._entry_list.append(entry)
        else:
            self.current_entry_number = count - 1
            self._entry_list.insert(self.current_entry_number, entry)

        self._dirty = True
        return True

    def delete_entry(self, entry_number):
        '''Delete the (entry_number - 1) record in the list, if such exists.
        Return the length of the remaining list.'''
        if entry_number > 0 and entry_number <= len(self._entry_list):
            self._entry_list.pop(entry_number - 1)
            self._dirty = True

        return len(self._entry_list)

    def make_short_title_list(self):
        '''Create a string of short titles from all entries in the list.
        A short title is "count AJBnum Title" and is used to look quickly
        at the list of titles.'''

        short_title_list = ''
        count = 1
        for entry in self._entry_list:
            short_title_list = short_title_list + str(count) + \
                               ' ' + entry['Title'] + '\n'
            count += 1

        return short_title_list

    #
    # schema utilities
    #
    def set_schema_name(self, sname):
        """Record the schema name so we can use it later."""
        self.schema_name = sname

    # file I/O
    def read_xml_file(self, filename=None):
        """Open and read the header stuff into _header and the entries
        into the entry list. If filename is not given, we use
        the value set in BookFile.set_file_name() if valid. Note that we
        do not care if the entries or header have been modified; that is
        the job of the calling routine.

        Return value is the number of record entries read."""

        if filename:
            self.set_file_name(filename)

        if self._file_name == '' or not os.path.isfile(self._file_name):
            return 0 # no records read

        # if we have a good file, then clear the entryList and header
        self._entry_list = []
        self._header = ''
        self._dirty = False

        count = 0

        # read and validate the XML file
        try:
            jf_schema = etree.XMLSchema(file=self.schema_name)
            parser = etree.XMLParser(schema=jf_schema)
        except etree.XMLSchemaParseError:
            # change to message Box but we don't have Qt loaded
            # return indicator to journalWin that schema file is unreadable?
            print('The schema {0} is not well formed'.format(self.schema_name))
            return 0
        try:
            jf_xml = etree.parse(self._file_name, parser=parser)
        except etree.XMLSyntaxError:
            # change to message Box but we don't have Qt loaded
            # return indicator to journalWin that xml file is unreadable?
            print('The xml file {0} is not well formed or is invalid'.format(self._file_name))
            return 0

        root_node = jf_xml.getroot()
        for child in root_node:
            if child.tag == 'Header':
                self.set_header(child.text)

            if child.tag == 'Journals':
                for entry in child:
                    temp_entry = journalentry.JournalEntry()
                    temp_entry.read_xml_to_entry(entry)
                    if temp_entry.is_valid():
                        count += 1
                        self._entry_list.append(temp_entry)

        self._dirty = False
        return count


    def write_xml_file(self, filename=None):
        """Write the entry list and header to a disk file.
        if filename is not given, we use BookEntry._file_name instead.

        Returns True if the file could be written or False otherwise."""

        if filename:
            self.set_file_name(filename)

        try:
            file_descriptor = open(self._file_name, 'w', encoding='UTF8')
        except (FileNotFoundError, PermissionError):
            return False

        # We do something clever here when we know how.
        jf_root = etree.Element('JournalFile')
        header = etree.SubElement(jf_root, 'Header')
        header.text = self.get_header()

        journals = etree.SubElement(jf_root, 'Journals')
        for entry in self._entry_list:
            entry_xml = entry.write_xml_from_entry()
            journals.append(entry_xml)

        jf_string = etree.tostring(jf_root,
                                   xml_declaration=True,
                                   method='xml', encoding='UTF-8')
        strstr = jf_string.decode(encoding='UTF-8')
        file_descriptor.write(strstr)

        file_descriptor.close()
        self._dirty = False


if __name__ == "__main__":

    def test_journal_file():
        '''Test the journal file methods.'''
        import sys

        jfile = JournalFile()
        jfile.read_xml_file('./xml/JournalFile.xml')

        print('The header for %s' % jfile.get_file_name())
        print(jfile.get_header())

        jfile.write_xml_file('journalfile_test.xml')
        print('We can read and validate a file with the parse() function')
        try:
            test_schema = etree.XMLSchema(file='./xml/journalfile.xsd')
            test_parser = etree.XMLParser(schema=test_schema)
            print('The schema is well formed')
        except etree.XMLSchemaParseError:
            print('The schema is not well formed')
            sys.exit(1)
        try:
            # etree.parse() returns an Etree rather than an Element
            etree.parse('./xml/JournalFile_test.xml', parser=test_parser)
            print('The xml file is well formed and valid')
        except etree.XMLSyntaxError:
            print('The xml file is not well formed or is invalid')


    test_journal_file()
