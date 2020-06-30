from ._version import __version__
from .functions import read, pack, publish, fix_pypdf

from os.path import basename
from inspect import stack
from matplotlib.pyplot import *


## Lookup keyword arguments
try:
    frame = stack()[0].frame
except(AttributeError):
    frame = stack()[0][0]
    
while(frame.f_globals['__name__'] != '__main__'):
    frame = frame.f_back
    
try:
    pypdfplot_kwargs = frame.f_globals['pypdfplot_kwargs']
except(KeyError):
    pypdfplot_kwargs = {}


## Read PyPDF file
pyname   = basename(sys.argv[-1])
if pyname != '':
    read(pyname,**pypdfplot_kwargs)


