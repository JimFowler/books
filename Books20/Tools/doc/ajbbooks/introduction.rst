Introduction
************

Overview
========

The **ajbbooks** program is part of the *Books20* project, which is
designed to catalog books published in Astronomy and Astrophysics
during the 20th Century. **ajbbooks** is designed to ease the
cataloging of entries found in the annual bibliographies
*Astronomischer Jahrsbericht* by providing a graphical interface
that focuses on the information and not on the formatting.  

**ajbbooks** was initially developed in Python 3.2.3 under Ubuntu
12.04 and uses Qt 4.8.1 with PyQt 4.9.1 for the graphical portions of
the software. The latest version (v1.9, Oct 2015) runs in Python 3.4.3
under Ubuntu 14.10 and uses Qt 4.8.6 with PyQt 4.10.4

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

The AJB primarily contains references to journal articles but also
contains references for books, film strips, and other photographic
material.  The *Books20* project is interested in the books. The AAA
has all books listed in section 3 with conference proceedings in
section 12. The folks at ARI were kind enough to package up these
sections and send them to me as electronic text file format so that I
could add them to the *Books20* database. However, in the AJB the
books were listed in the relevant subject section under the authors
name and no such electronic listing was available. Therefore I had to
go through the paper copies of AJB one by one and search out the book
entries by hand.


History
=======

Initial cataloging started with AJB volume 68 in late September of
2010 and was done with Microsoft Word™ using text entry and
comma-separated fields. Microsoft Word™ was chosen because it used the
UTF-8 encoding system so I had access to the special characters used
in foreign languages.  With this method however, there were numerous
problems in keeping the fields in their proper places, particularly
because there was often missing field data in the AJB entries.  Many
passes with Microsoft Excel™ and other testing tools were required to
spot these problems by eye.

**ajbbooks** was written to ease this task.  By creating a form based
graphical interface, I could concentrate on the information and not on
the formatting. I started on 20 July 2012 while finishing AJB volume
60 and had a working version by February 2013. The first test was to
proofread the manual entry file for AJB volume 58.  By March of 2013 I
was satisfied with the program and began converting the ten hand
written files that had already by done.  In each of them I found
additional errors that had not been caught in the previous
proofreading which demonstrated the usefulness of the program.  AJB
volume 57 was the first volume to be completely done with
**ajbbooks**.
