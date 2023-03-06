# Begin copyright
#
#  /home/jrf/Documents/books/Books20/Tools/build/Makefile.am
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
build_software: ${SUB_DIRS}
	@echo "Building software in ${CURDIR}"
	@echo "Nothing to build in ${CURDIR}"

.PHONY: build_docs
build_docs: ${SUB_DIRS} hjs_catalogue.pdf

.PHONY: hjs_catalogue.pdf
hjs_catalogue.pdf catalogue hjs: hjs_catalogue.tex biography.tex library.tex
	books.tex hjs.bib hjs_baas_obit.bib
	inventory94.tex author.ind
	${LATEX} -draftmode hjs_catalogue
	${BIBER} hjs_catalogue
	${LATEX} -draftmode hjs_catalogue
	${LATEX} hjs_catalogue

.PHONY: author.ind
author.ind: author.index
	cp author.index author.ind

.PHONY: the_books.tex
the_books.tex: ../../Data/HJS/hjs_full.xml catalogue_xml.py
	python catalogue_xml.py -s Year -o the_books.tex ../../Data/HJS/hjs_full.xml

.PHONY: test_hjs.pdf
test_hjs.pdf: test_books.tex test_hjs.tex
	${LATEX} -draftmode test_hjs.tex
	${LATEX} -draftmode test_hjs.tex
	${LATEX} test_hjs.tex

.PHONY: test_books.tex
test_books.tex: cat_entry.py
	python test_hjs.py

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
install_docs: ${SUB_DIRS}
	@echo "Installing docs from ${CURDIR}"
	@echo "Nothing to install from  ${CURDIR}"


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
	${RM} -f books.tex test_books.tex test_hjs.pdf

.PHONY: distclean
distclean: ${SUB_DIRS}
	@echo "Doing distclean of ${CURDIR}"
	${RM} -f Makefile Makefile.in

#
# Targets you might want in general
#
.PHONY: install_python
install_python:
	$(PYTHON) setup.py install --prefix=${PYTHON_INSTALL_DIR}


.PHONY: clean_tex
clean_tex:
	${RM} -f *.aux *.bbl *.bcf *.blg *.idx *.ilg *.ind *.log *.dvi *.toc *.out *.run.xml

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
