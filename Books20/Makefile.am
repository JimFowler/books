# Begin copyright
#
#  /home/jrf/Documents/books/Books20/Makefile.am
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
# The top level make file for the Books20 Project
#

#
# Define and export the base directory
#
BOOKS20_ROOT ?= ${CURDIR}
export BOOKS20_ROOT

#
# Include local definitions
#
include ${BOOKS20_ROOT}/makefile.local

#
# Run make in these sub-directories
#
SUB_DIRS = Docs Tools Manuscript  WebPages

#
# Build any software and/or documents
#
all: build_software build_docs

.PHONY: local_vars
local_vars:
	@echo 'These are the local variable defined in makefile.local'
	@echo '      which points to makefile.${LOCAL_HOST}'
	@echo
	@echo '  prefix = ${prefix}'
	@echo '  BOOKS20_ROOT = ${BOOKS20_ROOT}'
	@echo '  BOOKS20_DIR = ${BOOKS20_DIR}'
	@echo '  EMACS_ELISP_DIR = ${EMACS_ELISP_DIR}'
	@echo '  EMACS_FILE_DIR = ${EMACS_FILE_DIR}'
	@echo '  PYTHON_INSTALL_DIR = ${PYTHON_INSTALL_DIR}'
	@echo '  TEX = ${TEX}'
	@echo '  BIBTEX= ${BIBTEX}'
	@echo '  LATEX = ${LATEX}'
	@echo '  BIBER = ${BIBER}'
	@echo '  LATEX_STYLE_DIR = ${LATEX_STYLE_DIR}'
	@echo '  PDF_INSTALL_DIR = ${PDF_INSTALL_DIR}'
	@echo '  PRIVATE_HTML_DIR = ${PRIVATE_HTML_DIR}'
	@echo '  PUBLIC_HTML_DIR = ${PUBLIC_HTML_DIR}'
	@echo '  PUBLIC_IMAGE_DIR = ${PUBLIC_IMAGE_DIR}'


.PHONY: ${SUB_DIRS}
${SUB_DIRS} :
	@echo "Running make ${MAKECMDGOALS} in $@"
	@${MAKE} -C $@ ${MAKECMDGOALS}


.PHONY: build_software
build_software: ${SUB_DIRS}
	@echo "Building software in ${CURDIR}"
	@echo "Nothing to build in ${CURDIR}"

.PHONY: build_docs
build_docs: ${SUB_DIRS}
	@echo "Building docs in ${CURDIR}"
	@echo "Nothing to build in ${CURDIR}"

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

.PHONY: distclean
distclean: ${SUB_DIRS}
	@echo "Doing distclean of ${CURDIR}"
	${RM} Makefile Makefile.in config.* configure 

#
# End of Makefile
#
