--
-- DeleteTables.sql
--
-- Created 24 November 2015
--   James R. Fowler
--
-- Delete the basic tables from the Collection database.
--
-- To Use:
--   sqlite3 Collection.db3
--    sqlite> .read DeleteTables.sql
--
--
-- The last known changes were checked in by $Author$
-- as revision $LastChangedRevision$
-- on $Date$
--
--
--

--
-- Drop the tables...
--
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Authors;
DROP TABLE IF EXISTS BookAuthor;
DROP TABLE IF EXISTS Vendors;
DROP TABLE IF EXISTS Projects;
DROP TABLE IF EXISTS BookProject;
DROP TABLE IF EXISTS Wanted;
DROP TABLE IF EXISTS ToDo;
--
-- end of DeleteTables.sql
--
