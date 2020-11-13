Questions to ask of a database
******************************

The database structure is defined by the questions we want to ask
of the data.  These questions drive the structure of tables or node,
joins or relationship, as well as indexes and constraints.

The basic data consists of Books, People, Organizations, Journals,
and Bibliographies.  There will probably be more to come as
new data and relationships are discovered.

At least some of these questions need to be formally defined and the
corresponding SQL and Cypher statements written so they can be used
as test statements on the database.

Questions, the notation C/B indicates that the questions is
relevant to the Collections and/or the Books20 database
  #. C/B, Show all information about Book|Person|Journal|Organization|... XXX.

  #. C/B, Select all books by author/editor/other A or publisher P
     on topic T.

  #. B, How many books were published in topic A for interval I?

  #. B, What author/editor published the most books in interval I?

  #. C/B, What fraction/number of books were published by University Presses
     for the time interval I?

  #. B, How many books were published by P for the interval I?
  #. C/B, Which books were published by P for the interval I?

  #. C, How many books were purchased from organization O for the interval I?
  #. C, Which books were purchased from organization O for the interval I?

  #. B, How many / which books on topic T were published in interval I ...
     by publisher P?

  #. B, Get link(s) to the review article in ADS for this(ese) book(s).

  #. C, Which books are in project P?

  #. C, Which projects in book B in?  [Project could also be a topic keyword]

  #. C/B How many books published in langauge l for years x-y?

  #. C/B How many books not published in English for years x-y?
