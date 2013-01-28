
all: ui_BookEntry.py ui_HeaderEntry.py


ui_BookEntry.py: ui_BookEntry.ui
	pyuic4 -o ui_BookEntry.py ui_BookEntry.ui

ui_HeaderEntry.py: ui_HeaderEntry.ui
	pyuic4 -o ui_HeaderEntry.py ui_HeaderEntry.ui

clean:
	rm -rf *~ testfile* *.pdf *.png *.aux *.log *.dvi

distclean: clean
	rm -rf ui_BookEntry.py ui_HeaderEntry.py *.pyc __pycache__