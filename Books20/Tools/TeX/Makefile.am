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
BIBTEX = bibtex

TEXFILES = style_guide

# This rather assumes I am installing in a home directory
INSTALLDIR = $(prefix)/texmf/tex/latex/books20
INSTALLFILES = books20.sty

#
# Basic TeX processing
#
style_guide: guide
guide: ${TEXFILES}
	${LATEX} style_guide.tex
	${LATEX} style_guide.tex
	${LATEX} style_guide.tex



#
# lines: count how many lines we have written
#
lines:
	wc ${TEXFILES} Makefile.am

install:
	install -m 444 ${INSTALLFILES} ${INSTALLDIR}

clean:
	rm -f *~

veryclean: clean
	rm -f *.aux *.log *.dvi *.toc *.out *.pdf

distclean: veryclean
	rm -f Makefile Makefile.in


