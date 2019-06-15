from setuptools import setup

files = []
doc_folder = 'docs/source/'

with open(doc_folder + 'index.rst','r') as f:
    line = f.readline()
    while line == '\n':
        line = f.readline()
    
    while line != '\n':
        line = f.readline()
    
    for line in f:
        if line != '\n':
            files.append(line.strip()+'.rst')

doc = ''
for fname in files:
    with open(doc_folder + fname,'r') as f:
       doc += f.read()
       doc += '\n'

img_link = 'https://pypdfplot.readthedocs.io/en/latest/_images/'
doc.replace('.. image:: _static/',
            '.. image:: ' + img_link)

with open('README.rst','w') as f:
    f.write(doc)



setup(name='pypdfplot',
      version='0.3.4',
      description="Saves plots as PDF with embedded generating script",
      author='Dirk van den Bekerom',
      author_email='dcmvdbekerom@gmail.com',
      license='MIT',
      #url = 'https://github.com/dcmvdbekerom/pypdfplot',
      packages=['pypdfplot'],
      install_requires=['matplotlib','PyPDF4'],
      project_urls={
        'Documentation': 'https://pypdfplot.readthedocs.io/',
        'GitHub': 'https://github.com/dcmvdbekerom/pypdfplot'}, 
      zip_safe=False,
      classifiers = [
          "Development Status :: 4 - Beta",
          "Intended Audience :: Science/Research",
          "Programming Language :: Python",
          "Topic :: Multimedia :: Graphics",
          "Topic :: Scientific/Engineering :: Visualization"],
      long_description=doc,
      long_description_content_type='text/x-rst')
