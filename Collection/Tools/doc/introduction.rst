Introduction
************

Overview
========

The **library** program is part of my *Collection* project, which is
designed to catalog books in my private library into an SQLite3
database.  **library** is designed to ease the cataloging of entries.

Since **library** is designed for my private collection it is not
quite like the old card catalogs of yore nor is it like a modern data
library database. Rather than using primary search terms like Title,
Author, and Subject, **library** can search on Title, Author,
Vendor/Publisher, or Collection.  Note that Vendor/Publisher are combined.
I buy books directly from publishers and there are book dealers who also
publish books, Oak Knoll Books being a prime example.

**library** was initially developed in Python 3.4.3 under Ubuntu 14.04
and uses Qt 4.8.6 with PyQt 4.10.4 for the graphical portions of the
software. The latest version (v1.0, Nov 2015) runs in Python 3.4.3
under Ubuntu 14.04 and uses Qt 4.8.6 with PyQt 4.10.4


History
=======

The original database was created in 1998 using Microsoft Access 97
and was later upgraded to Access 2000 and eventually to
Access 2013. The Access database was not well designed as it was only
the second databases I had ever created.  Porting the data to SQLite3
was an exercise in programming and an attempt to improve the
database.  The first version of **library** maintains the
original features available in the Access database with some clean up.
The Wants table was also split out of the Books table to provide
for unqiue BookId values.
