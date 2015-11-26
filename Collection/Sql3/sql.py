#! /usr/bin/env python3
#
#  Test scripts for the Python interface to SQL Lite 3.
#
#

import os, sys
import sqlite3

# Debugging
import pprint
pp = pprint.PrettyPrinter()

Database = 'Collection.db3'

conn = sqlite3.connect(Database)
cur = conn.cursor()

Query = 'SELECT ProjName, ProjectId FROM Projects ORDER BY ProjName;'
Query2 = 'SELECT * FROM Projects WHERE ProjName == "History of Spectroscopy"';

#
# This does not work.  Note that cur, result, and result2 all point
#   to the same object.
#
result = cur.execute(Query)
#result2 = cur.execute(Query2)
# This will print the rows from Query2
for row in result:
    pp.pprint(row)

# select books under the project Astronomcal Lives, project id = 4.  Need 
# to learn better SQL as this query selects all books that are associated with a project

BookProjOrig = '''SELECT BookProject.ProjectID, Projects.ProjName, BookProject.BookID, BookAuthor.AsWritten, Authors.LastName, Authors.FirstName, Books.Title, Books.Copyright, Books.Edition, Books.Printing, Books.PurchaseDate, Books.PurchasePrice, Books.PurchasedFrom, Books.PublishedAt, Books.Publisher, Books.MyCondition, Books.Description
FROM Projects INNER JOIN ((Books INNER JOIN (Authors INNER JOIN BookAuthor ON Authors.AuthorID = BookAuthor.AuthorID) ON Books.BookID = BookAuthor.BookID) INNER JOIN BookProject ON Books.BookID = BookProject.BookID) ON Projects.ProjectID = BookProject.ProjectID
WHERE (((BookAuthor.Priority)=1))
ORDER BY Books.Copyright;'''

BookProj = '''SELECT BookProject.ProjectID, Projects.ProjName, BookProject.BookID, BookAuthor.AsWritten, Authors.LastName, Authors.FirstName, Books.Title, Books.Copyright, Books.Edition, Books.Printing, Books.PurchaseDate, Books.PurchasePrice, Books.PurchasedFrom, Books.PublishedAt, Books.Publisher, Books.MyCondition, Books.Description
FROM Projects INNER JOIN ((Books INNER JOIN (Authors INNER JOIN BookAuthor ON Authors.AuthorID = BookAuthor.AuthorID) ON Books.BookID = BookAuthor.BookID) INNER JOIN BookProject ON Books.BookID = BookProject.BookID) ON Projects.ProjectID = 4
WHERE (((BookAuthor.Priority)=1))
ORDER BY Books.Copyright;'''

cur.execute(BookProj)
count = 0
for row in cur:
    pp.pprint(row)
    count += 1
print(count)

