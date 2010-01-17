--
-- DeleteTables.sql
--
-- Created 19 April 2009
--   James R. Fowler
--
-- Delete the basic tables from the Collection database.
--
-- To Use:
--   mysql -u BookMaster -p
--    mysql> source DeleteTables.sql
--
--
-- The last known changes were checked in by $Author$
-- as revision $LastChangedRevision$
-- on $Date$
--
--
--


--
-- Use the Collection database if not already selected
--
USE Collection

--
-- And drop the tables...
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Authors;
DROP TABLE IF EXISTS BookAuthor;
DROP TABLE IF EXISTS Vendors;
DROP TABLE IF EXISTS Projects;
DROP TABLE IF EXISTS BookProject;
--
-- end of DeleteTables.sql
--
