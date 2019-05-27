import numpy as np
import pypdfplot as plt

x = np.arange(-10,20,0.1)
y = x**2

plt.plot(x,y)
plt.publish()
