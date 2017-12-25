#
# Makefile
#
#   This makefile contains the instructions for building the
#   section on series for the book "Some Important Books in Astronomy and
#   Astrophysics in the 20th Century"
#
#
#   Copyright 2017 James R. Fowler
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
BIBTEX = bibtex

SERIES_FILES = series.tex HarvardBooksAstronomy.tex uchicago.tex uaspacescience.tex
HANDBOOK_FILES = handbuch.tex

BIBFILES = references.bib

#
# Basic TeX processing
#
#	 ${BIBTEX} series.aux
series: ${SERIES_FILES}
	${LATEX} series.tex
	${LATEX} series.tex
	${LATEX} series.tex

handbuch handbook: handbuch.tex
	${LATEX} handbuch.tex
	${LATEX} handbuch.tex
	${LATEX} handbuch.tex



#
# lines: count how many lines we have written
#
lines:
	wc ${TEXFILES} Makefile.am
#	wc ${TEXFILES} ${BIBFILES} Makefile


clean:
	rm -f *~

veryclean: clean
	rm -f *.aux *.log *.dvi *.lot *.toc *.out *.pdf

distclean: veryclean
	rm -f Makefile Makefile.in


