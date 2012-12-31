Operation
*********

The **BookEntry** program may be started from the command line with
the ``BookEntry`` command. The main display window looks like:

.. image:: mainwindow.png

The main features are the top line with the Index number and the AJB
number along with the buttons to switch between existing records, the
main entry information from Authors to Comments, and the ``Accept``
button on the right hand side.

Command Line Arguments
======================

BookEntry [-h] [-v] [filename]

  -h --help -- print this usage message and then exit

  -v --version -- print the current version and then exits

  filename -- open an existing file and reads the entries

Menus
=====

Many of the menus are standard and should be familar to most users.  


File
----

**New**:

**Open**: Selecting the Open option brings up a file section dialog
box that allows one to select an existing file. The file name will be
displayed in the window title bar. Files are opened either to check
the entries in the file or to add additional entries to the file.  The
form will display the last entry. Simply click the ``Accept`` button
to bring up a blank entry item to be filled in. Alternatively use the
``Next`` and ``Previous`` buttons under the ``Index`` number to step
through the records in order verify the records have been properly
entered.

**Save**: If the entries were opened through an existing file either via
the command line or the **Open** menu item, then write the existing
entries to that file.  If the entries are a new file, then open the save-as
dialog to get the new file name.

**Save As**: Bring up a dialog box requesting a file name in which to
save the existing entries.  If the file already existed, the user will
be asked for confirmation before overwriting the file.

**Print Entry**:

**Quit**: Close the window and quits the application.  If there are
unsaved changes to the entries the user will be asked to save the
changes first.


Edit
----

**Cut**:

**Copy**:

**Paste**:

**Insert Symbol**:

**Edit Header**:

Help
----

**About BookEntry**: brings up a dialog box with basic information
about the program, the author, and the run-time environment.

