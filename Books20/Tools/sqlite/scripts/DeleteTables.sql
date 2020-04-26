--
-- DeleteTables.sql
--
-- Created 24 November 2015 for the Collections database
--   James R. Fowler
--
-- Modified 25 April 2020 for Journal database
--
-- Delete the basic tables from the journals database.
--
-- To Use:
--   sqlite3 journals.db3
--    sqlite> .read DeleteTables.sql
--
--


--
-- Drop the tables...
--
DROP TABLE IF EXISTS JournalPublisher;
DROP TABLE IF EXISTS JournalInfo;
DROP TABLE IF EXISTS Publishers;
DROP TABLE IF EXISTS JournalDesignator;
DROP TABLE IF EXISTS Journals;
DROP TABLE IF EXISTS ToDo;
--
-- end of DeleteTables.sql
--
