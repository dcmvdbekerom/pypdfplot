from ._version import __version__
from matplotlib.pyplot import *
from .classes import PyPdfFileReader,PyPdfFileWriter,b_,warnings
import sys
import os
from os.path import normcase,realpath
import inspect
import subprocess

if sys.version_info[0] < 3:
    input = raw_input

def available_filename(fname):
    base,ext = os.path.splitext(fname)
    i = 1
    fname = base + ext
    while os.path.isfile(fname):
        fname = base + '({:1d})'.format(i) + ext
        i += 1

    return fname

def read(input_file,verbose = True,skip = False):
    
    if not skip:
        with open(input_file,'rb') as fr:
            read_buf = fr.read()
            first1k = read_buf[:1024]
            pdf_start = first1k.find(b_("%PDF"))
            
            if pdf_start >= 0:
                
                if verbose: print('\nPypdfplot loaded from mixed PyPDF file')
                pr = PyPdfFileReader(read_buf[pdf_start:])
                
                if verbose: print('Extracting embedded files:')
                pyfile = pr.extractEmbeddedFiles()

            else:
                if verbose: print('\nPypdfplot loaded from Python-only file')
                fr.seek(0)
                pyfile = fr.read().replace(b_('\r\n'),b_('\n'))
                fnames = []

        return pyfile
        
    ## If reading is skipped:
    else:
        if verbose: print('Skip reading PyPDF file')
        warnings.warn('PyPDF file not read, it must be read before file imports in main script')
        return b_(''),0 #TO-DO: should not return ,0

    
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
    
    global _packlist,_filespacked,_pyfile,_imported_packlist

    ## Save the matplotlib plot
    temp_plot = available_filename('temp_plot.pdf')
    if verbose: print('\nSaving figure as temporary file: ' + temp_plot)
    savefig(temp_plot)

    ## Name the output file
    if output == None:
        output = base + '.pdf'
    elif os.path.splitext(output)[1] == '':
        output += '.pdf'
    elif os.path.splitext(output)[1] not in ['.pdf','.py']:
        output = os.path.splitext(output)[0] + '.pdf'
        warnings.warn('Invalid extension, saving as {:s}'.format(output))
    if verbose: print('Output filename: ' + output)

    ## If the output file already exists, try to remove it
    if os.path.isfile(output):
        do_overwrite = False
        if prompt_overwrite:
            warnings.warn('Local copy of ' + output + ' found')
            warnings.warn('Overwrite file? (y/n)')
            yes_no = input('')
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
        _pyfile = read(pyname,**new_kwargs)

    ## Write the PyPDF file
    if verbose: print('\nPreparing PyPDF file:')
    with open(temp_plot,'rb') as fr, open(output,'wb+') as fw:
        pw = PyPdfFileWriter(fr,fw)

        ## TO-DO: at some point this should be done with the                 
        for fname in _packlist:
            if verbose: print('-> Attaching '+ fname)
            with open(fname,'rb') as fa:
                fdata = fa.read()
                pw.addAttachment(fname,fdata)

        if verbose: print('-> Attaching ' + pyname)
        fdata = _pyfile + b_('\n"""')
        pw.addAttachment(pyname,fdata)
        pw.setPyFile(pyname)
        pw.setPyPDFVersion(__version__)

        if verbose: print('-> Writing '+output+'\n')
        pw.write()

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
                try:
                    del_script = "python -c \"import os, time; time.sleep(1); os.remove('{}');\"".format(pyname)
                    subprocess.Popen(del_script)
                    warnings.warn(pyname + ' removed, saving script in editor will make it reappear...!')
                except:
                    warnings.warn('Unable to remove ' + pyname)
        else:
            warnings.warn('Attempt to delete __init__ file was prevented')

    ## Show the plot:
    if show_plot:
        if verbose: print('\nShowing plot...')
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

def fix_pypdf(fname,
              output           = None,
              in_place         = True,
              verbose          = True):
    
    ## Reads Class IIA PyPDF file and converts it to Class I
    base,ext = os.path.splitext(fname)
    if output == None:
        output = available_filename(base + '_FIXED' + ext)
    else:
        if output == fname:
            if in_place == False:
                warnings.warn('Output name same as input, in_place set to True')
                in_place = True
        
    with open(fname,'rb') as fr, open(output,'wb') as fw:
        if verbose: print('-> Reading ' + fname)
        pw = PyPdfFileWriter(fr,0)
        if verbose: print('-> Saving as ' + output)
        pw.write(fw)
    
    if in_place:
        if verbose: print('-> Removing ' + fname)
        try:
            os.remove(fname)
            if verbose: print('-> Renaming ' + output + ' to ' + fname)
            os.rename(output,fname)
        except:
            try:
                del_script = "python -c \"import os, time; time.sleep(1); os.remove('{:}'); os.rename('{:}','{:}');\"".format(fname,output,fname)
                subprocess.Popen(del_script)
                if verbose: print('-> Renaming ' + output + ' to ' + fname)
            except:
                warnings.warn('Unable to remove ' + fname + ', file saved as ' + output + 'instead')

       
## Initialize variables
pyname   = os.path.basename(sys.argv[-1])
base,ext = os.path.splitext(pyname)

_packlist = []
_filespacked = False
_pyfile = b_('')

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
    _pyfile = read(pyname,**pypdfplot_kwargs)


