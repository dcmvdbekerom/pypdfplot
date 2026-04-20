|badge_docs|

.. |badge_docs| image:: https://readthedocs.org/projects/pypdfplot/badge/
                :target: https://pypdfplot.readthedocs.io/
                :alt: Documentation Status

************
Overview
************

The ``pypdfplot`` package provides a backend to ``Matplotlib`` that generates a PDF file of the plot with the generating Python script embedded.

Normally, once a ``Matplotlib`` plot is saved as PNG or PDF file, the link between the plot and its generating Python script is lost. The philosophy behind ``pypdfplot`` is that there should be no distinction between the Python script that generates a plot and its output PDF file, much like there is no such distinction in an Origin or Excel file. As far as ``pypdfplot`` is concerned, *the generating script* **is** *the plot.*

When the ``pypdfplot`` backend is loaded and a figure is saved with ``plt.savefig()``, the generating Python script is embedded into the output PDF file in such a way that when the PDF file is renamed from .pdf to .py, the file can be read by a Python interpreter directly without alteration. The script can be modified to implement changes in the plot, after which the script is ran again to produce the updated PDF file of the plot -- including the updated embedded generating script.

The resulting file is both a valid Python file and a valid PDF file, and is conveniently call a PyPDF file. The compatibility with both Python and PDF is achieved by arranging the data blocks in the PyPDF file in a very specific order, such that the PDF-part is read as comment block in Python, and the Python-part is seen as an embedded file by a PDF reader.

To learn more about how to use ``pypdfplot``, read the full manual [here](https://pypdfplot.readthedocs.io/), or check out the commented examples in the `examples folder <https://github.com/dcmvdbekerom/pypdfplot/tree/develop/examples>`__.




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

It is further recommended to save the figure with the keyword ``cleanup`` = ``'False'``.  

  
.. _Quickstart:

**********
Quickstart
**********

In this example, a plot is produced with ``Matplotlib`` and saved as PyPDF-file using the ``pypdfplot`` backend.

First, create a new python file and call it e.g. ``example.py``. 

To produce a PyPDF-file, all you have to do is import the ``pypdfplot`` backend by adding the line ``import pypdfplot.backend`` before importing ``Matplotlib``: 

.. code:: python

    import pypdfplot.backend
    import matplotlib.pyplot as plt
    import numpy as np
    
    x = np.arange(-10,20,0.1)
    y = x**2
    
    plt.plot(x,y)
    plt.savefig('example.pdf')

After running this script, the file ``example.py`` will have been removed and replaced by a new file ``example.pdf``:

.. image:: https://pypdfplot.readthedocs.io/en/latest/_images/example_plot.png

As can be seen in the "Attachments" column on the left, the orginal ``example.py`` generating script is embedded in the PDF file.

The script can be accessed by renaming ``example.pdf`` back to ``example.py`` and opening it in a text editor:

.. code:: python

    #%PDF-1.4 24 0 obj << /Type /EmbeddedFile /Length        690 >> stream
    import pypdfplot.backend
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.arange(-10,20,0.1)
    y = x**2

    plt.plot(x,y)
    plt.savefig('example.pdf')

    """
    --- Do not edit below ---
    endstream
    endobj
    1 0 obj

    << ... >>

    startxref
    9567
    %%EOF
    0000010174 LF
    PyPDF-1.0
    """

It can be seen that after saving the plot with the ``pypdfplot`` backend, a commented line was added at the first line and a large comment block was appended at the end of the file. These comments contain all the necessary data for displaying the PDF and should not be altered directly by the user.

To update the plot, the user should instead modify the generating Python script and the PDF will be updated after running the script again!

For example, let's add another plot, e.g. a sine function:

.. code:: python

    #%PDF-1.4 24 0 obj << /Type /EmbeddedFile /Length        690 >> stream
    import pypdfplot.backend
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.arange(-10,20,0.1)
    y1 = x**2
    y2 = 100*np.sin(x)

    plt.plot(x,y1)
    plt.plot(x,y2)
    plt.savefig('example.pdf')

    """
    --- Do not edit below ---
    endstream
    endobj
    1 0 obj

    << ... >>

    startxref
    9567
    %%EOF
    0000010174 LF
    PyPDF-1.0
    """

After running ``example.py``, the file is again replaced by our updated ``example.pdf``:

.. image:: https://pypdfplot.readthedocs.io/en/latest/_images/example_plot2.png




*********
Changelog
*********
v0.7.0
======
- Switch to the new pypdf as dependency over PyPDF4.
- Add backup of pyfile in the pypdf file, and read it if the original pyfile is lost.
- Add tests that run with pytest
- Fix issues with docs

v0.6.5
======
- Previous patch introduced a new problem with the "Do not edit below" string. This is now solved.

v0.6.4
======
- Prevent deletion of output when input is .pdf
- Fixes additional PyPDF4 compatibility issues

v0.6.3
======
- Fix compatibility with PyPDF4 v1.27.0

v0.6.2
======
- Fix missing installation of backend
- Fix some links in docs

v0.6.1
======
- Documentation completely updated
- Removed legacy ``publish()`` function, only works as ``Matplotlib`` backend now.
- Changed ``auto_extract()`` to ``unpack()``
- Changed ``file_list`` to ``pack_list``
- Added ``__PYPDFVERSION__`` as canonical version no.
- Added ``pw.setPyPDFVersion()`` to ``fix_pypdf()``


v0.6.0
======

First official release
