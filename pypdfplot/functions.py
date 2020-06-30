from matplotlib.pyplot import show,savefig
from .classes import PyPdfFileReader,PyPdfFileWriter,b_,warnings
from ._version import __version__
import sys
import os
from os.path import normcase,realpath
import subprocess
import io

_packlist = []
_filespacked = False
_pyfile = b_('')

if sys.version_info[0] < 3:
    input = raw_input

def _available_filename(fname):
    base,ext = os.path.splitext(fname)
    i = 1
    fname = base + ext
    while os.path.isfile(fname):
        fname = base + '({:1d})'.format(i) + ext
        i += 1

    return fname

def read(input_file,verbose = True,skip = False):
    global _pure_py,_pyfile,_pyname
    _pyname = input_file #TO-DO: Should be filename instead of file
    if not skip:
        with open(input_file,'rb') as fr:
            read_buf = fr.read()
            first1k = read_buf[:1024]
            pdf_start = first1k.find(b_("%PDF"))
            
            if pdf_start >= 0:
                _pure_py = False
                
                if verbose: print('\nPypdfplot loaded from mixed PyPDF file')
                pr = PyPdfFileReader(read_buf[pdf_start:])
                
                if verbose: print('Extracting embedded files:')
                _pyfile = pr.extractEmbeddedFiles()

            else:
                _pure_py = True
                if verbose: print('\nPypdfplot loaded from Python-only file')
                fr.seek(0)
                _pyfile = fr.read().replace(b_('\r\n'),b_('\n'))
                fnames = []
        
    ## If reading is skipped:
    else:
        if verbose: print('Skip reading PyPDF file')
        warnings.warn('PyPDF file not read, it must be read before file imports in main script')
        _pyfile = b_('')

    
def pack(packfiles):
    global _packlist
    packlist = ([packfiles] if isinstance(packfiles,str) else packfiles)
    for item in packlist:
        if item not in _packlist:
            _packlist.append(item)
    return packfiles


def publish(output           = None,
            cleanup          = True,
            show_plot        = True,
            prompt_overwrite = False,
            verbose          = True,
            col_width        = 79,
            **kwargs):
    
    global _packlist,_filespacked,_pyfile,_imported_packlist

    ## Save the matplotlib plot
    if verbose: print('\nSaving figure...')
    try:
        show_kwargs = {'block':kwargs.pop('block')}
    except:
        show_kwargs = {}
    temp_buf = io.BytesIO()
    savefig(temp_buf,format='pdf',**kwargs)

   

    ## If input PyPDF file hasn't been read yet, do that now
    if _pyfile == b_(''):
        new_kwargs = dict(pypdfplot_kwargs)
        new_kwargs['skip'] = False
        read(_pyname,**new_kwargs)

    ## Write the PyPDF file
    if verbose: print('\nPreparing PyPDF file:')
    output_buf = io.BytesIO()
    pw = PyPdfFileWriter(temp_buf,output_buf)
              
    for fname in _packlist:
        if verbose: print('-> Attaching '+ fname)
        with open(fname,'rb') as fa:
            fdata = fa.read()
            pw.addAttachment(fname,fdata)

    if verbose: print('-> Attaching ' + _pyname)
    fdata = _pyfile + b_('\n"""')
    pw.addAttachment(_pyname,fdata)
    pw.setPyFile(_pyname)
    pw.setPyPDFVersion(__version__)

    ## Name the output file
    if output == None:
        output = os.path.splitext(_pyname)[0] + '.pdf'
    elif os.path.splitext(output)[1] == '':
        output += '.pdf'
    elif os.path.splitext(output)[1] not in ['.pdf','.py']:
        output = os.path.splitext(output)[0] + '.pdf'
        warnings.warn('Invalid extension, saving as {:s}'.format(output))

    ## If the output file already exists, try to remove it:
    if os.path.isfile(output):
        do_overwrite = False
        if prompt_overwrite:
            warnings.warn('Local copy of ' + output + ' found\nOverwrite file? (y/n)')
            yes_no = input('')
            if yes_no.strip().lower()[0] == 'y':
                do_overwrite = True
            else:
                output = _available_filename(output)
                warnings.warn('Publishing as {:s} instead'.format(output))
        else:
            do_overwrite = True

        if do_overwrite:
            try:
                os.remove(output)
            except:
                warnings.warn('Unable to overwrite local file ' + output)
                output = _available_filename(output)
                warnings.warn('Publishing as {:s} instead'.format(output))
    
    ## Write the output file:
    if verbose: print('\nSaving '+output+'...\n')
    pw.write()
    with open(output,'wb+') as fw:
        output_buf.seek(0)
        for line in output_buf:
            while len(line) > col_width + 1:
                i = line[:col_width].rfind(b_(' '))
                fw.write(line[:i]+b_('\n'))
                line = line[i+1:]
            fw.write(line)

    _filespacked = True    

    ## Remove the generating python file or create a new purely Python one:
    if cleanup or not _pure_py:
        if verbose: print('-> Removing ' + _pyname)
        if normcase(realpath(_pyname)) != normcase(realpath(__file__)): 
            try:
                os.remove(_pyname)
                warnings.warn(_pyname + ' removed:\nSaving script in editor will make it reappear...!\n')
            except:
                try:
                    del_script = "python -c \"import os, time; time.sleep(1); os.remove('{}');\"".format(_pyname)
                    subprocess.Popen(del_script)
                    warnings.warn(_pyname + ' removed:\nSaving script in editor will make it reappear...!\n')
                except:
                    warnings.warn('Unable to remove ' + _pyname)
        else:
            warnings.warn('Attempt to delete __init__ file was prevented')

    ## Write the Python file if needed:
    if not cleanup and not _pure_py:
        with open(_pyname,'wb') as fw:
            fw.write(_pyfile)

    ## Cleanup files if needed:
    if cleanup:
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

    ## Show the plot:
    if show_plot:
        if verbose: print('Showing plot...')
        show(**show_kwargs)


def fix_pypdf(fname,
              output           = None,
              in_place         = True,
              verbose          = True):
    
    ## Reads severed file and fixes xref tables and lengths
    base,ext = os.path.splitext(fname)
    if output == None:
        output = _available_filename(base + '_FIXED' + ext)
    else:
        if output == fname:
            if in_place == False:
                warnings.warn('Output name same as input, in_place set to True')
                in_place = True
        
    with open(fname,'rb') as fr, open(output,'wb') as fw:
        if verbose: print('-> Reading ' + fname)
        pw = PyPdfFileWriter(fr,fw)
        if verbose: print('-> Saving as ' + output)
        pw.write()
    
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

