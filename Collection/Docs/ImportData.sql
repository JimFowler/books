--
-- ImportData.sql
--
-- Created 19 April 2009
--   James R. Fowler
--
-- Import the data from the old Access database to the new
-- MySql database Collection.
--
-- To Use:
--   mysql -u BookMaster -p
--    mysql> source ImportData.sql
--
--   $Log$
--
--   $History$
--
--


--
-- Use the Collection database if not already selected
--
USE Collection

--
-- Import the data from the Books.txt file into the table Books
--
LOAD DATA LOCAL INFILE 'Books.txt' INTO TABLE Books
  FIELDS TERMINATED BY '|'
  IGNORE 1 LINES;

--
-- Import the data from the Authors.txt file into the table Authors
--
LOAD DATA LOCAL INFILE 'Authors.txt' INTO TABLE Authors
  FIELDS TERMINATED BY '|'
  IGNORE 1 LINES;

--
-- Import the data from the Projects.txt file into the table Projects
--
LOAD DATA LOCAL INFILE 'Projects.txt' INTO TABLE Projects
  FIELDS TERMINATED BY '|'
  IGNORE 1 LINES;

--
-- Import the data from the Vendors.txt file into the table Vendors
--
LOAD DATA LOCAL INFILE 'Vendors.txt' INTO TABLE Vendors
  FIELDS TERMINATED BY '|'
  IGNORE 1 LINES;

--
-- Import the data from the BookProject.txt file into the table BookProject
-- 
LOAD DATA LOCAL INFILE 'BookProject.txt' INTO TABLE BookProject
  FIELDS TERMINATED BY '|'
  IGNORE 1 LINES;

--
-- Import the data from the BookAuthor.txt file into the table BookAuthor
--    LINES TERMINATED BY '\n'
LOAD DATA LOCAL INFILE 'BookAuthor.txt' INTO TABLE BookAuthor
  FIELDS TERMINATED BY '|'
  IGNORE 1 LINES;

--
-- end of ImportData/sql
--

