#
# Makefile for bookenty user interfaces and resources files
#
#  J. R. Fowler 2013
#
#

#
# Definitions
#
PYUIC = pyuic4
PYRCC = pyrcc4 -py3

#
# Target lists
#
USER_INTERFACES = ui_BookEntry.py ui_HeaderEntry.py ui_OrigStr.py \
		ui_EntrySelect.py

RESOURCE_FILES = ajb_rc.py


all: $(USER_INTERFACES) $(RESOURCE_FILES)
#
# Convert the XML designer files to Python files
#
ui_BookEntry.py: ui_BookEntry.ui
	$(PYUIC) -o ui_BookEntry.py ui_BookEntry.ui

ui_HeaderEntry.py: ui_HeaderEntry.ui
	$(PYUIC) -o ui_HeaderEntry.py ui_HeaderEntry.ui

ui_OrigStr.py: ui_OrigStr.ui
	$(PYUIC) -o ui_OrigStr.py ui_OrigStr.ui

ui_EntrySelect.py: ui_EntrySelect.ui
	$(PYUIC) -o ui_EntrySelect.py ui_EntrySelect.ui


#
# Convert the XML resource files to Python files
#
ajb_rc.py: ajb_rc.qrc
	$(PYRCC) -o ajb_rc.py ajb_rc.qrc


#
# Clean up our mess (what mess...)
#
clean:
	rm -rf *~ testfile* *.pdf *.png *.aux *.log *.dvi

distclean: clean
	rm -rf $(USER_INTERFACES) $(RESOURCE_FILES) *.pyc __pycache__