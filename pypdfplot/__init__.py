from pypdfplot._version import __version__
from pypdfplot.functions import unpack, fix_pypdf

## Legacy import for the publish() function:

## from matplotlib.pyplot import *

## Specifically, ^this^ import is the reason publish() was deprecated in v0.6.
## Use plt.savefig() instead with import pypdfplot.backend at the top of your
## script.
