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

TEXFILES = DatabaseDesign.tex
#
# Basic TeX processing
#
docs: DatabaseDesign

DatabaseDesign: DatabaseDesign.tex
	${LATEX} DatabaseDesign.tex
	${BIBTEX} DatabaseDesign.bcf
	${LATEX} DatabaseDesign.tex
	${LATEX} DatabaseDesign.tex

#
# lines: count how many lines we have written
#
lines:
	wc ${TEXFILES} ${BIBFILES} Makefile
#
# Installation
#
install_pdf: DatabaseDesign
	@echo "Installing PDF files in ${PUBLICHTML}"
	install -m 444 -p ./DatabaseDesign.pdf $(PUBLICHTML)

clean:
	rm -f *~

clean_tex:
	rm -f *.aux *.bbl *.bcf *.blg *.log *.dvi *.toc *.out *.pdf *.run.xml

veryclean: clean clean_tex

distclean: veryclean
	rm -f Makefile Makefile.in
