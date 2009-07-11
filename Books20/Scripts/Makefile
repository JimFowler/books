#
# Makefile
#
#   This makefile contains the instructions for building the
#   scripts for the book "Some Important Books in Astronomy and
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

TEX    = pdftex
LATEX  = pdflatex
BIBTEX = bibtex

PRINTER = lp -Phome

SAVFILES = backup.date InitialSetup.sql CreateTables.sql DeleteTables.sql \
	   Rebuild.sql arabib.pl Makefile

default:
	@echo "Make options:"
	@echo "    veryclean: clean up the directory of uneccessary files,"
	@echo "    svn: archive important files in subversion,"
	@echo "    backuptar: create scripts.tgz,"
	@echo "    eod: end of day, clean up and create tar file."
	@echo ""



#
# Archive in svn
#
svn:
	@echo "svn routines for books20 are not defined yet"


#
# Backup routines
#
backuptar: backupdate
	tar -zcf scripts.tgz ${SAVFILES}

backupdate:
	date > backup.date

veryclean:
	rm -f  *~ core


#
# End of Day stuff.  Clean up messy files. Make backups
#
eod: veryclean backuptar
