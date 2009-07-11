#
# Makefile
#
#   This makefile contains the instructions for building the
#   building the stuff for the book "Some Important Books in Astronomy and
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

PRINTER = lp -Phome

PUBLICWEB = /home/jrf/public_html

PRIVATEWEB = /home/jrf/private_html

SUBDIRS = Data Docs Manuscript Scripts WebPages

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
install:
	@echo "install routines for Books20 are not defined yet"

#
# Archive in svn
#
svn:
	@echo "svn routines for Books20 are not defined yet"


#
# Backup routines
#
backuptar: backupdate
	tar -zcf ../Books20.tgz .

backupdate:
	date > backup.date

#
# clean up the mess
#
veryclean:
	rm -f  backup.date *~ core
	@for sdir in ${SUBDIRS} ; do \
		echo "Making veryclean in $$sdir"; \
		(cd $$sdir; make veryclean);\
	done


#
# End of Day stuff.  Clean up messy files. Make backups
#
eod: veryclean backuptar

#
# end of Makefile
#
