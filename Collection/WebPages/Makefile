#
# Makefile
#
#   This makefile contains the instructions for building the
#   webpages for accessing my book collection
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

PRINTER = lp -Phome

PUBLICWEB = /home/jrf/public_html

PRIVATEWEB = /home/jrf/private_html

PUBLICWEBPAGES = MyCollection.php Collection.css BookView.php AllBooks.php \
		AllAuthors.php AuthorView.php AllProjects.php ProjectView.php

PRIVATEFILES = 

PRIVATEPHP =

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
install: install_private install_public

install_private: ${PRIVATEFILES}
	@echo "Installing private web files"
	@if [ ! -d ${PRIVATEWEB} ]; then \
		echo "Making ${PRIVATEWEB}"; \
		mkdir ${PRIVATEWEB}; \
	fi
	install --mode=444 --preserve-timestamps ${PRIVATEFILES} ${PRIVATEWEB}
#	install --mode=444 --preserve-timestamps ${PRIVATEPHP} ${PRIVATEWEB}

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
