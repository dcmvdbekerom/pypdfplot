from .__init__ import *

import sys
import os

## Read PyPDF file
pyname   = os.path.basename(sys.argv[-1])
if pyname != '':
    extract(pyname)

