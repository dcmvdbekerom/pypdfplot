
************
Quickstart
************

The ``pypdfplot`` package provides a backend for ``Matplotlib`` for producing PyPDF-files.
This section goes through a basic example that shows how to use ``pypdfplot``.

Simple Example
==============

For this example, the goal is to produce a red plot of the quadratic function from -10 to 20.
To start off, you first plot this in the conventional way using ``Matplotlib``.

Create a new python file, let's call it ``example.py``. 

Open the file and enter the following script:

.. code:: python

    import matplotlib.pyplot as plt
    import numpy as np
    
    x = np.arange(-10,20,0.1)
    y = x**2
    
    plt.plot(x,y,'r')
    plt.savefig('example.pdf')
	
After running this script, you should get the following figure:

.. image:: _static/plot.png

To produce a PyPDF-file, all you have to do is add a line on the top to import the backend: 

.. code:: python

    import pypdfplot.backend
    import matplotlib.pyplot as plt
    import numpy as np
    
    x = np.arange(-10,20,0.1)
    y = x**2
    
    plt.plot(x,y,'r')
    plt.savefig(example.pdf)

After running this script, if you look in the folder where the ``example.py`` file once was, you'll notice it has been replaced by a new file ``example.pdf``.
Of course the fact that the ``example.py`` file disappeared doesn't mean the script is gone -- it is now embedded in the PyPDF file ``example.pdf``!

You can find evidence of this by opening the ``example.pdf`` file:

.. image:: _static/plot_pdf.png

The table on the left shows all files that are embedded, and clearly ``example.py`` is there.

Most versions of Acrobat reader don't allow the embedded .py file to be opened for security reasons.
To access the python script, rename ``example.pdf`` to ``example.py`` and open the file.
This is what you should find:

.. code:: python

    #%PDF-1.3 23 0 obj << /Type /EmbeddedFile /Length 124 >> stream
    import pypdfplot.backend
    import matplotlib.pyplot as plt
    import numpy as np
    
    x = np.arange(-10,20,0.1)
    y = x**2
    
    plt.plot(x,y,'r')
    plt.savefig('example.pdf')
    
    """
    endstream
    endobj
    1 0 obj
    
    <...>
    
    startxref
    8829
    %%EOF
    0000009410
    PyPDF
    """

The first line is the PDF header that helps the PDF reader to determine this is a valid PDF file.
It also includes the object header for the EmbeddedFile object of our ``example.py`` file. 
This line may not be altered, as it will result in corruption of the PyPDF file.

What follows is the original python script, followed by a large multiline string. 
This multiline string contains all the PDF objects including the data for any remaining embedded files (see `PyPDF File specification`_).
Making any edits in this string will again likely result in corruption of the file, so it is strongly discouraged.

In between the first line and the multiline string is the original python script, which may be edited in any way.
For example, let's give the plot a title and change the color to blue:

.. code:: python

    #%PDF-1.3 23 0 obj << /Type /EmbeddedFile /Length 124 >> stream
    import pypdfplot.backend
    import matplotlib.pyplot as plt
    import numpy as np
    
    x = np.arange(-10,20,0.1)
    y = x**2
    
    plt.plot(x,y,'b')
    plt.title('Blue Example')
    plt.savefig('example.pdf')
    
    """
    endstream
    endobj
    1 0 obj
    
    <...>
    
    startxref
    8829
    %%EOF
    0000009410
    PyPDF
    """
	
Again, after running the script the ``example.py`` file is replaced by the ``example.pdf`` file.
When you open ``example.pdf``, you should find the updated blue plot with caption:

.. image:: _static/plot_pdf2.png


