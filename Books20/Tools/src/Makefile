
all: ui_BookEntry.py ui_HeaderEntry.py


ui_BookEntry.py: ui_BookEntry.ui
	pyuic4 -o ui_BookEntry.py ui_BookEntry.ui

clean:
	rm *~ testfile*

distclean: clean
	rm -rf ui_BookEntry.py *.pyc __pycache__