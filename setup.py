import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='pypdfplot',
      version='0.1',
      description='Produces pyplot plots in PDF format with embedded Python code',
      long_description = long_description,
      long_description_content_type="text/markdown",
      author='Dirk van den Bekerom',
      author_email='dcmvdbekerom@gmail.com',
      license='GPL-3.0-or-later',
      packages=setuptools.find_packages(),
      classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Visualization"),
      install_requires=['matplotlib'],
      zip_safe=False)

