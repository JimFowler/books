##
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/ajbbook/entrydisplay.py
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
'''This file contains the functions to convert an AJBentry to/from the
display in the BookEntry form. The file is used by ajbwindow.py.

These functions should be split into
get_string from form()
convert_string_to_entry()
so that we can properly test them with unittests

'''
import re

from PyQt5 import QtWidgets

from nameparser import HumanName

from aabooks.ajbbook import ajbentry

# Note: that this regex will silently reject a suffix
#     that is not '' or [a-c].
r2 = re.compile(r'(\d+)([a-c]{0,1})', re.UNICODE)

def entry_to_display(self, entry):
    '''Given an entry, display the parts on the GUI display.'''

    entry_display_ajbnum(self, entry)
    entry_display_authors(self, entry)
    entry_display_editors(self, entry)
    entry_display_title(self, entry)
    entry_display_publishers(self, entry)
    entry_display_edition(self, entry)
    entry_display_year(self, entry)
    entry_display_pagination(self, entry)
    entry_display_price(self, entry)
    entry_display_review(self, entry)
    entry_display_language(self, entry)
    entry_display_fromlanguage(self, entry)
    entry_display_translators(self, entry)
    entry_display_transof(self, entry)
    entry_display_compilers(self, entry)
    entry_display_contributors(self, entry)
    entry_display_reprint(self, entry)
    entry_display_reference(self, entry)
    entry_display_others(self, entry)
    entry_display_keywords(self, entry)
    entry_display_unknown(self, entry)

def entry_display_ajbnum(self, entry):
    '''Convert an Entry Num to an AJB number display.'''

    anum = entry['Num']
    self.volNum.setText(str(anum['volNum']))
    self.secNum.setText(str(anum['sectionNum']))
    if int(anum['subsectionNum']) > -1:
        self.subSecNum.setText(str(anum['subsectionNum']))
    else:
        self.subSecNum.setText('0')
    self.itemNum.setText(str(anum['entryNum']) + anum['entrySuf'])
    self.pageNum.setText(str(anum['pageNum']))

def entry_display_authors(self, entry):
    '''Convert an Entry Authors to display authorEntry.'''

    astr = ''
    if entry.not_empty('Authors'):
        authors = entry['Authors']
        if authors:
            first = True
            for author in authors:
                if not first:
                    astr += '\n'
                first = False
                astr += str(author)
    self.authorEntry.setText(astr)

def entry_display_editors(self, entry):
    '''Convert an Entry Editors to display editorEntry.'''

    astr = ''
    if entry.not_empty('Editors'):
        editors = entry['Editors']
        if editors:
            first = True
            for editor in editors:
                if not first:
                    astr += '\n'
                first = False
                astr += str(editor)
    self.editorEntry.setText(astr)

def entry_display_title(self, entry):
    '''Convert an Entry Title to display titleEntry.'''

    astr = ''
    if entry.not_empty('Title'):
        astr += str(entry['Title'])
    self.titleEntry.setText(astr)

def entry_display_publishers(self, entry):
    '''Convert an Entry Publishers to display publEntry.'''

    astr = ''
    if entry.not_empty('Publishers'):
        first = True
        for publisher in entry['Publishers']:
            if not first:
                astr += '\n'
            first = False
            astr += str(publisher['Place']) + ' : ' \
                + str(publisher['PublisherName'])
    self.publEntry.setText(astr)

def entry_display_edition(self, entry):
    '''Conver an Entry Edition to display editionEntry.'''

    astr = ''
    if entry.not_empty('Edition'):
        astr += str(entry['Edition'])
    self.editionEntry.setText(astr)

def entry_display_year(self, entry):
    '''Convert an Entry Year to display yearEntry.'''
    # Year
    astr = ''
    if entry.not_empty('Year'):
        astr += str(entry['Year'])
    self.yearEntry.setText(astr)

def entry_display_pagination(self, entry):
    '''Convert an Entry Pagination to display pageEntry.'''

    astr = ''
    if entry.not_empty('Pagination'):
        astr += str(entry['Pagination'])
    self.pageEntry.setText(astr)

def entry_display_price(self, entry):
    '''Convert Entry Price to display priceEntry.'''

    astr = ''
    if entry.not_empty('Price'):
        astr += str(entry['Price'])
    self.priceEntry.setText(astr)

def entry_display_review(self, entry):
    '''Convert an Entry Reviews to display reviewsEntry.'''

    astr = ''
    if entry.not_empty('Reviews'):
        reviews = entry['Reviews']
        first = True
        if reviews:
            for review in reviews:
                if not first:
                    astr += '\n'
                astr += str(review)
                first = False
    self.reviewsEntry.setPlainText(astr)

def entry_display_language(self, entry):
    '''Convert an Entry Language to display tolangEntry.'''

    astr = ''
    if entry.not_empty('Language'):
        astr += str(entry['Language'])
    self.tolangEntry.setText(astr)

def entry_display_fromlanguage(self, entry):
    '''Convert an Entry TranslatedFrom to display fromlangEntry.'''

    astr = ''
    if entry.not_empty('TranslatedFrom'):
        astr += (entry['TranslatedFrom'])
    self.fromlangEntry.setText(astr)

