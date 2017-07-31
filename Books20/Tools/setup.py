#
# setup.py
#
# installation instructions for python install
#
# run as
#   python3 setup.py install --prefix=/home/jrf
#
from distutils.core import setup

setup( name='bookentry',
       version='1.0.0',
       description='AJB BooksEntry tool',
       author='James R. Fowler',
       author_email='jrf12@mac.com',
       url='http://het.as.utexas.edu/jrf/20thCentury.html',
       platforms=['Ubuntu 12.04',
                  'Ubuntu 13',
                  'Ubuntu 14.10 LTS',
                  'Ubuntu 16.10 LTS'],
       packages=['bookentry'],
       scripts=['ajbbooks', 'journals', 'ppxml', 'validateXML'],
       package_data={'bookentry': ['symbols.txt']},
       )

