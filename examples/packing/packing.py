import pypdfplot as plt
import pandas as pd

df = pd.read_excel('data.xlsx')
plt.plot(df.x,df.y,'b-')
#hello

with open('title.txt','r') as f:
    title = f.readline()
    xlabel = f.readline()
    ylabel = f.readline()

plt.title(title)
plt.xlabel(xlabel)
plt.ylabel(ylabel)

plt.pack(['data.xlsx',
          'title.txt'])

plt.publish(in_place = False)
#plt.cleanup()
