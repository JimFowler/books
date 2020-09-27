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
  LOAD CSV WITH HEADERS FROM 'file:///Authors.txt' AS row FIELDTERMINATOR '|'
  MERGE (:Person {personID: row.AuthorID,
                  lastName: row.LastName,
                  firstName: row.FirstName});

  LOAD CSV WITH HEADERS FROM 'file:///Books.txt' AS row FIELDTERMINATOR '|'
  MERGE (:Book {bookID: row.BookID, Title: row.Title});

  LOAD CSV WITH HEADERS FROM 'file:///Projects.txt' AS row FIELDTERMINATOR '|'
  MERGE (:Project {projectID: row.ProjectID,
		   name: row.ProjectName,
		   description: row.Description});
	 
  :COMMIT // commit the nodes,  we would make indexes here as well
  
  LOAD CSV WITH HEADERS FROM 'file:///BookAuthor.txt' AS row FIELDTERMINATOR '|'
  MATCH (b:Book), (p:Person)
  WHERE b.bookID = row.BookID AND p.personID = row.AuthorID
  CREATE (b)-[r:Author {priority: row.Priority}]->(p);

  LOAD CSV WITH HEADERS FROM 'file:///BookProject.txt' AS row FIELDTERMINATOR '|'
  MATCH (b:Book), (p:Project)
  WHERE b.bookID = row.BookID AND p.projectID = row.projectID
  CREATE (b)-[r:Project {notes: row.Notes}]->(p);
       

  :COMMIT // commit the relationships
	 
