
"""
In most cases, a plot depends on some external files. These files can be
embedded in the pypdf-file just like the generating script. To do this,
set the `pack_files` keyword to a list with the filenames that need to be
embedded.

The `cleanup` keyword is a toggle to determine if the local files should be
removed once packed in the pypdf-file. Setting it to `True` will remove all
local copies of the files that are embedded, which is usually desirable.
`cleanup` is `True` by default.

When running the script later, the script will expect that these embedded
files are present locally. This can be guaranteed by extracting the files
the moment the backend is loaded, which should always be before `matplotlib`
is loaded. To do this, instead of importing `pypdfplot.backend`, import
`pypdfplot.backend.unpack`.

"""

import pypdfplot.backend.unpack
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel('data.xlsx')
plt.plot(df.x,df.y,'o')

with open('title.txt','r') as f:
    title = f.readline()
    xlabel = f.readline()
    ylabel = f.readline()

plt.title(title)
plt.xlabel(xlabel)
plt.ylabel(ylabel)

plt.savefig('packing.pdf',
            pack_list = ['data.xlsx',
                         'title.txt'],
            cleanup = False,
            )
