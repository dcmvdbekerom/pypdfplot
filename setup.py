from setuptools import setup

setup(name='pypdfplot',
      version='0.3',
      description="Saves plots as PDF with embedded generating script",
      author='Dirk van den Bekerom',
      author_email='dcmvdbekerom@gmail.com',
      license='MIT',
      packages=['pypdfplot'],
      install_requires=['matplotlib','PyPDF2'],
      zip_safe=False)
