'''Stuff that knows about authors within
the Collection database.'''

# -*- mode: python; -*-

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import bookentry.symbol as symbol

import collection.ui_author as ui_author
import collection.selectDialog as selectDialog

# Debugging
import pprint
pp = pprint.PrettyPrinter()

class AuthorView( QDialog, ui_author.Ui_authorDialog):
    '''View the information about a specific authors
    Must be called with _authorId = to a specific Author ID
    or None if you want to create a new author. _db is the
    database we are currently working with.  It doesn't make
    any sense to not pass the _db to the class.
    '''
    def __init__( self, parent=None, _db=None ):
        super(AuthorView, self).__init__(parent)
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
        self.connect(self.lastNameEdit, SIGNAL('textChanged(QString)'),
                     self.setAuthorDirty)
        self.connect(self.firstNameEdit, SIGNAL('textChanged(QString)'),
                     self.setAuthorDirty)
        self.connect(self.middleNameEdit, SIGNAL('textChanged(QString)'),
                     self.setAuthorDirty)
        self.connect(self.bornEdit, SIGNAL('textChanged(QString)'),
                     self.setAuthorDirty)
        self.connect(self.diedEdit, SIGNAL('textChanged(QString)'),
                     self.setAuthorDirty)

        # for a text edit box
        self.connect(self.commentsEdit, SIGNAL('textChanged()'),
                     self.setAuthorDirty)

        # Get book information
        '''
        self.connect(self.bookList,
                     SIGNAL('itemDoubleClicked(QListWidgetItem*)'),
                     self.getItem)

        self.connect(self.bookList,
                     SIGNAL('itemClicked()'),
                     self.getItem)
        '''
        self.db = _db
        self.authorId = None
        self.isNew = True
        self.dirty = False


    def setAuthorDirty(self):
        #print('setAuthorDirty')
        self.dirty = True

    def clearAuthorDirty(self):
        #print('clearAuthorDirty')
        self.dirty = False

    def SaveIfDirty(self):
        #print('SaveIfDirty', self.dirty)
        if self.dirty:
            ans = QMessageBox.warning( self, 'Save Author?',
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
            queryStmt = 'DELETE FROM Authors WHERE AuthorId = %d;' % (self.authorId)
            # ask yes/no
            ans = QMessageBox.warning( self, 'Delete Author?',
                                       'Are you sure you want to delete this author? This action can not be undone!',
                                       QMessageBox.Yes,
                                       QMessageBox.No )
            if ans == QMessageBox.Yes:
                self.db.execute(queryStmt)
                self.db.commit()
                self.clearAuthorDirty()
                self.quit()

    def save(self):
        # needs db.cursor or database
        if self.isNew:

            name = self.NameEdit.text()
            description = self.descriptionEdit.toPlainText()
            # add other info TODO
            queryStmt = 'INSERT INTO Authors LastName, Description) VALUES ("%s", "%s");' % (name, description)
            self.db.execute(queryStmt)

            # get new author id somehow, requires Name to be unique
            queryStmt = 'SELECT AuthorId FROM Author WHERE LastName = "%s";' % (name)
            res = self.db.execute(queryStmt)
            author = res.fetchone()
            self.authorId = int(author[0])
            self.idLabel.setText(self.authorId)
            self.clearAuthorDirty()
            self.isNew = False

        elif self.dirty:

            name = self.nameEdit.text()
            description = self.descriptionEdit.toPlainText()
            # get other info TODO
            queryStmt = "UPDATE Authors SET LastName = '%s', Description = '%s' WHERE AuthorId = %d;" % (name, description, self.authorId)
            print(queryStmt)
            self.db.execute(queryStmt)
            self.clearAuthorDirty()

        self.db.commit()
        return

    def clearForm(self):
        self.idLabel.setText('')
        self.NameEdit.setText('New Author')
        self.descriptionEdit.setText('Enter author description')
        self.lastNameEdit.clear()
        self.firstNameEdit.clear()
        self.middleNameEdit.clear()
        self.bornEdit.clear()
        self.diedEdit.clear()
        self.commentsEdit.clear()
        self.urlEdit.clear()

        self.bookList.clear()

    def new(self):
        self.SaveIfDirty()
        self.authorId = None
        self.clearForm()
        self.isNew = True
        self.clearAuthorDirty()
        
    def quit(self):
        self.SaveIfDirty()
        self.close()


    #
    # various functions to get information about a Author
    #
    def setAuthorId(self, _authorId):
        self.SaveIfDirty()
        if _authorId is None:
            # Create a new author
            self.new()
        else:
            # Look up an old author
            # get other info TODO
            search =  'SELECT * from Authors WHERE AuthorId = %d' % (_authorId)

            res = self.db.execute(search)
            author = res.fetchone()
            self.authorId = _authorId
            self.idLabel.setText(   str(author[0]))
            self.lastNameEdit.setText(  author[1] )
            self.middleNameEdit.setText(author[2] )
            self.firstNameEdit.setText( author[3] )
            self.bornEdit.setText(      author[4] )
            self.diedEdit.setText(      author[5] )
            self.commentsEdit.setText(  author[6] )

            # grab other info TODO
            self.isNew = False
            self.getPublishedList(_authorId)
            self.clearAuthorDirty()

        self.show()

            
    def getPublishedList(self, _authorId):
        self.bookspublished = self.db.getBooksAssociatedByAuthor(_authorId)
        for b in self.bookspublished:
            ent = '%s,   %s,   %s' % (b[0], b[1], b[2])
            self.bookList.addItem(ent)

            

    def getPublishedItem(self, item):
        #print('AuthorView: getPublishedItem called with:')
        #print(item.text())
        row = self.publishedList.currentRow()
        #print('row is', row, 'item should be')
        #print(self.bookproj[row])
        bookId = self.bookpurchased[row][4]
        print('calling bookView with bookId %d and title %s' % (bookId, self.bookpurchased[row][0]))
        #call book view with bookId


class Author(object):
    '''Handle the general Author stuff.  It makes
     no sense to call this class and not pass a database
    as _db to it.'''

    def __init__(self, parent=None, _db=None):

        if _db is None:
            pass

        # A dictionary of AuthorName: AuthorId
        self.authorDict = {}

        # the database to talk to for information
        # We pass this to our views so they can talk to the
        # database also.
        self.db = _db

        # a author view
        self.view = None
        # but what if we want more than one author view???


    def getAuthors(self):
        self.authorDict = self.db.getAuthorDict()
        
    def selectAuthor(self):
        '''Get list of Authors and open a selection window so the
        users can pick one.'''
        self.getAuthors()
        l = list(self.authorDict.keys())
        l.sort()
        
        self.authorSelect = selectDialog.selectDialog(
            _title='Authors List',
            _list=l,
            _viewFunction=self.authorView,
            _newFunction=self.authorView)
        
        self.authorSelect.show()
        

    def authorView(self, name):

        if name is not None:
            self.getAuthors()
            authorId = self.authorDict[name]
        else:
            authorId = None

        self.view = AuthorView(_db = self.db)
        self.view.setAuthorId(authorId)




