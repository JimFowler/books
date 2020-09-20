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

