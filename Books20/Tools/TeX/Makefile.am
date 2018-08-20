#
# Makefile
#
#   This makefile contains the instructions for building the
#   style guide for the book "Some Important Books in Astronomy and
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
BIBTEX = biber

STYLEFILES = style_guide.tex style_latex.tex style_python.tex \
	style_english.tex

# This rather assumes I am installing in a home directory
TEX_INSTALLDIR = $(prefix)/texmf/tex/latex/books20
TEX_INSTALLFILES = books20.sty

EMACS_INSTALLDIR = $(prefix)/Emacs
EMACS_INSTALLFILES = books20.el generic_copyright.tex

PDF_INSTALLDIR = ../../PDF
PDF_INSTALLFILES = style_guide.pdf


#
# Basic TeX processing
#
guide: style_guide
style_guide: style_guide.pdf
style_guide.pdf: ${STYLEFILES}
	${LATEX} style_guide.tex
	${BIBTEX} style_guide.bcf
	${LATEX} style_guide.tex
	${LATEX} style_guide.tex



#
# lines: count how many lines we have written
#
lines:
	wc ${STYLEFILES} ${TEX_INSTALLFILES} ${EMACS_INSTALLFILES} Makefile.am

install: 
	install -m 444 ${TEX_INSTALLFILES} ${TEX_INSTALLDIR}
	install -m 444 ${EMACS_INSTALLFILES} ${EMACS_INSTALLDIR}

install_pdf: ${PDF_INSTALLFILES}
	install -m 444 ${PDF_INSTALLFILES} ${PDF_INSTALLDIR}

clean:
	rm -f *~

veryclean: clean
	rm -f *.aux *.bbl *.bcf *.blg *.log *.dvi *.toc *.out *.pdf *.run.xml

distclean: veryclean
	rm -f Makefile Makefile.in


