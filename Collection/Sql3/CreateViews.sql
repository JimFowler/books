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
       SELECT ToDoId, Task, DateOfEntry, DateCompleted
       FROM ToDo
       ORDER BY DateOfEntry;

--
-- These two require joins
--

--CREATE VIEW viewAllBooks AS
--       SELECT Books.Title, Authors.LastName, Books.Copyright, BookId
--	 FROM some inner join
--       ORDER BY Authors.LastName, Books.Copyright;
-- 
--CREATE VIEW viewAllWants AS
--       SELECT Wanted.Title, Authors.LastName, Wanted.Copyright, WantedId
--       FROM some inner join
--       ORDER BY Authors.LastName, Books.Copyright;
--

--
-- end of CreateViews.sql
--
