--
-- CreateTables.sql
--
-- Created 21 November 2015
--   James R. Fowler
--
-- Create the basic tables required for the Collection database.
--
-- To Use:
--    $ sqlite3 Collection.db3
--       sqlite> .read CreateTables.sql
--
--
-- The last known changes were checked in by $Author$
-- as revision $LastChangedRevision$
-- on $Date$
--
--

PRAGMA foreign_keys;

--
-- Create the basic table for individual book entries.
--
-- Should make accession number CONSTRAINT UNIQUE AUTO_INCREMENT
-- and move the wants list to another database.
-- 
CREATE TABLE Books
    --
    -- Unique key.
    --
   (BookId          INT AUTO_INCREMENT PRIMARY KEY NOT NULL,

    --
    -- Basic publishing information. Must have a title
    --   for the entry to be valid
    --
    Title           TEXT NOT NULL,

    --
    -- Copyright date
    --
    Copyright       TEXT NULL,

    --
    -- Zero or Null values is unknown
    --
    Edition         INT UNSIGNED NULL,
    Printing        INT UNSIGNED NULL,

    --
    -- YYYY-MM-DD if known, otherwise 1001-01-01.
    -- If month or day are unknown use YYYY-01-01.
    --
    PurchaseDate    DATE NULL,

    --
    --  Zero values means this was free or was a gift.
    --   $0.01 mean I know a paid something for it but I don't
    --   recall what
    --
    PurchasePrice   FLOAT UNSIGNED NULL,

    --
    -- Link to Vendor table through the VendorId.
    -- Zero or Null values mean unknown
    --
    PurchasedFrom   INT UNSIGNED NULL REFERENCES Vendors(VendorId),

    --
    -- The location the book was published,
    --
    PublishedAt     TEXT NULL,

    --
    -- Link to Vendor table through the Vendor_ID. These condition
    --  statements are based on the definitions from Americam Bookman
    --  magazine.
    --
    Publisher       INT UNSIGNED NULL REFERENCES Vendors(VendorId),
    MyCondition     TEXT CHECK( MyCondition IN
    		  ("Reading", "Poor", "Good", "Very Good", "Fine", "As New" )),

    --
    -- Bibliographic description of the book, pages counts, figures,
    --   tables, index, etc.
    --
    Description     TEXT NULL,
    Comments        TEXT NULL,

    -- Wanted      CHECK( Wanted IN (No,Yes)),
    Wanted          INT,

    --
    -- Should not have two books with the same AccessionNumber
    --
    AccessionNumber INT UNSIGNED UNIQUE NOT NULL
   )

    -- The basic description of each book.
;

--
-- Create the basic table for wanted books.
--
-- These books are desired for my collection and this
-- table contains the basic information about them.
-- 
CREATE TABLE Wanted
    --
    -- Unique key.
    --
   (WantId        INT AUTO_INCREMENT PRIMARY KEY NOT NULL,

    --
    -- Title is the only required field
    --
    Title         TEXT NOT NULL,

    --
    -- YYYY as a string because the YEAR(4) type only stores
    --  years from 1901 - 2155.
    --
    Copyright     CHAR(4) NULL,

    --
    -- Zero or Null values is unknown
    --
    Edition       INT UNSIGNED NULL,
    Printing      INT UNSIGNED NULL,
    PurchasePrice FLOAT UNSIGNED NULL,

    --
    -- The location the book was published,
    --
    PublishedAt   TEXT NULL,

    --
    -- Link to Vendor table through the VendorId.
    --
    Publisher     INT UNSIGNED NULL REFERENCES Vendors(VendorId),

    --
    -- Bibliographic description of the book, pages counts, figures,
    --  tables, index, etc.
    --
    Description   TEXT NULL,
    Comments      TEXT NULL
   )

    -- Basic description of desired books.
;


--
-- Create the basic table for individual authors.
--
CREATE TABLE Authors
   (AuthorId INT AUTO_INCREMENT PRIMARY KEY NOT NULL,

    --
    -- The name used for sorting, usually the family name,
    -- but may be the given name. In which case reverse the values
    -- in the first and last name columns.
    --
    LastName   TEXT NOT NULL,

    --
    -- Any other names associated with the author.
    --
    MiddleName TEXT NULL,

    --
    -- Given name.
    --
    FirstName  TEXT NULL,

    --
    -- YYYY-MM-DD if known, otherwise 1001-01-01.
    -- If month or day are unknown use YYYY-01-01.
    --
    Born       DATE NULL,
    Died       DATE NULL,

    --
    -- Other information about the author that we might use.
    -- Interesting facts about the author
    --
    Comments   TEXT NULL
   )

    -- Basic description of each known author.
;

--
-- Create the Vendor/Publisher table. Because publishers may be
--  vendors as well.
--
CREATE TABLE Vendors
   (VendorId INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    VendorName     TEXT NOT NULL,
    MailingAddress TEXT NULL,
    MailingCity    TEXT NULL,
    MailingState   TEXT NULL,
    MailingCounty  TEXT NULL,
    MailingPostalCode TEXT NULL,
    ShippingAddress TEXT NULL,
    ShippingCity    TEXT NULL,
    ShippingState   TEXT NULL,
    ShippingCounty  TEXT NULL,
    ShippingPostalCode TEXT NULL,
    PhoneNumber     TEXT NULL,
    FaxNumber       TEXT NULL,
    EmailAddress    TEXT NULL,
    URL		    TEXT NULL,
    Comments	    TEXT NULL
   )

    -- Basic vender/publisher information.
;


--
-- Create the Projects table
--
CREATE TABLE Projects
      (ProjectId      INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
       ProjectName    TEXT NOT NULL,
       Description    TEXT NULL
      )

      -- The basic project information.

;


--
-- Create the many-to-many link between books and authors.
--
CREATE TABLE BookAuthor
   (BookAuthorId  INT  AUTO_INCREMENT PRIMARY KEY NOT NULL,

    --
    -- The author id for the author being referenced.    
    --
    AuthorId      INT UNSIGNED NOT NULL REFERENCES Authors(AuthorId),

    --
    -- The book id for the book being referenced.
    --
    BookId        INT UNSIGNED NOT NULL REFERENCES Books(BookId),

    --
    -- What author is this, primary, secondary, etc.
    --
    Priority      INT UNSIGNED NOT NULL,

    --
    -- How the authors name is written on the title page. This may be
    -- different from the authors full name give in the author table
    -- and different for different books.
    --
    AsWritten     TEXT(128) NOT NULL 
   )

;

--
-- Create the many-to-many link linking books and projects
--
CREATE TABLE BookProject
      (ProjBookId INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
       ProjectId  INT UNSIGNED NOT NULL REFERENCES Project(ProjectId),
       BookId     INT UNSIGNED NOT NULL REFERENCES Books(BookId),
       Notes      TEXT NULL
      )
;


CREATE TABLE ToDo
       (ID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
        DateOfEntry DATE NOT NULL,
	Task  TEXT NOT NULL,
	DateCompleted DATE NULL
       )
;

--
-- end of CreateTables.sql
--
