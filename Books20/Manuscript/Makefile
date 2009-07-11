#
# Makefile
#
#   This makefile contains the instructions for building the
#   manuscript for the book "Some Important Books in Astronomy and
#   Astrophysics in the 20th Century"
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

TEXFILES = astro_20.tex astro_pre.tex books20.tex intro.tex \
	 preface.tex the_books.tex the_process.tex

BIBFILES = references.bib


SAVFILES = backup.date ${TEXFILES} ${BIBFILES} Makefile

default:
	@echo "Make options:"
	@echo "    manuscript: create the PDF manuscript,"
	@echo "    install: copy the PDF files to the web directory,"
	@echo "    lines: count how many lines we have written to date,"
	@echo "    veryclean: clean up the directory of uneccessary files,"
	@echo "    svn: archive important files in subversion,"
	@echo "    backuptar: create books20.tgz,"
	@echo "    eod: end of day, clean up and create tar file."
	@echo ""

#
# Basic TeX processing
#
manuscript: ${TEXFILES} ${BIBFILES}
	${LATEX} books20.tex
	${BIBTEX} books20.aux
	${LATEX} books20.tex
	${LATEX} books20.tex


#
# Copy the PDF file to the web site
#
install: manuscript
	cp --backup --update books20.pdf ${WEBPAGES}


#
# lines: count how many lines we have written
#
lines:
	wc ${TEXFILES} ${BIBFILES} Makefile


#
# Archive in svn
#
svn:
	@echo "svn routines for books20 are not defined yet"


#
# Backup routines
#
backuptar: backupdate
	tar -zcf books20.tgz ${SAVFILES}

backupdate:
	date > backup.date

veryclean:
	rm -f *.aux *.log *.blg *.bbl *.toc  *.pdf *~ backup.date core


#
# End of Day stuff.  Clean up messy files. Make backups
#
eod: veryclean backuptar
