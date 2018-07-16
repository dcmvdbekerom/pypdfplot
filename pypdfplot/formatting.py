def append_pdf(fbuf,extra_bytes):
    
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

def chop(buf,line_len):
    rbuf = ''
    line_length = line_len-1
    temp_buf = buf[:-5]
    trailer  = buf[-5:].replace('\n','\n%')
    while len(temp_buf)>line_length:
        rbuf    += '%'+temp_buf[:line_length]+'\n'
        temp_buf     = temp_buf[ line_length:]

    rbuf += '%' + temp_buf + trailer
    return rbuf

def glue(buf,line_len):
    rbuf = ''
    line_length = line_len-1
    temp_buf = buf[:-7]
    trailer  = buf[-7:].replace('%','')
    while len(temp_buf)>line_length:
        rbuf     += temp_buf[1:line_length+1]
        temp_buf  = temp_buf[(line_length+2):]
    rbuf += temp_buf[1:] + trailer
    return rbuf
