#! /usr/bin/env python3
#
#
''' Generic DataBase class implements a simple sqlite3 database interface.
'''

import sqlite3

class DataBase(object):

    def __init__(self, parent=None, dbname=None):

        # variables
        self.DBName = None
        self.connection = None
        self.cursor = None
        
        self.setDBName(dbname)
        return self.openDB()

    def setDBName(self, name):
        self.DBName = name

    def getDBName(self):
        return self.DBName

    def isValid(self):
        if self.cursor is not None:
            return True
        else:
            return False

    def openDB(self, name=None):

        if name is not None:
            self.setDBName(name)
            self.connection = sqlite3.connect(name)
        elif self.DBName is not None:
            self.connection = sqlite3.connect(self.DBName)

        if self.connection is not None:
            self.cursor = self.connection.cursor()

        return self.cursor

    def closeDB(self):
        if self.connection is not None:
            self.connection.close()

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
