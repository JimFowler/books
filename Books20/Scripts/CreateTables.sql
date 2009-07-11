--
-- CreateTables.sql
--
-- Created 19 April 2009
--   James R. Fowler
--
-- Create the basic tables required for the Books20 database.
--
-- To Use:
--   mysql -u BookMaster -p
--    mysql> source CreateTables.sql
--
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
-- Create the basic table for individual book entries.
--
CREATE TABLE Book
    --
    -- Basic database info.
    --
   (Book_ID     INT AUTO_INCREMENT PRIMARY KEY,
    SubBookID   INT UNSIGNED  COMMENT 'This book is affiliated with the book at the ID given.',
    SubIndex    INT UNSIGNED  COMMENT 'This book is number n in the list of subsidiary books.',
    Include     ENUM('No','Yes') DEFAULT 'No'   COMMENT 'Should this book be included in the manuscript?',
    --
    -- Find some way to include picture information.
    --

    --
    -- Basic publishing information.
    --
    Title       VARCHAR(128),
    SubTitle    VARCHAR(128),
    Copyright   CHAR(4)       COMMENT 'YYYY as a string because the YEAR(4) type only stores years from 1901 - 2155.',
    Edition     INT UNSIGNED NOT NULL DEFAULT 1,
    Publisher   INT UNSIGNED  COMMENT 'Link to Publisher table through the Publisher_ID.',
    Location    VARCHAR(64)   COMMENT 'The location the book was published,',
    ISBN        VARCHAR(16)   COMMENT 'The ISBN number if the book has one.',
    Description VARCHAR(1024) COMMENT 'Bibliographic description of the book, pages counts, figures, tables, index, etc.',

    --
    -- Description of why this book is important.
    --
    Keywords    BLOB           COMMENT 'Searchable keyword description. Maybe use a SET type here?',
    OtherLists  BLOB	       COMMENT 'This book is included in other lists such as DeVorkin, Kemp or Astronomical Jabberwocky.',
    Importance  BLOB           COMMENT 'Why in the world is this book listed in the database'
   )

    COMMENT = 'Basic description of each book.'
;


--
-- Create the basic table for individual authors.
--
CREATE TABLE Author
   (Author_ID INT AUTO_INCREMENT PRIMARY KEY,

    --
    -- Basic author information.
    --
    FirstName VARCHAR(64)  COMMENT 'Given name.',
    LastName  VARCHAR(64)  COMMENT 'The name used for sorting, usually the family name, but may be the given name. In which case reverse the values in the first and last name columns.',
    MidNames  VARCHAR(128) COMMENT 'Any other names associated with the author.',
    BirthDate DATE         COMMENT 'YYYY-MM-DD if known, otherwise NULL. If month or day are unknown use YYYY-01-01.',
    DeathDate DATE         COMMENT 'YYYY-MM-DD if known, otherwise NULL. If month or day are unknown use YYYY-01-01.',

    --
    -- Other information about the author that we might use.
    --
    Biography BLOB         COMMENT 'Interesting facts about the author, limited to 65535 chars or about 13000 words.'
   )

    COMMENT = 'Basic description of each known author.'
;

--
-- Create the many-to-many link between books and authors.
--
CREATE TABLE BookAuthor
   (BookAuthor_ID  INT AUTO_INCREMENT PRIMARY KEY,
    Book_ID        INT UNSIGNED          COMMENT 'The book id for the book being referenced.',
    Author_ID      INT UNSIGNED          COMMENT 'The author id for the author being referenced.',
    Priority       INT UNSIGNED NOT NULL COMMENT 'What author is this, primary, secondary, etc.',
    AsWritten      VARCHAR(128)          COMMENT 'How the authors name is written on the title page. This may be different than the authors full name give in the author table and different for different books.'
   )

    COMMENT = 'A many to many link between authors and books.'
;

--
-- Create the Publisher table
--
CREATE TABLE Publisher
   (Publisher_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(128),
    Description BLOB COMMENT 'Basic facts about this publisher.'
   )

    COMMENT = 'Basic publisher information.'
;


--
-- end of CreateTables.sql
--
