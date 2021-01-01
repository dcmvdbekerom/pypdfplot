import pypdfplot.auto_extract as plt
import numpy as np

x = np.arange(-10,20,0.1)

for n in range(3):

    y = x**(n+1)
    
    plt.plot(x,y,'r-',lw = 2)
    plt.publish('', multiples = 'add_page')
    plt.clf()

plt.publish('multi_page.pdf', multiples = 'finalize')
