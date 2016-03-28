"""Updater class. Provides update signals from low
level windows to higher level windows."""
# -*- mode: Python;-*-

from PyQt4.QtCore import *

class UpDater(QObject):

    def __init__(self):
        super(UpDater, self).__init__()
        return

    def bookListChanged(self):
        # emit signal to anybody who care about Book lists
        self.emit(SIGNAL('bookListChanged'))
        return

    def authorListChanged(self):
        # emit signal to anybody who care about Author lists
        self.emit(SIGNAL('authorListChanged'))
        return

    def vendorListChanged(self):
        # emit signal to anybody who care about Vendor lists
        self.emit(SIGNAL('vendorListChanged'))
        return

    def projectListChanged(self):
        # emit signal to anybody who care about Projects lists
        self.emit(SIGNAL('projectListChanged'))
        return

    def wantListChanged(self):
        # emit signal to anybody who care about Wants lists
        self.emit(SIGNAL('wantListChanged'))
        return

    def todoListChanged(self):
        # emit signal to anybody who care about ToDo task lists
        self.emit(SIGNAL('todoListChanged'))
        return


if __name__ == '__main__':

    class recv(QObject):

        def __init__(self):
            super(recv, self).__init__()
            return

        def bookList():
            print('book list triggered')
            return

        def authorList():
            print('author list triggered')
            return

        def vendorList():
            print('vendor list triggered')
            return

        def projectList():
            print('project list triggered')
            return

        def wantList():
            print('want list triggered')
            return

        def todoList():
            print('ToDo list triggered')
            return


    a = UpDater()
    b = recv()

    b.connect( a, SIGNAL('bookListChanged'),    recv.bookList)
    b.connect( a, SIGNAL('authorListChanged'),  recv.authorList)
    b.connect( a, SIGNAL('vendorListChanged'),  recv.vendorList)
    b.connect( a, SIGNAL('projectListChanged'), recv.projectList)
    b.connect( a, SIGNAL('wantListChanged'),    recv.wantList)
    b.connect( a, SIGNAL('todoListChanged'),    recv.todoList)

    a.bookListChanged()
    a.authorListChanged()
    a.vendorListChanged()
    a.projectListChanged()
    a.wantListChanged()
    a.todoListChanged()
