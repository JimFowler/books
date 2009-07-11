--
-- InitialSetup.sql
--
--  The initial setup for the Collection database
--
--  Created 20 April 2009
--    James R. Fowler
--
-- To Use:
--   mysql -u root -p
--    mysql> source InitialSetup.sql
--
--   $Log$
--
--   $History$
--
--


--
--   Create the database Collection
--
CREATE DATABASE Collection;

--
--   The BookMaster account is the one that can modify the database,
--   creating tables and adding records. Note: user names are case
--     sensitive.
--
GRANT ALL PRIVILEGES ON Collection.* to 'BookMaster'@'localhost';
GRANT ALL PRIVILEGES ON Collection.* to 'BookMaster'@'Biblion';

--
-- end of InitialSetup.sql
--
