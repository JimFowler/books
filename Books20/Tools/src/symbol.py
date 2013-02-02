"""A table of unicode characters (symbols) that may be inserted into
any of the text fields.

The basic code for the button and the window were taken from the
character_picker package developed by Rich Griswold and described
in his blog
http://richgriswold.wordpress.com/2009/10/17/character-picker/

The packaged was modified for BookEntry.
"""
# -*- mode: Python; -*-

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import codecs

class MyButton( QToolButton ):
    """Create a button with a associated text string,
    in our case a character. When the button is clicked
    it emits the text string."""
    def __init__( self, parent=None ):
        QToolButton.__init__( self, parent )
        QObject.connect( self, SIGNAL("clicked()"), self.slotClicked )

    def slotClicked( self ):
        self.emit( SIGNAL( "sigClicked" ), ( self.text(), )) 

class SymbolForm( QDialog ):
    """Create a table of buttons which emit their character
    when pressed."""

    def __init__( self, file_name, font_family, font_size, parent=None ):
        QWidget.__init__( self, parent )
        self.setObjectName('symbolForm')
        
        try:
            file = codecs.open( file_name, 'r', 'utf-8' )
        except IOError as ex:
            print(ex)
            exit( 1 )
            
        self.setWindowTitle( 'Insert Symbol...' )
        
        self.clicked = False
        self.font = QFont( font_family, int( font_size ) )
        
        self.scrollArea = QScrollArea( self )
        self.scrollArea.setWidgetResizable( True )
        self.scrollAreaWidgetContents = QWidget( self.scrollArea )
        self.gridLayout = QGridLayout( self.scrollAreaWidgetContents )
        self.gridLayout.setSpacing( 0 )
        self.scrollArea.setWidget( self.scrollAreaWidgetContents )
        
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.setExclusive( True )
        self.buttons = dict()
        
        row = 0
        col_max = 0
        id = 0
        for line in file:
            col = 0
            for char in line:
                if '\n' != char:
                    button = MyButton( self.scrollAreaWidgetContents )
                    button.setCheckable( True )
                    button.setFont( self.font )
                    button.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding )
                    button.setText( char )
                    button.setObjectName('%03d%03dButton'%(row,col))
                    self.gridLayout.addWidget( button, row, col, 1, 1 )
                    self.buttonGroup.addButton( button, id )
                    QObject.connect( button, SIGNAL("sigClicked"), self.slotClicked )
                    self.buttons[row, col] = button
                    col += 1
                    id += 1
            if col > col_max:
                col_max = col
            row += 1

        spacerItem = QSpacerItem( 40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum )
        self.gridLayout.addItem( spacerItem, 0, col_max, 1, 1 )
        spacerItem = QSpacerItem( 20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding )
        self.gridLayout.addItem( spacerItem, row, 0, 1, 1 )
        self.setLayout(self.gridLayout)

    def keyPressEvent( self, event ):
        if type( event ) == QKeyEvent:
            self.close()
            event.accept()
        else:
            event.ignore()

    def slotClicked( self, obj ):
        char =  obj[0]
        self.clicked = True
        self.emit( SIGNAL( "sigClicked" ), ( char, ) )
        self.clicked = False



if __name__ == "__main__":
    import sys
    
    app = QApplication( sys.argv )
    myapp = SymbolForm( 'symbols.txt', 'FreeSans', 12 )
    myapp.show()
    sys.exit( app.exec_() )
                    
