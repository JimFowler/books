--
-- Rebuild.sql
--
-- Created 26 May 2009
--   James R. Fowler
--
-- Rebuild the MySql database Books20
--
-- To Use:
--   mysql -u BookMaster -p
--    mysql> source Rebuild.sql
--
-- The last known changes were checked in by $Author$
-- as revision $LastChangedRevision$
-- on $Date$
--

--
-- Use the Books20 database if not already selected
--
USE Books20

--
-- Delete the old tables
--
source DeleteTables.sql;

--
-- Create the tables and import the data
--
source CreateTables.sql;
-- source ImportData.sql;

--
-- End of Rebuild.sql
--
