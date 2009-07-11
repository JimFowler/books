--
-- DeleteTables.sql
--
-- Created 19 April 2009
--   James R. Fowler
--
-- Delete the basic tables required for the Books20 database.
--
-- To Use:
--   mysql -u BookMaster -p
--    mysql> source DeleteTables.sql
--
-- The last known changes were checked in by $Author$
-- as revision $LastChangedRevision$
-- on $Date$
--
--


--
-- Use the Books20 database if not already selected
--
USE Books20

--
-- And drop the tables...
DROP TABLE IF EXISTS Book;
DROP TABLE IF EXISTS Author;
DROP TABLE IF EXISTS BookAuthor;
DROP TABLE IF EXISTS Publisher;

--
-- end of DeleteTables.sql
--
