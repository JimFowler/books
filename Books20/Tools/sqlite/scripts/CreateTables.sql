-- CreateTables.sql
--
-- Begin copyright
--
--   /home/jrf/Documents/books/Books20/Tools/sqlite/scripts/CreateTables.sql
--
--   Part of the Books20 Project
--
--   Copyright 2020 James R. Fowler
--
--   All rights reserved. No part of this publication may be
--   reproduced, stored in a retrival system, or transmitted
--   in any form or by any means, electronic, mechanical,
--   photocopying, recording, or otherwise, without prior written
--   permission of the author.
--
--
-- End copyright
--
-- Created 21 November 2015 for Collections database
--   James R. Fowler
--
-- Modified 24 April 2020 for journals database.
--  James R. Fowler
--
-- Create the basic tables required for the journal database.
--
-- To Use:
--    $ sqlite3 journal.db3
--       sqlite> .read CreateTables.sql
--
--
--

PRAGMA foreign_keys;

--
-- Create the basic table for individual journal entries
--
-- Is it wise to keep the sub-titles and abbreviations
-- in the same table as titles? So far, yes.
--
-- 
CREATE TABLE Journals
   (
    --
    -- Unique key.
    --
    JournalId       INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,

    --
    -- A title of the journal, a sub_title, or an abbreviation.
    --
    Title           TEXT NOT NULL,

    --
    -- ParentId is a link to another JournalId. It will be zero 
    -- if this is a main title or a valid JournalId if this is a
    -- sub-title or abbreviation.
    --
    ParentId	    INTEGER NULL REFERENCES Journals(JournalId)
                    ON UPDATE CASCADE,

    --
    -- TitleLevel is 0 for a main title, , >=1 if this is a
    -- sub-title (first sub-title, second sub-title, etc.), or -1 if
    -- this is a abbreviation for the main title.
    --
    TitleLevel      INTEGER NOT NULL
   )
;


CREATE TABLE JournalComments
   (
    --
    -- Unique key.
    --
    CommentId     INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,


    --
    -- Title is the only required field. This is a link to the
    -- entries in the Title table.
    --
    JournalId     INTEGER NOT NULL REFERENCES Journals(JournalId)
                  ON UPDATE CASCADE
                  ON DELETE CASCADE,

    --
    -- Rambling words about the journal
    --
    Comment       TEXT NOT NULL
   )
;

--
-- Create the Journal Information table
--
-- Journals will have a start/end date and may have merged
-- into or merged from another journal.  This table
-- keeps track of that information.  This data is not
-- included in the Titles table because sub-titles and
-- abbreviations don't have this information so the table
-- would have a lot of empty fields.
--
CREATE TABLE JournalInfo
   (
    --
    -- Unique key.
    --
    InfoId        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,

    --
    -- Title is the only required field. This is a link to the
    -- entries in the Title table.
    --
    JournalId     INTEGER NOT NULL REFERENCES Journals(JournalId)
                  ON UPDATE CASCADE
                  ON DELETE CASCADE,

    --
    -- The date for this transaction. It will be the StartDate
    -- if this is a 'Prev" transaction, or an EndDate if this is
    -- a 'Next' transaction. Dates should be YYYY[-MM[-DD]].
    --
    DateStamp     TEXT NOT NULL,

    --
    -- JRefId is the title of the journal this journal
    -- was merged or renamed as.
    --
    JRefId        INTEGER NULL REFERENCES Journals(JournalId)
                  ON UPDATE CASCADE
                  ON DELETE CASCADE,

    --
    -- RefType is the type of transaction this is.
    -- It can be either a reference to the 'Next'
    -- title or the 'Prev' title.
    -- Choices are 'Start', 'Next', 'Prev', and 'End'
    --
    RefType       TEXT NOT NULL,

    --
    -- Rambling statement about this reference info.
    --
    Comments      TEXT NULL
   )
;

--
-- Create the Designators table.
--
-- Designators are keys to other databases and may include entries
-- like ISSN (Internation Serial Serial Number), LCCN (Library of
-- Congress catalog number), DDCN (Dewey Decimal Catalogue number),
-- ADS (the Astrophysical Data System bitstem code), or other to be
-- determined. They may be 0 or many entries for a particular title.
--
CREATE TABLE JournalDesignator
   (
    --
    -- The unique id.
    --
    JournalDesigId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,

    --
    -- The journal id that this entry is for.
    -- 
    JournalId      INTEGER NOT NULL REFERENCES Journals(JournalId)
                   ON UPDATE CASCADE
                   ON DELETE CASCADE,

    --
    -- The key word for the designator ISSN, DDCN, ADS, etc.
    --
    KeyName	   TEXT NOT NULL,

    --
    -- The value for the key word.
    --
    KeyValue       TEXT NOT NULL
   )
;

--
-- Create the Publisher table.
--
CREATE TABLE Publishers
   (
    --
    -- Unique Id.
    --
    PublisherId    INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,

    --
    -- The name of the publisher.
    --
    PublisherName  TEXT NOT NULL,

    --
    -- The primary location of the publisher.
    --
    City           TEXT NULL,

    --
    -- The primary country of the publisher.
    --
    Country        TEXT NULL,

    --
    -- Ramblings about the publisher.
    --
    Comments	   TEXT NULL
   )
;

--
-- Create the many-to-many link between titles and publishers.
-- Note that there may be more than one entry for a particular
-- title as the journal may have changed publishers.
--
CREATE TABLE JournalPublisher
   (
    --
    -- Unique Id
    --
    JournalPublId  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,

    --
    -- The journal id for the Title being referenced.    
    --
    JournalId      INTEGER NOT NULL REFERENCES Journal(JournalId)
                   ON UPDATE CASCADE
                   ON DELETE CASCADE,

    --
    -- The publisher id for the publisher being referenced.
    --  What to do if the Publisher is deleted?
    --
    PublisherId    INTEGER NOT NULL REFERENCES Publisher(PublisherId)
                   ON UPDATE CASCADE
                   ON DELETE CASCADE,

    --
    -- Place of publication.
    --
    Place	   TEXT NULL,

    --
    -- The start date for this title/publisher combination.
    -- Dates should be YYYY[-MM[-DD]].
    --
    StartDate      TEXT NULL,

    --
    -- The end date for this title/publisher combination.
    -- Dates should be YYYY[-MM[-DD]].
    --
    EndDate        TEXT NULL
   )
;


CREATE TABLE ToDo
   (
    --
    -- Unique Id
    --
    ToDoId        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,

    --
    -- Short Summary of task.
    --
    Summary       TEXT NOT NULL,

    --
    -- Longer description of the task.
    --
    Task          TEXT NULL,

    --
    -- Dates should be YYYY-MM-DD.
    --
    DateOfEntry   TEXT NOT NULL,
    DateCompleted TEXT NULL
   )
;

--
-- end of CreateTables.sql.
--
