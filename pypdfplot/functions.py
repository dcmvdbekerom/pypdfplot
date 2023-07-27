import matplotlib.pyplot as plt
from pypdfplot.classes import (PyPdfFileReader, PyPdfFileWriter,
                               PdfReader)
import warnings
from pypdfplot._version import __version__
import sys
import os
from os.path import normcase, realpath
import subprocess
import io
import pickle

if sys.version_info[0] < 3:
    input = raw_input

class PyPdfHandler:

    def __init__(self):
        self.packlist = []
        self.py_file = b''
        self.pypdf_fname = ''
        self.iteration = 0
        self.verbose = False


    def unpack(self):

        self.pypdf_fname = os.path.basename(sys.argv[0])

        with open(self.pypdf_fname, 'rb') as fr:

            #TO-DO: byte level operations should go to classes.py
            read_buf = fr.read()
            first1k = read_buf[:1024]
            pdf_start = first1k.find(b"%PDF")

            #try:
            if pdf_start >= 0:
                            
                pr = PyPdfFileReader(read_buf[pdf_start:])
                
                if self.verbose: print('Extracting embedded files:')
                self.py_file = pr.extractEmbeddedFiles()

                if self.verbose: print('\nPypdfplot loaded from mixed PyPDF file')
                self.pure_py = False

            #except:
            else:
                            
                fr.seek(0)
                self.py_file = fr.read().replace(b'\r\n',b'\n')

                if self.verbose: print('\nPypdfplot loaded from Python-only file')
                self.pure_py = True


    def write_pypdf(self,
                    plot_bytes,
                    output_fname     = None,
                    pack_list        = [],    # TO-DO: add boolean flags for CLI: 
                    cleanup          = True,  # -k, --keep_files
                    multiple         = ['pickle','add_page','finalize'][0],
                    force_pickle     = False, # -f, --force_pickle
                    verbose          = True,  # -s, --silent
                    prompt_overwrite = False, # -p, --prompt_overwrite
                    **kwargs):

        self.output_fname = output_fname
        self.pack_list = pack_list
        self.cleanup = cleanup
        self.multiple = multiple
        self.force_pickle = force_pickle
        self.verbose = verbose
        self.prompt_overwrite = prompt_overwrite
        self.kwargs = kwargs

        ## Init PyPdfWriter:
        if multiple == 'pickle' or self.iteration == 0:
            
            if verbose: print('\nPreparing PyPDF file:')
            self.pw = PyPdfFileWriter()

            ## If input PyPDF file hasn't been read yet, do that now:
            if self.py_file == b'':
                self.unpack()

        ## Add a page with the plot to the PyPDF file:
        self.do_pickle = (force_pickle if multiple != 'pickle' or self.iteration == 0 else True)
        if multiple in ['pickle', 'add_page']:
            if verbose: print('Adding page...')
            self.add_page(plot_bytes)     

        ## Write output:
        if multiple in ['pickle', 'finalize']:
            self.finalize_pypdf()
            
        self.iteration += 1


    def add_page(self, plot_bytes):
        pr = PdfReader(plot_bytes)
        self.pw.append_pages_from_reader(pr)


    def finalize_pypdf(self):

        writesuccess = False

        ## Name the output file
        if self.output_fname == None:
            #DvdB: When does this happen?
            self.output_fname = os.path.splitext(self.pypdf_fname)[0] + '.pdf' #TO-DO: Make sure to prevent self-deletion!!
        elif os.path.splitext(self.output_fname)[-1] == '':
            self.output_fname += '.pdf'
        elif os.path.splitext(self.output_fname)[1] not in ['.pdf','.py']: #TO-DO: Shouldn't this be just '.pdf'?
            self.output_fname = os.path.splitext(self.output_fname)[0] + '.pdf'
            warnings.warn('Invalid extension, saving as {:s}'.format(self.output_fname))
        
        self.py_packed_fname = self.output_fname[:-3] + 'py'

        ## Attach Python file and auxiliary files:
        if self.do_pickle:
            if self.verbose: print('-> Pickling figure...')
                    
            if len(self.pack_list):
                warnings.warn('pack_list will be ignored when pickling figure!')

            fig_fname = output_fname[:-3] + 'pkl'
            fig = plt.gcf()
            fig.canvas = plt.figure().canvas
            fdata = pickle.dumps(fig)
            self.pw.add_attachment(fig_fname, fdata)

            flines = ["import pypdfplot.backend.unpack",
                      "import matplotlib.pyplot as plt",
                      "from pickle import load",
                      "",
                      "with open('" + fig_fname + "','rb') as f:",
                      "    fig = load(f)",
                      "",
                      "plt.figure(fig.number)",
                      "",
                      "## Plot customizations go here...",
                      "",
                      "plt.savefig('" + self.output_fname + "',",
                      "            pack_list = ['" + fig_fname + "'])",
                      ""]
            
            fdata = '\n'.join(flines).encode() 
            self.pw.addPyFile(self.py_packed_fname, fdata)
            
        else:
            
            for fname in self.pack_list:
                if self.verbose: print('-> Attaching '+ fname)
                with open(fname, 'rb') as fa:
                    fdata = fa.read()
                    self.pw.add_attachment(fname, fdata)

            if self.verbose: print('-> Attaching ' + self.py_packed_fname)
            self.pw.addPyFile(self.py_packed_fname, self.py_file)
        
        ## If the output file already exists, try to remove it:
        if os.path.isfile(self.output_fname):
            do_overwrite = False
            if self.prompt_overwrite:
                warnings.warn('Local copy of ' + self.output_fname + ' found\nOverwrite file? (y/n)')
                yes_no = input('')
                if yes_no.strip().lower()[0] == 'y':
                    do_overwrite = True
                else:
                    self.output_fname = available_filename(self.output_fname)
                    warnings.warn('Publishing as {:s} instead'.format(self.output_fname))
            else:
                do_overwrite = True

            if do_overwrite:
                try:
                    os.remove(output_fname)
                except:
                    warnings.warn('Unable to overwrite local file ' + self.output_fname)
                    self.output_fname = available_filename(self.output_fname)
                    warnings.warn('Publishing as {:s} instead'.format(self.output_fname))
        
        ## Write the output file:
        if self.verbose: print('\nSaving ' + self.output_fname + '...\n')
        with open(self.output_fname,'wb+') as fw:
            self.pw.write(fw)

        write_success = True

        ## Remove the generating python file or create a new purely Python one:
        if self.cleanup or not self.pure_py:
            if os.path.splitext(self.pypdf_fname)[1] == '.py':
                if remove_file(self.pypdf_fname, verbose=self.verbose):
                    warnings.warn(self.pypdf_fname + ' removed:\nSaving script in editor will make it reappear...!\n')

        ## Write the Python file if needed, and remove it if not:
        if self.cleanup:
            # Remove the local copy of the packed Python file if it happens to be present
            # TO-DO: This might be overzealous, consider removing...
            remove_file(self.py_packed_fname, verbose=self.verbose)
        else:
            if not self.pure_py:
                with open(self.py_packed_fname, 'wb') as fw:
                    fw.write(self.py_file)

        ## Cleanup files if needed:
        if self.cleanup:
            if write_success:
                if self.verbose and len(self.pack_list): print('\nCleaning up attached files:')
                for fname in self.pack_list:
                    remove_file(fname, verbose=self.verbose)
            else:
                warnings.warn("Files weren't packed into PyPDF file yet, aborting cleanup")





