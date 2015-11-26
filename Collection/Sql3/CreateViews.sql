--
-- CreateViews.sql
--
-- Created 24 November 2015
--   James R. Fowler
--
-- Create the basic views required for the Collection database.
--  Views are dynamic data sets that will be used frequently.
--
-- To Use:
--    $ sqlite3 Collection.db3
--       .read CreateViewss.sql
--
--
-- The last known changes were checked in by $Author$
-- as revision $LastChangedRevision$
-- on $Date$
--
--

CREATE VIEW viewAllProjectNames AS 
       SELECT ProjectName, ProjectId
       FROM Projects
       ORDER BY ProjectName;

CREATE VIEW viewAllVendorNames AS 
       SELECT VendorName, VendorId
       FROM Vendors
       ORDER BY VendorName;




--
-- end of CreateTables.sql
--
