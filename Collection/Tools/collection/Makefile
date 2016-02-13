#
# Makefile for collection user interfaces and resource files
#
#  J. R. Fowler Nov 2015
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
USER_INTERFACES = ui_mainWindow.py ui_select.py\
		  ui_book.py ui_author.py\
		  ui_vendor.py ui_project.py ui_tasks.py

RESOURCE_FILES = 


all: $(USER_INTERFACES) $(RESOURCE_FILES)

#
# Convert the XML designer files to Python files
#
ui_mainWindow.py: designer/ui_mainWindow.ui
	$(PYUIC) -o ui_mainWindow.py designer/ui_mainWindow.ui

ui_select.py: designer/ui_select.ui
	$(PYUIC) -o ui_select.py designer/ui_select.ui

ui_book.py: designer/ui_book.ui
	$(PYUIC) -o ui_book.py designer/ui_book.ui

ui_want.py: designer/ui_want.ui
	$(PYUIC) -o ui_want.py designer/ui_want.ui

ui_author.py: designer/ui_author.ui
	$(PYUIC) -o ui_author.py designer/ui_author.ui

ui_project.py: designer/ui_project.ui
	$(PYUIC) -o ui_project.py designer/ui_project.ui

ui_vendor.py: designer/ui_vendor.ui
	$(PYUIC) -o ui_vendor.py designer/ui_vendor.ui

ui_reports.py: designer/ui_reports.ui
	$(PYUIC) -o ui_reports.py designer/ui_reports.ui

ui_tasks.py: designer/ui_tasks.ui
	$(PYUIC) -o ui_tasks.py designer/ui_tasks.ui



clean:
	rm -f *~

distclean: clean
	rm -rf $(USER_INTERFACES) $(RESOURCE_FILES) *.pyc __pycache__

