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


        #newFileAction = createAction( self, '&New File',
        #                               self.openNewFile, 'Ctrl+N' )
        #openFileAction = createAction( self, '&Open File...',
        #                               self.askOpenFile, 'Ctrl+O' )
        #saveAction = createAction( self, '&Save File',
        #                           self.saveFile, 'Ctrl+S')
        #saveAsAction = createAction( self, 'Save File &As...',
        #                             self.saveFileAs, 'Ctrl+A')
        #newEntAction = createAction( self, 'New &Entry',
        #                             self.newEntry, 'Ctrl+E')
        #saveEntAction = createAction( self, 'Save Ent&ry', 
        #                              self.saveEntry, 'Ctrl+R' )
        #printAction = createAction( self, '&Print Entry', self.printEntry,
        #                            'Ctrl+P')
        exitAction = createAction(self, '&Quit', self.quit, 'Ctrl+Q',
                                  'filequit', 'Close the Application')

        #fileMenu.addAction(newFileAction)
        #fileMenu.addAction(openFileAction)
        #fileMenu.addAction(saveAction)
        #fileMenu.addAction(saveAsAction)
        #fileMenu.addSeparator()
        #fileMenu.addAction(newEntAction)
        #fileMenu.addAction(saveEntAction)
        #fileMenu.addAction(printAction)
        #fileMenu.addSeparator()
        fileMenu.addAction(exitAction)




        # set up the Edit menus, Cut, Copy, Paste, Delete  make gray
        cutAction = createAction(self, 'Cu&t', None, 'Ctrl+X')
        cutAction.setEnabled(False)
        copyAction = createAction(self, '&Copy', None, 'Ctrl+C') 
        copyAction.setEnabled(False)
        pasteAction = createAction(self, '&Paste', None, 'Ctrl+V')
        pasteAction.setEnabled(False)
        deleteAction = createAction(self, '&Delete', None, 'Del')
        deleteAction.setEnabled(False)
        addInfoAction = createAction(self, 'Additional &Info...',
                                     None, 'Ctrl+T')
        symbolAction = createAction(self, '&Insert Symbol...', self.openSymbol, 'Ctrl+I')
        #headerAction = createAction(self, 'Edit &Header...',
        #                            self.editHeader, 'Ctrl+H')
        #origstrAction = createAction(self, 'Show Original String',
        #                            self.showOrigStr)
        #setvolnumAction = createAction(self, 'Set Volume Number...',
        #                            self.setVolumeNumberInteractive)

        #fontsizeAction = createAction(self, 'Set font size...', None, None)
        #fontsizeAction.setEnabled(False)

        #fonttypeAction = createAction(self, 'Set font...', None, None)
        #fonttypeAction.setEnabled(False)


        editMenu = menuBar.addMenu('&Edit')
        editMenu.addAction( cutAction)
        editMenu.addAction( copyAction ) 
        editMenu.addAction( pasteAction )
        editMenu.addAction( deleteAction)
        editMenu.addSeparator()
        editMenu.addAction( symbolAction)
        #editMenu.addAction( headerAction)
        #editMenu.addAction( origstrAction)
        #editMenu.addAction( setvolnumAction)
        #editMenu.addAction( fontsizeAction)
        #editMenu.addAction( fonttypeAction)



        # set up the Help menus
        helpMenu = menuBar.addMenu('&Help')
        aboutAction = createAction(self, '&About Collections...',
                                   self.helpAbout )
        helpMenu.addAction(aboutAction)
