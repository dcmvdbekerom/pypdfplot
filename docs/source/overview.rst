
************
Overview
************

The ``pypdfplot`` package provides a backend to ``Matplotlib`` that generates a PDF file of the plot with the generating Python script embedded.

Normally, once a ``Matplotlib`` plot is saved as PNG or PDF file, the link between the plot and its generating Python script is lost. The philosophy behind ``pypdfplot`` is that there should be no distinction between the Python script that generates a plot and its output PDF file, much like there is no such distinction in an Origin or Excel file. As far as ``pypdfplot`` is concerned, *the generating script* **is** *the plot.*

When the ``pypdfplot`` backend is loaded and a figure is saved with ``plt.savefig()``, the generating Python script is embedded into the output PDF file in such a way that when the PDF file is renamed from .pdf to .py, the file can be read by a Python interpreter directly without alteration. The script can be modified to implement changes in the plot, after which the script is ran again to produce the updated PDF file of the plot -- including the updated embedded generating script.

The resulting file is both a valid Python file and a valid PDF file, and is conveniently call a PyPDF file. The compatibility with both Python and PDF is achieved by arranging the data blocks in the PyPDF file in a very specific order, such that the PDF-part is read as comment block in Python, and the Python-part is seen as an embedded file by a PDF reader.

To learn more about how to use ``pypdfplot``, continue with reading :ref:`Quickstart`, or check out the commented examples in the `examples folder <https://github.com/dcmvdbekerom/pypdfplot/tree/develop/examples>`__.


