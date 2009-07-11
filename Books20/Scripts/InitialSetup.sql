--
-- InitialSetup.sql
--
--  The initial setup for a empty MySql installation.
--  Run this script only once.
--
--  Created 18 April 2009
--    James R. Fowler
--
-- To Use:
--   mysql -u BookMaster -p
--    mysql> source InitialSetup.sql
--
-- The last known changes were checked in by $Author$
-- as revision $LastChangedRevision$
-- on $Date$
--
--


--
--   Add password to the root account
-- 
SET PASSWORD FOR 'root'@'Biblion'   = PASSWORD('MNyt34sdqwlk');
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('MNyt34sdqwlk');
SET PASSWORD FOR 'root'@'127.0.0.1' = PASSWORD('MNyt34sdqwlk');

--
--   Delete the anonymous accounts
--
DROP USER ''@'Biblion';
DROP USER ''@'localhost';

--
--   Create the database Books20
--
CREATE DATABASE Books20;

--
--   The BookMaster account is the one that can modify the database,
--   creating tables and adding records. Note: user names are case
--     sensitive.
--
CREATE USER 'BookMaster'@'Bibilon'   IDENTIFIED BY 'papyrus';
CREATE USER 'BookMaster'@'localhost' IDENTIFIED BY 'papyrus';
GRANT ALL PRIVILEGES ON Books20.* to 'BookMaster'@'localhost';
GRANT ALL PRIVILEGES ON Books20.* to 'BookMaster'@'Biblion';

--
--   The Reader account is use to view the database only.  It can be
--   accessed from the outside from any host. We limit the number of
--   queries and connections for now so that automatic software can
--   not trash the system.  We will raise these values when we go
--   live on the web.
--
CREATE USER 'Reader'@'Biblion'   IDENTIFIED BY 'librarycard';
CREATE USER 'Reader'@'localhost' IDENTIFIED BY 'librarycard';
CREATE USER 'Reader'@'%'         IDENTIFIED BY 'librarycard';
GRANT SELECT ON Books20.* to 'Reader'@'Biblion'
GRANT SELECT ON Books20.* to 'Reader'@'localhost'
GRANT SELECT ON Books20.* to 'Reader'@'%'
  WITH MAX_QUERIES_PER_HOUR 100
       MAX_CONNECTIONS_PER_HOUR 100;


--
-- Create the Roller DB for my blog
--
CREATE DATABASE rollerdb;

--
-- Create the roller db user
--
CREATE USER 'blogmaster'@'Biblion'   IDENTIFIED BY 'blahblah'
CREATE USER 'blogmaster'@'localhost' IDENTIFIED BY 'blahblah'
GRANT ALL PRIVILEGES ON rollerdb.* to 'blogmaster'@'Biblion'   WITH GRANT OPTION
GRANT ALL PRIVILEGES ON rollerdb.* to 'blogmaster'@'localhost' WITH GRANT OPTION


--
-- end of InitialSetup.sql
--
