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
TEX    = pdftex
LATEX  = pdflatex
BIBTEX = biber

PUBLICHTML = $(htmldir)

#
# Basic TeX processing
#
docs: Notes

Notes:
	${LATEX} Notes.tex
	${BIBTEX} Notes.bcf
	${LATEX} Notes.tex
	${LATEX} Notes.tex

#
# lines: count how many lines we have written
#
lines:
	wc ${TEXFILES} ${BIBFILES} Makefile
#
# Installation
#
install_pdf: Notes
	@echo "Installing PDF files in ${PUBLICHTML}"
	install -m 444 -p ./Notes.pdf $(PUBLICHTML)

#
# Clean
#

clean:
	rm -f *~

veryclean: clean
	rm -f *.aux *.bbl *.bcf *.blg *.log *.dvi *.toc *.out *.pdf *.run.xml

distclean: veryclean
	rm -f Makefile Makefile.in
