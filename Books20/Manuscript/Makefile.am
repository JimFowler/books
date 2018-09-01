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
TEX    = pdftex
LATEX  = pdflatex
BIBTEX = biber

TEXFILES = astro_20.tex astro_pre.tex books20.tex intro.tex \
	 preface.tex the_books.tex the_process.tex

BIBFILES = references.bib

#
# Basic TeX processing
#
manuscript: ${TEXFILES} ${BIBFILES}
	${LATEX} books20
	${BIBTEX} books20
	${LATEX} books20
	${LATEX} books20


#
# lines: count how many lines we have written
#
lines:
	wc ${TEXFILES} ${BIBFILES} Makefile


