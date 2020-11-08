  //
  // Load the CSV tables from my Access database 'Books and Projects'
  //

  // Create node key constraints on the node ID property to enforce
  // existance and uniqueness.
CREATE CONSTRAINT UniqueBusinessKey IF NOT EXISTS on (b:Business)
       ASSERT (b.businessId, b.name) IS NODE KEY;

CREATE CONSTRAINT UniqueProjectKey IF NOT EXISTS on (p:Project)
       ASSERT (p.projectId, p.name) IS NODE KEY;

CREATE CONSTRAINT UniquePersonKey IF NOT EXISTS on (p:Person)
       ASSERT (p.personId, p.lastName) IS NODE KEY;

CREATE CONSTRAINT UniqueBookKey IF NOT EXISTS on (b:Book)
       ASSERT (b.bookId, b.title, b.accessionNumber) IS NODE KEY;

CREATE CONSTRAINT UniqueBookIdConstraint IF NOT EXISTS on (b:Book)
       ASSERT b.bookId IS UNIQUE;

CREATE CONSTRAINT UniqueBookAccessionConstraint IF NOT EXISTS on (b:Book)
       ASSERT b.accessionNumber IS UNIQUE;

       
  //
  // Load the Vendors.txt file as (:Business) nodes
  //
  // Need to load vendor file before the Books file so that (:Book)
  // nodes can be put in relationship PURCHASED_FROM and PUBLISHED_BY
  // with the (:Business) nodes
  //
LOAD CSV WITH HEADERS FROM 'file:///Vendors.txt' AS row
CREATE (b:Business {businessId: toInteger(row.VendorID),
		    name: row.Name})
    WITH row, b, row.MailingAddress + '\n' + row.MailingCity + ', ' + row.MailingStateProv + ' ' + row.MailingPostalCode + '\n' + row.MailingCountry as mailaddress
      SET b.mailAddress = CASE mailaddress WHEN "" THEN null ELSE trim(mailaddress) END
      SET b.emailAddress = CASE trim(row.EmailAddress) WHEN "" THEN null ELSE trim(row.EmailAddress) END
      SET b.phoneNumber = CASE trim(row.PhoneNumber) WHEN "" THEN null ELSE trim(row.PhoneNumber) END
      SET b.comments = CASE trim(row.Comments) WHEN "" THEN null ELSE trim(row.Comments) END
      SET b.url = CASE trim(row.URL) WHEN "" THEN null ELSE trim(row.URL) END;

	 
  //
  // Load the Authors.txt file as (:Person) nodes
  //	
LOAD CSV WITH HEADERS FROM 'file:///Authors.txt' AS row
  CREATE (person:Person {personId: toInteger(row.AuthorID),
                         lastName: row.LastName})
    WITH row, person
      SET person.firstName = CASE trim(row.FirstName) WHEN "" THEN null ELSE trim(row.FirstName) END
      SET person.middleName = CASE trim(row.MiddleName) WHEN "" THEN null ELSE trim(row.MiddleName) END
      SET person.born = CASE trim(row.Born) WHEN "" THEN null ELSE row.Born END
      SET person.died = CASE trim(row.Died) WHEN "" THEN null ELSE row.Died END
      SET person.comments = CASE trim(row.Comments) WHEN "" THEN null ELSE row.Comments END;

  //
  // Load the Projects.txt file as (:Project) nodes
  //	
LOAD CSV WITH HEADERS FROM 'file:///Projects.txt' AS row
  CREATE (project:Project {projectId: toInteger(row.ProjectID),
   		           name: row.ProjectName,
   		           description: row.Description});


  //
  // Load the Books.txt file as (:Book) nodes
  //
LOAD CSV WITH HEADERS FROM 'file:///Books.txt' AS row
CREATE (book:Book {bookId: toInteger(row.BookID),
		   title: row.Title,
		   accessionNumber: toInteger(row.AccessionNumber)})
      SET book.copyright = CASE trim(row.Copyright) WHEN "" THEN null ELSE row.Copyright END
      SET book.edition = CASE trim(row.Edition) WHEN "" THEN null ELSE row.Edition END
      SET book.printing = CASE trim(row.Printing) WHEN "" THEN null ELSE row.Printing END
      SET book.publishedAt = CASE trim(row.PublishedAt) WHEN "" THEN null ELSE row.PublishedAt END
      SET book.condition = CASE trim(row.Condition) WHEN "" THEN null ELSE row.Condition END
      SET book.description = CASE trim(row.Description) WHEN "" THEN null ELSE row.Description END
      SET book.comments = CASE trim(row.Comments) WHEN "" THEN null ELSE row.Comments END
    WITH row, book
    MATCH (seller:Business {businessId: toInteger(row.PurchasedFrom)})
    MERGE (book)-[purchasedfrom:PURCHASED_FROM]->(seller)
	SET purchasedfrom.date = CASE trim(row.PurchaseDate) WHEN "" THEN null ELSE row.PurchaseDate END
	SET purchasedfrom.price = CASE trim(row.PurchasePrice) WHEN "" THEN null ELSE row.PurchasePrice END
    WITH row, book
    MATCH (publisher:Business {businessId: toInteger(row.Publisher)})
	  MERGE (book)-[:PUBLISHED_BY]->(publisher);




  // Delete the empty Person record PersonId == 265
  MATCH (empty_person:Person {personId: 265}) detach delete empty_person;

  // Create the Indexes
  CREATE INDEX LocationIndex for (b:Book) on (b.publishedAt);


  // load the relationship tables
  LOAD CSV WITH HEADERS FROM 'file:///BookAuthor.txt' AS row
  MATCH (book:Book), (person:Person)
  WHERE book.bookId = toInteger(row.BookID) AND person.personId = toInteger(row.AuthorID)
  CREATE (person)-[r:AUTHOR_OF {priority: row.Priority}]->(book);

  LOAD CSV WITH HEADERS FROM 'file:///BookProject.txt' AS row
  MATCH (book:Book), (project:Project)
  WHERE book.bookId = toInteger(row.BookID) AND project.projectId = toInteger(row.ProjectID)
  CREATE (book)-[r:IN_PROJECT {notes: row.Notes}]->(project);
