import pypdfplot.backend
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(-10,20,0.1)
y = x**2

plt.plot(x,y,'r-',lw = 2)
plt.savefig('example.pdf')