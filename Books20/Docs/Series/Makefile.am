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

BUILT_TABLE_FILES = springerASSLtable.tex springerAALtable.tex cambCAPStable.tex
TABLE_FILES = 
SERIES_TEX_FILES = series.tex intro.tex other.tex \
	harvard.tex uchicago.tex uarizona.tex springer.tex \
	cambridge.tex

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
build_docs: ${SUB_DIRS} series.pdf


series.pdf: ${BUILT_TABLE_FILES} ${TABLE_FILES} ${SERIES_TEX_FILES}
	${LATEX} -draftmode series
	${BIBER} series
	${LATEX} -draftmode series
	${LATEX} series

springerASSLtable.tex: springer_assl_table.py
	python springer_assl_table.py > springerASSLtable.tex

springerAALtable.tex: springer_aal_table.py
	python springer_aal_table.py > springerAALtable.tex

cambCAPStable.tex: camb_caps.py
	python camb_caps.py > cambCAPStable.tex

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
	install -m 444 -p ./series.pdf ${PDF_INSTALL_DIR}

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
