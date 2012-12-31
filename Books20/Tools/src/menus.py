"""Create the menus for the AJB BookEntry window
"""
# -*- mode: Python;-*-

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

def createAction(self, text, slot=None, shortcut=None, icon=None,
                 tip=None, checkable=False, signal="triggered()"):
    """Usage: createAction( self, text, slot=None, shortcut=None, icon=None,
                            tip=None, checkable=False, signal="triggered")
    """
    action = QAction(text, self)                                  
    if icon is not None:                                          
        action.setIcon(QIcon(":/{0}.png".format(icon)))           
    if shortcut is not None:                                      
        action.setShortcut(shortcut)                              
    if tip is not None:                                           
        action.setToolTip(tip)                                    
        action.setStatusTip(tip)                                  
    if slot is not None:                                          
        self.connect(action, SIGNAL(signal), slot)
    else:
        action.enabled = False
    if checkable:                                                 
        action.setCheckable(True)                                 
    return action                                                 


def createMenus( self, menuBar):

        # set up the File menus
        fileMenu = menuBar.addMenu('&File')


        newFileAction = createAction( self, '&New',
                                       self.openNew, 'Ctrl+N' )
        openFileAction = createAction( self, '&Open',
                                       self.openFile, 'Ctrl+O' )
        saveAction = createAction( self, '&Save', self.saveFile, 'Ctrl-S')
        saveAsAction = createAction( self, 'Save &As...', self.saveFileAs, '')
        printAction = createAction( self, '&Print Entry...', self.printEntry, 'Ctrl+P')
        exitAction = createAction(self, '&Quit', self.quit, 'Ctrl+Q', 'filequit',
                     'Close the Application')

        fileMenu.addAction(newFileAction)
        fileMenu.addAction(openFileAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addAction(printAction)
        fileMenu.addAction(exitAction)




        # set up the Edit menus, Cut, Copy, Paste, Delete  make gray
        cutAction = createAction(self, 'Cu&t', None, 'Ctrl+X')
        copyAction = createAction(self, '&Copy', None, 'Ctrl+C') 
        pasteAction = createAction(self, '&Paste', None, 'Ctrl+V')
        deleteAction = createAction(self, '&Delete', None, 'Del')
        symbolAction = createAction(self, '&Insert Symbol...', None, 'Ctrl+I')
        headerAction = createAction(self, 'Edit &Header', None, 'Ctrl+H')

        editMenu = menuBar.addMenu('&Edit')
        editMenu.addAction( cutAction)
        editMenu.addAction( copyAction ) 
        editMenu.addAction( pasteAction )
        editMenu.addAction( deleteAction)
        editMenu.addSeparator()
        editMenu.addAction( symbolAction)
        editMenu.addAction( headerAction)



        # set up the Help menus
        helpMenu = menuBar.addMenu('&Help')
        aboutAction = createAction(self, '&About Book Entry...',
                                   self.helpAbout )
        helpMenu.addAction(aboutAction)