def entry_display_translators(self, entry):
    '''Convert an Entry Translators to display translatorEntry.'''

    astr = ''
    if entry.not_empty('Translators'):
        translators = entry['Translators']
        if translators:
            first = True
            for translator in translators:
                if not first:
                    astr += '\n'
                first = False
                astr += str(translator)
    self.translatorEntry.setText(astr)

def entry_display_transof(self, entry):
    '''Convert an Entry TranslationOf to display transofEntry.'''

    astr = ''
    if entry.not_empty('TranslationOf'):
        astr += str(entry['TranslationOf'])
    self.transofEntry.setText(astr)

def entry_display_compilers(self, entry):
    '''Convert an Entry Compilers to display compilersEntry.'''

    astr = ''
    if entry.not_empty('Compilers'):
        compilers = entry['Compilers']
        if compilers:
            first = True
            for compiler in compilers:
                if not first:
                    astr += '\n'
                first = False
                astr += str(compiler)
    self.compilersEntry.setText(astr)

def entry_display_contributors(self, entry):
    '''Convert an Entry Contibutors to display contribEntry.'''

    astr = ''
    if entry.not_empty('Contributors'):
        contributors = entry['Contributors']
        if contributors:
            first = True
            for contributor in contributors:
                if not first:
                    astr += '\n'
                first = False
                astr += str(contributor)
    self.contribEntry.setText(astr)

def entry_display_reprint(self, entry):
    '''Convert an Entry Reprint to display reprintEntry.'''

    astr = ''
    if entry.not_empty('Reprint'):
        astr += str(entry['Reprint'])
    self.reprintEntry.setText(astr)

def entry_display_reference(self, entry):
    '''Convert an Entry Reference to display referenceEntry.'''

    astr = ''
    if entry.not_empty('Reference'):
        astr += str(entry['Reference'])
    self.referenceEntry.setText(astr)

def entry_display_others(self, entry):
    '''Convert an Entry Others to display commentsEntry.'''

    astr = ''
    if entry.not_empty('Others'):
        comments = entry['Others']
        first = True
        for comment in comments:
            if not first:
                astr += '\n'
            first = False
            astr += str(comment)
    self.commentsEntry.setPlainText(astr)

def entry_display_keywords(self, entry):
    '''Convert an Entry Keywords to display keywordEntry.'''

    astr = ''
    if entry.not_empty('Keywords'):
        keywords = entry['Keywords']
        first = True
        for keyword in keywords:
            if not first:
                astr += '\n'
            first = False
            astr += str(keyword)
    self.keywordEntry.setPlainText(astr)

def entry_display_unknown(self, entry):
    '''Pop a dialog if we get an unknown field type.'''

    for field in entry.keys():
        if self.known_entry_fields.count(field) == 0:
            QtWidgets.QMessageBox.warning(self, 'Unknown Entry Field',
                f'Unknown field \"{field}:  {entry["field"]}\"\n in entry {entry["index"]}\n',
                                          QtWidgets.QMessageBox.Ok)



def display_to_entry(self):
    '''Copy the display into a new entry and
    return the entry. Note that this functions expects the
    the display fields to be valid and no tests are done
    for validity of the display entry or the ajbentry.'''

    entry = ajbentry.AJBentry()

    display_entry_index(self, entry)
    display_entry_ajbnum(self, entry)
    display_entry_authors(self, entry)
    display_entry_editors(self, entry)
    display_entry_title(self, entry)
    display_entry_publishers(self, entry)
    display_entry_edition(self, entry)
    display_entry_year(self, entry)
    display_entry_pagination(self, entry)
    display_entry_price(self, entry)
    display_entry_reviews(self, entry)
    display_entry_language(self, entry)
    display_entry_fromlanguage(self, entry)
    display_entry_translators(self, entry)
    display_entry_transof(self, entry)
    display_entry_compilers(self, entry)
    display_entry_contributors(self, entry)
    display_entry_reprint(self, entry)
    display_entry_reference(self, entry)
    display_entry_others(self, entry)
    display_entry_keywords(self, entry)

    return entry

def display_entry_index(self, entry):
    '''Convert the display indexEntry to Entry Index.'''

    index = int(self.indexEntry.text())
    entry['Index'] = str(index - 1)

def display_entry_ajbnum(self, entry):
    '''Convert the display ajbnum to entry Num.'''

    num = {}
    num['volume'] = self.default_volume_name

    items = r2.split(self.itemNum.text().strip())

    num['volNum'] = int(self.volNum.text())
    num['sectionNum'] = int(self.secNum.text())
    num['subsectionNum'] = int(self.subSecNum.text())
    num['entryNum'] = int(items[1])
    num['entrySuf'] = items[2]
    num['pageNum'] = int(self.pageNum.text())

    entry['Num'] = num

def display_entry_authors(self, entry):
    '''Convert the display authorEntry to entry Authors.'''

    entrya = []
    authors = self.authorEntry.toPlainText()
    if authors:
        alist = authors.split('\n')
        for line in alist:
            name = HumanName(line)
            entrya.append(name)
    entry['Authors'] = entrya

