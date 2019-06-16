from setuptools import setup

version = '0.3.7'

try:
    with open('VERSION','w') as f:
        f.write(version)
except:
    pass

try:
    #If building package, complile README.rst
    files = []
    doc_folder = 'docs/source/'
    
    with open(doc_folder + 'index.rst','r') as f:
        line = f.readline()
        while line == '\n':
            line = f.readline()
        
        while line != '\n':
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
    doc = doc.replace('.. image:: _static/',
                      '.. image:: ' + img_link)

    with open('README.rst','w') as f:
        f.write(doc)
except:
    # Otherwise, just load the readme:
    with open('README.rst','r') as f:
        doc = f.read()

setup(name='pypdfplot',
      version = version,
      description="Saves plots as PDF with embedded generating script",
      author='Dirk van den Bekerom',
      author_email='dcmvdbekerom@gmail.com',
      license='MIT',
      packages=['pypdfplot'],
      install_requires=['matplotlib','PyPDF4','numpy'],
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
