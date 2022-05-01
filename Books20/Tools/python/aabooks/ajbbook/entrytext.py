#
# -*- mode: python;-*-
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/ajbbook/entrytext.py
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
"""
This file contains the functions to convert an AJBentry to
a comma separated.  Note that the text format is depricated
and no longer in use.  It has been supplanted by the XML format.
However, we keep this around just in case.
"""

import re
from aabooks.ajbbook import ajbcomments as comments
from aabooks.lib import utils

#
# We disable these pylint warnings. exec() is used to
# minimize the number of statement and variables
# in event_from_text() and we have much too long a
# function in parse_comments(). However, we are not
# going the change parse_comments() because it is complicated
# and the text format is deprecated.
#

# pylint: disable=exec-used,too-many-branches,too-many-statements

#
# Build the regular expression compilers to we don't
# build the them every time we enter the entry_from_text()
# function.
#
__reg1__ = re.compile(r'\A\d+ +\d+\.\d+', re.UNICODE)

#
# Ascii comma separated variable file, read/write functions
#
#def write_text_from_entry(entry):
def entry_to_text(entry):
    """Write an AJBentry back into the string format that it came from.
    It should be the case that write(read(ajbstr)) == ajbstr up to
    the order of the comments and that read(write(ajbent)) == ajbent."""

    if not entry.is_valid():
        return ''

    entrystr = entry.num_str()[4:]

    entrystr += entry_text_authoreditor(entry)
    entrystr += ', ' + entry['Title'].replace(', ', ' comma ')

    entrystr += entry_text_publishers(entry)
    entrystr += entry_text_year(entry)
    entrystr += entry_text_pagination(entry)
    entrystr += entry_text_price(entry)
    entrystr += entry_text_reviews(entry)
    # the following are the various comment types
    entrystr += entry_text_edition(entry)
    entrystr += entry_text_reprint(entry)
    entrystr += entry_text_compilers(entry)
    entrystr += entry_text_contributors(entry)
    entrystr += entry_text_translated(entry)
    entrystr += entry_text_additional_editors(entry)
    entrystr += entry_text_additional_publishers(entry)
    entrystr += entry_text_language(entry)
    entrystr += entry_text_others(entry)
    entrystr += entry_text_reference(entry)

    return entrystr

def entry_text_authoreditor(entry):
    '''Convert entry Reviews to entry string review field'''

    entrystr = ' '

    if entry.not_empty('Authors'):
        entrystr += utils.make_name_str(entry['Authors'])
    elif entry.not_empty('Editors'):
        entrystr += utils.make_name_str(entry['Editors'])
        entrystr += ' ed.'

    return entrystr

def entry_text_publishers(entry):
    '''Convert entry Reviews to entry string review field'''

    entrystr = ''

    if entry.not_empty('Publishers'):
        entrystr += ', '
        if entry['Publishers'][0]['Place']:
            entrystr += entry['Publishers'][0]['Place']

        entrystr += ', '
        if entry['Publishers'][0]['PublisherName']:
            name = entry['Publishers'][0]['PublisherName']
            name = name.replace(', ', ' comma ')
            entrystr += name
    else:
        entrystr += ', , '

    return entrystr

def entry_text_year(entry):
    '''Convert entry Reviews to entry string review field'''

    entrystr = ', '

    if entry.not_empty('Year'):
        entrystr += str(entry['Year'])

    return entrystr

def entry_text_pagination(entry):
    '''Convert entry Reviews to entry string review field'''

    entrystr = ', '

    if entry.not_empty('Pagination'):
        entrystr += str(entry['Pagination'])

    return entrystr

def entry_text_price(entry):
    '''Convert entry Reviews to entry string review field'''

    entrystr = ', '

    if entry.not_empty('Price'):
        entrystr += str(entry['Price'])

    return entrystr

def entry_text_reviews(entry):
    '''Convert entry Reviews to entry string review field'''

    entrystr = ', '

    if entry.not_empty('Reviews'):
        first = True
        for review in entry['Reviews']:
            if not first:
                entrystr += ' and '
            first = False
            entrystr += review

    return entrystr

def entry_text_edition(entry):
    '''Convert entry Edition to entry string edition'''

    entrystr = ', '
    if entry.not_empty('Edition'):
        entrystr += str(entry['Edition'])
        num = int(entry['Edition'])
        if  num == 1:
            entrystr += 'st'
        elif num == 2:
            entrystr += 'nd'
        elif num == 3:
            entrystr += 'rd'
        else:
            entrystr += 'th'
        entrystr += ' edition;'

    return entrystr

def entry_text_reprint(entry):
    '''Convert entry Reprint to entry string reprint of'''

    entrystr = ' '

    if entry.not_empty('Reprint'):
        entrystr += 'reprint of '
        entrystr += str(entry['Reprint'])
        entrystr += ';'

    return entrystr

