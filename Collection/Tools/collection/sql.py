#! /usr/bin/env python3
#
#  Scripts for the Python interface to SQL Lite 3.
#
#

import sqlite3

import collection.database as database

class collectionDB(database.DataBase):
    
    def __init__(self, parent=None, _dbname=None):
        super(collectionDB, self).__init__(parent)
        if _dbname is not None:
            self.open(_dbname)

    def open(self, name):
        self.cursor = self.openDB(name)
        if self.cursor is None:
            return False
        else:
            return True

    def getAuthorDict(self):
        '''get the list of projects from the database. Return a dictionary
        of {'LastName, FirstName': AuthorId.}'''
        self.cursor.execute('SELECT * FROM viewAllAuthorNames;')
        d = {}
        tlist = self.cursor.fetchall()
        for t in tlist:
            name = str(t[0]) + ', ' + str(t[1]) 
            d[name ] = t[2]

        return d

    def getVendorDict(self):
        '''get the list of vendors from the database. Return a dictionary
        of {VendorName: VendorId.}'''
        return self.getList('SELECT * FROM viewAllVendorNames;')

    def getProjectDict(self):
        '''get the list of projects from the database. Return a dictionary
        of {ProjectName: ProjectId.}'''
        return self.getList('SELECT * FROM viewAllProjectNames;')

    def getToDoDict(self):
        '''get the list of projects from the database. Return a dictionary
        of {Summary: ToDoId.}'''
        return self.getList('SELECT * FROM viewAllToDoTasks;')

    def getList(self, sqlStatement):
        self.cursor.execute(sqlStatement)
        d = {}
        tlist = self.cursor.fetchall()
        for t in tlist:
            d[str(t[0])] = t[1]

        return d

#
# Self Test
#
if __name__ == '__main__':

    import sys, os
    
    Query2 = 'SELECT * FROM Projects WHERE ProjName == "History of Spectroscopy"';

    db = collectionDB()
    name = db.getDBName()
    
    if db.isValid():
        print('%s is valid DB' % (name))
    else:
        print('Error sql.py: db is not valid DB!')

    db.closeDB()

    db.open('/home/jrf/Documents/books/Collection/Collection.db3')
    name = db.getDBName()

    if db.isValid():
        print('%s is valid DB' % (name))
    else:
        print('Error sql.py: db is not valid DB!')

    pdict = db.getToDoList()
    for p in pdict:
        print(p, pdict[p])

    print(pdict.keys())
    #result = cur.execute(Query)
    #for row in result:
    #    pp.pprint(row)

    db.closeDB()


