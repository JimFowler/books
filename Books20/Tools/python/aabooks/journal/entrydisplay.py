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



def entry_to_display(self, entry):
        """Given an entry, display the parts on the GUI display."""

        astr = ''
        if entry.not_empty('Title'):
            astr += entry['Title']
        if entry.not_empty('subTitle'):
            astr = astr + '\n' + entry['subTitle']
        if entry.not_empty('subsubTitle'):
            astr = astr + '\n' + entry['subsubTitle']
        self.titleEdit.setText(astr)

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


        astr = ''
        if entry.not_empty('Abbreviations'):
            first = True
            for mem in entry['Abbreviations']:
                if not first:
                    astr += '\n'
                first = False
                astr += mem
        self.abbreviationsEdit.setText(astr)

        astr = ''
        if entry.not_empty('startDate'):
            astr += entry['startDate']
        self.startDateEdit.setText(astr)

        astr = ''
        if entry.not_empty('endDate'):
            astr += entry['endDate']
        self.endDateEdit.setText(astr)

        astr = ''
        if entry.not_empty('linkprevious'):
            first = True
            for mem in entry['linkprevious']:
                if not first:
                    astr += '\n'
                first = False
                astr += mem
        self.LinkPreviousEdit.setText(astr)

        astr = ''
        if entry.not_empty('linknext'):
            first = True
            for mem in entry['linknext']:
                if not first:
                    astr += '\n'
                first = False
                astr += mem
        self.LinkNextEdit.setText(astr)

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


        astr = ''
        if entry.not_empty('Comments'):
            first = True
            for mem in entry['Comments']:
                if not first:
                    astr += '\n'
                first = False
                astr += mem
        self.CommentsEdit.setText(astr)

        self.repaint()


    def display_to_entry(self):
        """Copy the display into a new entry and
        return the entry."""
        entry = journalentry.JournalEntry()

        # Titles
        mem = self.titleEdit.toPlainText().strip()
        if mem:
            alist = mem.split('\n')
            alist_len = len(alist)
            if not alist:
                return None
            entry['Title'] = alist[0]
            if alist_len > 1 and  alist[1] != 0:
                entry['subTitle'] = alist[1]
            if alist_len > 2 and alist[2] != 0:
                entry['subsubTitle'] = alist[2]


        # Publishers
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


        # Abbreviations
        mem = self.abbreviationsEdit.toPlainText()
        if mem:
            alist = mem.split('\n')
            for line in alist:
                entry['Abbreviations'].append(line.strip())

        # startDate
        entry['startDate'] = self.startDateEdit.text().strip()

        # endDate
        entry['endDate'] = self.endDateEdit.text().strip()

        # link previous
        mem = self.LinkPreviousEdit.toPlainText()
        if mem:
            alist = mem.split('\n')
            for line in alist:
                entry['linkprevious'].append(line.strip())

        # link next
        mem = self.LinkNextEdit.toPlainText()
        if mem:
            alist = mem.split('\n')
            for line in alist:
                entry['linknext'].append(line.strip())

        # Designators
        mem = self.designatorEdit.toPlainText()
        if mem:
            alist = mem.split('\n')
            for line in alist:
                flds = line.split(':')
                entry['Designators'][flds[0].strip()] = flds[1].strip()


        # Comments
        mem = self.CommentsEdit.toPlainText()
        if mem:
            alist = mem.split('\n')
            for line in alist:
                entry['Comments'].append(line)

        return entry
