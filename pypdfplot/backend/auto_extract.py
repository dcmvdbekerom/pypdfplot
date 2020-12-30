from pypdfplot.backend.__init__ import *

print('EXTRACT FUNCTION GOES HERE')

import sys
import os

## Read PyPDF file
pyname = os.path.basename(sys.argv[-1])
if pyname != '':
    extract(pyname)

