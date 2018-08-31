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
2010 and was done with Microsoft Word™ using plain-text entry and
comma-separated fields. Microsoft Word™ was chosen because it used the
UTF-8 encoding system so I had access to the special characters used
in foreign languages.  With this method however, there were numerous
problems in keeping the fields in their proper places, particularly
because there was often missing field data in the AJB entries.  Many
passes with Microsoft Excel™ and other testing tools were required to
spot these problems by eye.

The decision to start with volume 68 and work my way back to volume
one was made to ease the task of reading the German language text.
Volume 68 had many English titles and authors while volume one had
primarily German titles. This decision has turned out to be good
overall and has made the task of cataloging much easier.

**ajbbooks** was written to ease this task.  By creating a form-based
graphical interface, I could concentrate on the information and not on
the formatting. Coding started on 20 July 2012 while finishing AJB
volume 60 and I had a working version (v1.0) by February 2013. The
early code was written to support Python 2.7 and Qt 4.7 but this was
quickly adapted to Python 3.x. The first test was to proofread the
manual entry file for AJB volume 58.  By March of 2013 (v1.1) I was
satisfied with the program and began converting the ten plain-text
files that had already by done.  In each of them I found additional
errors that had not been caught in the previous proofreading, which
demonstrated the usefulness of the program.  AJB volume 57 was the
first volume to be completely done with **ajbbooks**.

Most of the minor versions of v1.x fixed problems with the internal
code or were cosmetic.  No new features were added though a number of
features which were not working in v1.0 were completed in later minor
revisions. **ajbbooks** v1.x also used the BookFileTxt format, a
comma-separated string of fields, as the external file format.  This
format utilized fixed-format to defined common items in an AJB entry
as well as a complicated regular expression format for a Comments
section to accomodate unusual information or common fields that we
neglected in the first definition of the BookFileTxt format.

However, this fixed-format style was very limiting as additional types
of information were found in the earlier volumes that did not occur in
the later volumes. In addition, the fixed-format style did not allow
for easy incorporation of information that was previously neglected in
the later volumes.

For this reason v2.0 incorporated a new XML based version of the
external file format called BookFileXml. Version 2.0 was also written
to support Python 3.5 and Qt 5.3. The XML format allowed the addition
of new fields and sub-fields.  Note, however, that the BookFileXml is
an extension of the BookFileTxt format in that it contains additional
information which is not available in BookFileTxt. So while it was easy
to convert BookFileTxt entries to BookFileXml, the additional information
available in the BookFileXml format did not have a counter-part in the
BookFileTxt entries.  Thus it is not always possible to go from
BooKFileXML to BookFileTxt entries. For this reason the use of the
BookFileTxt format for the external file will be dropped in a future
version.

The table of labeled versions is given below.

=================== ==== =========================================
Date                Ver. Comment
=================== ==== =========================================
2013-01-26 12:34:52 v0.1 Really got bookfile working this time
2013-02-11 18:51:55 v1.0 Full working version
2013-03-16 15:53:39 v1.1 Default symbols.txt file now available
2013-03-19 18:45:26 v1.2 Insert Entry button working
2013-05-09 19:00:13 v1.5 Split makeNamelist() and makeNameStr()
2013-10-20 20:38:01 v1.6 Added resources and program icon
2014-01-11 18:49:21 v1.7 Added version flag to ajbbooks
2016-01-16 13:10:36 v1.9 Completed version 1 documentation
=================== ==== =========================================

