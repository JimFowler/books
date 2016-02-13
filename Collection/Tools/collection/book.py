'''Stuff that knows about Books within
the Collection database.'''

# -*- mode: python; -*-

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import bookentry.symbol as symbol

import collection.ui_book as ui_book
import collection.selectDialog as selectDialog

# Debugging
import pprint
pp = pprint.PrettyPrinter()

class BookView( QDialog, ui_book.Ui_Dialog):
    '''View the information about a specific  books
    Must be called with _bookId = to a specific Book ID
    or None if you want to create a new book. _db is the
    database we are currently working with.  It doesn't make
    any sense to not pass the _db to the class.
    '''
    def __init__( self, parent=None, _db=None ):
        super(BookView, self).__init__(parent)
        self.setupUi(self)

        self.connect( self.closeButton,
                      SIGNAL('released()'),
                      self.quit )

        self.connect( self.saveButton,
                      SIGNAL('released()'),
                      self.save )

        self.connect( self.deleteButton,
                      SIGNAL('released()'),
                      self.delete )

        self.connect( self.newButton,
                      SIGNAL('released()'),
                      self.new )

        # for a line edit box
        self.connect(self.summaryEdit, SIGNAL('textChanged(QString)'),
                     self.setBookDirty)
        self.connect(self.createdEdit, SIGNAL('textChanged(QString)'),
                     self.setBookDirty)
        self.connect(self.completionEdit, SIGNAL('textChanged(QString)'),
                     self.setBookDirty)

        # for a text edit box
        self.connect(self.descriptionEdit, SIGNAL('textChanged()'),
                     self.setBookDirty)

        self.db = _db
        self.bookId = None
        self.isNew = True
        self.dirty = False


    def setBookDirty(self):
        #print('setBookDirty')
        self.dirty = True

    def clearBookDirty(self):
        #print('clearBookDirty')
        self.dirty = False

    def SaveIfDirty(self):
        #print('SaveIfDirty', self.dirty)
        if self.dirty:
            ans = QMessageBox.warning( self, 'Save  book?',
                                       'Entry has changed. Do you want to save it?',
                                       QMessageBox.Save,
                                       QMessageBox.No,
                                       QMessageBox.Cancel )
            if ans == QMessageBox.Save:
                self.save()

        
    #
    # Button actions
    #
    def delete(self):
        if not self.isNew:
            queryStmt = 'DELETE FROM  WHERE Id = %d;' % (self.bookId)
            # ask yes/no
            ans = QMessageBox.warning( self, 'Delete  book?',
                                       'Are you sure you want to delete this book? This action can not be undone!',
                                       QMessageBox.Yes,
                                       QMessageBox.No )
            if ans == QMessageBox.Yes:
                self.db.execute(queryStmt)
                self.db.commit()
                self.clearBookDirty()
                self.quit()

    def save(self):
        # needs db.cursor or database
        if self.isNew:

            summary = self.summaryEdit.text()
            create = self.createdEdit.text()
            complete = self.completionEdit.text()
            description = self.descriptionEdit.toPlainText()
            # add other info TODO
            queryStmt = 'INSERT INTO  (Summary, Description, DateOfEntry, DateCompleted) VALUES ("%s", "%s", "%s", "%s");' % (summary, description, create, complete)
            self.db.execute(queryStmt)

            # get new book id somehow, requires Name to be unique
            queryStmt = 'SELECT Id FROM  WHERE Summary = "%s";' % (summary)
            res = self.db.execute(queryStmt)
            book = res.fetchone()
            self.bookId = int(book[0])
            self.idLabel.setText(self.bookId)
            self.clearBookDirty()
            self.isNew = False

        elif self.dirty:

            summary = self.summaryEdit.text()
            create = self.createdEdit.text()
            complete = self.completionEdit.text()
            description = self.descriptionEdit.toPlainText()
            queryStmt = "UPDATE  SET Summary = '%s', Book = '%s', DateOfEntry = '%s', DateCompleted = '%s' WHERE VendorId = %d;" % (summary, description, create, completion, self.vendorId)
            print(queryStmt)
            self.db.execute(queryStmt)
            self.clearBookDirty()

        self.db.commit()
        return

    def clearForm(self):
        self.summaryEdit.setText('New To Do Book')
        self.createdEdit.clear()
        self.completionEdit.clear()
        self.descriptionEdit.setText('Enter book description')

    def new(self):
        self.SaveIfDirty()
        self.bookId = None
        self.clearForm()
        self.isNew = True
        self.clearBookDirty()
        
    def quit(self):
        self.SaveIfDirty()
        self.close()


    #
    # various functions to get information about a  Book
    #
    def setBookId(self, _bookId):
        self.SaveIfDirty()
        if _bookId is None:
            # Create a new book
            self.new()
        else:
            # Look up an old book
            search =  'SELECT * from  WHERE Id = %d' % (_bookId)

            res = self.db.execute(search)
            vendor = res.fetchone()
            self.bookId = _bookId
            self.idLabel.setText(    str(vendor[0]))
            self.summaryEdit.setText(    vendor[1] )
            self.descriptionEdit.setText(vendor[2] )
            self.createdEdit.setText(    vendor[3] )
            self.completionEdit.setText( vendor[4] )
            self.isNew = False
            self.clearBookDirty()


        self.show()


class Book(object):
    '''Handle the general Book stuff.  It makes
     no sense to call this class and not pass a database
    as _db to it.'''

    def __init__(self, parent=None, _db=None):

        if _db is None:
            pass

        # A dictionary of VendorName: VendorId
        self.bookDict = {}

        # the database to talk to for information
        # We pass this to our views so they can talk to the
        # database also.
        self.db = _db

        # a book view
        self.view = None
        # but what if we want more than one vendor view???


    def getBooks(self):
        self.booksDict = self.db.getBookDict()
        
    def selectBook(self):
        '''Get list of Vendors and open a selection window so the
        users can pick one.'''
        self.getBooks()
        l = list(self.booksDict.keys())
        
        self.bookSelect = selectDialog.selectDialog(
            _title='To Do Book List',
            _list=l,
            _viewFunction=self.bookView,
            _newFunction=self.bookView)
        
        self.bookSelect.show()
        

    def bookView(self, name):

        if name is not None:
            self.getBooks()
            bookId = self.booksDict[name]
        else:
            bookId = None

        self.view = BookView(_db = self.db)
        self.view.setBookId(bookId)




