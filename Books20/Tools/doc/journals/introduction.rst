Introduction
************

Overview
========

The **journal** program is part of the *Books20* project, which is
designed to catalog books published in Astronomy and Astrophysics
during the 20th Century. **journal** is designed to ease the
cataloging of journalentries found in the annual bibliographies
*Astronomischer Jahrsbericht* by providing a graphical interface that
focuses on the information and not on the formatting.

**journal** was initially developed in Python 3.4.3 under Ubuntu 14.04
and uses Qt 4.8.6 with PyQt 4.10.4 for the graphical portions of the
software.

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

The AJB volumes contain a list of the journals reviewed for that
particular volume and year. The *Books20* needs references to these
journals so that the book reviews may be linked more information about
the journal


History
=======

Although initial cataloging of books was started with AJB volume 68 in
late September of 2010, I did not have a need for the journal entries
until 2016 when I began thinking about the final database. I had
already written **ajbbooks** and was working on version 2.0 of that
program using XML as the output format.  I was also beginning to work
on the SQLlite version of my library collection.  These factors
motivated me to add the **journals** programs to my toolbox.
