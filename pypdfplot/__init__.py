from matplotlib.pyplot import *
from .classes import PyPdfFileReader,PyPdfFileWriter,b_,PdfReadError,warnings,available_filename
import sys
import os
from os.path import normcase,realpath
import binascii
import zlib

pyname   = os.path.basename(sys.argv[-1])
base,ext = os.path.splitext(pyname)

_pack_list = []
_filespacked = False
_pyfile = b_('')
_revision = 0

if pyname != '':
    with open(pyname,'rb') as fr:
        try:
            #T: parse CR LF to LF
            pr = PyPdfFileReader(fr)
            #D: print('Reading as mixed PyPDF file...')
            _pyfile = pr.pyObj.getData()[:-4]
            _revision = pr.revision + 1

            root_obj = pr.trailer['/Root']
            file_dict = root_obj['/Names']['/EmbeddedFiles']['/Names']
            fnames = [fname for fname in file_dict[0::2]]
            fobjs  = [fobj['/EF']['/F'] for fobj in file_dict[1::2]]

            for fname,obj in zip(fnames,fobjs):
                if obj != pr.pyObj:
                    sname = fname
                    ## in debug, all data is loaded.
                    ## in release, data only needs to
                    ## be loaded if file does not exist
                    ## locally.
                    
                    #D: print(fname,obj)
                    fdata = obj.getData()
                    if not os.path.isfile(sname):
                        with open(sname,'wb') as fw:
                            fw.write(fdata)

        except(PdfReadError):
            #D: print('Reading as Python-only file...')
            fr.seek(0)
            _pyfile = fr.read().replace(b_('\r\n'),b_('\n'))

      
def pack(pack_list):
    global _pack_list
    _pack_list += pack_list


def publish(output           = None,
            in_place         = True,
            show_plot        = True,
            prompt_overwrite = False,
            verbose          = True,
            **kwargs):
    
    global _filespacked

    ## Save the matplotlib plot
    temp_plot = available_filename('temp_plot.pdf')
    if verbose: print('Saving figure as temporary file: ' + temp_plot)
    savefig(temp_plot)

    ## Name the output file
    if output == None:
        output = base + '.pdf'
    elif os.splitext(output)[1] == '':
        output += '.pdf'
    elif os.splitext(output)[1] != '.pdf':
        output = os.splitext(output)[0] + '.pdf'
        warnings.warn('Invalid extension, publishing as {:s}'.format(output))
    if verbose: print('Output filename: ' + output)

    ## If the output file already exists, try to remove it
    if os.path.isfile(output):
        do_overwrite = False
        if prompt_overwrite:
            warnings.warn('Local duplicate of output file found')
            warnings.warn('Overwrite file? (y/n)')
            yes_no = raw_input('')
            if yes_no.strip().lower()[0] == 'y':
                do_overwrite = True
            else:
                output = available_filename(output)
                warnings.warn('Publishing as {:s} instead'.format(output))
        else:
            do_overwrite = True

        if do_overwrite:
            try:
                os.remove(output)
            except:
                warnings.warn('Unable to overwrite local duplicate of output file')
                output = available_filename(output)
                warnings.warn('Publishing as {:s} instead'.format(output))

    ## Write the PyPDF file
    if verbose: print('\nPreparing PyPDF file:')
    with open(temp_plot,'rb') as fr, open(output,'wb+') as fw: #T: Why wb+ again?
        pw = PyPdfFileWriter(fr,_revision)
        
        for fname in _pack_list:
            if verbose: print('-> Attaching '+ fname)
            with open(fname,'rb') as fa:
                fdata = fa.read()
                pw.addAttachment(fname,fdata)

        if verbose: print('-> Attaching Python file')
        fdata = _pyfile + b_('\n"""')
        pw.addAttachment(pyname,fdata)

        if verbose: print('-> Writing output\n')
        pw.write(fw)

    _filespacked = True    

    ## Remove the temporary plot
    if verbose: print('Cleaning up:\n-> Removing temporary plot')
    try:
        os.remove(temp_plot)
    except:
        warnings.warn('Unable to remove temporary plot file')
        
    ## Remove the generating python file
    if in_place:
        if verbose: print('-> Removing generating Python file')
        if verbose: print('   (Caution: Saving Python file in editor will make it reappear!)')
        if normcase(realpath(pyname)) != normcase(realpath(__file__)): 
            try:
                os.remove(pyname)
            except:
                warnings.warn('Unable to remove generating Python file')
        else:
            warnings.warn('Attempt to delete library file was aborted')    

    ## Show the plot:
    if verbose: print('\nShowing plot...')
    if show_plot:
        show(**kwargs)

def cleanup():
    if _filespacked:
        if verbose: print('Cleaning up attached files:')
        for fname in _pack_list:
            if verbose: print('-> Removing ' + fname)
            try:
                os.remove(fname)
            except:
                warnings.warn('Unable to remove {:s}.'.format(fname))
    else:
        warnings.warn("Files weren't packed into PyPDF file yet, aborting cleanup") 
