#
# Makefile
#
#   This makefile contains the instructions for building the
#   auxillary documents for the project Books20 "Some Important
#   Books in Astronomy and Astrophysics in the 20th Century"
#
#
#   Copyright 2008 James R. Fowler
#
#   All rights reserved. No part of this publication may be
#   reproduced, stored in a retrival system, or transmitted
#   in any form or by any means, electronic, mechanical,
#   photocopying, recording, or otherwise, without prior written
#   permission of the author.
# 
#
#   The last known changes were checked in by $Author$
#   as revision $LastChangedRevision$
#   on $Date$
#
#

TEX    = pdftex
LATEX  = pdflatex
BIBTEX = bibtex

PRINTER = lp -Phome

WEBPAGES = /home/jrf/public_html

TEXFILES = DatabaseDesign.txt

BIBFILES = BooksRead.bib BooksNoted.bib


SAVFILES = backup.date ${TEXFILES} ${BIBFILES} Makefile

default:
	@echo "Make options:"
	@echo "    docs: create all the PDF documents,"
	@echo "    install: copy the PDF files to the web directory,"
	@echo "    lines: count how many lines we have written to date,"
	@echo "    veryclean: clean up the directory of uneccessary files,"
	@echo "    cvs: archive important files in cvs,"
	@echo "    backuptar: create books20.tgz,"
	@echo "    eod: end of day, clean up and create tar file."
	@echo ""

#
# Basic TeX processing
#
docs: DatabaseDesign Quotes

DatabaseDesign: DatabaseDesign.tex
	${LATEX} DatabaseDesign.tex
	${LATEX} DatabaseDesign.tex

Quotes:
	${LATEX} Quotes.tex
	${BIBTEX} Quotes.aux
	${LATEX} Quotes.tex
	${LATEX} Quotes.tex

Notes:
	${LATEX} Notes.tex
	${BIBTEX} Notes.aux
	${LATEX} Notes.tex
	${LATEX} Notes.tex

#
# Copy the PDF file to the web site
#
install: docs



#
# lines: count how many lines we have written
#
lines:
	wc ${TEXFILES} ${BIBFILES} Makefile


#
# Archive in cvs
#
cvs:
	@echo "cvs routines for books20 are not defined yet"


#
# Backup routines
#
backuptar: backupdate
	tar -zcf Books20-docs.tgz ${SAVFILES}

backupdate:
	date > backup.date

veryclean:
	rm -f *.aux *.log *.blg *.bbl *.toc  *.pdf *~ core


#
# End of Day stuff.  Clean up messy files. Make backups
#
eod: veryclean backuptar
