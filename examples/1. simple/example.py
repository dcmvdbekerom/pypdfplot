
"""
Run this script to generate the pypdf-file, which appears as a pdf-file in the
folder. Because this Python script will be embedded in the .pdf, the original
.py file will be removed. Saving this script after running it makes the .py
file reappear, which is not needed as is already embedded in the .pdf file!

Rename the .pdf file to .py and edit the script to modify the plot,
run it again to process the modifications.

A zip-file with this script is provided for convenience to replace this
scrip once it is removed.

"""

import pypdfplot.backend
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(-10,20,0.1)
y = x**2

plt.plot(x,y)
plt.savefig('example.pdf')
