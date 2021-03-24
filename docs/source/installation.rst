
************
Installation
************

PyPI repository
===============

Install the package from the PyPI repository opening a command prompt and enter:

.. code:: bash

    pip install pypdfplot


Github or download
==================

Alternatively, the source files can be downloaded directly from the GitHub `repository <https://github.com/dcmvdbekerom/pypdfplot>`__. After downloading the source files, navigate to the project directory and install the package by opening a command prompt and enter:

.. code:: bash

    python setup.py install
    
Anaconda/Spyder
===============

In order for ``pypdfplot`` to work in an Anaconda/Spyder environment, the package has to be installed from source with the "`editable`" option.

Download the source code following the instructions above. Open an Anaconda prompt and navigate to the directory with the source code.
Now install the package by typing in the Anaconda prompt:

.. code:: bash

    pip install -e .

Installing the package with the "`editable`" option guarantees that the libraries are reloaded each time the code is ran. 

This will produce a warning in the IPyhton console, which can be turned off by unchecking the "`Show reloaded module list`" box in the ``Tools`` > ``Preferences`` > ``Python interpreter`` menu in Spyder.

Next, navigate to the ``Graphics`` tab in the ``Tools`` > ``Preferences`` > ``IPython console`` menu and set the backend to "`Automatic`".

It is further recommended to save the figure with the keyword ``cleanup`` = ``'False'``, see :ref:`savefig()`.  

  