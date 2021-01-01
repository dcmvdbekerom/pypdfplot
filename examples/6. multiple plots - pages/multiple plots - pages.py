import pypdfplot.backend.auto_extract
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(-10,20,0.1)

for n in range(3):

    y = x**(n+1)
    
    plt.plot(x,y,'r-',lw = 2)
    plt.savefig('', multiple = 'add_page')
    plt.clf()

plt.savefig('multi_page.pdf', multiple = 'finalize')
