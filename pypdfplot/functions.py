from matplotlib.pyplot import show,savefig,gcf
from .classes import PyPdfFileReader,PyPdfFileWriter,b_,warnings
from ._version import __version__
import sys
import os
from os.path import normcase,realpath
import subprocess
import io
import pickle

_packlist = []
_write_success = False
_py_file = b_('')
_pypdf_fname = ''
_iterations = 0
_first_output_fname = ''

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


def extract(fname = None,
            save_pypdf = False, #TO-DO: This will replace fix_pypdf in the future
            verbose = True,
            ):
    
    global _pure_py,_py_file
    _pypdf_fname = fname

    if fname == None:
        fname = os.path.basename(sys.argv[0])
    
    with open(fname,'rb') as fr:
        read_buf = fr.read()
        first1k = read_buf[:1024]
        pdf_start = first1k.find(b_("%PDF"))

        #try:
        if pdf_start >= 0:
                        
            pr = PyPdfFileReader(read_buf[pdf_start:])
            
            if verbose: print('Extracting embedded files:')
            _py_file = pr.extractEmbeddedFiles()

            if verbose: print('\nPypdfplot loaded from mixed PyPDF file')
            _pure_py = False

        #except:
        else:
                        
            fr.seek(0)
            _py_file = fr.read().replace(b_('\r\n'),b_('\n'))

            if verbose: print('\nPypdfplot loaded from Python-only file')
            _pure_py = True

    return fname


