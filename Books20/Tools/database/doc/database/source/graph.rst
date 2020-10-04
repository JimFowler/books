Graph Databases
***************

Introduction
============

Notes from the on-line classes from Neo4j at
https://Neo4j/graphacademy

Graphs are uniquely useful when answering a questions that involves
following a path along a chain of items.

Mathematically, graphs consist of Vertices and Edges. A vertex (or
node) is defined mathematically as place where two or more edges some
together.

Neo4j graphs consist of ``Node`` and ``Relationship``. It is possible
to have nodes without relationships but you can not have relationships
without nodes. Relationships (and nodes) can carry information
(properties, Neo4j is a property database). Relationships must have a
``type`` and a ``direction``.

A ``path`` is a traversal of nodes and relationship.  A node may be
visited more than once but a relationship may only be traversed once.

A ``graph database`` is an online database management system that
support ``Create``, ``Read``, ``Update``, and ``Delete`` (CRUD)
operations.  Relationships take first priority in graph
databases. Storing relationships and connection as first class
entities is the biggest value that graph databases bring to an
application.

The Neo4j Graph Platform
========================

Neo4j DBMS
__________

the Neo4j DBMS includes the processes and resources needed to manage a
single instance or a set of instances. A Neo4j ``instance`` is a
single process that runs the Neo4j server code. At a minimum a Neo4j
instance contains the ``system database`` and a ``default database``.

The system database contains metadata about the databases as well as
security configuration. The default database is the "user" database
where you implement your graph model. In Neo4j Enterprise you may have
more than one "user" database.

Neo4j supports ``atomicity``, ``consistency``, ``isolation``, and
``durability`` (ACID) guarantees for data. The Neo4j ``graph engine``
interprets Cypher statements and executes kernel-level code to store
and retrieve data.  This engine can be tuned for you application.

Neo4j Aura
__________

Neo4j Aura support Neo4j in the cloud with the most up-to-date
version of Neo4j.  The back end is managed by Neo4j engineers.
This does require an account and a monthly subscription fee.

Neo4j Sandbox
_____________

A temporary site in the cloud where you can experiment with Neo4j.  Database are
available for three days but can be extended to 10 days.  Use the Browser
Sync to save Cypher scripts from the Sandbox.

Neo4j Desktop
_____________

Intended for local development of a Neo4j application.  Only one instance
or database can be run at one time.

Neo4j Browser
_____________

A web based interface to Neo4j DBMS.  Support saving Cyper scripts and
visualizing graphs.  cypher-shell can also be used to connect to a live
instance.

Libraries
_________

Libraries or plugins can be incorporated into your application. APOC
and GraphQL are two of the most popular libraries.


Introduction to Cypher
======================

Cypher is a query language for graph databases. It is open language and
can be found at https://opencypher.org.

Nodes are specified by () or (variable:Label1:Label2). Note that node
can have multiple labels. Use ``call db.schema.visualization() to see
the graph schema of the current graph. Nodes may also have properties.

A relationship is a directed connection between two nodes that has a
relationship type and it may have properties.

The is a ``Cypher Style Guide`` which can be found in Appendix A
of the Cypher Manual.

Cypher style recommendations

  * node labels are CamelCase and begin with an upper-case letter.
  * property keys, variable, parameters, aliases, and functions are
    camelCase and begin with a lower-case letter.
  * relationships are UPPER_CASE and may use the underscore.
  * cypher keywords are UPPER_CASE but are case insensitive the the
    interpreter.
  * string constants are in single quotes unless the string contains
    a quote or an apostrophe.
  * specify variables only when needed for later use
  * place named nodes and relationship before anonymous nodes n the
    Cypher statements.
  * specify anonymous relationships with -->, --, or <--.
  * create nodes first, then create relationships

Filters on Queries
==================

One can use WHERE to filter on properties.  The common mathematical
and Boolean functions are available as well as various string
functions.  Regular expressions are also available but note that if
the WHERE clause includes a regular expression, then the indexes will
not be used resulting in longer searches.

Note that a property may be a list.

Working with Patterns in Queries
================================


Working with Cypher Data
========================

Controlling the Query Chain
===========================

You can use WITH to select out variables in the first
part of a query to use in the second part of the query or
in a second match query.


Controlling Results Returned
============================

You can use DISTINCT in the RETURN or in a WITH clause so that rows
with identical values will only be returned once.  ORDER_BY and LIMIT
are also available and again can be used in the RETURN or WITH clause.

Creating Nodes
==============

Can create or assign nodes with more than one label by using CREATE
(:Movie:Action {title: 'Batman Begins'}). You can add a label later
on with SET x:LABEL where x is a reference to the node. SET will be
ignored if the LABEL already exists. One can remove a label with
REMOVE x:LABEL. Again this command will be ignored if the node
does not have the label you are trying to remove.

