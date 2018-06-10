# -*- coding: utf-8 -*-
from matplotlib.pyplot import *

import os
import sys
import datetime
import pickle

LINE_LENGTH = 128

cleanup_list = []
packed_files = []
file_package = ''
file_table   = ''
file_ptr = 0

pyname   = os.path.basename(sys.argv[0])
base,ext = os.path.splitext(pyname)

if pyname != '':
    with open(pyname,'rb') as f:
        fbuf = f.read().replace('\r\n','\n')
        __fbuf = fbuf

        ## find revision
        eos = fbuf.find('')
        rev_str = fbuf[eos+1:].split('\n')[3]

        if rev_str[12:21] == 'Revision:':
            rev = int(rev_str[21:31])+1
        else:
            rev = 1

        ## unpack files
        try:
            ipdf = fbuf[eos+1:].find('%PDF') + eos + 1
            i1   = fbuf[ipdf:].find('\n')+ipdf+2
            table_size = int(fbuf[i1   :i1+10])
            n_files    = int(fbuf[i1+11:i1+21])

            table = fbuf[i1+21:i1+table_size+21].split('\n')[1:-1]

            for line in table:
                cols   = line.split('|')
                fname  = cols[0][1:]
                begin  = int(cols[1]) + i1 + 20 + table_size
                end    = int(cols[2]) + begin

                buf = fbuf[begin:end]
                
                trailer = buf[-7:].replace('%','')
                pibuf   = buf[1:-7].replace('\n%','')+trailer

                if not os.path.exists(fname):
                    with open(fname,'wb') as f:
                        f.write(pickle.loads(pibuf))
                    print 'File "'+fname+'" unpacked...'
                else:
                    print 'File "'+fname+'" already exists, skip unpacking...'

        except(ValueError):
            print 'No packed files found...'
            pass
    print '~~~'

        
def pack(fname,cleanup = False):
    global file_package,file_table,file_ptr
    with open(fname,'rb') as f:
        buf = f.read()
    temp_buf = pickle.dumps(buf,0)
    pibuf = ''
    while len(temp_buf)>LINE_LENGTH:
        pibuf    += temp_buf[:LINE_LENGTH ]+'\n'
        temp_buf  = temp_buf[ LINE_LENGTH:]
    
    pibuf += temp_buf+'\n'
    pibuf = '%'+pibuf.replace('\n','\n%')[:-1]

    file_package += pibuf
    packed_files.append(fname)

    file_table += '%{:s}|{:d}|{:d}\r\n'.format(fname,file_ptr,len(pibuf))
    file_ptr   += len(pibuf)
    
    if cleanup:
        cleanup_list.append(fname)

    print 'File "'+fname+'" marked for packaging'+(' & deletion in folder' if cleanup else '')+'...'
            

def __append_pdf(fbuf,extra_bytes):
    
    extra_len = len(extra_bytes)
    i1 = fbuf.rfind('startxref')
    startxref = fbuf[i1:]
    startxref_list = startxref.split('\n')
    i2 = int(startxref_list[1])
    startxref_list[1] = '{:d}'.format(i2 + extra_len)

    xref = fbuf[i2:i1]
    xref_list = xref.split('\n')
    N = int(xref_list[1].split(' ')[1])

    for i in range(1,N):
        line = xref_list[i+2]
        n  = int(line[:10])
        n += extra_len
        xref_list[i+2] = '{:010d}'.format(n)+line[10:]

    xref2      = '\n'.join(xref_list)
    startxref2 = '\n'.join(startxref_list)

    fbuf1 = xref  + startxref
    fbuf2 = xref2 + startxref2

    body = fbuf[:i2]
    i3 = body.find('%PDF')
    i4 = body[i3:].find('\n')+i3+1
    body2 = body[:i4] + extra_bytes + body[i4:] 

    fbuf2 = body2 + xref2 + startxref2

    return fbuf2

def publish(cleanup = ['all','none','individual'][2],
            inplace = True,
            do_show = True
            ):

    global file_table,file_package

    py_file = __fbuf[:eos]
        
    now = datetime.datetime.now()
    version_info = " ### -+- Don't remove this line -+- ###\r\n"+\
                   " ###  |    Date:    {:}   |  ###\r\n".format(now.strftime("%Y-%m-%d"))+\
                   " ###  |    Time:         {:}   |  ###\r\n".format(now.strftime("%H:%M"))+\
                   " ###  |    Revision: {:9d}   |  ###\r\n".format(rev)+\
                   " ### -+--------------------------+- ###\r\n\r\n"+\
                   '"""\r\n'

    ## Prepare packing: 
    file_table = '%{:010} {:010d}\r\n'.format(len(file_table),len(packed_files)) + file_table
    file_package = file_table + file_package

    ## Save the plot:
    plotname = base + '_plot.pdf'
    savefig(plotname)

    with open(plotname,'rb') as f:
        plot_file = f.read()
        
    os.remove(plotname)
    plot_file = __append_pdf(plot_file,file_package)

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
    if os.path.exists(savename):    
        for fname in cleanup_list:
            os.remove(fname)

        if inplace:
            if ext == '.py':
                os.remove(pyname)

    ## Output:

    print '~~~\nPublished file: "'+savename+'"...!'
    print 'Packed {:d} file'.format(len(packed_files))+('s...' if len(packed_files) >1 else '...')
    print 'Revision: '+str(rev)
    print '~~~\nYou can now close the Python editor...'

    if do_show:
        show()
    return 0
