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

  #. C, Which books are in project P for interval I?

  #. C, Which projects is book B in?

  #. C, How many books were purchased from organization O for the interval I?

  #. C, Which books were purchased from organization O for the interval I?

  #. C/B, Show all information about Book|Person|Journal|Organization|... XXX.

  #. C/B, Select all books by author/editor/other A or publisher P
     on topic T.

  #. C/B, What fraction/number of books were published by University Presses
     for the time interval I?

  #. C/B, How many books not published in English for years interval I?

  #. C/B, Which books were published by P for the interval I?

  #. B, How many books were published in topic A for interval I?

  #. B, What author/editor published the most books in interval I?

  #. B, How many / which books for keyword (topic) K were published in interval I ...
     by publisher P?

  #. B, Which publisher printed the most books on keyword (topic) K during interval I?

  #. B, Get link(s) to the review article in ADS for this(ese) book(s).

  #. B, How many books published in langauge L for interval I?

  #. B, What reviewer had the most reviews by year Y for interval I?

  #. B, How many books for section S1 to S2 for interval I by year Y?

  #. B, How many books were published by P for the interval I by year?