def entry_text_compilers(entry):
    '''Convert entry Compilers to entry string compiled by'''

    entrystr = ' '

    if entry.not_empty('Compilers'):
        entrystr += 'compiled by '
        entrystr += utils.make_name_str(entry['Compilers'])
        entrystr += ';'

    return entrystr

def entry_text_contributors(entry):
    '''Convert entry Contributors to entry string contributors'''

    entrystr = ' '

    if entry.not_empty('Contributors'):
        entrystr += 'contributors '
        entrystr += utils.make_name_str(entry['Contributors'])
        entrystr += ';'

    return entrystr

def entry_text_translated(entry):
    '''Convert entry Translated or TranslatedFrom to
    an entrystr translator comment.'''

    entrystr = ' '

    # translated from by
    if entry.not_empty('Translators') or entry.not_empty('TranslatedFrom'):
        entrystr += 'translated '
        if entry.not_empty('TranslatedFrom'):
            entrystr += 'from '
            entrystr += entry['TranslatedFrom']
        if entry.not_empty('Translators'):
            entrystr += ' by '
            entrystr += utils.make_name_str(entry['Translators'])
        entrystr += ';'

    return entrystr

def entry_text_additional_editors(entry):
    '''Convert the entry Editors to entrystr edited by
    but only if the author field is populated in which
    case these are additional editors.'''

    entrystr = ' '

    # additional editors
    if entry.not_empty('Authors') and entry.not_empty('Editors'):
        # need to include editors in comments
        entrystr += 'edited by '
        entrystr += utils.make_name_str(entry['Editors'])
        entrystr += ';'

    return entrystr

def entry_text_additional_publishers(entry):
    '''Convert the entry Publishers to entrystr also published'''

    entrystr = ' '

    # additional publishers
    if entry['Publishers'].__len__() > 1:
        extrapubl = entry['Publishers'][1:]
        entrystr += 'also published '
        first = True
        for publ in extrapubl:
            if not first:
                entrystr += ' and '
            first = False
            entrystr += f"{publ['Place'].replace(', ', ' comma ')}:"
            entrystr += f" {publ['PublisherName'].replace(', ', ' comma ')}"
        entrystr += ';'

    return entrystr

def entry_text_language(entry):
    '''Convert the entry Language to entrystr language'''

    entrystr = ' '

    if entry.not_empty('Language'):
        entrystr += f'in {entry["Language"]};'

    return entrystr

def entry_text_others(entry):
    '''Convert the entry Others to entrystr others'''

    entrystr = ' '
    # others (the comments)
    if entry.not_empty('Others'):
        for other in entry['Others']:
            entrystr += f"other {other.replace(', ', ' comma ')}; "

    return entrystr

def entry_text_reference(entry):
    '''Convert the entry Reference to the entrystr reference'''

    entrystr = ''
    if entry.not_empty('Reference'):
        entrystr += f'reference {entry["Reference"]};'

    return entrystr

#def read_text_to_entry(entry, line):
def entry_from_text(entry, line):
    """Parse a line with an AJB entry in it placing the values in the
    Entry dictionary. Returns True if this is a parsable line and
    false if it is not."""

    #
    # __reg1__ is used to check the beginning of a line
    # for an item number, volnum and section number. If no numbers are
    # seen, then we reject the line.
    #

    if line and __reg1__.match(line):
        entry['OrigStr'] = line
        fields = line.split(',')
        fieldnum = -1
        for field in fields:

            fieldnum += 1
            field = field.replace(' comma ', ', ')
            field = field.strip()
            exec(f'text_entry_field{fieldnum}(entry, field)')

def text_entry_field0(entry, field):
    '''AJBnum and Authors'''
    _parse_field0(entry, field)

def text_entry_field1(entry, field):
    '''Title'''
    entry['Title'] = field

def text_entry_field2(entry, field):
    '''place of publication'''
    place = "" + field
    entry['Publishers'].append({'Place' : place})

def text_entry_field3(entry, field):
    '''Publisher'''
    publishername = "" + field
    entry['Publishers'][0]['PublisherName'] = publishername

def text_entry_field4(entry, field):
    '''Publication Year'''
    entry['Year'] = field

def text_entry_field5(entry, field):
    '''Page Count'''
    entry['Pagination'] = field

def text_entry_field6(entry, field):
    '''Price'''
    entry['Price'] = field

def text_entry_field7(entry, field):
    '''Reviews'''
    if field:
        entry['Reviews'] = field.split(' and ')

def text_entry_field8(entry, field):
    '''Comments and other material'''
    entry['Comments'] = field
    _parse_comments(entry, field)


