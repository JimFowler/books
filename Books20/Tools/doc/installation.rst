Installation
************

BookEntry uses the python library *distutils* to install and
distribute the packages. More documentation about the installation
program can be found by running the command

``pydoc distutils.core.setup``

The BookEntry package may be installed from
the Tools directory with the command

``python3 setup.py install``

My default is to install all the packages required for BookEntry in my
home directory so I use

``python3 setup.py install --home=~``

Or you can install in a different system directory with

``python3 setup.py install --prefix=/opt/local``