def display_entry_editors(self, entry):
    '''Convert display editorsEntry to entry Editors.'''

    entrya = []
    editors = self.editorEntry.toPlainText()
    if editors:
        alist = editors.split('\n')
        for line in alist:
            name = HumanName(line)
            entrya.append(name)
    entry['Editors'] = entrya

def display_entry_title(self, entry):
    '''Convert display titleEntry to entry Title.'''

    entry['Title'] = self.titleEntry.toPlainText()

def display_entry_publishers(self, entry):
    '''Convert display publEntry to entry.'''

    entrya = []
    publishers = self.publEntry.toPlainText()
    if len(publishers) != 0:
        try:
            plist = publishers.split('\n')
            for publ in plist:
                pdict = {}
                place, publisher = publ.split(':')

                if not place:
                    place = ''
                if not publisher:
                    publisher = ''

                pdict['Place'] = place.strip()
                pdict['PublisherName'] = publisher.strip()
                entrya.append(pdict)

            entry['Publishers'] = entrya
        except ValueError:
            pass

def display_entry_edition(self, entry):
    '''Convert display editionEntry to entry Edition.'''

    edition = self.editionEntry.text()
    if len(edition) != 0:
        entry['Edition'] = edition

def display_entry_year(self, entry):
    '''Convert display yearEntry to entry Year.'''

    year = self.yearEntry.text()
    if len(year) != 0:
        entry['Year'] = year

def display_entry_pagination(self, entry):
    '''Convert display pageEntry to entry Pagination.'''

    pages = self.pageEntry.text()
    if len(pages) != 0:
        entry['Pagination'] = pages

def display_entry_price(self, entry):
    '''Convert display priceEntry to entry Price.'''

    price = self.priceEntry.text()
    if len(price) != 0:
        entry['Price'] = price

def display_entry_reviews(self, entry):
    '''Convert display reviewsEntry to entry Reviews.'''

    entrya = []
    reviews = self.reviewsEntry.toPlainText()
    if len(reviews) != 0:
        rlist = reviews.split('\n')
        for review in rlist:
            entrya.append(review)
    entry['Reviews'] = entrya

def display_entry_language(self, entry):
    '''Convert display tolangEntry to entry Language.'''

    lang = self.tolangEntry.text()
    if len(lang) != 0:
        entry['Language'] = lang

def display_entry_fromlanguage(self, entry):
    '''Convert display fromlangEntry to entry TranslatedFrom.'''

    lang = self.fromlangEntry.text()
    if len(lang) != 0:
        entry['TranslatedFrom'] = lang

def display_entry_translators(self, entry):
    '''Convert display translatorEntry to entry Translators.'''

    entrya = []
    translators = self.translatorEntry.toPlainText()
    if len(translators) != 0:
        tlist = translators.split('\n')
        for line in tlist:
            name = HumanName(line)
            entrya.append(name)
    entry['Translators'] = entrya

def display_entry_transof(self, entry):
    '''Convert display transofEntry to entry TranslationOf.'''

    transof = self.transofEntry.text()
    if len(transof) != 0:
        entry['TranslationOf'] = transof

def display_entry_compilers(self, entry):
    '''Convert display compilersEntry to entry Compilers.'''

    entrya = []
    compilers = self.compilersEntry.toPlainText()
    if len(compilers) != 0:
        clist = compilers.split('\n')
        for line in clist:
            name = HumanName(line)
            entrya.append(name)
    entry['Compilers'] = entrya

def display_entry_contributors(self, entry):
    '''Convert display contribEntry to entry Contributors.'''

    entrya = []
    contrib = self.contribEntry.toPlainText()
    if len(contrib) != 0:
        clist = contrib.split('\n')
        for line in clist:
            name = HumanName(line)
            entrya.append(name)
    entry['Contributors'] = entrya

def display_entry_reprint(self, entry):
    '''Convert display reprintEntry to entry Reprint.'''

    reprint = self.reprintEntry.text()
    if len(reprint) != 0:
        entry['Reprint'] = reprint

def display_entry_reference(self, entry):
    '''Convert display referenceEntry to entry Reference.'''

    ref = self.referenceEntry.text()
    if len(ref) != 0:
        entry['Reference'] = ref

def display_entry_others(self, entry):
    '''Convert display commentsEntry to entry Others.'''

    entrya = []
    comments = self.commentsEntry.toPlainText()
    if len(comments) != 0:
        clist = comments.split('\n')
        for line in clist:
            entrya.append(line)
    entry['Others'] = entrya

def display_entry_keywords(self, entry):
    '''Convert display keywordsEntry to entry Keywordss.'''

    entrya = []
    keywords = self.keywordEntry.toPlainText()
    if len(keywords) != 0:
        klist = keywords.split('\n')
        for line in klist:
            entrya.append(line)
    entry['Keywords'] = entrya

#
#
#
if __name__ == '__main__':
    print('No unit tests for entrydisplay.py.')
