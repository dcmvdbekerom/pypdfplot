"""
After packing the files, they can be unpacked by renaming the .pdf to .py, and running the script with the keyword
`cleanup` = `False`. This extracts all files to the local folder. When the embedded file already exists locally, it
will not be extracted and the local copy is kept. This makes it easy to exctract files and run the script again and
again, without losing any local changes to the dependent files.

A typical way to edit a pypdf-file with embedded files would be as follows:

(1) rename .pdf to .py, 
(2) run the script with `cleanup` = `False`, 
(3) edit the local files, e.g. changing some data in the excel file, 
(4) run the script again with `cleanup` = `True`. 

Now you have the plot with the updated files embedded, and also updated the plot that depend on these files.

"""