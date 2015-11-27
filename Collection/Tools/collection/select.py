#! /usr/bin/env python3
#
'''Generic Select dialog class'''

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import collection.ui_select as ui_select

class Select( QDialog, ui_select.Ui_SelectionDialog ):
    """Select is the class which handles the list selection form
    for display of entries from the database.
    """
    def __init__( self, parent=None, _title=None, _list=None,
                  _viewFunction=None, _newFunction=None ):

        super(Select, self).__init__(parent)
        self.setupUi(self)

        #
        # internal variables
        #
        self.currentItem = None
        self.viewFunction = None
        self.newFunction = None

        if _title is not None:
            self.setTitle(_title)

        if _list is not None:
            self.setListEntrys(_list)

        if _viewFunction is not None:
            self.setViewFunction(_viewFunction)

        if _newFunction is not None:
            self.setNewFunction(_newFunction)

        #
        # Signal and Slots
        #
        self.connect(self.itemList_Widget, SIGNAL('itemSelectionChanged()'),
                                                  self.getSelectedItem )
        self.connect(self.itemList_Widget, 
                     SIGNAL('itemDoubleClicked()'),
                     self.doubleClick)

        self.connect(self.view_Button, SIGNAL('released()'), self.viewAction )
        self.connect(self.new_Button, SIGNAL('released()'), self.newAction )
        self.connect(self.close_Button, SIGNAL('released()'), self.close )

        return

    def doubleClick(self, item):
        print('doubleClick called with ', item.text())

    def setTitle(self, title):
        self.selectTitle_Label.setText(ui_select._translate("Dialog", title, None))
        return

    def setViewFunction(self, func):
        '''Set the function to be called with the view button is released
        or an item is doubleClicked.  Functions must take QListWidgetItem
        as an input argument.'''
        self.viewFunction = func
        return

    def setNewFunction(self, func):
        '''Set the function to be called with the New buttons is released.
        The newFUnction will be called with an argument of None.'''
        self.newFunction = func
        return

    def setListEntrys(self, listEntrys):
        '''Set the elements in the QListWidget.  listEntrys must be a list
        of strings.'''
        if isinstance(listEntrys, list):
            #for item in listEntrys:
            self.itemList_Widget.addItems(listEntrys)
            return True
        else:
            print('not list', type(listEntrys), listEntrys)
            return False

    def getSelectedItem(self):
        '''Get the current selected item in the listWidget.'''
        itemlist = self.itemList_Widget.selectedItems()
        # type is QListWidgetItem
        self.currentItem = itemlist[0]

        if self.currentItem is not None:
            print('getSelectedItem:', self.currentItem.text())

        return

    def viewAction(self):
        '''Called when an item is doubleClicked or the View button is pressed.'''
        if self.currentItem is None:
            return
        print('View action:', self.currentItem.text())
        self.viewFunction(self.currentItem)
        
    def newAction(self):
        self.newFunction(None)


if __name__ == '__main__':

    import sys

    def printItem(item):
        '''item is of type QListWidgetItem.'''
        print('printItem() called')
        if item is None:
            print('no item selected')
        else:
            print('Item is ', item.text())

    def newItem(item):
        print('newItem called:')

    testList = []

    app = QApplication(sys.argv)
    app.setApplicationName('Generic Select Test')

    for i in range(20):
        testList.append('item %d' % (i))

    form = Select(_title='My Test Title',
                  _viewFunction=printItem,
                  _newFunction=newItem,
                  _list=testList)

    # or we can explicitly set the title and functions
    #form.setTitle('My Test Title')
    #form.setViewButtonFunction(printItem)
    #form.setNewButtonFunction(newItem)

    form.show()
    sys.exit(app.exec_())


