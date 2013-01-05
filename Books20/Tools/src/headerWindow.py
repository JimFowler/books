"""A window for editing the header section of bookfiles.

Need a dirty flag and dialog if exiting w/o save after changes have
been made.

Cancel button closes w/o asking or saving
Ok button saves and closes.

Close menu item askes to save if file is dirty.
Need a handle to a bookfile to get/set the header text. bookfile is the storage place for the header.
"""

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class HeaderWindow(QtGui.QDialog):
    def __init__(self, MainWindow, bf=None):
        super(HeaderWindow, self).__init__()

        self.initUI()
        self.setBookFile(bf)

    def initUI(self):
        #self.statusBar().showMessage('Ready')

        self.setGeometry(0, 0, 770,505)
        self.setWindowTitle('Edit Header -')

        self.verticalLayoutWidget = QtGui.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 771, 501))
        self.verticalLayoutWidget.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding )
        #self.setCentralWidget(self.verticalLayoutWidget)

        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 10)

        self.headerEntry = QtGui.QTextEdit(self.verticalLayoutWidget)
        self.headerEntry.setObjectName(_fromUtf8("headerEntry"))
        self.headerEntry.textChanged.connect(self.setDirty)
        self.verticalLayout.addWidget(self.headerEntry)


        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancelButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.cancelButton.setText('Cancel')
        self.cancelButton.setToolTip('Discard changes and close window')
        self.cancelButton.clicked.connect(self.noSaveClose)
        self.horizontalLayout.addWidget(self.cancelButton)
        self.okButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.okButton.setText('Ok')
        self.okButton.setToolTip('Save changes and close window')
        self.okButton.clicked.connect(self.SaveClose)
        self.horizontalLayout.addWidget(self.okButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        #self.addWidget(self.verticalLayout)
        '''saveAction =  QtGui.QAction(QtGui.QIcon('exit24.png'), '&Save', self)
        saveAction.setStatusTip('Save the header text')
        saveAction.triggered.connect(self.saveHeaderText)

        exitAction = QtGui.QAction(QtGui.QIcon('exit24.png'), '&Close', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Close edit window')
        exitAction.triggered.connect(self.AskAndClose)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        #self.toolbar = self.addToolBar('Exit')
        #self.toolbar.addAction(exitAction)
        '''

    def setFileName(self, file):
        self.setWindowTitle('Edit Header - %s'%file)

    def setBookFile(self, bf):
        self.bookfile = bf

    def saveHeaderText(self):
        if self.bookfile:
            self.bookfile.setHeader(self.getHeaderText())
            self.clearDirty()

    def AskAndClose(self):
        if self.getDirty() == True:
            resp = QtGui.QMessageBox.warning(self, "Warning",
             '''The header has been modified\n
                Do you want to save your changes?''',
                                             QtGui.QMessageBox.Save,
                                             QtGui.QMessageBox.Discard,
                                             QtGui.QMessageBox.Cancel )
            if resp == QtGui.QMessageBox.Save:
                self.SaveClose()
            elif resp == QtGui.QMessageBox.Discard:
                self.noSaveClose()
            elif resp == QtGui.QMessageBox.Cancel:
                return

 
    def SaveClose(self):
        self.saveHeaderText()
        self.close()

    def noSaveClose(self):
        # restore the current header before closing
        self.setHeaderText(self.bookfile.getHeader())
        self.close()
    
    def setDirty(self):
        self.dirty = True

    def clearDirty(self):
        self.dirty = False

    def getDirty(self):
        return self.dirty

    def setHeaderText(self, textstr):
        self.headerEntry.setPlainText(textstr)
        self.clearDirty()

    def getHeaderText(self):
        return self.headerEntry.toPlainText()


#
# Test functions
#
def main():
    app = QtGui.QApplication(sys.argv)
    ex = HeaderWindow()
    bf = BookFile()
    ex.setBookFile(bf)
    ex.setHeaderText(bf.getHeader())
    ex.show()
    app.exec_()

    print('The Header is:')
    print(bf.getHeader())

if __name__ == '__main__':
    import sys
    from bookfile import *
    main()

