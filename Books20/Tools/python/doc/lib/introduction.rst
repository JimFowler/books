..  Begin copyright
.. 
..   /home/jrf/Documents/books/Books20/Tools/python/doc/lib/introduction.rst
..   
..    Part of the Books20 Project
.. 
..    Copyright 2020 James R. Fowler
.. 
..    All rights reserved. No part of this publication may be
..    reproduced, stored in a retrieval system, or transmitted
..    in any form or by any means, electronic, mechanical,
..    photocopying, recording, or otherwise, without prior written
..    permission of the author.
.. 
.. 
..  End copyright


Introduction
************

Overview
========

The **aabooks.lib** module is part of the **aabooks** python module in
the *Books20* project. The project is designed to catalog books
published in Astronomy and Astrophysics during the 20th
Century. **aabooks.lib** contains the common python files used
by the various programs in the project

**aabooks.lib** was initially developed in 2018 Python 3.5 under Ubuntu 18.04.
It currently runs under Python 3.7.

The *Astronomischer Jahrsbericht* (AJB) is an annual publication which
indexes all publications in Astronomy and Astrophysics for the
previous year. It was published between 1900 and 1968 (index years
1899-1967) by the Astronomischen Rechen-Institut (ARI) in Heidelberg,
Germany. The publication language was German. However, AJB cataloged
items from all over the world, so numerous languages are represented
in the entries.

The AJB was superseded in 1969 by *Astronomy and Astrophysics
Abstracts* (AAA) also published by ARI.  The AAA was published in
English, as English had become the dominant language in Astronomy
after World War Two, and was published until 2000 when the online
versions became the dominant mechanism for literature searches.


History
=======

Initial cataloging of books was started with the AJB volumes in late
September of 2010 using the **bookentry** program, later renamed as
**ajbooks**. In 2016 work was started on the **journal** program
to capture information about the journals that held reviews of the
books.  There were many files that were common to both programs and at
first the were loaded from the module ajbbooks. This quickly became a
nuisance and in 2018 these files were split into **aabook.lib**,
**aabook.ajbbook**, and **aabook.journal**.
