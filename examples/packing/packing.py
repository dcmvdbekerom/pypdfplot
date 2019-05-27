import pypdfplot as plt
import pandas as pd
import numpy as np

df = pd.read_excel('data.xlsx')
plt.plot(df.x,df.y,'r-')

with open('title.txt','r') as f:
    title = f.readline()
    xlabel = f.readline()
    ylabel = f.readline()

plt.title(title)
plt.xlabel(xlabel)
plt.ylabel(ylabel)

plt.pack(['data.xlsx',
          'title.txt'])

plt.publish()
#plt.cleanup()
