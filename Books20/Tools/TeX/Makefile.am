# Begin copyright
#
#  /home/jrf/Documents/books/Books20/Tools/TeX/Makefile.am
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
#   All Makefiles should have these targets at a minimum. The targets
#   don't need to do anything but `make` should not generate an error
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

LATEX_STYLE_INSTALL_FILES = books20.sty

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
build_docs: ${SUB_DIRS} test_sty.pdf

#
# Basic TeX processing
#
test_sty.pdf: test_sty.tex
	${LATEX} -draftmode test_sty
	${BIBER} test_sty
	${LATEX} -draftmode test_sty
	${LATEX} test_sty

#
# Install any software and/or documents
#
.PHONY: install
install: install_software install_docs

.PHONY: install_software
install_software: ${SUB_DIRS} build_software install_tex

.PHONY: install_docs
install_docs: ${SUB_DIRS} build_docs install_pdf

.PHONY: install_text
install_tex: 
	install -m 444 ${LATEX_STYLE_INSTALL_FILES} ${LATEX_STYLE_DIR}

.PHONY: install_pdf
install_pdf: test_sty.pdf
	install -m 444 test_sty.pdf ${PDF_INSTALL_DIR}

#
# Clean up the mess
#
.PHONY: clean
clean: ${SUB_DIRS}
	@echo "Doing clean of ${CURDIR}"
	${RM} -f *~

.PHONY: veryclean
veryclean: ${SUB_DIRS} clean clean_tex clean_pdf
	@echo "Doing veryclean of ${CURDIR}"

.PHONY: distclean
distclean: ${SUB_DIRS} veryclean
	@echo "Doing distclean of ${CURDIR}"
	${RM} Makefile Makefile.in


#
# lines: count how many lines we have written
#
lines:
	wc ${TEX_INSTALLFILES}

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
