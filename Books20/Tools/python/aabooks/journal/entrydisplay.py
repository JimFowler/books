## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/journal/entrydisplay.py
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
'''The file contains the display_to_entry() and
entry_to_display() functions to convert a JournalEntry to
the display form JournalWindow in journalwindow.py.

'''

from aabooks.journal import journalentry

def entry_to_display(self, entry):
    '''Given an entry, display the parts on the GUI display.'''

    entry_display_title(self, entry)
    entry_display_publishers(self, entry)
    entry_display_abbreviations(self, entry)
    entry_display_startdate(self, entry)
    entry_display_enddate(self, entry)
    entry_display_linkprevious(self, entry)
    entry_display_linknext(self, entry)
    entry_display_designators(self, entry)
    entry_display_comments(self, entry)


def entry_display_title(self, entry):
    '''Convert entry Title and subTitle to display titleEdit.'''

    astr = ''
    if entry.not_empty('Title'):
        astr += entry['Title']
    if entry.not_empty('subTitle'):
        astr = astr + '\n' + entry['subTitle']
    if entry.not_empty('subsubTitle'):
        astr = astr + '\n' + entry['subsubTitle']
    self.titleEdit.setText(astr)

def entry_display_publishers(self, entry):
    '''Convert entry Publishers to display publisherEdit.'''

    astr = ''
    if entry.not_empty('Publishers'):
        first = True
        for mem in entry['Publishers']:
            if not first:
                astr += '\n'
            first = False
            if mem.__contains__('Place'):
                astr += mem['Place']
            astr += ' : '
            if mem.__contains__('Name'):
                astr += mem['Name']
            astr += ' : '
            if mem.__contains__('startDate'):
                astr += mem['startDate']
            astr += ' : '
            if mem.__contains__('endDate'):
                astr += mem['endDate']
    self.publisherEdit.setText(astr)

def entry_display_abbreviations(self, entry):
    '''Convert entry Abbreviations to display abbreviationsEdit.'''

    astr = ''
    if entry.not_empty('Abbreviations'):
        first = True
        for mem in entry['Abbreviations']:
            if not first:
                astr += '\n'
            first = False
            astr += mem
    self.abbreviationsEdit.setText(astr)

def entry_display_startdate(self, entry):
    '''Convert entry startDate to display startDateEdit.'''

    astr = ''
    if entry.not_empty('startDate'):
        astr += entry['startDate']
    self.startDateEdit.setText(astr)

def entry_display_enddate(self, entry):
    '''Convert entry endDate to display endDateEdit.'''

    astr = ''
    if entry.not_empty('endDate'):
        astr += entry['endDate']
    self.endDateEdit.setText(astr)

def entry_display_linkprevious(self, entry):
    '''Convert entry linkprevious to display LinkPreviousEdit.'''

    astr = ''
    if entry.not_empty('linkprevious'):
        first = True
        for mem in entry['linkprevious']:
            if not first:
                astr += '\n'
            first = False
            astr += mem
    self.LinkPreviousEdit.setText(astr)

def entry_display_linknext(self, entry):
    '''Convert entry linknext to display LinkNextEdit.'''

    astr = ''
    if entry.not_empty('linknext'):
        first = True
        for mem in entry['linknext']:
            if not first:
                astr += '\n'
            first = False
            astr += mem
    self.LinkNextEdit.setText(astr)

def entry_display_designators(self, entry):
    '''Convert entry Designators to display designatorsEdit.'''

    astr = ''
    if entry.not_empty('Designators'):
        first = True
        for mem in entry['Designators']:
            if not first:
                astr += '\n'
            first = False
            astr += mem
            astr += ' : '
            astr += entry['Designators'][mem]
    self.designatorEdit.setText(astr)

def entry_display_comments(self, entry):
    '''Convert entry Comments to display CommentsEdit.'''

    astr = ''
    if entry.not_empty('Comments'):
        first = True
        for mem in entry['Comments']:
            if not first:
                astr += '\n'
            first = False
            astr += mem
    self.CommentsEdit.setText(astr)


def display_to_entry(self):
    '''Copy the display into a new entry and return the entry. The display
    values should have already been checked for validity.  These
    functions do no checks for good data.

    '''

    entry = journalentry.JournalEntry()
    display_entry_title(self, entry)
    display_entry_publishers(self, entry)
    display_entry_abbreviations(self, entry)
    display_entry_startdate(self, entry)
    display_entry_enddate(self, entry)
    display_entry_linkprevious(self, entry)
    display_entry_linknext(self, entry)
    display_entry_designators(self, entry)
    display_entry_comments(self, entry)

    return entry

def display_entry_title(self, entry):
    '''Convert display titleEdit to entry Title and subTitle. Should
    modify this to handle more than 2 sub-titles.

    '''

    mem = self.titleEdit.toPlainText().strip()
    if mem:
        alist = mem.split('\n')
        alist_len = len(alist)
        entry['Title'] = alist[0]
        if alist_len > 1 and  alist[1] != 0:
            entry['subTitle'] = alist[1]
        if alist_len > 2 and alist[2] != 0:
            entry['subsubTitle'] = alist[2]

def display_entry_publishers(self, entry):
    '''Convert display publisherEdit to entry Publishers.'''

    mem = self.publisherEdit.toPlainText()
    if mem:
        alist = mem.split('\n')
        for line in alist:
            pubd = {}
            fields = line.split(':')
            num_fields = len(fields)
            # Check len(flds) here, pop dialog if not 4
            if num_fields > 0:
                pubd['Place'] = fields[0].strip()
            if num_fields > 1:
                pubd['Name'] = fields[1].strip()
            if num_fields > 2:
                pubd['startDate'] = fields[2].strip()
            if num_fields > 3:
                pubd['endDate'] = fields[3].strip()

            entry['Publishers'].append(pubd)

def display_entry_abbreviations(self, entry):
    '''Convert display abbreviationsEdit to entry Abbreviations.'''

    mem = self.abbreviationsEdit.toPlainText()
    if mem:
        alist = mem.split('\n')
        for line in alist:
            entry['Abbreviations'].append(line.strip())

def display_entry_startdate(self, entry):
    '''Convert display startDateEdit to entry startDate.'''

    entry['startDate'] = self.startDateEdit.text().strip()

def display_entry_enddate(self, entry):
    '''Convert display endDateEdit to entry endDate.'''

    entry['endDate'] = self.endDateEdit.text().strip()

def display_entry_linkprevious(self, entry):
    '''Convert display LinkPrevious to entry libprevious.'''

    mem = self.LinkPreviousEdit.toPlainText()
    if mem:
        alist = mem.split('\n')
        for line in alist:
            entry['linkprevious'].append(line.strip())

def display_entry_linknext(self, entry):
    '''Convert display LinkNextEdit to entry linknext.'''

    mem = self.LinkNextEdit.toPlainText()
    if mem:
        alist = mem.split('\n')
        for line in alist:
            entry['linknext'].append(line.strip())

def display_entry_designators(self, entry):
    '''Convert display designatorsEdit to entry Designators.'''

    mem = self.designatorEdit.toPlainText()
    if mem:
        alist = mem.split('\n')
        for line in alist:
            flds = line.split(':')
            entry['Designators'][flds[0].strip()] = flds[1].strip()

def display_entry_comments(self, entry):
    '''Convert display CommentsEdit to entry Comments.'''
    mem = self.CommentsEdit.toPlainText()
    if mem:
        alist = mem.split('\n')
        for line in alist:
            entry['Comments'].append(line)
