Introduction
************

The **ajbbooks** program is part of the *Books20* project, which is
designed to catalog books published in Astronomy and Astrophysics
during the 20th Century. **ajbbooks** is designed to ease the
cataloging of entries found in the annual bibliographies
*Astronomischer Jahrsbericht* by providing a graphical interface
that focuses on the information and not on the formatting.  Previous
cataloging was done with Microsoft Word™ using text entry and
comma-separated fields.  With this method however, there were numerous
problems in keeping the fields in the proper place particularly
because there was often missing field data in the AJB entries.  Many
passes with Microsoft Excel™ and other testing tools were required
to spot these problems by eye.

**ajbbooks** was developed in Python 3.2.3 under Ubuntu 12.04 and uses
Qt 4.8.1 with PyQt 4.9.1 for the graphical portions of the software.

Overview
________

The *Astronomischer Jahrsbericht* (AJB) is an annual publication which
indexes all publications in Astronomy and Astrophysics for the
previous year. It was published between 1900 and 1968 (index years
1899-1967) by the Astronomischen Rechen-Institut (ARI) in Heidelberg,
Germany. The publication language was German. The AJB was superseded
in 1969 by *Astronomy and Astrophysics Abstracts* (AAA) also published
by ARI.  The AAA was published in English, as English had become the
dominant language in Astronomy after World War Two, and was published
until 2000 when the online versions became the dominant mechanism for
literature searches.

The AJB contains references mostly of journal articles but also
contains references for books, film strips, and other photographic
material.  The *Books20* project is primarily interested in the
books. The AAA has all books listed in section 3 with conference
proceedings in section 12. The folks at ARI were kind enough to
package up these sections and send them to me in electronic form as
text files so that I could add them to the *Books20*
database. However, in the AJB the books were listed in the relevant
subject section under the authors name and no such electronic listing
was available. Therefore I had to go through the paper copies one by
one and search out the book entries by hand.
