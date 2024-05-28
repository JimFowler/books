#
# ${LATEX} is undefined
# ${TEX} is tex
#

#
# General conventions described in GNU Make manual
#

SHELL = /bin/sh

prefix = ~
#
# Local variables that need unique defintions for
# different machines. These should be in makefile.local
#
LATEX ?= pdflatex
BIBTEX ?= biber

#
# Installation locations
#
# (This rather assumes I am installing in a home directory)
#
#
# create the directories if they don't exist.
#  mkdir -p will work but is GNU specific and
# may not be available on all machines.
#

#
# location of LaTeX *.sty files or packages
#
INSTALL_STYLE_FILES = yes
TEX_INSTALL_DIR ?= $(prefix)/texmf/tex/latex/books20

#
# Location for emacs elisp files. This must be somewhere in the
# load-path for your version of emacs. If you don't use emacs,
# then you don't need this.  Should have a INSTALL_ELISP variable
# to test against.
#
INSTALL_ELISP = yes
ELISP_INSTALL_DIR = $(prefix)/Emacs

#
# Location where *.pdf files can be moved to
#
PDF_INSTALL_DIR = ../../PDF


#
# If this is uncommented, then make will not
# echo any commands
#
.SILENT:

.PHONY: all
all: 
	echo 'SHELL is ' ${SHELL}
	echo 'LaTeX is ' ${LATEX}
	echo 'TeX is ' ${TEX}

#
# Do I need generic targets for this
# or will doc: work?
#
pdf:
html:

install: install-elisp

ifeq ($(INSTALL_ELISP), yes)
install-elisp:
	echo 'Installing elisp files from local makefile to ${ELISP_INSTALL_DIR}'
else
install-elisp:
	echo 'empty install-elisp target should be defined in global file'
endif

install-html:
install-pdf:

uninstall:

clean:

veryclean:
distclean:

