#
# Makefile
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

#
#   This makefile contains the instructions for installing the LaTeX
#   style package for the book "Some Important Books in Astronomy and
#   Astrophysics in the 20th Century"
#

TEX    = pdftex
LATEX  = pdflatex
BIBTEX = biber

# This rather assumes I am installing in a home directory
TEX_INSTALLDIR = $(prefix)/texmf/tex/latex/books20
TEX_INSTALLFILES = books20.sty

PDF_INSTALLDIR = ../../PDF
PDF_INSTALLFILES = 


#
# Basic TeX processing
#
test: test_sty.tex
	${LATEX} test_sty
	${BIBTEX} test_sty
	${LATEX} test_sty
	${LATEX} test_sty

#
# lines: count how many lines we have written
#
lines:
	wc ${TEX_INSTALLFILES} Makefile.am

install: install_tex

install_tex: 
	install -m 444 ${TEX_INSTALLFILES} ${TEX_INSTALLDIR}

install_pdf: ${PDF_INSTALLFILES}
	install -m 444 ${PDF_INSTALLFILES} ${PDF_INSTALLDIR}

clean:
	rm -f *~

veryclean: clean
	rm -f *.aux *.bbl *.bcf *.blg *.log *.dvi *.toc *.out *.pdf *.run.xml

distclean: veryclean
	rm -f Makefile Makefile.in


