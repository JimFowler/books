"""A table of unicode characters (symbols) that may be inserted into
any of the text fields.

The basic code for the button and the window were taken from the
character_picker package developed by Rich Griswold.  They were
modified for the BookEntry package.
"""

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import codecs

class MyButton( QToolButton ):
	def __init__( self, parent=None ):
		QToolButton.__init__( self, parent )
		QObject.connect( self, SIGNAL("clicked()"), self.slotClicked )

	def slotClicked( self ):
		self.emit( SIGNAL( "sigClicked" ), ( self.text(), ) )

class SymbolForm( QMainWindow ):
    def __init__( self, file_name, icon_name, font_family, font_size, parent=None ):
        QWidget.__init__( self, parent )

        try:
            file = codecs.open( file_name, 'r', 'utf-8' )
        except IOError as ex:
            print(ex)
            exit( 1 )
            
        self.icon = QIcon()
        self.icon.addPixmap( QPixmap( os.path.join( sys.path[0], 'character_picker.png' ) ), QIcon.Normal, QIcon.Off )
        self.setWindowIcon( self.icon )
        self.setWindowTitle( 'Insert Symbol...' )

        self.clicked = False
        self.font = QFont( font_family, int( font_size ) )
        self.clipboard = QApplication.clipboard()
        QObject.connect( self.clipboard, SIGNAL("dataChanged()"), self.clipboardChanged )
        QObject.connect( self.clipboard, SIGNAL("selectionChanged()"), self.clipboardChanged )
        
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
        self.setCentralWidget( self.scrollArea )

    def clipboardChanged( self ):
        if self.clicked is False:
            button = self.buttonGroup.checkedButton()
            if button is not None:
                self.buttonGroup.setExclusive( False )
                button.setChecked( False )
                self.buttonGroup.setExclusive( True )

    def keyPressEvent( self, event ):
        if type( event ) == QKeyEvent:
            self.close()
            event.accept()
        else:
            event.ignore()

    def slotClicked( self, obj ):
        char = unicode( obj[0] )
        self.clicked = True
        self.clipboard.setText( char, QClipboard.Selection )
        self.clipboard.setText( char, QClipboard.Clipboard )
        self.clicked = False


def get_settings():
    prog_name = 'character_picker'
    settings = QSettings( QSettings.IniFormat, QSettings.UserScope, 'RichGriswold', prog_name )

    original_font_name = 'FreeSans'
    original_font_size = 12
    font_name = str( settings.value( 'font_name', original_font_name ) )
    font_size = int( settings.value( 'font_size',  original_font_size ) )
    
    settings_dir = os.path.split( str( settings.fileName() ) )[0]
    file_name = os.path.join( settings_dir, prog_name + '.txt' )
    icon_name = os.path.join( settings_dir, prog_name + '.png' )
    
    vals = dict()
    vals['original_font_name'] = original_font_name
    vals['original_font_size'] = original_font_size
    vals['file_name'] = file_name
    vals['font_name'] = font_name
    vals['font_size'] = font_size
    vals['icon_name'] = icon_name
    vals['prog_name'] = prog_name
    vals['settings_dir'] = settings_dir
    vals['settings'] = settings
    return vals



if __name__ == "__main__":
    import os
    import signal
    import sys
    
    signal.signal( signal.SIGINT, signal.SIG_DFL )
    
    settings = get_settings()
    
    app = QApplication( sys.argv )
    myapp = SymbolForm( settings['file_name'], settings['icon_name'], settings['font_name'], settings['font_size'] )
    myapp.show()
    sys.exit( app.exec_() )
                    
