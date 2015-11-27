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
USER_INTERFACES = ui_mainWindow.py

RESOURCE_FILES = 


all: $(USER_INTERFACES) $(RESOURCE_FILES)

#
# Convert the XML designer files to Python files
#
ui_mainWindow.py: designer/ui_mainWindow.ui
	$(PYUIC) -o ui_mainWindow.py designer/ui_mainWindow.ui



clean:
	rm -f *~

distclean: clean
	rm -rf $(USER_INTERFACES) $(RESOURCE_FILES) *.pyc __pycache__

