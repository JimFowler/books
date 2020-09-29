neo4j
*****

I have been looking at `Neo4j <https://neo4j.com>`_ as an example of a
graph database.  Neo4j thinks of nodes as nouns, properties of nodes
as ajective, relationships as verbs, and properties of relationships
as adverbs.

Converting RDBS to Neo4j. Replace foreign keys with relationships.
Convert join tables (many-to-many tables) to relationships with
properties.

Installation
============

Desktop
_______

Installing ndo4j desktop. Download from neo4j.com. Click the download
button.  I downloaded
neo4j-desktop-offline-1.3.4-x86_64.AppImage. Change the mode of the
file to executable, create a soft link as ``neodesk`` and run the
program.

Server
______

To install neo4j we add neo4j.com to the list of active repositories
and the use ``apt`` to install.  So run the following commands as root::

  wget -O - https://debian.neo4j.com/neotechnology.gpg.key | \
    sudo apt-key add -
  echo 'deb https://debian.neo4j.com stable latest' | \
    sudo tee -a /etc/apt/sources.list.d/neo4j.list
  apt update
  apt install ne04j

To start the database server run the following as root::

  sudo service neo4j start

Connect to the neo4j brower service at `localhost:7474
<http://localhost:7474/browser/>`_.

Install the Python neo4j module::

  pip install neo4j

 
How to design a graph
=====================

This information came from the Oracle Youtube video on
designing a graph database and it matches essentially what
the neo4j videos discuss.

  1. Understand data source,

     a. what are entities, books, people, business, journals, reviews

     b. what are the relationships and properties of relationships.
	people to books, books to books, people to people
	business to books, people to business, etc

  2. What do we want to achieve, navigation, pattern matching,
     analytics, visualization, etc.

  3. construct the graph model

  4. Populate the graph and test the work load.
     It's ok to do a lot of trial and error


Visulization Tools
==================

These visualization tools were mentioned in a Youtube
video from Oracle about there version of a graph database

Cytoscape, Linkurious, Keylines, Centrifuge, Tom Sawyer,
Gephi, https://github.com/tinkerpop

Oracles Graph Blog  https://blogs.oracle.com/bigdataspatialgraph

Design
======

Nodes
_____

Nodes may be indexed on their properties

The nodes may consist of the following labels,

  * :Series
  * :Book:MultiVolume
  * :Person
  * :Corporate
  * :Journal
  * :Review
  * :Project
  * :Bibliography - AJB, AAA, others?
  * :Year, :Month, :Day

    * properties: value, month_name, month_number

  * something for the AJB/AAA counts

Relationships
_____________

Remember that relationship can not be indexed. For faster searches
we should keep relationship properties to a minimum if we plan to make
decisions based on those properties.

The relationships may consist of,

  * :Book to :MultiVolume

    * :PART_OF {volume: n{
      
  * :Book to :Book
    
    * :EDITION_OF {edition: n}
	
    * :REPRINT_OF
    * :TRANSLATION_OF

  * :Book to :Person
    
    * :AUTHOR {authorNumber: n}	
    * :EDITOR {editorNumber: n}
    * :TRANSLATOR {translatorNumber: n}
    * :COMPILER {compilerNumber: n}
    * :CONTRIBUTER {contributorNumber: n}
    * :ILLUSTRATOR {illustratorNumber: n}

  * :Book to :Corporate
    
    * all of the book-to-people relations
    * :PRINTED_BY
    * :PUBLISHED_BY

      * properties: copyright:
	
    * :PURCHASED_FROM {purchaseYear:, purchasePrice:}
	
  * :Review
    
    * :OF_BOOK -> (:Book)
    * :IN_JOURNAL -> (:Journal {issue: n, page: m}
    * :REVIEWED_BY -> (:Person)
