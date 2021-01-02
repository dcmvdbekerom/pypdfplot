
************
Overview
************

The ``pypdfplot`` package provides a backend to ``Matplotlib`` that generates a PDF file of the plot with the generating Python script embedded.

Although ``Matplotlib`` is a very powerful and flexible plotting tool, once a plot is saved as PNG or PDF file, the link between the plot and its generating Python script is lost. The philosophy behind ``pypdfplot`` is that there should be no distinction between the Python script that generates a plot and its output PDF file, much like there is no such distinction in an Origin or Excel file. As far as ``pypdfplot`` is concerned, *the generating script* **is** *the plot.*

When the backend is loaded and a figure is saved using ``plt.savefig()``, the generating Python script is embedded into the output PDF-file in such a way that when the PDF file is renamed from .pdf to .py, the file can be read by a Python interpreter without alteration. The script can then be edited at will to implement changes in the plot, after which the script is ran again to produce the updated PDF file of the plot -- including the updated embedded generating script.

The resulting file, which is both a Python file and a PDF-file, is conveniently called a PyPDF-file.

