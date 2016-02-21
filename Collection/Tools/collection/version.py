'''Information about the program and version numbers'''

import platform
from PyQt4.QtCore import *

__major_ver__ = 1
__minor_ver__ = 0
__patch_ver__ = 0

__major_ver_str = str(__major_ver__)
__minor_ver_str = str(__minor_ver__)
__patch_ver_str = str(__patch_ver__)
 
__version__ = '.'.join([__major_ver_str, __minor_ver_str, __patch_ver_str])

def aboutString():
    aboutStr = '''<b>Library Database</b> v {0}
    <p>Author: J. R. Fowler
    <p>Copyright &copy; 2015
    <p>All rights reserved.
    <p>This application is used to work with the database
    CardCatalog.db3.  This database is the card catalog 
    information about books in my library collection.
    <p>Python {1} - Qt {2} - PyQt {3} on {4}'''.format(
    __version__, platform.python_version(),
    QT_VERSION_STR, PYQT_VERSION_STR,
    platform.platform())
        
    return aboutStr

