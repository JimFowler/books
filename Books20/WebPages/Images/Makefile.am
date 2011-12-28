#
# Makefile.am
#
#   This makefile contains the instructions for working with the
#   webpages images for the book "Some Important Books in Astronomy and
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
PUBLICIMAGES = bookrow.jpg

PUBLICWEB = $(prefix)/public_html

install: install_images

install_images: ${PUBLICIMAGES}
	@if [ ! -d ${PUBLICWEB}/Images ]; then \
		echo "Making ${PUBLICWEB}/Images"; \
		mkdir ${PUBLICWEB}/Images; \
	fi
	install --mode=444 --preserve-timestamps ${PUBLICIMAGES} ${PUBLICWEB}/Images

#
# end of Makefile
#

