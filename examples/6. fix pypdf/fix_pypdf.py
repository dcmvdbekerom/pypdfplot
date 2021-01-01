
"""
Most PDF-readers are unaware of the PyPDF-format, so saving a .pdf file in e.g.
Adobe Acrobat reader will format the .pdf file in a way that makes it unreadable
for pypdfplot. The pypdf-file can be fixed by calling `fix_pypdf()`, with the
input file and ouput file as argument. The output filename can be omitted, in
which case the operation is performed in-place.

"""

from pypdfplot import fix_pypdf

fix_pypdf('linearized.pdf','fixed.pdf')
