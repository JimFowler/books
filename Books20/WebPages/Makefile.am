#
# Makefile.am
#
#   This makefile contains the instructions for building the
#   webpages for the book "Some Important Books in Astronomy and
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
#   History:
#     21 May 2010 installed Ubuntu 10.04 and my php pages would not load.
#             The php5 distribution no longer allows php scripts in 
#             user directories.  Move my public pages to /var/www/jrf.
#
#

PRINTER = lp -Phome

PUBLICHTML = $(prefix)/public_html
PUBLICWEB = /var/www/jrf

PRIVATEWEB = $(prefix)/private_html

PUBLICWEBPAGES = 20thCentury.php BooksBooks.php ToDoList.php index.html \
	Bibliographies.php BlogLists.php Auction.php robots.txt

PRIVATEFILES = 20thCentury.txt BookMaking.txt BooksOnLine.txt \
	BookStores.txt Collecting.txt HistoryAstronomy.txt \
	HistoryPublishing.txt HistoryReading.txt \
	HomeLibrary.txt Libraries.txt RareBooks.txt References.txt \
	Resources.txt SociologyScience.txt ToDoList.txt Tools.txt \
	BibSources.txt BibTools.txt BibRefs.txt BlogLists.txt Auctions.txt
PRIVATEPHP = phpBooks.inc

SAVFILES = ${PUBLICWEBPAGES} ${PRIVATEFILES} ${PRIVATEPHP}

#
# HTML
#
#  Normally the pages are installed as php scripts and the associated
# private text files. However, on some of my machines, primarily my
# Mac Book, I don't have a web server running. In these cases I install
# the HTML pages and read them as file:///...
#
install_html: install_private install_images
	@echo "Installing HTML pages in ${htmldir}"
	@if [ ! -d ${htmldir} ]; then \
		echo "Making ${htmldir}"; \
		mkdir ${htmldir}; \
	fi
	@if [ ! -d .tmp ]; then \
		mkdir .tmp ; \
	fi
	@for page in ${PUBLICWEBPAGES}; do \
	    if `echo $${page} | grep --silent php`; then \
		basepage=`basename $${page} \.php` ; \
		php $${page}| sed s/php/html/ > ./.tmp/$${basepage}.html ; \
		install -m 0444 -p ./.tmp/$${basepage}.html ${htmldir} ; \
	    else \
		install -m 0444 -p $${page} ${htmldir} ; \
	    fi ; \
	 done
	@rm -rf ./.tmp

#
# Install the pages
#
install: install_private install_public install_images

install_private: ${PRIVATEFILES}
	@echo "Installing private web files"
	@if [ ! -d ${PRIVATEWEB} ]; then \
		echo "Making ${PRIVATEWEB}"; \
		mkdir ${PRIVATEWEB}; \
	fi
	install -m 0444 -p ${PRIVATEFILES} ${PRIVATEWEB}
	install -m 0444 -p ${PRIVATEPHP} ${PRIVATEWEB}

install_public: ${PUBLICWEBPAGES}
	@echo "Installing public web files"
	@if [ ! -d ${htmldir} ]; then \
		echo "Making ${htmldir}"; \
		mkdir ${htmldir}; \
	fi
	install --mode=444 --preserve-timestamps ${PUBLICWEBPAGES} ${htmldir}

install_images:
	@echo "Installing Images"
	@(cd Images; make install)

#
# end of Makefile
#
