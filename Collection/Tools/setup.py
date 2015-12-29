#
# setup.py
#
# installation instructions for python install
#
# run as
#   python3 setup.py install --prefix=/home/jrf
#
from distutils.core import setup

setup( name='collection',
       version='1.0.0',
       description='Library Database Tool',
       author='James R. Fowler',
       author_email='jrf12@mac.com',
       url='http://het.as.utexas.edu/jrf/20thCentury.html',
       platforms=['Ubuntu 12.04',
                  'Ubuntu 13',
                  'Ubuntu 14.10 LTS',
                  'MacOS X.11.2 El Capitan'],
       packages=['collection'],
       scripts=['librarian'],
       )

