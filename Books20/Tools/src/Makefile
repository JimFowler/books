
all: ui_BookEntry.py ui_HeaderEntry.py ui_OrigStr.py


ui_BookEntry.py: ui_BookEntry.ui
	pyuic4 -o ui_BookEntry.py ui_BookEntry.ui

ui_HeaderEntry.py: ui_HeaderEntry.ui
	pyuic4 -o ui_HeaderEntry.py ui_HeaderEntry.ui

ui_OrigStr.py: ui_OrigStr.ui
	pyuic4 -o ui_OrigStr.py ui_OrigStr.ui

clean:
	rm -rf *~ testfile* *.pdf *.png *.aux *.log *.dvi

distclean: clean
	rm -rf ui_BookEntry.py ui_HeaderEntry.py ui_OrigStr.py *.pyc __pycache__