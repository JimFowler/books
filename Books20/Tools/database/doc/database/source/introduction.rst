Introduction
************

At the beginning of the project I wrote a note about Database Design.
This was a simple document created without a lot of thought and
it does not explain a lot of detail about what might be needed in
a database for the project.  I have learned a little bit more in the
intervening years; this document is the result.


SQL or noSQL
============

Should we use an SQL or a noSQL database?  Choices would most likely
be between SQLite or mondoDB.  I like the SQL databases for the formal
orgainization that they provide. The noSQL database provides the
ability to add new columns or data to the system with out having the
rebuild the database.  As a general rule different Database Management
Systems (DBMS) work well for specific classes of problem. Some are
best for low volume transactions, while some are excellent for high
volume transactions rates.

My criteria for selecting a DBMS include cost, ease of use, access to
python bindings, and ...

One idea, suggested by Neo4j, is that some companies have multiple
database types.  A relationaly database for tabular data and a graph
database for relationship type data.  This may be an option


SQL
___

SQL database systems, e.g. mySQL or SQLite, are relational databases.
The basic objects are tables and records which define relationship
between tables through foreign keys.  A well defined and very mature
language, SQL, is used to access these tables and records independent
of how the data is organized on the storage system. However, SQL can
be difficult to work with if there are multiple tables that require
multiple joings

SQLite3
_______

The system I am considering, SQLite, works well for low volume, low
transaction rate databases. I expect the books database to contain no
more than 30,000 books, some 20,000 authors and publishers, and 400
journals.  This is very small compared with the HET which uses SQLite
for the nightly logs. These databases contain some 6 million events
and 16 million attributes entries which are generatated at a rate of
60-100 events per second


noSQL
=====

Graph Databases
_______________

The Carnegie Mellon University Database Group has their `class
lectures <https://www.youtube.com/channel/UCHnBsf2rH-K7pn09rb3qvkA>`_
about database systems on YouTube. Since April 2020 they have been
running a series called Quarantine 2020 Database. On August 22,
2020 the talk was by Gavin Mendel_Gleason about `TerminusDB
<https://www.youtube.com/watch?v=CaESy_ILFDs&list=PLSE8ODhjZXjagqlf1NxuBQwaMkrHXi-iz&index=16&t=0s>`_,
a graph database used as a revision control system for data.  His
description of graph databases matched what I thought I was trying to
do with the Books20 database.

The description of a possible database structure given below consists
of relationships between objects, people, organizations, books, and
journals. When I think about the design of the relational database for
the books I primarily think about the relationship or join tables that
descibe the many-to-many relationships, not the physical object
tables.  For a dataset that principally consists of relationship, a
graph database may be the right choice. Graph database consists of
nodes, e.g.\ people or books, which have properties, name, date, etc.,
and relationships, e.g.\ isAuthor, isTranslator, publishedBy, or
published, when can have properties as well, for example, date
published or second author.  Both nodes and relationship may have
labels such as :person or :business. 

``Cyper`` is the query language and it is supported by the
'OpenCypher group <https://www.opencypher.org>`_. This seems to
be an easier language to work in than SQL but I will have to layout
a schema and write some queries to verify that this is true.

Some other graph databases are

* ArangoDB  Apache
* TerminusDB GPL3
* Grakn Core  GNU
* JanusGraph Apache 2 with Linux support
* neo4j

High Level Overview
===================

Independent of the style of the database there are certain actions
that any software system would have to support.  We need to be able to
``insert`` a new record (either a full or partial record), ``update``
an existing record with new or revised data, ``delete`` a record
and any associated records in other tables, and finally ``read`` full
or partial data about a record.

High level records are books, journals, people, and organizations. These
all have relationships to each other. The following illustration
shows the high level entities and some possible relations between
them.

.. image:: ./images/high_level_block.png

May want to track queries in order to run analytics later on.


Sample Queries
==============

To plan the database we need to define the expected queries
that we might want to run.  This will have define what tables
are needed.

  Q1. Show all information about Book|Person|Journal|Organization XXX

  Q2. Select all books by author/translator/person A or publisher P

  Q3. How many books were published in topic A for year Y

  Q4. What author/editor published the most books in year Y
  

Development
***********

As an initial test I have developed two strawman databases. The first
uses the information in the journals.xml files. There are about 230
journals with associated information as well as some publishers in
this file. I have already begun to create an SQLite3 database with
this information but it is not complete nor have I fully defined all
the procedures to implement CRUD.

I am also using the Collection data (my personal book catalog) as a
test data set that can be exprimented with.  This data was created in
a Microsoft Access database (back in 1997) and is easily converted to
CSV file format for import into another database.  I have already
created an SQLite3 database with it but have not defined all the
procedures to fully implement CRUD.
