# -*- coding: utf-8 -*-

import pypdfplot as plt
import pandas as pd
import numpy as np

df = pd.read_excel('data.xlsx')
plt.plot(df.x,df.y,'r-')

plt.xlabel('x axis (cm)')
plt.ylabel('y axis (V)')

with open('title.txt','r') as f:
    title = f.readline()

plt.title(title)

plt.pack(['data.xlsx',
          'title.txt'],
         cleanup = True)

plt.publish()
plt.show()