def publish(output_fname     = None,
            file_list        = [],
            cleanup          = True,
            show_plot        = True,
            multiples        = 'pickle',#'pages',
            force_pickle     = False,
            verbose          = True,
            prompt_overwrite = False,
            **kwargs):
    
    global _py_file, _pypdf_fname, _iterations, _first_output_fname

    ## Save the matplotlib plot
    if verbose: print('\nSaving figure...')
    try:
        show_kwargs = {'block':kwargs.pop('block')}
    except:
        show_kwargs = {}
        
    plot_bytes = io.BytesIO()
    savefig(plot_bytes,format='pdf',**kwargs)
    
    ## If input PyPDF file hasn't been read yet, do that now
    if _py_file == b_(''):
        _pypdf_fname = extract()

    ## Name the output file
    if multiples != 'pages' or _iterations == 0:
        if output_fname == None:
            output_fname = os.path.splitext(_pypdf_fname)[0] + '.pdf' #DO-DO: Make sure to prevent self-deletion!!
        elif os.path.splitext(output_fname)[1] == '':
            output_fname += '.pdf'
        elif os.path.splitext(output_fname)[1] not in ['.pdf','.py']: #TO-DO: Shouldn't this be just '.pdf'?
            output_fname = os.path.splitext(output_fname)[0] + '.pdf'
            warnings.warn('Invalid extension, saving as {:s}'.format(output_fname))

    elif multiples = 'pickle':
        output_fname = _first_output_fname
        
    _py_packed_fname = output_fname[:-3] + 'py'
    
    if _iterations == 0:
        _first_output_fname = output_fname


    if multiples == 'pickle' or _iterations == 0:

        ## Write the regular PyPDF file
        if verbose: print('\nPreparing PyPDF file:')
        output_bytes = io.BytesIO()
        pw = PyPdfFileWriter(plot_bytes,output_bytes)

        if force_pickle or _iterations > 0:
            if len(file_list) > 0:
                warnings.warn('file_list will be ignored when pickling figure!')

            fig_fname = output_fname[:-3] + 'pkl'
            fdata = pickle.dumps(gcf())
            pw.addAttachment(fig_fname,fdata)

            flines = [b"import pypdfplot.auto_extract as plt",
                      b"from pickle import load",
                      b"",
                      b"with open('" + fig_fname.encode() + b"','rb') as f:",
                      b"    fig = load(f)",
                      b"",
                      b"plt.figure(fig.number)",
                      b"",
                      b"## Plot customizations go here...",
                      b"",
                      b"plt.publish('" + output_fname.encode() + b"',",
                      b"            file_list = ['" + fig_fname.encode() + b"'])",
                      b"",
                      b'"""']
            
            fdata = b'\n'.join(flines) 
            pw.addAttachment(_py_packed_fname,fdata)
            
        elif multiples == 'pages':         
            for fname in file_list:
                if verbose: print('-> Attaching '+ fname)
                with open(fname,'rb') as fa:
                    fdata = fa.read()
                    pw.addAttachment(fname,fdata)

            if verbose: print('-> Attaching ' + _py_packed_fname)

            fdata = _py_file + b_('\n"""')
            pw.addAttachment(_py_packed_fname,fdata)
        
        pw.setPyFile(_py_packed_fname)
        pw.setPyPDFVersion(__version__)

    else:

        ## This is a consecutive call with 'pages' enabled,
        ## so open previous file and append current plot as page:

        ## TO-DO: This procedure rewrites the entire file each time,
        ##        Would be more efficient to simply attach pages

        warnings.warn('Multiple pages not currently implemented!!!!')
        
        

    ## If the output file already exists, try to remove it:
    if os.path.isfile(output_fname):
        do_overwrite = False
        if prompt_overwrite:
            warnings.warn('Local copy of ' + output_fname + ' found\nOverwrite file? (y/n)')
            yes_no = input('')
            if yes_no.strip().lower()[0] == 'y':
                do_overwrite = True
            else:
                output_fname = _available_filename(output_fname)
                warnings.warn('Publishing as {:s} instead'.format(output_fname))
        else:
            do_overwrite = True

        if do_overwrite:
            try:
                os.remove(output_fname)
            except:
                warnings.warn('Unable to overwrite local file ' + output_fname)
                output_fname = _available_filename(output_fname)
                warnings.warn('Publishing as {:s} instead'.format(output_fname))
    
    ## Write the output file:
    if verbose: print('\nSaving ' + output_fname + '...\n')
    pw.write()
    with open(output_fname,'wb+') as fw:
        output_bytes.seek(0)

        ## Trim column length:
        col_width = 79
        for line in output_bytes:
            while len(line) > col_width + 1:
                i = line[:col_width].rfind(b_(' '))
                fw.write(line[:i]+b_('\n'))
                line = line[i+1:]
            fw.write(line)

    _write_success = True
    _iterations += 1

    ## Remove the generating python file or create a new purely Python one:
    if cleanup or not _pure_py:
        if os.path.isfile(_pypdf_fname):
            if verbose: print('-> Removing ' + _pypdf_fname)
            if normcase(realpath(_pypdf_fname)) != normcase(realpath(__file__)): 
                try:
                    os.remove(_pypdf_fname)
                    warnings.warn(_pypdf_fname + ' removed:\nSaving script in editor will make it reappear...!\n')
                except:
                    try:
                        del_script = "python -c \"import os, time; time.sleep(1); os.remove('{}');\"".format(_pypdf_fname)
                        subprocess.Popen(del_script)
                        warnings.warn(_pypdf_fname + ' removed:\nSaving script in editor will make it reappear...!\n')
                    except:
                        warnings.warn('Unable to remove ' + _pypdf_fname)
            else:
                warnings.warn('Attempt to delete __init__ file was prevented')

    ## Write the Python file if needed, and remove it if not:
    if cleanup:
        # Remove the packed file if it happens to be present
        # TO-DO: This might be overzealous, consider removing...
        if os.path.isfile(_py_packed_fname): 
            os.remove(_py_packed_fname)
    else:
        if not _pure_py:
            with open(_py_packed_fname,'wb') as fw:
                fw.write(_py_file)

    ## Cleanup files if needed:
    if cleanup:
        if _write_success:
            if verbose: print('\nCleaning up attached files:')
            for fname in file_list:
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
              output_fname     = None,
              in_place         = True,
              verbose          = True):
    
    ## Reads severed file and fixes xref tables and lengths
    base,ext = os.path.splitext(fname)
    if output_fname == None:
        output_fname = _available_filename(base + '_FIXED' + ext)
    else:
        if output_fname == fname:
            if in_place == False:
                warnings.warn('Output name same as input, in_place set to True')
                in_place = True
        
    with open(fname,'rb') as fr, open(output_fname,'wb') as fw:
        if verbose: print('-> Reading ' + fname)
        pw = PyPdfFileWriter(fr,fw)
        if verbose: print('-> Saving as ' + output_fname)
        pw.write()
    
    if in_place:
        if verbose: print('-> Removing ' + fname)
        try:
            os.remove(fname)
            if verbose: print('-> Renaming ' + output_fname + ' to ' + fname)
            os.rename(output_fname,fname)
        except:
            try:
                del_script = "python -c \"import os, time; time.sleep(1); os.remove('{:}'); os.rename('{:}','{:}');\"".format(fname,output_fname,fname)
                subprocess.Popen(del_script)
                if verbose: print('-> Renaming ' + output_fname + ' to ' + fname)
            except:
                warnings.warn('Unable to remove ' + fname + ', file saved as ' + output_fname + 'instead')

