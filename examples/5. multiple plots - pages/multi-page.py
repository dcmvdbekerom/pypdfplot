
"""
In example 4 the challenge of multiple figures from a single script was
introduced. This example presents perhaps a more convenient solution:
The multiple plots are stored as separate pages in the pypdf-file.

This is achieved by calling `plt.savefig()` with the keyword `multiple` =
`'add_page'`. Once the loop is finished, call `plt.savefig()` one more time
with the keyword `multiple` = `finalize`. Note that during the loop the
filename is ignored, so you can pass an empty string. The filename of the
output file, as well as the list of files to embed, are determined by the
arguments to the last call with the `multiple` = `finalize` keyword.

"""

import pypdfplot.backend
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(-10,20,0.1)

for n in range(3):

    y = x**(n+1)
    
    plt.plot(x,y,'r-',lw = 2)
    plt.savefig('', multiple = 'add_page')
    plt.clf()

plt.savefig('multi_page.pdf', multiple = 'finalize')
