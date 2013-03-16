from distutils.core import setup

setup( name='BookEntry',
       version='1.0.0',
       description='AJB BooksEntry tool',
       author='James R. Fowler',
       author_email='jrf12@mac.com',
       url='http://het.as.utexas.edu/jrf/20thCentury.html',
       platforms=['Ubuntu 12.04'],
       packages=['bookentry'],
       scripts=['BookEntry'],
       package_data={'bookentry': ['symbols.txt']},
       )

