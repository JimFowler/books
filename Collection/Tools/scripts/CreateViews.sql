--
-- CreateViews.sql
--
-- Created 24 November 2015
--   James R. Fowler
--
-- Create the basic views required for the Collection database.
--  Views are dynamic data sets that will be used frequently.
--
-- To Use:
--    $ sqlite3 Collection.db3
--       .read CreateViews.sql
--
--
--

CREATE VIEW viewAllProjectNames AS 
       SELECT ProjectName, ProjectId
       FROM Projects
       ORDER BY ProjectName;

CREATE VIEW viewAllVendorNames AS 
       SELECT VendorName, VendorId
       FROM Vendors
       ORDER BY VendorName;

CREATE VIEW viewAllAuthorNames AS 
       SELECT LastName, FirstName, AuthorId
       FROM Authors
       ORDER BY LastName;

CREATE VIEW viewAllToDoTasks AS
       SELECT Summary, ToDoId
       FROM ToDo
       ORDER BY DateOfEntry;

CREATE VIEW viewAllBooks AS
       SELECT Books.Title, Authors.LastName, Books.Copyright, Books.BookId
       FROM Authors INNER JOIN
                    (BookAuthor INNER JOIN Books 
                                ON BookAuthor.BookId = Books.BookId)
                    ON BookAuthor.AuthorId = Authors.AuthorId
       WHERE BookAuthor.Priority = 1
       ORDER BY Authors.LastName ASC, Books.Copyright ASC;
   
--
-- Assumes we have Wants and WantAuthor tables
--
--CREATE VIEW viewAllWants AS
--       SELECT Wants.Title, Authors.LastName, Wants.Copyright, Wants.WantId
--       FROM Authors INNER JOIN
--                    (WantAuthor INNER JOIN Wants
--                                ON WantAuthor.WantId = Wants.WantId)
--                    ON BookAuthor.AuthorId = Authors.AuthorId
--       WHERE WantAuthor.Priority = 1
--       ORDER BY Authors.LastName ASC, Wants.Copyright ASC;
--

--
-- end of CreateViews.sql
--
