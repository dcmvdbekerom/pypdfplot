
"""
Producing multiple plots from a single generating script poses a challenge,
because you want to embed the generating Python script with the loop on one
hand, but also want every plot produced in the loop be a stand-alone pypdf-file
that can be modified on its own.

By default, this is solved in the following way: The generating script --
including the entire loop -- is stored in the first pypdf-file. For consequent
plots, the figure is pickled and a short python script is attached that
unpickles the figure and plots them. This way each of the individual plots
still has some (limited) configurability, and if you want to modify all files
at once you can simply modify the generating script in the first pypdf-file in
the loop.

Pickling consecutive plots is enabled by specifying the `multiple` =`'pickle'`
keyword. Since this is the default setting, no keyword is specified in this
example.

Pickling can be forced even when not in a loop by passing the keyword argument
`force_pickle` = `True`, (by default it is `False`). Note that when pickling a
plot, no other files (other than the generating .py file) are embedded in the
pypdf-file, because the plot output now only depends on the pickled figure.

Another (more convenient?) way of handling multiple plots is to add the plots
as new pages in a single pypdf-file, as illustrated in example 5.
"""

import pypdfplot.backend
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(-10,20,0.1)

for n in range(3):

    y = x**(n+1)
    
    plt.plot(x,y,'r-',lw = 2)
    plt.savefig('plot{:d}.pdf'.format(n+1))
    plt.clf()
