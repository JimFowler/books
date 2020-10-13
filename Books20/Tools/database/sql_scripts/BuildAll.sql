-- BuildAll the initial database for the journal
--
-- Begin copyright
--
--  /home/jrf/Documents/books/Books20/Tools/sqlite/scripts/BuildAll.sql
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
--  invoke as sqlite3 journals.db3
--     .read ./Tools/sqlite/scripts/BuildAll
--
.read   ./Tools/sqlite/scripts/CreateTables.sql
-- .separator |
-- .import ./Data/Vendors.txt Vendors
-- .import ./Data/Authors.txt Authors
-- .import ./Data/Projects.txt Projects
-- .import ./Data/Books.txt Books
-- .import ./Data/Wanted.txt Wants
-- .import ./Data/BookAuthor.txt BookAuthor
-- .import ./Data/BookProject.txt BookProject
-- .import ./Data/ToDo.txt ToDo
-- .read   ./Tools/sqlite/scripts/CreateViews.sql
--
--   End of BuildAll
--