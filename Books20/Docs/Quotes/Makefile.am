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
BIBTEX = bibtex

PUBLICHTML = $(htmldir)

TEXFILES = Quotes.tex

#
# Basic TeX processing
#
docs: Quotes

Quotes:
	${LATEX} Quotes.tex
	${BIBTEX} Quotes.aux
	${LATEX} Quotes.tex
	${LATEX} Quotes.tex


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