#
# Private functions
#
def _parse_field0(entry, line):

    fields = line.split(' ', 2)

    _parse_index(entry, fields[0])

    entry['Num'] = utils.parse_ajbnum(fields[1])

    if len(fields) > 2:
        _parse_authors(entry, fields[2].strip())



def _parse_index(entry, line):
    """
    Get the file Index value (i.e. what number is this entry
    in the file.)
    """
    entry['Index'] = line.strip()


def _parse_authors(entry, line):
    """split out the authors/editors
    """
    edt = False
    comp = False

    if line.endswith('ed.'):
        edt = True
        line = line.replace('ed.', '   ')
    elif line.endswith('comp.'):
        comp = True
        line = line.replace('comp.', '    ')

    names = utils.make_name_list(line)

    if edt:
        entry['Editors'] = names
    elif comp:
        entry['Compilers'] = names
    else:
        entry['Authors'] = names



def _parse_comments(entry, field):
    """comment"""
    cparser = comments.Comment.parser()
    results = cparser.parse_text(field, reset=True, multi=True)
    #
    # Look for translators, language, edition, and other publishers
    #
    if results:
        for result in results:
            grammar_name = result.elements[0].grammar_name
            if grammar_name == 'Edition':
                entry['Edition'] = result.elements[0].edition_num

            elif grammar_name == 'Reference':
                entry['Reference'] = str(result.find(comments.AJBNum)).strip()

            elif grammar_name == 'Reprint':
                tmp = result.find(comments.AJBNum)
                if tmp:
                    entry['Reprint'] = str(tmp).strip()
                tmp = result.find(comments.Year)
                if tmp:
                    entry['Reprint'] = str(tmp).strip()

            elif grammar_name == 'Editors':
                line = str(result.find(comments.NameList))
                name = utils.make_name_list(line)
                if entry.not_empty('Editors'):
                    entry['Editors'].extend(name)
                else:
                    entry['Editors'] = name

            elif grammar_name == 'Contributors':
                line = str(result.find(comments.NameList))
                name = utils.make_name_list(line)
                if entry.not_empty('Contributors'):
                    entry['Contributors'].extend(name)
                else:
                    entry['Contributors'] = name

            elif grammar_name == 'Compilers':
                line = str(result.find(comments.NameList))
                name = utils.make_name_list(line)
                if entry.not_empty('Compilers'):
                    entry['Compilers'].extend(name)
                else:
                    entry['Compilers'] = name

            elif grammar_name == 'Translation':
                tmp = result.find(comments.FromLanguage)
                if tmp:
                    entry['TranslatedFrom'] = str(tmp.elements[1]).strip()

                tmp = result.find(comments.ToLanguage)
                if tmp:
                    entry['Language'] = str(tmp.elements[1]).strip()

                tmp = result.find(comments.NameList)
                if tmp:
                    name = utils.make_name_list(str(tmp))
                    if entry.not_empty('Translators'):
                        entry['Translators'].extend(name)
                    else:
                        entry['Translators'] = name

            elif grammar_name == 'Publishers':
                tmp = str(result.find(comments.PublisherList))
                # the space chars in the split avoids problems with
                # e.g. Rand McNally & Sons
                tlist = tmp.split(' and ')
                for pub in tlist:
                    parts = pub.split(':')
                    entry['Publishers'].append({'Place' : parts[0].strip(),
                                                'PublisherName': parts[1].strip()})

            elif grammar_name == 'Language':
                entry['Language'] = str(result.find(comments.Word)).strip()

            elif grammar_name == 'Other':
                name = str(result.find(comments.Words)).strip()
                if not entry.not_empty('Others'):
                    entry['Others'] = []
                entry['Others'].append(name)

            else:
                print(f'Unknown grammer name {grammar_name}')



