from setuptools import setup

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
          "Topic :: Scientific/Engineering :: Visualization"])
