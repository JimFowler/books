#
# Makefile
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
#
#   The last known changes were checked in by $Author$
#   in revision $LastChangedRevision$
#   on $Date$
#
#   History:
#     21 May 2010 installed Ubuntu 10.04 and my php pages would not load.
#             The php5 distribution no longer allows php scripts in 
#             user directories.  Move my public pages to /var/www/jrf.
#
#

PRINTER = lp -Phome

#PUBLICWEB = /home/jrf/public_html
PUBLICWEB = /var/www/jrf

PRIVATEWEB = /home/jrf/private_html

PUBLICWEBPAGES = 20thCentury.php BooksBooks.php ToDoList.php index.html \
	Bibliographies.php BlogLists.php robots.txt

PRIVATEFILES = 20thCentury.txt BookMaking.txt BooksOnLine.txt \
	BookStores.txt Collecting.txt HistoryAstronomy.txt \
	HistoryPublishing.txt HistoryReading.txt \
	HomeLibrary.txt Libraries.txt RareBooks.txt References.txt \
	Resources.txt SociologyScience.txt ToDoList.txt Tools.txt \
	BibSources.txt BibTools.txt BibRefs.txt BlogLists.txt

PRIVATEPHP = phpBooks.inc

SAVFILES = ${PUBLICWEBPAGES} ${PRIVATEFILES} ${PRIVATEPHP}

default:
	@echo "Make options:"
	@echo "    install: copy the files to the web directory,"
	@echo "    veryclean: clean up the directory of uneccessary files,"
	@echo "    svn: archive important files in subversion,"
	@echo "    backuptar: create webpages.tgz,"
	@echo "    eod: end of day, clean up and create tar file."
	@echo ""


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
	install --mode=444 --preserve-timestamps ${PRIVATEFILES} ${PRIVATEWEB}
	install --mode=444 --preserve-timestamps ${PRIVATEPHP} ${PRIVATEWEB}

install_public: ${PUBLICWEBPAGES}
	@echo "Installing public web files"
	@if [ ! -d ${PUBLICWEB} ]; then \
		echo "Making ${PUBLICWEB}"; \
		mkdir ${PUBLICWEB}; \
	fi
	install --mode=444 --preserve-timestamps ${PUBLICWEBPAGES} ${PUBLICWEB}

install_images:
	@echo "Installing Images"
	@(cd Images; make install)

#
# Archive in svn
#
svn:
	@echo "svn routines for books20 are not defined yet"

addprop:
	svn propset svn:keywords "Data Author Revision"  ${PUBLICWEBPAGES} ${PRIVATEFILES} ${PRIVATEPHP}

#
# Backup routines
#
backuptar: backupdate
	tar -zcf webpages.tgz ${SAVFILES}

backupdate:
	date > backup.date

#
# clean up the mess
#
veryclean:
	rm -f  *~ core


#
# End of Day stuff.  Clean up messy files. Make backups
#
eod: veryclean backuptar

#
# end of Makefile
#
