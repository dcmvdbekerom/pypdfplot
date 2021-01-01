
"""
Most PDF-readers are unaware of the PyPDF-format, so saving a .pdf file in e.g.
Adobe Acrobat reader will format the .pdf file in a way that makes it unreadable
for pypdfplot. Among other things, this may introduce binary characters that
cannot be interpreted by Python. Additionally, a so called linearized PDF-file
my be produced, which is not suitable for pypdfplot.

The pypdf-file can be fixed by calling `fix_pypdf()`, with the
input file and ouput file as argument. The output filename can be omitted, in
which case the operation is performed in-place.

Once fixed successfully, you should retrieve the unpacking.pdf from example 3.

"""

from pypdfplot import fix_pypdf

fix_pypdf('linearized.pdf','fixed.pdf')