You can a property to an existing node with SET x:propertyName =
value.  Note that if value is null, the property will be removed.
One can also use REMOVE x:propertyName
Once a property key exists it remains in the graph even if no nodes
have that property key

Creating Relationship
=====================

Create a relationship as::

  CREATE (x)-[:REL_TYPE]->(y); or

  CREATE (x)<-[:REL_TYPE]-(y);

  MATCH (p:Person), (m:Movie)
  WHERE p.name = 'Emil Eifrem' AND
      m.title = 'Forrest Gump'
  MERGE (p)-[:ACTED_IN]->(m)

Best practice is to use the later method. Relationships must have a
direction but can be searched in either direction. You can set
properties of relationships with::

  CREATE (a)-[r:REL_TYPE]->(m)
  SET r.propertyKey = value;

A left-to-right relationship is assumed if you forget to specify the
direction when MERGE creates a new relationship.


Deleting Nodes and Relationships
================================

Must delete all relationship linked to a node before deleting
the node.  Use

DETACH DELETE (n) to clear links and delete node.

Merging Data
============

Best practice when using MERGE is to specify only properties
that have unique values or constraints.

MERGE will automatically create nodes and relationship
if it can not find matching nodes and relationships.  So, then,

MERGE (m:LABEL {prop: x})-[]->()

finds only the nodes that have only the property 'prop'. If your node
has additional properties it will not find those nodes.  Best practice is
to create nodes first, then create relationships.

A case statement may be used for SET or RETURN::

  MATCH (p:Person)-[rel:ACTED_IN]->(m:Movie)
  WHERE m.title = 'Forrest Gump'
  SET rel.roles =
  CASE p.name
    WHEN 'Tom Hanks' THEN ['Forrest Gump']
    WHEN 'Robin Wright' THEN ['Jenny Curran']
    WHEN 'Gary Sinise' THEN ['Lt. Dan Taylor']
  END

Defining Constraints for your Data
==================================

Cypher allows you to define

  * Uniqueness constraint for a node property
  * Existence constraint for a node property
  * Uniqueness constraint for a set of node properties

To create a constraint::

  CREATE CONSTRAINT NameOfConstraint on (l:Label) ASSERT l.property IS UNIQUE;
  CREATE CONSTRAINT NameOfConstraint on (l:Label) ASSERT exists(l.property);

To create a constraint on a relationship::

  create constraint NameOfConstraint on ()-[r:REL]-() assert exists(r.prop);
  
Neo4j will issue an error and the constraint will not be made if a
node currently exists which does not match the constraint.

To see constraints::

  CALL db.constraints()

To delete a constraint::

  DROP CONSTRAINT NameOfConstraint

To create combined contra int or node key::

  CREATE CONSTRAINT NameOfConstraint on (l:Label)
  ASSERT(l.prop1, l,prop2) IS NODE KEY;

 A node key is also used as a composite index on the Label node.

Using Indexes
=============

Constraints and node keys are single property and conposite indexes
respectively.

Single property indexes are used for equality (=), range comparision
(<, <=, >, >=), list membership (IN), string comparisions
(STARTS WITH, ENDS WITH, CONTAINS), existence checks (EXISTS),
spatial distance searches (distance()), and spatial bounding
searches (point()).

Composite indexes are used only for quality checks and list membership

Neo4j recommends creating indexes after node creation when making
a large graph.  You can create an index with ::

  CREATE INDEX IndexName FOR (l:Label) ON (l.propertyKey);

A composite index is created with::
  
  CREATE INDEX IndexName FOR (l:Label) ON (l.prop1, l.prop2);

A full schema index is based on string values only and be used for

  * node or relationship properties
  * single or multiple properties
  * single or multiple types of nodes (labels)
  * single or multiple types of relationships

An index on multiple node or relationship properties is created with a
call to the function::

  CALL db.index.fulltext.createNodeIndex('MovieTitlePersonName',
    ['Movie', 'Person'], ['title', 'name'])

  CALL db.index.fulltext.createRelationshipIndex('IndexName', ...

To used a particular index you must call the query procedure::

  CALL db.index.fulltext.queryNodes(
  'MovieTitlePerson', 'Jerry') YIELD node, score
  RETURN node.title, score;

where ``score`` is a Lucene score based on how much of ``jerry``
was part of the title or name.

You can look for a partial index match be specifying the particular
property you wish to search on::

  CALL db.index.fulltext.queryNodes(
  'MovieTitlePerson', 'name:Jerry') YIELD node, score
  RETURN node, score;

Drop an index on a property with the command::

  DROP INDEX Indexname;

but for a full-text schema index use the procedure::

  CALL db.index.fulltext.drop('IndexName')

