#! /usr/bin/env python3
#
#
'''The DataBase class implements a simple sqlite3 database interface. This
provides a parent class for more particular database classes
'''

import sqlite3

class DataBase(object):
    '''A generic interface to an SQLite3 database.'''
    def __init__(self, parent=None, dbname=None):

        # variables
        self.DBName = None
        self.connection = None
        self.cursor = None
        
        self.setDBName(dbname)
        return self.openDB()

    def setDBName(self, name):
        '''Sets the filename of the current open database.'''
        self.DBName = name

    def getDBName(self):
        '''Returns the filename of the current open database.'''
        return self.DBName

    def isValid(self):
        '''Return True is a database is open and there is a valid
        cursor object.'''
        if self.cursor is not None:
            return True
        else:
            return False

    def openDB(self, _name=None):
        '''Open an sqlite3 database file named _name. If _name is not
        given, then we try to open the filename in the varialbles
        self.DBName. Returns the cursor to the calling function or
        None if it could not open the database.  The child class
        should use this cursor to interogate the database. Really
        should provide some diagnostic information if it can't open
        the database.'''
        self.closeDB()

        if _name is not None:
            self.setDBName(_name)
            self.connection = sqlite3.connect(_name)
        elif self.DBName is not None:
            self.connection = sqlite3.connect(self.DBName)
        else:
            return None

        if self.connection is not None:
            self.cursor = self.connection.cursor()

        return self.cursor

    def commit(self):
        '''Commit current changes to the database. If this is not
        called before closing, all changes will not be written to the
        disk file. This is a Python sqlite3 feature.'''
        if self.connection is not None:
            self.connection.commit()

    def closeDB(self):
        '''Close any open database. Reset the connection, cursor
        and name variables.'''
        if self.connection is not None:
            self.connection.commit()
            self.connection.close()

        self.setDBName(None)
        self.cursor = None
        self.connection = None

#
# Self Test
#
if __name__ == '__main__':

    import pprint
    pp = pprint.PrettyPrinter()

    # create a database with data

    # and test queries on it

#
# End of database.py
#
