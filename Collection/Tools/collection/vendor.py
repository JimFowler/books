'''Stuff that knows about vendors within
the Collection database.'''

# -*- mode: python; -*-

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import bookentry.symbol as symbol

import collection.ui_vendor as ui_vendor
import collection.selectDialog as selectDialog

# Debugging
import pprint
pp = pprint.PrettyPrinter()

class VendorView( QDialog, ui_vendor.Ui_Dialog):
    '''View the information about a specific vendor/publisher.
    Must be called with _vendid = to a specific Vendor ID
    or None if you want to create a new vendor. _db is the
    database we are currently working with.  It doesn't make
    any sense to not pass the _db to the class.
    '''
    def __init__( self, parent=None, _db=None ):
        super(VendorView, self).__init__(parent)
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
        self.connect(self.nameEdit, SIGNAL('textChanged(QString)'),
                     self.setVendorDirty)
        self.connect(self.mailAddressEdit, SIGNAL('textChanged(QString)'),
                     self.setVendorDirty)
        self.connect(self.mailCityEdit, SIGNAL('textChanged(QString)'),
                     self.setVendorDirty)
        self.connect(self.mailCodeEdit, SIGNAL('textChanged(QString)'),
                     self.setVendorDirty)
        self.connect(self.mailCountryEdit, SIGNAL('textChanged(QString)'),
                     self.setVendorDirty)
        self.connect(self.shipAddressEdit, SIGNAL('textChanged(QString)'),
                     self.setVendorDirty)
        self.connect(self.shipCityEdit, SIGNAL('textChanged(QString)'),
                     self.setVendorDirty)
        self.connect(self.shipCodeEdit, SIGNAL('textChanged(QString)'),
                     self.setVendorDirty)
        self.connect(self.shipCountryEdit, SIGNAL('textChanged(QString)'),
                     self.setVendorDirty)
        self.connect(self.phoneEdit, SIGNAL('textChanged(QString)'),
                     self.setVendorDirty)
        self.connect(self.faxEdit, SIGNAL('textChanged(QString)'),
                     self.setVendorDirty)
        self.connect(self.urlEdit, SIGNAL('textChanged(QString)'),
                     self.setVendorDirty)
        self.connect(self.emailEdit, SIGNAL('textChanged(QString)'),
                     self.setVendorDirty)

        # for a text edit box
        self.connect(self.descriptionEdit, SIGNAL('textChanged()'),
                     self.setVendorDirty)

        # Get book information
        '''
        self.connect(self.bookList,
                     SIGNAL('itemDoubleClicked(QListWidgetItem*)'),
                     self.getItem)

        self.connect(self.bookList,
                     SIGNAL('itemClicked()'),
                     self.getItem)

        self.connect(self.publishedList,
                     SIGNAL('itemDoubleClicked(QListWidgetItem*)'),
                     self.getItem)

        self.connect(self.publishedList,
                     SIGNAL('itemClicked()'),
                     self.getItem)
                     '''
        self.db = _db
        self.vendorId = None
        self.isNew = True
        self.dirty = False


    def setVendorDirty(self):
        #print('setVendorDirty')
        self.dirty = True

    def clearVendorDirty(self):
        #print('clearVendorDirty')
        self.dirty = False

    def SaveIfDirty(self):
        #print('SaveIfDirty', self.dirty)
        if self.dirty:
            ans = QMessageBox.warning( self, 'Save Vendor/Publisher?',
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
            queryStmt = 'DELETE FROM Vendors WHERE VendorId = %d;' % (self.vendorId)
            # ask yes/no
            ans = QMessageBox.warning( self, 'Delete Vendor/Publisher?',
                                       'Are you sure you want to delete this vendor? This action can not be undone!',
                                       QMessageBox.Yes,
                                       QMessageBox.No )
            if ans == QMessageBox.Yes:
                self.db.execute(queryStmt)
                self.db.commit()
                self.clearVendorDirty()
                self.quit()

    def save(self):
        # needs db.cursor or database
        if self.isNew:

            name = self.NameEdit.text()
            description = self.descriptionEdit.toPlainText()
            # add other info TODO
            queryStmt = 'INSERT INTO Vendors (VendorName, Description) VALUES ("%s", "%s");' % (name, description)
            self.db.execute(queryStmt)

            # get new vendor id somehow, requires Name to be unique
            queryStmt = 'SELECT VendorId FROM Vendors WHERE VendorName = "%s";' % (name)
            res = self.db.execute(queryStmt)
            vendor = res.fetchone()
            self.vendorId = int(vendor[0])
            self.idLabel.setText(self.vendorId)
            self.clearVendorDirty()
            self.isNew = False

        elif self.dirty:

            name = self.nameEdit.text()
            description = self.descriptionEdit.toPlainText()
            # get other info TODO
            queryStmt = "UPDATE Vendors SET VendorName = '%s', Description = '%s' WHERE VendorId = %d;" % (name, description, self.vendorId)
            print(queryStmt)
            self.db.execute(queryStmt)
            self.clearVendorDirty()

        self.db.commit()
        return

    def clearForm(self):
        self.NameEdit.setText('New Vendor/Publisher')
        self.descriptionEdit.setText('Enter vendor description')
        self.mailAddressEdit.clear()
        self.mailCityEdit.clear()
        self.mailStateEdit.clear()
        self.mailCodeEdit.clear()
        self.mailCountryEdit.clear()
        self.shipAddressEdit.clear()
        self.shipCityEdit.clear()
        self.shipStateEdit.clear()
        self.shipCodeEdit.clear()
        self.shipCountryEdit.clear()
        self.phoneEdit.clear()
        self.faxEdit.clear()
        self.emailEdit.clear()
        self.urlEdit.clear()
        # clear other fields TODO
        self.bookList.clear()
        self.publishedList.clear()

    def new(self):
        self.SaveIfDirty()
        self.vendorId = None
        self.clearForm()
        self.isNew = True
        self.clearVendorDirty()
        
    def quit(self):
        self.SaveIfDirty()
        self.close()


    #
    # various functions to get information about a Vendor/Publisher
    #
    def setVendorId(self, _vendorId):
        self.SaveIfDirty()
        if _vendorId is None:
            # Create a new vendor/publisher
            self.new()
        else:
            # Look up an old vendor/publisher
            # get other info TODO
            search =  'SELECT * from Vendors WHERE VendorId = %d' % (_vendorId)

            res = self.db.execute(search)
            vendor = res.fetchone()
            self.vendorId = _vendorId
            self.idLabel.setText(str(vendor[0]))
            self.nameEdit.setText(   vendor[1] )
            self.mailAddressEdit.setText(vendor[2] )
            self.mailCityEdit.setText(   vendor[3] )
            self.mailStateEdit.setText(  vendor[4] )
            self.mailCountryEdit.setText(vendor[5] )
            self.mailCodeEdit.setText(   vendor[6] )
            self.shipAddressEdit.setText(vendor[7] )
            self.shipCityEdit.setText(   vendor[8] )
            self.shipStateEdit.setText(  vendor[9] )
            self.shipCountryEdit.setText(vendor[10] )
            self.shipCodeEdit.setText(   vendor[11] )
            self.phoneEdit.setText(  vendor[12] )
            self.faxEdit.setText(    vendor[13] )
            self.emailEdit.setText(  vendor[14] )
            self.urlEdit.setText(    vendor[15] )
            self.descriptionEdit.setText( vendor[16] )
            # grab other info TODO
            self.isNew = False
            self.getPublishedList(_vendorId)
            self.getPurchasedList(_vendorId)
            self.clearVendorDirty()


        self.show()

    def getPurchasedList(self, _vendorId):
        self.bookspurchased = self.db.getBooksPurchasedFromVendor(_vendorId)
        for b in self.bookspurchased:
            if b[3] == '':
                name = b[2]
            else:
                name = b[3]

            ent = '%s,   %s,   %s' % (b[0], name, b[1])
            self.bookList.addItem(ent)

            
    def getPublishedList(self, _vendorId):
        self.bookspublished = self.db.getBooksPublishedByVendor(_vendorId)
        for b in self.bookspublished:
            if b[3] == '':
                name = b[2]
            else:
                name = b[3]

            ent = '%s,   %s,   %s' % (b[0], name, b[1])
            self.publishedList.addItem(ent)

            
    def getPurchasedItem(self, item):
        #print('VendorView: getPurchasedItem called with:')
        #print(item.text())
        row = self.bookList.currentRow()
        #print('row is', row, 'item should be')
        #print(self.bookproj[row])
        bookId = self.bookpurchased[row][4]
        print('calling bookView with bookId %d and title %s' % (bookId, self.bookpurchased[row][0]))
        #call book view with bookId

    def getPublishedItem(self, item):
        #print('VendorView: getPublishedItem called with:')
        #print(item.text())
        row = self.publishedList.currentRow()
        #print('row is', row, 'item should be')
        #print(self.bookproj[row])
        bookId = self.bookpurchased[row][4]
        print('calling bookView with bookId %d and title %s' % (bookId, self.bookpurchased[row][0]))
        #call book view with bookId


class Vendor(object):
    '''Handle the general vendor stuff.  It makes
     no sense to call this class and not pass a database
    as _db to it.'''

    def __init__(self, parent=None, _db=None):

        if _db is None:
            pass

        # A dictionary of VendorName: VendorId
        self.vendorDict = {}

        # the database to talk to for information
        # We pass this to our views so they can talk to the
        # database also.
        self.db = _db

        # a vendor view
        self.view = None
        # but what if we want more than one vendor view???


    def getVendors(self):
        self.vendorDict = self.db.getVendorDict()
        
    def selectVendor(self):
        '''Get list of Vendors and open a selection window so the
        users can pick one.'''
        self.getVendors()
        l = list(self.vendorDict.keys())
        l.sort()
        
        self.vendorSelect = selectDialog.selectDialog(
            _title='Vendor/Publisher List',
            _list=l,
            _viewFunction=self.vendorView,
            _newFunction=self.vendorView)
        
        self.vendorSelect.show()
        

    def vendorView(self, name):

        if name is not None:
            self.getVendors()
            vendorId = self.vendorDict[name]
        else:
            vendorId = None

        self.view = VendorView(_db = self.db)
        self.view.setVendorId(vendorId)




