import pypdfplot as plt
import numpy as np

x = np.arange(-10,20,0.1)

for n in range(3):

    y = x**(n+1)
    
    plt.plot(x,y,'b-',lw = 2)
    plt.publish('plot{:d}.pdf'.format(n+1),
                multiples = 'pickle')
