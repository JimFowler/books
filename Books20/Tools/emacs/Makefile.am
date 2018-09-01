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
EMACS_INSTALLDIR = ${prefix}/Emacs
EMACS_INSTALLFILES = books20.el

PDF_INSTALLDIR = ../../PDF
PDF_INSTALLFILES = 


#
# Basic TeX processing
#
test:
	${LATEX}
	${BIBTEX}
	${LATEX} 
	${LATEX} 

#
# lines: count how many lines we have written
#
lines:
	wc ${EMACS_INSTALLFILES} Makefile.am

install: install_emacs

install_emacs: 
	install -m 444 ${EMACS_INSTALLFILES} ${EMACS_INSTALLDIR}
	install -m 444 generic_copyright.tex ${EMACS_INSTALLDIR}/Files

install_pdf: ${PDF_INSTALLFILES}
	install -m 444 ${PDF_INSTALLFILES} ${PDF_INSTALLDIR}

clean:
	rm -f *~

veryclean: clean


distclean: veryclean
	rm -f Makefile Makefile.in


