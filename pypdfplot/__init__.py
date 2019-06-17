from matplotlib.pyplot import *
from .classes import PyPdfFileReader,PyPdfFileWriter,b_,PdfReadError,warnings,available_filename,IndirectObject,NameObject
import sys
import os
from os.path import normcase,realpath
import binascii
import zlib
import inspect

def read(input_file,
         verbose = True,
         skip = False):
    if not skip:
        with open(input_file,'rb') as fr:
            try:
                ## Extract generating Python script
                #T: parse CR LF to LF
                pr = PyPdfFileReader(fr)
                if verbose: print('\nReading as mixed PyPDF file')
                pyfile = pr.pyObj.getData()[:-4]
                revision = pr.revision + 1

                ## Extract other embedded files
                root_obj = pr.trailer['/Root']
                file_dict = root_obj['/Names']['/EmbeddedFiles']['/Names']

                fnames = []
                fobjs  = []
                
                file_dict = root_obj['/Names']['/EmbeddedFiles']['/Names']

                for i in range(0,len(file_dict),2):
                    fnames.append(file_dict[i])
                    fobj = file_dict[i+1]
                    if isinstance(fobj,IndirectObject):
                        fobj = fobj.getObject()
                    fobjs.append(fobj['/EF']['/F'])

                if verbose: print('Extracting embedded files:')
                for fname,obj in zip(fnames,fobjs):
                    if obj != pr.pyObj:
                        sname = fname                    
                        if not os.path.isfile(sname):
                            fdata = obj.getData()
                            with open(sname,'wb') as fw:
                                fw.write(fdata)
                                if verbose: print('-> Extracing ' + sname)
                        else:
                            if verbose: print('-> ' + fname +' already exists, skipping')

            except(PdfReadError):
                ## Read as Python-only file
                if verbose: print('Reading as Python-only file')
                fr.seek(0)
                pyfile = fr.read().replace(b_('\r\n'),b_('\n'))
                revision = 0
                fnames = []
                
        return pyfile,revision

    ## If reading is skipped:
    else:
        if verbose: print('Skip reading PyPDF file')
        warnings.warn('PyPDF file not read, it must be read before file imports in main script')
        return b_(''),0

    
def pack(packfiles):
    global _packlist
    packlist = ([packfiles] if isinstance(packfiles,str) else packfiles)
    for item in packlist:
        if item not in _packlist:
            _packlist.append(item)
    return packfiles


def publish(output           = None,
            in_place         = True,
            show_plot        = True,
            prompt_overwrite = False,
            verbose          = True,
            **kwargs):
    
    global _packlist,_filespacked,_pyfile,_revision,_imported_packlist

    ## Save the matplotlib plot
    temp_plot = available_filename('temp_plot.pdf')
    if verbose: print('\nSaving figure as temporary file: ' + temp_plot)
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
            warnings.warn('Local copy of ' + output + ' found')
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
                warnings.warn('Unable to overwrite local file ' + output)
                output = available_filename(output)
                warnings.warn('Publishing as {:s} instead'.format(output))

    ## If input PyPDF file hasn't been read yet, do that now
    if _pyfile == b_(''):
        new_kwargs = dict(pypdfplot_kwargs)
        new_kwargs['skip'] = False
        _pyfile,_revision = read(pyname,**new_kwargs)

    ## Write the PyPDF file
    if verbose: print('\nPreparing PyPDF file:')
    with open(temp_plot,'rb') as fr, open(output,'wb+') as fw:
        pw = PyPdfFileWriter(fr,_revision)
                        
        for fname in _packlist:
            if verbose: print('-> Attaching '+ fname)
            with open(fname,'rb') as fa:
                fdata = fa.read()
                pw.addAttachment(fname,fdata)

        if verbose: print('-> Attaching ' + pyname)
        fdata = _pyfile + b_('\n"""')
        pw.addAttachment(pyname,fdata)
        pw.setPyFile(pyname)

        if verbose: print('-> Writing '+output+'\n')
        pw.write(fw)

    _filespacked = True    

    ## Remove the temporary plot
    if verbose: print('Cleaning up:\n-> Removing ' + temp_plot)
    try:
        os.remove(temp_plot)
    except:
        warnings.warn('Unable to remove ' + temp_plot)
        
    ## Remove the generating python file
    if in_place:
        if verbose: print('-> Removing ' + pyname)
        if normcase(realpath(pyname)) != normcase(realpath(__file__)): 
            try:
                os.remove(pyname)
                warnings.warn(pyname + ' removed, saving script in editor will make it reappear...!')
            except:
                warnings.warn('Unable to remove ' + pyname)
        else:
            warnings.warn('Attempt to delete library file was prevented')    

    ## Show the plot:
    if verbose: print('\nShowing plot...')
    if show_plot:
        show(**kwargs)

def cleanup(verbose = True):
    if _filespacked:
        if verbose: print('\nCleaning up attached files:')
        for fname in _packlist:
            if verbose: print('-> Removing ' + fname)
            try:
                os.remove(fname)
            except:
                warnings.warn('Unable to remove {:s}.'.format(fname))
    else:
        warnings.warn("Files weren't packed into PyPDF file yet, aborting cleanup")

def fix_pypdf(fname):
    ## Reads Class IIA PyPDF file and converts it to Class I
    base,ext = os.path.splitext(fname)
    output = base+'_fixed'+ext
    with open(fname,'rb') as fr, open(output,'wb') as fw:
        pr = PyPdfFileReader(fr)
        pw = PyPdfFileWriter(pr).write(fw)
        
## Initialize variables
pyname   = os.path.basename(sys.argv[-1])
base,ext = os.path.splitext(pyname)

_packlist = []
_filespacked = False
_pyfile = b_('')
_revision = 0

## Lookup keyword arguments
try:
    frame = inspect.stack()[0].frame
except(AttributeError):
    frame = inspect.stack()[0][0]
    
while(frame.f_globals['__name__'] != '__main__'):
    frame = frame.f_back
    
try:
    pypdfplot_kwargs = frame.f_globals['pypdfplot_kwargs']
except(KeyError):
    pypdfplot_kwargs = {}

## Read PyPDF file
if pyname != '':
    _pyfile,_revision = read(pyname,**pypdfplot_kwargs)

