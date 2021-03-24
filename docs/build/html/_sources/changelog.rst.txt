
*********
Changelog
*********
v0.6.5
======
- Previous patch introduced a new problem with the "Do not edit below" string. This is now solved.

v0.6.4
======
- Prevent deletion of output when input is .pdf
- Fixes additional PyPDF4 compatibility issues

v0.6.3
======
- Fix compatibility with PyPDF4 v1.27.0

v0.6.2
======
- Fix missing installation of backend
- Fix some links in docs

v0.6.1
======
- Documentation completely updated
- Removed legacy ``publish()`` function, only works as ``Matplotlib`` backend now.
- Changed ``auto_extract()`` to ``unpack()``
- Changed ``file_list`` to ``pack_list``
- Added ``__PYPDFVERSION__`` as canonical version no.
- Added ``pw.setPyPDFVersion()`` to ``fix_pypdf()``


v0.6.0
======

First official release