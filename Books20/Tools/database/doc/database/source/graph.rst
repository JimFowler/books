Graph Databases
***************

Notes from the on-line classes from Neo4j at
https://Neo4j/graphacademy


Introduction
============

Graphs are uniquely useful when answering questions that involves
following a path along a chain of items.

Mathematically, graphs consist of Vertices and Edges. A vertex (or
node) is defined mathematically as place where two or more edges
(relationships) come together.

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
__________________

One can use WHERE to filter on properties.  The common mathematical
and Boolean functions are available as well as various string
functions.  Regular expressions are also available but note that if
the WHERE clause includes a regular expression, then the indexes will
not be used resulting in longer searches.

Note that a property may be a list.

Working with Patterns in Queries
________________________________


Working with Cypher Data
________________________

Controlling the Query Chain
___________________________

You can use WITH to select out variables in the first
part of a query to use in the second part of the query or
in a second match query.


Controlling Results Returned
____________________________

You can use DISTINCT in the RETURN or in a WITH clause so that rows
with identical values will only be returned once.  ORDER_BY and LIMIT
are also available and again can be used in the RETURN or WITH clause.

Creating Nodes
______________

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
_____________________

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
________________________________

Must delete all relationship linked to a node before deleting
the node.  Use

DETACH DELETE (n) to clear links and delete node.

Merging Data
____________

Best practice when using MERGE is to specify only properties
that have unique values or constraints.

MERGE will automatically create nodes and relationship
if it can not find matching nodes and relationships.  So, then,::

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
__________________________________

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
_____________

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

Using Query Best Practices
__________________________

One can set parameters that may be used in queries as::

  :params actorName => 'Tom Hanks' or
  :params {actorName:'Tom Hanks', movieName:'Top Gun'}

and referenced as ``$actorName``.  The later command replaces
the entire parameter set.  Clear all parameters with::

  :params {}

or a single parameter but giving the list of parameters with
out the one deleted.

In order to build a good graph and to write efficient queries
use ``EXPLAIN`` and ``PROFILE`` to examine the action of the
database when executing the query.

A good graph model and query minimizes the number of rows
processed. Cypher queries may take a long time  becuase the
query takes a long time to create the result string or to execute
in the graph engine. Queries can be monitored with::

  :queries

but this in only available in the Enterprise edition of Neo4j.
Long running queries can be kill by

  * opening another brower and running ``:queries``,
    use the kill button next to the query
  * by closing the result pane in the query brower
  * by closing the query browser

Using LOAD CSV for Import
_________________________

To load data from a csv file into Neo4j, there are a number
of steps that need to take place.

  1. Determine how the CSV file will be structured
  2. Determine if normalized or denormalized data are used
  3. Ensure that the data IDs to be used are unique
  4. Ensure data in CSV file is clean
  5. Execute Cypher code to inspect the data
  6. Determine if the data needs to be transformed
  7. If required, encusre constraints are created in the graph
  8. Determine the size of the data to be loaded
  9. Executre Cypher code to load data
  10. Add indexes to the graph

The command is::

  LOAD CSV WITH HEADERS FROM 'uri' as row...

where ``url`` is either is either ``http://`` for a file on the
Internet or ``file:///`` for a CSV file relative to the ``import``
directory. LOAD CSV has a limit of 100K rows.


Graph Data Modeling
===================

Neo4j is a property graph database.  Applicatinos retrieve
data by traversing the graph. The model consists of

  * nodes
  * relationships
  * properties - provide specific values to nodes or relationships
  * labels - used to catagorize a set of nodes

Traversal means anchoring at a node based on
a specfic property values, then travesing the graph to satisfy
the query.

Arrow tool http://apcjones.com/arrows

Workflow for graph data modeling

  1. Build the intial graph data model
  2. Create and profile Cypher queries to support the model
  3. Create data in the database to support the model
  4. Identify additional questions for the application
  5. Modify the graph data model to support new questions
  6. Refactor the database to support the revised graph data model
  7. Create and profile the Cypher queries to support the revised model
  8. repeat steps 4--7

Designing the initial data model

  1. Understand the domain
     a. describe the application in detail
     b. identify the stakeholders and developers
     c. Identify the users of the applications
     d. enumerate the use cases
  2. Create high-level sample data
  3. Define specific questions for the application
  4. Identify entities
     a. defined properties to answer the application questions,
	
	(otherwise they are merely decoration). Properties are used to
	identify anchors, traversing the graph, and returning
	data. Decorators should be left out of the initial model.

5. Identify connections between entities

     Connections are the verbs in your application questions. Avoid
     using noun for connection names.
     
  6. Test the questions against the entities
  7. Test scalability

     Identify how many of each node might occur. Use EXPLAIN
     and PROFILE to examine queries

Your model should address the uniqueness of nodes.  Nodes with lots of
fan-outs are known as super-nodes and should be used with case.  They
can cause difficulties in traversal if you traverse through a
super-node and follow all the fan-outs

Nodes should have a one or more properties that uniquely identify
them. These properties may never be used in a query but they can
differentiate between nodes.

Use an intermediate node if you have a relationship that needs to
connect to more than one node.  Or if you have sub-properties
of a relationship property. Intermediate nodes can also be used to
reduce fan-out.

Relationship can be used as a link-list, e.g. NEXT or PREVIOUS
relationships. Do not use doubly-linked lists, it is not necessary.

Timeline trees are useful for date or interval searches.  Need unique
identifiers for node however.

If many nodes in the model have the same value for a property
another solution is to use the propery value as a label.  Recall
the nodes can have multiple labels.

Implementing Graph Data Models
==============================

Profiling Queries
_________________

The workflow for profiling and examining queries is

  1. Load data into the graph
  2. Create queries that answer the application questions
  3. Execute the quires against the data to see if they retrieve
     the correct informtion
  4. PROFILE the query execution
  5. Identify problems and weaknesses in the query execution

     a. Can the query be rewritten to perform better?
     b. do we need to refactor the graph?

  6. If necessary, modify the graph data model and refactor the graph
  7. PROFILE the same type of query against the refactored data.

     Note that the query may need to be rewritten due to changes
     in the graph data model.

Implementing Graph Date Models
==============================

Typically a refactor of a model will require additional nodes
and relationship. These new nodes primarily pull data out of the
node or relationship properties and put them in new nodes or '
relationship. The goal is to optimize queries by finding anchor
nodes quickly and not having to search the entire database
multiple times for a query.
