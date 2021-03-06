--
-- Rebuild.sql
--
-- Created 3 May 2009
--   James R. Fowler
--
-- Rebuild the MySql database Collection.
--
-- To Use:
--   mysql -u BookMaster -p
--    mysql> source Rebuild.sql
--
--
-- The last known changes were checked in by $Author$
-- as revision $LastChangedRevision$
-- on $Date$
--
--

--
-- Use the Collection database if not already selected
--
USE Collection

--
-- Delete the old tables
--
source DeleteTables.sql;

--
-- Create the tables and import the data
--
source CreateTables.sql;
source ImportData.sql;

--
-- End of Rebuild.sql
--
