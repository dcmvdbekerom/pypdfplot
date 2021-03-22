from setuptools import setup
from sys import path
path.append("pypdfplot")
from _version import __version__
import re

try:
    #If building package, complile README.rst
    doc_folder = 'docs/source/'
    
    with open(doc_folder + 'index.rst','r') as f:
        index_text = f.read()

    doc = ''
    fnames = [f+'.rst' for f in re.findall('    (\w+)',index_text)]
    for fname in fnames:
        with open(doc_folder + fname,'r') as f:
           doc += f.read() + '\n'

    img_link = 'https://pypdfplot.readthedocs.io/en/latest/_images/'
    doc = doc.replace('.. image:: _static/', '.. image:: ' + img_link)
    doc = re.sub(r':ref:(`[\w ]+`)', r'\1_', doc) 

    with open('README.rst','w') as f:
        f.write(doc)


except:
    print('Skip rebuilding README.rst...')
    # Otherwise, just load the readme:
    with open('README.rst','r') as f:
        doc = f.read()

setup(name='pypdfplot',
    version = __version__,
    description="Saves plots as PDF with embedded generating script",
    author='Dirk van den Bekerom',
    author_email='dcmvdbekerom@gmail.com',
    license='GPLv3',
    packages=['pypdfplot','pypdfplot/backend'],
    install_requires=['matplotlib','PyPDF4'],
    project_urls={
        'Documentation': 'https://pypdfplot.readthedocs.io/',
        'GitHub': 'https://github.com/dcmvdbekerom/pypdfplot'}, 
    zip_safe=False,
    classifiers = [
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
         "Development Status :: 4 - Beta",
         "Intended Audience :: Science/Research",
         "Programming Language :: Python",
         "Topic :: Multimedia :: Graphics",
         "Topic :: Scientific/Engineering :: Visualization"],
    long_description=doc,
    long_description_content_type='text/x-rst',
    entry_points = {
        'console_scripts': ['fix_pypdf=pypdfplot.cli:main'],
    }
      )
