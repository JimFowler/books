# Begin copyright
#
#  /home/jrf/Documents/books/Books20/Docs/Series/Makefile.am
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

BUILT_TABLE_FILES =  STtable.tex
JOURNAL_TABLE_FILES =
JOURNAL_TEX_FILES = journals.tex skytel.tex fbc.tex

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
build_docs: ${SUB_DIRS} journals.pdf

journals.pdf: ${JOURNAL_FILES} ${BUILT_TABLE_FILES}
	${LATEX} -draftmode journals
	${BIBER} journals
	${LATEX} -draftmode journals
	${LATEX} journals

STtable.tex: skytel_table.py
	python skytel_table.py > STtable.tex

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

install_pdf:
	@echo "Installing PDF files in ${PDF_INSTALL_DIR}"
	install -m 444 -p ./journals.pdf ${PDF_INSTALL_DIR}

#
# Other useful stuff
#

#
# lines: count how many lines we have written
#
lines:
	wc ${SERIES_TEX_FILES} ${BIB_FILES} Makefile


#
# Clean up the mess
#
.PHONY: clean
clean: ${SUB_DIRS} clean_tex
	@echo "Doing clean of ${CURDIR}"
	${RM} -f *~

.PHONY: veryclean
veryclean: ${SUB_DIRS} clean clean_pdf
	${RM} -rf __pycache__

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
	${RM} -f *.aux *.bbl *.bcf *.blg *.log *.lot *.dvi *.toc *.out *.run.xml
	${RM} -f ${BUILT_TABLE_FILES}

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
