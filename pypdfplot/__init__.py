# -*- coding: utf-8 -*-
from matplotlib.pyplot import *
from .formatting import *

import os
import sys
import datetime
import pickle
import binascii

LINE_LENGTH = 128

cleanup_list = []
packed_files = []
trim_list = []
collision_list = []
file_package = ''
file_table   = ''
file_ptr = 0

pyname   = os.path.basename(sys.argv[0])
base,ext = os.path.splitext(pyname)

if pyname != '':
    with open(pyname,'rb') as f:
        fbuf = f.read().replace('\r\n','\n')#.replace('\r','\n')

        ## Find revision
        eos = fbuf.find('')
        rev_str = fbuf[eos+1:].split('\n')[3]

        if rev_str[12:21] == 'Revision:':
            rev = int(rev_str[21:31])+1
        else:
            rev = 1

        ## Unpack files
        try:
            ipdf = fbuf[eos+1:].find('%PDF') + eos + 1
            i1   = fbuf[ipdf:].find('\n')+ipdf+2
            i2   = i1 + 32
            table_size  = int(fbuf[i1   :i1+10])
            n_files     = int(fbuf[i1+11:i1+21])
            line_length = int(fbuf[i1+22:i1+32])
            
            table = fbuf[i2:i2+table_size].split('\n')[1:]
            
            for line in table:
                cols   = line.split('|')
                fname  = cols[0][1:]
                begin    = int(cols[1]) + i2 + 1 + table_size
                end      = int(cols[2]) + begin
                crc_pack = int(cols[3])
                
                if not os.path.exists(fname):
                    buf   = fbuf[begin:end] 
                    pibuf = glue(buf,line_length)
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

def pack(fnames,cleanup = False):#,trim_path = True):
    global file_package,file_table,file_ptr

    if type(fnames) == type(''):
        fnames = [fnames]

    for fname in fnames:
        with open(fname,'rb') as f:
            buf = f.read()

        crc   = binascii.crc32(buf)
        pibuf = chop(pickle.dumps(buf,0),LINE_LENGTH)

##        if trim_path:
##            trim_list.append(fname)
##            fname = os.path.basename(fname)
        
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

    global file_table,file_package

    py_file = fbuf[:eos]

    while(py_file[-2] != '\n'):
        py_file += '\n'

##    for fname in trim_list:
##        py_file.replace(fname,os.path.basename(fname))

    now = datetime.datetime.now()
    version_info = " ### -+- Don't remove this line -+- ###\n"+\
                   " ###  |    Date:    {:}   |  ###\n".format(now.strftime("%Y-%m-%d"))+\
                   " ###  |    Time:         {:}   |  ###\n".format(now.strftime("%H:%M"))+\
                   " ###  |    Revision: {:9d}   |  ###\n".format(rev)+\
                   " ### -+--------------------------+- ###\n\n"+\
                   '"""\n'

    ## Prepare packing: 
    file_table = '%{:010} {:010d} {:010d}\n'.format(len(file_table),len(packed_files),LINE_LENGTH) + file_table
    file_package = file_table + file_package

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
        sbuf  = ''
        sbuf += py_file 
        sbuf += version_info
        sbuf += plot_file
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
    print 'Revision: '+str(rev)
    print '~~~'
    if close_editor_warning:
        #TODO: Use warnings module for warnings
        print '[WARNING] Packed files have been updated and deleted in folder.'
        print '[WARNING] You must CLOSE this editor WITHOUT SAVING to prevent loss of data.'
        print '[WARNING] Saving and re-running the script will overwrite the updated files with the older ones.'
    else:
        print 'You can now close the Python editor...'

    if do_show:
        show()
    return
