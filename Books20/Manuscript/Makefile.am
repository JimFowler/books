# Begin copyright
#
#  /home/jrf/Documents/books/Books20/Playground/Makefile_generic.am
#  
#   Part of the Books20 Project
#
#   Copyright 2018 James R. Fowler
#
#   All rights reserved. No part of this publication may be
#   reproduced, stored in a retrival system, or transmitted
#   in any form or by any means, electronic, mechanical,
#   photocopying, recording, or otherwise, without prior written
#   permission of the author.
#
#
# End copyright

#
#   The generic feature of a Makefile.am.  All Makefiles
#   should have these targets at a minimum. The targets don't
#   need to do anything but `make` should not generate an error
#   because the target does not exist.
#

#
# Include local definitions
#
include ${BOOKS20_ROOT}/makefile.local

#
# Run make in these sub-directories
#
SUB_DIRS = 

TEX_FILES = astro_20.tex astro_pre.tex books20.tex intro.tex \
	preface.tex the_books.tex the_process.tex

BIB_FILES =
#
# Build any software and/or documents
#
all: build_software build_docs

.PHONY: ${SUB_DIRS}
${SUB_DIRS} :
	@echo "Running make ${MAKECMDGOALS} in $@"
	@${MAKE} -C $@ ${MAKECMDGOALS}


.PHONY: build_software
build_software: ${SUB_DIRS}
	@echo "Building software in ${CURDIR}"
	@echo "Nothing to build in ${CURDIR}"

.PHONY: build_docs
build_docs: ${SUB_DIRS} books20.pdf


#
# Basic TeX processing
#
books20.pdf: ${TEX_FILES} ${BIB_FILES}
	${LATEX} -draftmode books20
	${BIBER} books20
	${LATEX} -draftmode books20
	${LATEX} books20

#
# Install any software and/or documents
#
.PHONY: install
install: install_software install_docs

.PHONY: install_software
install_software: ${SUB_DIRS}
	@echo "Installing software from ${CURDIR}"
	@echo "Nothing to install from  ${CURDIR}"

.PHONY: install_docs
install_docs: ${SUB_DIRS} build_docs install_pdf

install_pdf: books20.pdf
	@echo "Installing PDF files in ${PDF_INSTALL_DIR}"
	install -m 444 -p ./books20.pdf ${PDF_INSTALL_DIR}
	@echo "Installing PDF files in ${PUBLIC_HTML_DIR}"
	install -m 444 -p ./books20.pdf ${PUBLIC_HTML_DIR}

#
# Other useful stuff
#

#
# lines: count how many lines we have written
#
lines:
	wc ${TEX_FILES} ${BIB_FILES} Makefile

#
# Clean up the mess
#
.PHONY: clean
clean: ${SUB_DIRS} clean_tex
	@echo "Doing clean of ${CURDIR}"
	${RM} -f *~

.PHONY: veryclean
veryclean: ${SUB_DIRS} clean clean_pdf


.PHONY: distclean
distclean: ${SUB_DIRS} veryclean
	@echo "Doing distclean of ${CURDIR}"
	${RM} Makefile Makefile.in

#
# Targets you might want in general
#
.PHONY: install_python
install_python:
	$(PYTHON) setup.py install --prefix=${PYTHON_INSTALL_DIR}


.PHONY: clean_tex
clean_tex:
	${RM} -f *.aux *.bbl *.bcf *.blg *.log *.dvi *.toc *.out *.run.xml

.PHONY: clean_pdf
clean_pdf:
	${RM} -f *.pdf

.PHONY: clean_c
clean_c:
	${RM} -f *.o .a 

.PHONY: clean_python
clean_python:
	${RM} -f *.pyc


#
# End of Makefile
#
