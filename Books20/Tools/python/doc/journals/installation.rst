..  Begin copyright
.. 
..   /home/jrf/Documents/books/Books20/Tools/python/doc/journals/installation.rst
..   
..    Part of the Books20 Project
.. 
..    Copyright 2016 James R. Fowler
.. 
..    All rights reserved. No part of this publication may be
..    reproduced, stored in a retrival system, or transmitted
..    in any form or by any means, electronic, mechanical,
..    photocopying, recording, or otherwise, without prior written
..    permission of the author.
.. 
.. 
..  End copyright


Installation
************

Installing
==========

BookEntry uses the python library *distutils* to install and
distribute the packages. More documentation about the installation
program can be found by running the command

``pydoc distutils.core.setup``

The BookEntry package may be installed from
the Tools directory with the command

``python3 setup.py install``

My default is to install all the packages required for BookEntry in my
home directory so I use

``python3 setup.py install --home=~``

Or you can install in a different system directory with

``python3 setup.py install --prefix=<dirname>``

You may need superuser privileges to install in system directories.

If you install in a non-standard directory, then you will need to
set the environment variables **PYTHONPATH**. I put the following in
my ``.bashrc`` file.

``export PYTHONPATH=/home/jrf/lib/python3.4/site-packages``

But if you use a variant of csh, then you could put the following
in your ``.cshrc`` file.

``setenv PYTHONPATH /home/jrf/lib/python3.4/site-packages``


Building and Installing the Documentation
=========================================

The documentation can be found in ./Tools/doc. It is written using
Sphinx version 1.2.2 (cf. `sphinx-doc.org
<http://sphinx-doc.org/>`_). Output formats may be HTML, LaTeX, pdf,
postscript, epub, or other formats.  I primarily use pdf and HTML.
(Making the pdf version requires that ``pdflatex`` be installed.)  You
can run ``make help`` to see what other formats are available.

To build the HTML and pdf documentation in the **doc** directory, run
the command

``make latexpdf html``

To install these files, run the commands

``mv _build/html/* <htmldir>``

``mv _build/latex/Journals.pdf <pdfdir>``



