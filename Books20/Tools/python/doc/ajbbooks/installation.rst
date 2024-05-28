..  Begin copyright
.. 
..   /home/jrf/Documents/books/Books20/Tools/python/doc/ajbbooks/installation.rst
..   
..    Part of the Books20 Project
.. 
..    Copyright 2012 James R. Fowler
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

Books20 uses the python tool *pip* to install and
distribute the packages. More documentation about the installation
program can be found by running the command

``pip help``

The Books20 package may be installed from
the Tools directory with the command

``pip install -v``

The project currently uses the Anaconda 3 python package
so I currently use the command,

``pip install --prefix=<dirname> .``

This will install in my version of python located in
/home/jrf/anaconda3

You may need superuser privileges to install in system directories.

If you install in a non-standard directory, then you will need to
set the environment variables **PYTHONPATH**. I put the following in
my ``.bashrc`` file.

``export PYTHONPATH=/home/jrf/lib/python3.5/site-packages``

But if you use a variant of csh, then you could put the following
in your ``.cshrc`` file.

``setenv PYTHONPATH /home/jrf/lib/python3.5/site-packages``

Anaconda now automatically adds the relevant lines to your ``.bashrc``
file so there is no need to do this unless you install in a different
location.

Building and Installing the Documentation
=========================================

The documentation can be found in ./Tools/python/doc. It is first
written using Sphinx version 1.2.2 and is now building under Sphinx
version 7.3.7 as of May 2024 (cf. `sphinx-doc.org
<http://sphinx-doc.org/>`_). Output formats may be HTML, LaTeX, pdf,
postscript, epub, or other formats.  I primarily use pdf and HTML.
(Making the pdf version requires that ``pdflatex`` be installed.)  You
can run ``make help`` to see what other formats are available.

To build the HTML and pdf documentation in the **doc** directory, run
the command

``make latexpdf html``

To install these files, run the commands

``mv _build/html/* <htmldir>``

``mv _build/latex/AJBbooks.pdf <pdfdir>``



