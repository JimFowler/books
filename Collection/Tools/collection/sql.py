#! /usr/bin/env python3
#
#  Test scripts for the Python interface to SQL Lite 3.
#
#

import sqlite3

import collection.database as database

class collectionDB(database.DataBase):
    
    def __init__(self, parent=None, _dbname=None):
        super(collectionDB, self).__init__(parent)

        self.cursor = self.openDB(_dbname)



#
# Self Test
#
if __name__ == '__main__':

    import sys, os
    
    Query = 'SELECT ProjName, ProjectId FROM Projects ORDER BY ProjName;'
    Query2 = 'SELECT * FROM Projects WHERE ProjName == "History of Spectroscopy"';

    db = collectionDB(_dbname='/home/jrf/Documents/books/Collection/Collection.db3')
    name = db.getDBName()

    if db.isValid():
        print('%s is valid DB' % (name))
    else:
        print('Error sql.py: db is not valid DB!')
        sys.exit(-1)

    db.closeDB()

    db = collectionDB()

    name = db.getDBName()
    
    if db.isValid():
        print('%s is valid DB' % (name))
    else:
        print('Error sql.py: db is not valid DB!')
        sys.exit(-1)

    db.closeDB()
    #result = cur.execute(Query)
    #for row in result:
    #    pp.pprint(row)



