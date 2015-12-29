#! /usr/bin/env python3
#
#  Scripts for the Python interface to SQL Lite 3.
#
#
'''The specific database class for talking to the Collection.db3 database.
This is a subclass of database.DataBase().'''

import sqlite3

import collection.database as database

class collectionDB(database.DataBase):
    '''The handler for Collection.db3'''
    def __init__(self, parent=None, _dbname=None):
        super(collectionDB, self).__init__(parent=parent)
        if _dbname is not None:
            self.open(_dbname)

    def open(self, name):
        '''Open the named database if possible. Returns True if successful
        or False otherwise.'''
        self.cursor = self.openDB(name)
        if self.cursor is None:
            return False
        else:
            return True

    def execute(self, sqlStmt):
        '''Execute arbitrary SQL statement. Returns the cursor '''
        return self.cursor.execute(sqlStmt)

    def getAuthorDict(self):
        '''Get the list of projects from the database. Return a dictionary
        of {'LastName, FirstName': AuthorId.}'''
        self.cursor.execute('SELECT * FROM viewAllAuthorNames;')
        d = {}
        tlist = self.cursor.fetchall()
        for t in tlist:
            name = str(t[0]) + ', ' + str(t[1]) 
            d[name ] = t[2]

        return d

    def getVendorDict(self):
        '''Get the list of vendors from the database. Return a dictionary
        of {VendorName: VendorId.}'''
        return self.getList('SELECT * FROM viewAllVendorNames;')

    def getProjectDict(self):
        '''Get the list of projects from the database. Return a dictionary
        of {ProjectName: ProjectId.}'''
        return self.getList('SELECT * FROM viewAllProjectNames;')

    def getToDoDict(self):
        '''Get the list of projects from the database. Return a dictionary
        of {Summary: ToDoId.}'''
        return self.getList('SELECT * FROM viewAllToDoTasks;')

    def getList(self, sqlStatement):
        self.cursor.execute(sqlStatement)
        d = {}
        tlist = self.cursor.fetchall()
        for t in tlist:
            d[str(t[0])] = t[1]

        return d

    def getBooksInProject(self, _projId):
        projId = int(_projId)
        books = self.cursor.execute("SELECT Books.Title, Books.Copyright, Authors.LastName, BookAuthor.AsWritten, Books.BookId FROM Authors INNER JOIN (BookAuthor INNER JOIN (Books INNER JOIN BookProject ON BookProject.ProjectId = ?) ON BookProject.BookId = Books.BookId) ON Books.BookId = BookAuthor.BookId WHERE BookAuthor.AuthorId = Authors.AuthorId and BookAuthor.Priority = 1 ORDER BY Books.Copyright;", (_projId,))

        

        return self.cursor.fetchall()

    
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


