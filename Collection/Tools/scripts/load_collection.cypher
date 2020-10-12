  :BEGIN
  // file must be in the ./imports directory of the project
  //
  // These commands will fail if there is a NULL value in any of the
  // requested fields in the row. However, we can replace the '||'
  // with an empty string '|""|' and the commands will work  
  //
  // Decide if we want empty string or no property if the field is empty.
  // If the latter we will need to use python to parse the csv files
  // and to write the cypher command to create the node or relationship
  //
  // Need to load vendor file first to that Book nodes can be put in relationship
  // PurchaseFrom and PublishedBy with the vendors
  //

CREATE CONSTRAINT UniqueBusinessIdConstraint on (b:Business) ASSERT v.busnessID IS UNIQUE;
CREATE CONSTRAINT UniquePersonIdConstraint on (p:Person) ASSERT p.personID IS UNIQUE;
CREATE CONSTRAINT UniqueProjectIdConstraint on (p:Project) ASSERT p.projectID IS UNIQUE;
CREATE CONSTRAINT UniqueBookIdConstraint on (b:Book) ASSERT b.bookID IS UNIQUE;

  LOAD CSV WITH HEADERS FROM 'file:///Vendors.txt' AS row FIELDTERMINATOR '|'
  CREATE (:Business {businessID: row.VenderID},
			 
       
  LOAD CSV WITH HEADERS FROM 'file:///Authors.txt' AS row FIELDTERMINATOR '|'
  CREATE (:Person {personID: row.AuthorID,
                  lastName: row.LastName,
                  firstName: row.FirstName});

  LOAD CSV WITH HEADERS FROM 'file:///Projects.txt' AS row FIELDTERMINATOR '|'
  CREATE (:Project {projectID: row.ProjectID,
		   name: row.ProjectName,
		   description: row.Description});

  // load the books and create the [:PUBLISHED_BY] and [:PURCHASE_FROM} relationships
  LOAD CSV WITH HEADERS FROM 'file:///Books.txt' AS row FIELDTERMINATOR '|'
  CREATE (:Book {bookID: row.BookID, title: row.Title});

  :COMMIT // commit the nodes,  we would make indexes here as well

  // load the relationships

  // Create the [:AUTHOR_OF] and [:EDITOR_OF] relationships
  LOAD CSV WITH HEADERS FROM 'file:///BookAuthor.txt' AS row FIELDTERMINATOR '|'
  MATCH (b:Book), (p:Person)
  WHERE b.bookID = row.BookID AND p.personID = row.AuthorID
  CREATE (b)-[r:Author {priority: row.Priority}]->(p);

  LOAD CSV WITH HEADERS FROM 'file:///BookProject.txt' AS row FIELDTERMINATOR '|'
  MATCH (b:Book), (p:Project)
  WHERE b.bookID = row.BookID AND p.projectID = row.projectID
  CREATE (b)-[r:Project {notes: row.Notes}]->(p);
       

  :COMMIT // commit the relationships
	 
