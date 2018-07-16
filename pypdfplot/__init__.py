# -*- coding: utf-8 -*-
from matplotlib.pyplot import *
mpl_show = show

from formatting import *

import os
import sys
import datetime
import pickle
import binascii

LINE_LENGTH = 80
PF_FTR1 = '# END OF PYTHON SCRIPT #\n"""\n'
FT_HDR1 = '%FILETABLE\n'
FT_HDR2 = '%{:010} {:010d} {:010d}\n'
TERMINATOR = '\n%"""' + bytearray([0x00,0xbf])

cleanup_list = []
packed_files = []
collision_list = []
file_package = ''
file_table   = ''
file_ptr = 0

pyname   = os.path.basename(sys.argv[0])
base,ext = os.path.splitext(pyname)

if pyname != '':
    with open(pyname,'rb') as f:
        fbuf = f.read().replace('\r\n','\n').replace('\r','\n')
        eos = fbuf.find(PF_FTR1)

        ## Unpack files
        try:
            i0 = fbuf[eos+1:].find(FT_HDR1) + eos + 1
            i1 = i0 + len(FT_HDR1)
            i2 = i1 + len(FT_HDR2.format(0,0,0))

            table_hdr = fbuf[i1:i1+len(FT_HDR2.format(0,0,0))]
            table_size,n_files,line_length = map(int,table_hdr.replace('%','').split(' '))
            table = fbuf[i2:i2+table_size-1].split('\n')

            for line in table:
                cols   = line.split('|')
                fname  = cols[0][1:]
                begin    = int(cols[1]) + i2 + table_size
                end      = int(cols[2]) + begin
                crc_pack = int(cols[3])
                
                if not os.path.exists(fname):
                    buf   = fbuf[begin:end]

                    pibuf = glue(buf,line_length).replace('\\X','\\x')
                    with open(fname,'wb') as f:
                        f.write(pickle.loads(pibuf))
                    print 'File "'+fname+'" unpacked...'
                else:
                    with open(fname,'rb') as f:
                        buf = f.read()
                    crc_local = binascii.crc32(buf)
                    if crc_pack != crc_local:
                        collision_list.append(fname)
                    print 'File "'+fname+'" already exists, skip unpacking...'

        except(ValueError):
            print 'No packed files found...'

        except Exception as e:
            print e
            
    print '~~~'
else:
    print "[WARNING] Python must be run from script, not from interpreter..."

def pack_pypdfplot():
    print __name__,__file__

def pack(fnames,cleanup = False):
    global file_package,file_table,file_ptr

    if type(fnames) == type(''):
        fnames = [fnames]

    for fname in fnames:
        with open(fname,'rb') as f:
            buf = f.read()

        crc   = binascii.crc32(buf)
        pibuf = chop(pickle.dumps(buf,0).replace('\\x','\\X'),LINE_LENGTH)

        file_package += pibuf
        file_table += '%{:s}|{:d}|{:d}|{:d}\n'.format(fname,file_ptr,len(pibuf),crc)
        file_ptr   += len(pibuf)
        packed_files.append(fname)
        
        if cleanup:
            cleanup_list.append(fname)

        print 'File "'+fname+'" marked for packaging'+(' & deletion in folder' if cleanup else '')+'...'
    return                


def publish(inplace = True,
            do_show = True
            ):

    global file_table,file_package,py_file

    py_file = fbuf[:eos]
    py_lines = py_file.splitlines()
    coding_header = '#'
    
    for i in range(len(py_lines)):
        line = py_lines[i]
        if line != '':
            if line[0] == '#':
                if 'coding:' in line:
                    coding_header = line +'\n#'
                elif not '%PDF' in line:
                    break
            else:
                break

    for j in range(1,len(py_lines)):
        line = py_lines[-j]
        if line != '':
            if line != PF_FTR1:
                break
            
    j = (len(py_lines) if j == 1 else 1-j)        
                
    py_file = '\n'+'\n'.join(py_lines[i:j]) + '\n\n'


    ## Prepare packing: 
    file_table = (FT_HDR1 + 
                  FT_HDR2.format(len(file_table),len(packed_files),LINE_LENGTH) + 
                  file_table)
    file_package = py_file + PF_FTR1 + file_table + file_package + TERMINATOR

    ## Save the plot:
    plotname = base + '_plot.pdf'
    savefig(plotname)

    with open(plotname,'rb') as f:
        plot_file = f.read()
        
    os.remove(plotname)
    plot_file = append_pdf(plot_file,file_package)

    ## Create the new combined file
    if sys.argv[0] == '':
        savename = input('Please specify filename:\n')
        if savename[:-4] != '.pdf':
            savename += '.pdf'
    else:
        savename = base + '.pdf'
    
    if os.path.exists(savename):
        os.remove(savename)

    with open(savename,'wb') as f:
        sbuf  = coding_header
        sbuf += plot_file
        sbuf += '"""\n'
        f.write(sbuf)

    ## Cleanup:
    close_editor_warning = False
    if os.path.exists(savename):    
        for fname in cleanup_list:
            if fname in collision_list:
                close_editor_warning = True
            os.remove(fname)
            if os.path.splitext(fname)[1] == '.py':
                if os.path.exists(fname+'c'):
                    os.remove(fname+'c')

        if inplace:
            if ext == '.py':
                os.remove(pyname)

    ## Output:
    print '~~~'
    print 'Published file: "'+savename+'"...!'
    print 'Packed {:d} file'.format(len(packed_files))+('s...' if len(packed_files) >1 else '...')
##    print 'Revision: '+str(rev)
    print '~~~'
    if close_editor_warning:
        #TODO: Use warnings module for warnings
        print '[WARNING] Packed files have been updated and deleted in folder.'
        print '[WARNING] You must CLOSE this editor WITHOUT SAVING to prevent loss of data.'
        print '[WARNING] Saving and re-running the script will overwrite the updated files with the older ones.'
    else:
        print 'You can now close the Python editor...'

    if do_show:
        mpl_show()
    return


def show(*varg,**kwarg):
##    print '[WARNING] Preview only, not published!'
    mpl_show(*varg,**kwarg)
