# Begin copyright
#
#  /home/jrf/Documents/books/Books20/WebPages/Makefile.am
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
SUB_DIRS = Images

# Installation files to go in those directories
PUBLICWEBPAGES = 20thCentury.php BooksBooks.php ToDoList.php index.html \
	Bibliographies.php BlogLists.php Auction.php BookBinding.php \
	Writing.php SemanticWeb.php DigitalHum.php robots.txt

PRIVATEFILES = 20thCentury.txt BookMaking.txt BooksOnLine.txt \
	BookStores.txt Collecting.txt HistoryAstronomy.txt \
	HistoryPublishing.txt HistoryReading.txt \
	HomeLibrary.txt Libraries.txt RareBooks.txt References.txt \
	Resources.txt SociologyScience.txt ToDoList.txt Tools.txt \
	BibSources.txt BibTools.txt BibRefs.txt BlogLists.txt Auctions.txt \
	BookBinding.txt Writing.txt SemanticWeb.txt DigitalHum.txt
PRIVATEPHP = phpBooks.inc

SAVFILES = ${PUBLICWEBPAGES} ${PRIVATEFILES} ${PRIVATEPHP}

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
build_docs: ${SUB_DIRS} html


#
# HTML
#
#  Normally the pages are installed as php scripts and the associated
# private text files. However, on some of my machines, primarily my
# Mac Book, I don't have a web server running. In these cases I install
# the HTML pages and read them as file:///...
#
.PHONY: html
html:
	@echo "Creating HTML web pages"
	@mkdir -p ./html
	@for page in ${PUBLICWEBPAGES}; do \
	    if `echo $${page} | grep --silent php`; then \
		basepage=`basename $${page} \.php` ; \
		php $${page} | sed s/php/html/ > ./html/$${basepage}.html ; \
	    else \
		cp $${page} ./html ; \
	    fi ; \
	done

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
install_docs: ${SUB_DIRS} install_html install_private install_public


.PHONY: install_html
install_html: html
	@echo "Installing HTML pages in ${PUBLIC_HTML_DIR}"
	@if [ ! -d ${PUBLIC_HTML_DIR} ]; then \
		echo "Making ${PUBLIC_HTML_DIR}"; \
		mkdir ${PUBLIC_HTML_DIR}; \
	fi
	install --mode=0444 --preserve-timestamps --target-directory=${PUBLIC_HTML_DIR} ./html/*

.PHONY: install_private
install_private: ${PRIVATEFILES}
	@echo "Installing private web files"
	@if [ ! -d ${PRIVATE_HTML_DIR} ]; then \
		echo "Making ${PRIVATE_HTML_DIR}"; \
		mkdir ${PRIVATE_HTML_DIR}; \
	fi
	install -m 0444 -p ${PRIVATEFILES} ${PRIVATE_HTML_DIR}
	install -m 0444 -p ${PRIVATEPHP} ${PRIVATE_HTML_DIR}

.PHONY: install_public
install_public: ${PUBLICWEBPAGES}
	@echo "Installing public web files"
	@if [ ! -d ${PUBLIC_HTML_DIR} ]; then \
		echo "Making ${PUBLIC_HTML_DIR}"; \
		mkdir ${PUBLIC_HTML_DIR}; \
	fi
	install --mode=444 --preserve-timestamps ${PUBLICWEBPAGES} ${PUBLIC_HTML_DIR}

#
# Clean up the mess
#
.PHONY: clean
clean: ${SUB_DIRS}
	@echo "Doing clean of ${CURDIR}"
	${RM} -f *~

.PHONY: veryclean
veryclean: ${SUB_DIRS} clean 
	${RM} -rf ./html

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