##
## Main work
##
if __name__ == '__main__':

    import unittest
    from aabooks.ajbbook.ajbentry import AJBentry

    TESTENT = {
        'ajbstr': '''4 66.145(1).29 P. W. Hodge, The Physics comma and \
Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, \
1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American \
216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other This is the \
ajbstr;''',

        'ajbstra' : '''4 66.145(1).29a P. W. Hodge, The Physics comma and \
Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, \
1966, 179pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American \
216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other This is the \
ajbstr;''',

        'ajbstra1' : '''4 66.145.29a P. W. Hodge, The Physics comma and \
Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, \
1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American \
216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other This is the \
ajbstr;''',

        'badajbstrd' : '''4 66.145.29d P. W. Hodge, The Physics comma \
and Astronomy of Galaxies and Cosmology, New York, McGraw-Hill Book Company, \
1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American \
216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, other This is the\
 ajbstr;''',

        'authorstr' : '''4 66.145(1).29 P. W. Hodge and I. A. Author and \
A. N. Other, The Physics comma and Astronomy of Galaxies and Cosmology, \
New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, Sci.\
 American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and Sky Tel. 33 \
109 and Sky Tel. 33 164, other This is the authorstr;''',

        'editorstr' : '''4 66.145.29 P.-W. Hodge jr. and I. A. Author III \
and A. Other and A. V. de la Name ed., The Physics comma and Astronomy of \
Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, \
$2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 \
and Sky Tel. 33 109 and Sky Tel. 33 164, other a first comment; edited by A. \
B. Name; translated from Italian into English by A. Trans; also published \
London: A Publishing Co.; other This is the editor string;''',

        'allfieldsstr' : '''4 66.145(0).29a P.-W. Hodge jr. and I. A. Author \
III and A. Other and A. V. de la Name, The Physics comma and Astronomy of \
Galaxies and Cosmology, New York, McGraw-Hill Book Company, 1966, 179 pp, \
$2.95 and $4.95, Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 \
and Sky Tel. 33 109 and Sky Tel. 33 164, 3rd edition; reprint of 1956; \
compiled by A. B. Compiler; contributors A. B. Contrib; \
translated from Italian by A. Trans; edited by A. B. Name; \
also published London: A Publishing Co.; \
in French; other a first comment; other This is the editor string; \
reference AJB 59.144.55b;''',

        'allfieldsstr2' : '''4 66.145(0).29 P.-W. Hodge jr. and I. A. Author \
III and A. Other and A. V. de la Name, The Physics comma and Astronomy of \
Galaxies and Cosmology, , , , , , Sci. American 216 Nr 2 142 and Sci. \
American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, reference \
AJB 59.144.55''',

        'badajbstr' : '''27 xx.145(1).309 P. W. Hodge, The Physics \
comma and Astronomy of Galaxies and Cosmology , New York, McGraw-Hill \
Book Company, 1966, 179 pp, $2.95 and $4.95, Sci. American 216 Nr 2 142 \
and Sci. American 216 Nr. 2 144 and Sky Tel. 33 109 and Sky Tel. 33 164, \
other This is the badstr;''',

        'badtitlestr' : '''27 66.145(1).309 P. W. Hodge, , \
New York, McGraw-Hill Book Company, 1966, 179 pp, $2.95 and $4.95, \
Sci. American 216 Nr 2 142 and Sci. American 216 Nr. 2 144 and \
Sky Tel. 33 109 and Sky Tel. 33 164, other This is the badstr;''',
        }


    class EntryTextTestCase(unittest.TestCase):
        '''Set up the unit tests'''

        def setUp(self):
            '''Initialize local stuff. We start with a fresh
            AJBentry object for every test.

            '''
            self.entry = AJBentry()

        def tearDown(self):
            '''Dispose of the Entry object at the end of every test.'''

            del self.entry

        def test_read_ajbstr(self):
            '''Test for valid entry with ajbstr'''

            self.entry.read_text_to_entry(TESTENT['ajbstr'])
            self.assertTrue(self.entry.is_valid())

        def test_read_ajbstra(self):
            '''Test for valid entry with ajbstra'''

            self.entry.read_text_to_entry(TESTENT['ajbstra'])
            self.assertTrue(self.entry.is_valid())

        def test_read_ajbstra1(self):
            '''Test for valid entry with ajbstra1'''

            self.entry.read_text_to_entry(TESTENT['ajbstra1'])
            self.assertTrue(self.entry.is_valid())

        def test_read_badajbstr(self):
            '''Test for invalid entry with badajbstr'''

            self.entry.read_text_to_entry(TESTENT['badajbstr'])
            self.assertFalse(self.entry.is_valid())

        def test_read_badtitlestr(self):
            '''Test for invalid entry with badtitlestr'''

            self.entry.read_text_to_entry(TESTENT['badtitlestr'])
            self.assertFalse(self.entry.is_valid())

        def test_read_multiauthor(self):
            '''Test for valid entry with authorstr'''

            self.entry.read_text_to_entry(TESTENT['authorstr'])
            self.assertTrue(self.entry.is_valid())

        def test_read_multieditor(self):
            '''Test for valid entry with editorstr'''

            self.entry.read_text_to_entry(TESTENT['editorstr'])
            self.assertTrue(self.entry.is_valid())

        def test_read_allfields(self):
            '''Test for valid entry with allfieldsstr'''

            self.entry.read_text_to_entry(TESTENT['allfieldsstr'])
            self.assertTrue(self.entry.is_valid())

        def test_write_allfields(self):
            '''Test for same strings when writing entries.'''

            self.entry.read_text_to_entry(TESTENT['allfieldsstr'])
            self.assertTrue(self.entry.is_valid())

            entry_str = '4 ' + self.entry.write_text_from_entry()
            self.assertEqual(entry_str, TESTENT['allfieldsstr'])

    unittest.main()
