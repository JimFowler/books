#
# Makefile for bookentry user interfaces and resources files
#
#  J. R. Fowler 2013
#
#

#
# Definitions
#
PYUIC = pyuic5
PYRCC = pyrcc5
#PYRCC = pyrcc4 -py3

#
# Target lists
#
USER_INTERFACES = ui_BookEntry.py ui_HeaderEntry.py ui_OrigStr.py \
		ui_EntrySelect.py ui_JournalSearch.py ui_JournalEntry.py

RESOURCE_FILES = ajb_rc.py


all: $(USER_INTERFACES) $(RESOURCE_FILES)
#
# Convert the XML designer files to Python files
#
ui_BookEntry.py: designer/ui_BookEntry.ui
	$(PYUIC) -o ui_BookEntry.py designer/ui_BookEntry.ui

ui_HeaderEntry.py: designer/ui_HeaderEntry.ui
	$(PYUIC) -o ui_HeaderEntry.py designer/ui_HeaderEntry.ui

ui_OrigStr.py: designer/ui_OrigStr.ui
	$(PYUIC) -o ui_OrigStr.py designer/ui_OrigStr.ui

ui_EntrySelect.py: designer/ui_EntrySelect.ui
	$(PYUIC) -o ui_EntrySelect.py designer/ui_EntrySelect.ui


ui_JournalSearch.py: designer/ui_JournalSearch.ui
	$(PYUIC) -o ui_JournalSearch.py designer/ui_JournalSearch.ui

ui_JournalEntry.py: designer/ui_JournalEntry.ui
	$(PYUIC) -o ui_JournalEntry.py designer/ui_JournalEntry.ui

#
# Convert the XML resource files to Python files
#
ajb_rc.py: Resources/ajb_rc.qrc
	$(PYRCC) -o ajb_rc.py Resources/ajb_rc.qrc


#
# Clean up our mess (what mess...)
#
clean:
	rm -rf *~ testfile* ajb58_books.xml *.pdf *.png *.aux *.log *.dvi

distclean: clean
	rm -rf $(USER_INTERFACES) $(RESOURCE_FILES) *.pyc __pycache__