def available_filename(fname):
    base,ext = os.path.splitext(fname)
    i = 1
    fname = base + ext
    while os.path.isfile(fname):
        fname = base + '({:1d})'.format(i) + ext
        i += 1

    return fname



            


handler = PyPdfHandler()
write_pypdf = handler.write_pypdf
unpack = handler.unpack


def remove_file(fname,verbose = True):

    success = False
    
    if os.path.isfile(fname):
        if verbose: print('-> Removing ' + fname + '...', end = '')
        if normcase(realpath(fname)) != normcase(realpath(__file__)): 
            try:
                os.remove(fname)
                success = True
            except:
                try:
                    ## Removing files via command line sometimes helps if os.remove doesn't work:
                    del_script = "python -c \"import os, time; time.sleep(1); os.remove('{}');\"".format(fname)
                    subprocess.Popen(del_script)
                    success = True
                    
                except:
                    warnings.warn('Unable to remove ' + fname + '...!')
                    success = False
        else:
            warnings.warn('Attempt to delete __init__ file was prevented')
            success = False

        if verbose:
            if success:
                print(' Done!')
            else:
                print(' FAILED!')
    else:
        success = True

    return success


def fix_pypdf(input_fname,
              output_fname = None,
              verbose = True):

    if verbose: print('Fixing ' + input_fname)

    if output_fname == None:
        output_fname = input_fname
    
    pw = PyPdfFileWriter()
    temp_output = io.BytesIO()
    
    #TO-DO: byte level operations should go to classes.py
    with open(input_fname,'rb') as fr: 
        try:
            fr.seek(-1024,2)
            last1k = fr.read()
            eof_addr = last1k.rfind(b'%%EOF')
            pypdf_str = last1k[eof_addr:].split()[2]

            if pypdf_str == b'PyPDF':
                warnings.warn(input_fname + ' is already compliant PyPDF-file, skipping!')
                return
            
        except(IndexError):
            pass
        
        pr = PdfReader(fr)     
        pw.cloneReaderDocumentRoot(pr)
        pw.write(temp_output)

    do_write = True
    if output_fname == input_fname:
        if not remove_file(input_fname, verbose=verbose):
            output_fname = _available_fname(output_fname)
            warnings.warn('File saved as ' + output_fname + 'instead')
          
    if verbose: print('Writing '+ output_fname + '...', end = '')
    temp_output.seek(0)
    with open(output_fname,'wb') as fw:
        fw.write(temp_output.read())

    if verbose: print(' Done!')

