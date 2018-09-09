## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/bookentry/menus.py
##  
##   Part of the Books20 Project
##
##   Copyright 2018 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrival system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright


"""Create the menus for the AJB BookEntry window
"""
try:
    from PyQt5.QtCore import *
    from PyQt5.QtGui  import *
    from PyQt5.QtWidgets import *
except:
    from PyQt4.QtCore import *
    from PyQt4.QtGui  import *
    
def createAction(self, text, slot=None, shortcut=None, icon=None,
                 tip=None, checkable=False, signal='triggered'):
    """Usage: createAction( self, text, slot=None, shortcut=None, icon=None,
                            tip=None, checkable=False, signal="triggered")
         Note: the vars 'slot', 'shortcut', 'icon', 'tip',
               and 'signal' should be of type string.
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
        #self.connect(action, SIGNAL(signal), slot)
        eval( 'action.' + signal + '.connect(' + slot + ')' )
    else:
        action.enabled = False
    if checkable:                                                 
        action.setCheckable(True)                                 
    return action                                                 


def createMenus( self, menuBar):

        # set up the File menus
        fileMenu = menuBar.addMenu('&File')


        newFileAction = createAction( self, '&New File',
                                      slot='self.openNewFile',
                                      shortcut='Ctrl+N' )
        
        openFileAction = createAction( self, '&Open File...',
                                       slot='self.askOpenFile',
                                       shortcut='Ctrl+O' )
        
        saveAction = createAction( self, '&Save File',
                                   slot='self.saveFile',
                                   shortcut='Ctrl+S')
        
        saveAsAction = createAction( self, 'Save File As...',
                                     slot='self.saveFileAs' )
        
        newEntAction = createAction( self, 'New &Entry',
                                     slot='self.newEntry',
                                     shortcut='Ctrl+E')

        nextEntAction = createAction( self, 'Next Entry',
                                     slot='self.on_nextButton_released',
                                      shortcut=None)

        prevEntAction = createAction( self, 'Prev &Entry',
                                     slot='self.on_prevButton_released',
                                      shortcut=None)

        saveEntAction = createAction( self, 'Save Ent&ry', 
                                      slot='self.saveEntry',
                                      shortcut='Ctrl+R' )

        printAction = createAction( self, '&Print Entry',
                                    slot='self.printEntry',
                                    shortcut='Ctrl+P')
        
        exitAction = createAction(self, '&Quit',
                                  slot='self.quit',
                                  shortcut='Ctrl+Q',
                                  icon='filequit',
                                  tip='Close the Application')

        fileMenu.addAction(newFileAction)
        fileMenu.addAction(openFileAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(newEntAction)
        fileMenu.addAction(nextEntAction)
        fileMenu.addAction(prevEntAction)
        fileMenu.addAction(saveEntAction)
        fileMenu.addAction(printAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)




        # set up the Edit menus, Cut, Copy, Paste, Delete  make gray
        cutAction = createAction(self, 'Cu&t', shortcut='Ctrl+X')
        cutAction.setEnabled(False)
        copyAction = createAction(self, '&Copy', shortcut='Ctrl+C') 
        copyAction.setEnabled(False)
        pasteAction = createAction(self, '&Paste', shortcut='Ctrl+V')
        pasteAction.setEnabled(False)
        deleteAction = createAction(self, '&Delete', shortcut='Del')
        deleteAction.setEnabled(False)
        addInfoAction = createAction(self, 'Additional &Info...',
                                     shortcut='Ctrl+T')
        
        symbolAction = createAction(self, '&Insert Symbol...',
                                    slot='self.openSymbol',
                                    shortcut='Ctrl+I')
        
        headerAction = createAction(self, 'Edit &Header...',
                                    slot='self.editHeader',
                                    shortcut='Ctrl+H')
        
        origstrAction = createAction(self, 'Show Original String',
                                     slot='self.showOrigStr')
        
        setvolnumAction = createAction(self, 'Set Volume Number...',
                                       slot='self.setVolumeNumberInteractive')

        fontsizeAction = createAction(self, 'Set font size...')
        fontsizeAction.setEnabled(False)

        fonttypeAction = createAction(self, 'Set font...')
        fonttypeAction.setEnabled(False)


        editMenu = menuBar.addMenu('&Edit')
        editMenu.addAction( cutAction)
        editMenu.addAction( copyAction ) 
        editMenu.addAction( pasteAction )
        editMenu.addAction( deleteAction)
        editMenu.addSeparator()
        editMenu.addAction( symbolAction)
        editMenu.addAction( headerAction)
        editMenu.addAction( origstrAction)
        editMenu.addAction( setvolnumAction)
        editMenu.addAction( fontsizeAction)
        editMenu.addAction( fonttypeAction)



        # set up the Help menus
        helpMenu = menuBar.addMenu('&Help')
        aboutAction = createAction(self, '&About Book Entry...',
                                   'self.helpAbout' )
        helpMenu.addAction(aboutAction)

if __name__ == '__main__':
    print('No tests available yet')
