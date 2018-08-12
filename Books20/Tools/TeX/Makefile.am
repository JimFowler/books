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

STYLEILES = style_guide.tex style_latex.tex style_python.tex

# This rather assumes I am installing in a home directory
INSTALLDIR = $(prefix)/texmf/tex/latex/books20
INSTALLFILES = books20.sty

#
# Basic TeX processing
#
guide: style_guide
style_guide: ${STYLEFILES}
	${LATEX} style_guide.tex
	${BIBTEX} style_guide.bcf
	${LATEX} style_guide.tex
	${LATEX} style_guide.tex



#
# lines: count how many lines we have written
#
lines:
	wc ${STYLEFILES} Makefile.am

install:
	install -m 444 ${INSTALLFILES} ${INSTALLDIR}

clean:
	rm -f *~

veryclean: clean
	rm -f *.aux *.bbl *.bcf *.blg *.log *.dvi *.toc *.out *.pdf *.run.xml

distclean: veryclean
	rm -f Makefile Makefile.in


