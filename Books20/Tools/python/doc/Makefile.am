# Begin copyright
#
#  /home/jrf/Documents/books/Books20/Tools/python/doc/Makefile.am
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

#
# Build any software and/or documents
#
all: build_software build_docs

.PHONY: ${SUB_DIRS}
${SUB_DIRS} :
	@echo "Running make ${MAKECMDGOALS} in $@"
	@${MAKE} -C $@ ${MAKECMDGOALS}


.PHONY: build_software
build_software:
	@echo "Building software in ${CURDIR}"
	@echo "Nothing to build in ${CURDIR}"

.PHONY: build_docs
build_docs: ajbbooks journals
	@echo "Can't build latexpdf docs in Tools/python/doc!"

.PHONY: ajbbooks
ajbbooks:
	${MAKE} -C ajbbooks html
#	${MAKE} -C ajbbooks latexpdf

.PHONY: journals
journals:
	${MAKE} -C journals html
#	${MAKE} -C journals latexpdf


#
# Install any software and/or documents
#
.PHONY: install
install: install_software install_docs

.PHONY: install_software
install_software:
	@echo "Installing software from ${CURDIR}"
	@echo "Nothing to install from  ${CURDIR}"

.PHONY: install_docs
install_docs: build_docs
	@echo "Can't install HTML docs in Tools/python/doc!"

.PHONY: dummy
dummy:
	${INSTALL} -m 444 -p ./ajbbooks/_build/latex/AJBbooks.pdf ${PDF_INSTALL_DIR}
	${INSTALL} -m 444 -p ./ajbbooks/_build/latex/AJBbooks.pdf ${PUBLIC_HTML_DIR_DIR}/ajbbooks
	${INSTALL} -m 444 -p ./journals/_build/latex/Journals.pdf ${PDF_INSTALL_DIR}
	${INSTALL} -m 444 -p ./journals/_build/latex/Journal.pdf ${PUBLIC_HTML_DIR_DIR}
# install HTML web pages for ajbbooks and journals


#
# Clean up the mess
#
.PHONY: clean
clean: ${SUB_DIRS}
	@echo "Doing clean of ${CURDIR}"
	${RM} -f *~

.PHONY: veryclean
veryclean: ${SUB_DIRS}
	@echo "Doing veryclean of ${CURDIR}"
	@echo "Nothing to do for veryclean in ${CURDIR}"

.PHONY: distclean
distclean: ${SUB_DIRS}
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
