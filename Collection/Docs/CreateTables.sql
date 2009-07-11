--
-- CreateTables.sql
--
-- Created 19 April 2009
--   James R. Fowler
--
-- Create the basic tables required for the Collection database.
--
-- To Use:
--   mysql -u BookMaster -p
--    mysql> source CreateTables.sql
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
-- Create the basic table for individual book entries.
--
-- Should make accession number CONSTRAINT UNIQUE AUTO_INCREMENT
-- and move the wants list to another database.
-- 
CREATE TABLE Books
    --
    -- Basic database info.
    --
   (BookId     INT AUTO_INCREMENT PRIMARY KEY,

    --
    -- Basic publishing information.
    --
    Title       VARCHAR(128),
    Copyright   CHAR(4) NULL      COMMENT 'YYYY as a string because the YEAR(4) type only stores years from 1901 - 2155.',
    Edition     INT UNSIGNED NULL COMMENT 'Zero or Null values is unknown',
    Printing    INT UNSIGNED NULL COMMENT 'Zero or Null values is unknown',
    PurchaseDate DATE NULL        COMMENT 'YYYY-MM-DD if known, otherwise 1001-01-01 If month or day are unknown use YYYY-01-01.',
    PurchasePrice FLOAT UNSIGNED NULL COMMENT 'Zero or Null values mean unknown',
    PurchasedFrom INT UNSIGNED NULL COMMENT 'Link to Publisher table which is also the vendor table. Zero or Null values means unknown.',
    PublishedAt VARCHAR(64)  COMMENT 'The location the book was published,',
    Publisher   INT UNSIGNED NULL COMMENT 'Link to Publisher table through the Publisher_ID.',
    MyCondition  ENUM('Reading', 'Poor', 'Good', 'Very Good', 'Fine', 'As New' ),
    Description VARCHAR(1024) COMMENT 'Bibliographic description of the book, pages counts, figures, tables, index, etc.',
    Comments    TEXT,
    Wanted      ENUM('No','Yes'),
    AccessionNumber INT UNSIGNED
   )

    COMMENT = 'Basic description of each book.'
;


--
-- Create the basic table for individual authors.
--
CREATE TABLE Authors
   (AuthorId INT AUTO_INCREMENT PRIMARY KEY,

    --
    -- Basic author information.
    --
    LastName   VARCHAR(64)  COMMENT 'The name used for sorting, usually the family name, but may be the given name. In which case reverse the values in the first and last name columns.',
    MiddleName VARCHAR(128) COMMENT 'Any other names associated with the author.',
    FirstName  VARCHAR(64)  COMMENT 'Given name.',
    Born       DATE         COMMENT 'YYYY-MM-DD if known, otherwise 1001-01-01 If month or day are unknown use YYYY-01-01.',
    Died       DATE         COMMENT 'YYYY-MM-DD if known, otherwise 1001-01-01. If month or day are unknown use YYYY-01-01.',

    --
    -- Other information about the author that we might use.
    --
    Comments   TEXT         COMMENT 'Interesting facts about the author, limited to 65535 chars or about 13000 words.'
   )

    COMMENT = 'Basic description of each known author.'
;

--
-- Create the many-to-many link between books and authors.
--
CREATE TABLE BookAuthor
   (BookAuthorId  INT  PRIMARY KEY,
    AuthorId      INT UNSIGNED NOT NULL COMMENT 'The author id for the author being referenced.',
    BookId        INT UNSIGNED NOT NULL COMMENT 'The book id for the book being referenced.',
    Priority       INT UNSIGNED NOT NULL COMMENT 'What author is this, primary, secondary, etc.',
    AsWritten      VARCHAR(128) NOT NULL COMMENT 'How the authors name is written on the title page. This may be different than the authors full name give in the author table and different for different books.'
   )

    COMMENT = 'A many to many link between authors and books.'
;

--
-- Create the Publisher table
--
CREATE TABLE Vendors
   (VendorId INT AUTO_INCREMENT PRIMARY KEY,
    Name           VARCHAR(128),
    MailingAddress VARCHAR(128),
    MailingCity    VARCHAR(128),
    MailingState   VARCHAR(128),
    MailingCounty  VARCHAR(128),
    MailingPostalCode VARCHAR(16),
    ShippingAddress VARCHAR(128),
    ShippingCity    VARCHAR(128),
    ShippingState   VARCHAR(128),
    ShippingCounty  VARCHAR(128),
    ShippingPostalCode VARCHAR(16),
    PhoneNumber     VARCHAR(16),
    FaxNumber       VARCHAR(16),
    EmailAddress    VARCHAR(128),
    URL		    VARCHAR(128),
    Comments	    TEXT
   )

    COMMENT = 'Basic vender/publisher information.'
;


--
-- Create the Projects table
--
CREATE TABLE Projects
      (ProjectId   INT AUTO_INCREMENT PRIMARY KEY,
       ProjName    VARCHAR(64),
       Description TEXT
      )

      COMMENT = 'The basic project information.'

;

--
-- Create the many-to-many table linking books and projects
--
CREATE TABLE BookProject
      (ProjBookId INT AUTO_INCREMENT PRIMARY KEY,
       ProjectId  INT UNSIGNED,
       BookId     INT UNSIGNED,
       Notes      TEXT
      )
;



--
-- end of CreateTables.sql
--