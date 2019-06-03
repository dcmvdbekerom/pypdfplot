from matplotlib.pyplot import *
from .classes import PyPdfFileReader,PyPdfFileWriter,b_,PdfReadError
import sys
import os
import binascii
import zlib

pyname   = os.path.basename(sys.argv[0])
base,ext = os.path.splitext(pyname)

_pack_list = []
_filespacked = False
_pyfile = b_('')
_revision = 0

if pyname != '':
    with open(pyname,'rb') as fr:
        try:
            pr = PyPdfFileReader(fr)
            #print('Reading as mixed PyPDF file...')
            _pyfile = pr.pyObj.getData()[:-4]
            _revision = pr.revision + 1

            root_obj = pr.trailer['/Root']
            file_dict = root_obj['/Names']['/EmbeddedFiles']['/Names']
            fnames = [fname for fname in file_dict[0::2]]
            fobjs  = [fobj['/EF']['/F'] for fobj in file_dict[1::2]]

            for fname,obj in zip(fnames,fobjs):
                if obj != pr.pyObj:
                    sname = fname
                    ##if not os.path.isfile(sname):
                    print(fname,obj)
                    fdata = obj.getData()
                    if not os.path.isfile(sname):
                        with open(sname,'wb') as fw:
                            fw.write(fdata)

        except(PdfReadError):
            #print('Reading as Python-only file...')
            fr.seek(0)
            _pyfile = fr.read().replace(b_('\r\n'),b_('\n'))

      
def pack(pack_list):
    global _pack_list
    _pack_list = pack_list


def publish(show_plot = True, **kwargs):
    global _filespacked
    
    temp_plot = 'temp_plot.pdf'
    i = 2
    while os.path.isfile(temp_plot):
        temp_plot = 'temp_plot{:d}.pdf'.format(i)
        i += 1

    savefig(temp_plot)

    output = base+'.pdf'
    if os.path.isfile(output):
        os.remove(output)
        
    with open(temp_plot,'rb') as fr, open(output,'wb+') as fw:
        pw = PyPdfFileWriter(fr,_revision)
        
        for fname in _pack_list:
            with open(fname,'rb') as fa:
                fdata = fa.read()
                pw.addAttachment(fname,fdata)

        fdata = _pyfile + b_('\n"""')
        pw.addAttachment(pyname,fdata)

        pw.write(fw)

    _filespacked = True    

    os.remove(temp_plot)
    if pyname != 'pypdfplot3.py':  
        try:
            os.remove(pyname)
        except:
            pass
        
    if show_plot:
        show(**kwargs)

def cleanup():
    if _filespacked:
        for fname in _pack_list:
            os.remove(fname)
