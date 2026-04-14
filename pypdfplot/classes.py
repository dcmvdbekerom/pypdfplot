# -*- coding: utf-8 -*-
#
# vim: sw=4:expandtab:foldmethod=marker
#
# Copyright (c) 2006, Mathieu Fenniak
# Copyright (c) 2007, Ashish Kulkarni <kulkarni.ashish@gmail.com>
# Copyright (c) 2019, Dirk van den Bekerom <dcmvdbekerom@gmail.com>
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# * The name of the author may not be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

debug = False


from pypdf import PdfWriter, PdfReader
from pypdf.generic import *
from pypdf.errors import PdfReadError

from pypdf._utils import (
    StrByteType,
    StreamType,
)
import warnings

from binascii import hexlify
import sys
import io
import os
import struct

__PYPDFVERSION__ = '1.0'
_pyfile_appendix = b'\n"""\n--- Do not edit below ---'

def ASCIIHexEncode(self):
    #TODO: replace with pypdf version
    self._data = hexlify(self._data) + b'>'
    try:
        f = self["/Filter"]
        if isinstance(f, ArrayObject):
            f.insert(0, NameObject("/ASCIIHexDecode"))
        else:
            newf = ArrayObject()
            newf.append(NameObject("/ASCIIHexDecode"))
            newf.append(f)
            f = newf
            
    except(KeyError):
        f = ArrayObject()
        f.append(NameObject("/ASCIIHexDecode"))

    self[NameObject("/Filter")] = f

    try:
        # Update DecodeParms if present:
        p = self["/DecodeParms"]
        if isinstance(p, ArrayObject):
            p.insert(0, NullObject())
        else:
            newp = ArrayObject()
            newp.append(NullObject())
            newp.append(p)
            p = newp
            
        self[NameObject("/DecodeParms")] = p
        
    except(KeyError): #TODO: when does this happen? Doesn't look safe..
        pass
   
StreamObject.ASCIIHexEncode = ASCIIHexEncode


class PyPdfFileReader(PdfReader):
    
    def __init__(self, read_buf, **kwargs):
        ##Fix XREF table, obj length, etc.:
        in_stream = self.sanitizePDF(read_buf)

        ##From this point we have a plain old regular PDF file
        super(PyPdfFileReader,self).__init__(in_stream, **kwargs)

    def sanitizePDF(self,read_buf,output = None):

        #TO-DO: Add correction for LF/CRLF mixup

        first1k = read_buf[:1024]
        py_obj = int(first1k.split()[1])

        last1k = read_buf[-1024:]
        startxref_addr = last1k.rfind(b'startxref')+len(b'startxref\n')
        filesize_addr = last1k.rfind(b'%%EOF')+len(b'%%EOF\n')

        old_size = int(last1k[filesize_addr:].split()[0])
        offset = len(read_buf) - old_size + 1 
        startxref = int(last1k[startxref_addr:].split()[0]) + offset

        br = io.BytesIO(read_buf)

        # Update object length:
        # TO-DO: replace with RE
        br.seek(0,0)
        line = br.readline()
        i1 = line.rfind(b'/Length')+len(b'/Length')
        i2 = line.rfind(b'>>')
        length_len = i2 - i1
        br.seek(i1)
        obj_length = int(br.read(length_len))
        new_length = obj_length + offset
        br.seek(i1)
        length_str = (' {:'+'{:d}'.format(length_len-2)+'d} ').format(new_length).encode()
        br.write(length_str)

        #Update xref table:
        br.seek(startxref,0)
        br.readline()
        nobj = int(br.readline().split()[1])
        br.readline()

        for i in range(1,nobj):
            addr = br.tell()
            obj_addr = int(br.read(10))

            if i != py_obj:
                obj_addr += offset
                br.seek(addr,0)
                br.write("{:010d}".format(obj_addr).encode())

            br.readline()

        #Update startxref:
        br.seek(-1024,2)
        br.seek(startxref_addr,1)
        addr = br.tell()
        br.write("{:d}\n%%EOF\n".format(startxref).encode())
        br.truncate()
        br.seek(0,0)

        ## Save to output (TO-DO: why is this even here?)
        if output != None:
            
            output_buf = br.read()
            with open(output,'wb') as f:
                f.write(output_buf)

        return br


    def extractEmbeddedFiles(self,verbose = True):

        #TODO: do this with: for name, file in pr.attachments.items(): 

        root_obj = self.trailer['/Root']
        file_dict = root_obj['/Names']['/EmbeddedFiles']['/Names']
        
        pyname = root_obj['/PyFile']
        for i in range(0,len(file_dict),2):
            fname = file_dict[i]
            fobjh = file_dict[i+1]

            if isinstance(fobjh,IndirectObject):
                fobjh = fobjh.get_object()

            fobj = fobjh['/EF']['/F']

            if isinstance(fobj,IndirectObject):
                fobj = fobj.get_object()

            if fname == pyname:
                pyfile = fobj.get_data()
                pyfile = pyfile[:pyfile.rfind(b'\n"""')]
                if verbose: print('-> Extracting generating script: ' + fname)
                
            else:  
                if not os.path.isfile(fname):
                    fdata = fobj.get_data()
                    with open(fname,'wb') as fw:
                        fw.write(fdata)
                        if verbose: print('-> Extracing ' + fname)
                else:
                    if verbose: print('-> ' + fname +' already exists, skipping')
        return pyfile


class PyPdfFileWriter(PdfWriter):
    def __init__(self, after_page_append=None, **kwargs): # in_stream,  out_stream,

       
        super(PyPdfFileWriter,self).__init__()
        # self._stream = io.BytesIO()
        self.col_width = 79 #TODO: make this cusomizable by user

        '''
        Create a copy (clone) of a document from a PDF file reader

        :param reader: PDF file reader instance from which the clone
            should be created.
        :callback after_page_append (function): Callback function that is invoked after
            each page is appended to the writer. Signature includes a reference to the
            appended page (delegates to appendPagesFromReader). Callback signature:

            :param writer_pageref (PDF page reference): Reference to the page just
                appended to the document.
        '''

        if debug:
            print("Number of Objects: %d" % len(self._objects))
            for obj in self._objects:
                print("\tObject is %r" % obj)
                if hasattr(obj, "indirectRef") and obj.indirectRef != None:
                    print("\t\tObject's reference is %r %r, at PDF %r" % (obj.indirectRef.idnum, obj.indirectRef.generation, obj.indirectRef.pdf))

##        reader = PdfFileReader(in_stream)   
##        self.appendPagesFromReader(reader)
   

    def addPyFile(self,fname,fdata):
        self.add_attachment(fname,fdata + _pyfile_appendix)
        self.root_object[NameObject("/PageMode")] = NameObject("/UseAttachments")
        self.root_object[NameObject('/PyFile')] = create_string_object(fname)
        
        #add backup
        backup_obj = DecodedStreamObject()
        backup_obj.set_data(fdata + _pyfile_appendix)
        
        backup_obj = backup_obj.flate_encode()
        backup_obj.ASCIIHexEncode()
        
        backup_ref = self._add_object(backup_obj)
        
        self.root_object[NameObject('/PyBackup')] = backup_ref
        
        

    def setPyPDFVersion(self,version):
        
        self.pypdf_version = version

        major_str, minor_str = version.split('.')[:2]
        self.major_pypdf_version = int(major_str)
        self.minor_pypdf_version = int(minor_str)

        self.root_object[NameObject('/PyPDFVersion')] = create_string_object(version)


##    # TODO
##    def setNewlineChar(self,newline_char):
##        self._root_object[NameObject('/PyPDFNewlineChar')] = create_string_object(newline_char)



    #overwrite from pypdf:
    def _write_pdf_structure(self, stream: StreamType) -> tuple[list[int], list[int]]:
        
        self.setPyPDFVersion(__PYPDFVERSION__)
        
        object_positions = len(self._objects)*[None]
        free_objects = []
        stream.write(b'#' + self.pdf_header.encode() + b" ")
        # stream.write(b"%\xE2\xE3\xCF\xD3 ") # not required
        
        
        # Find PyFile obj:
        try:
            pyname = self.root_object['/PyFile']
            obj_list = self.root_object["/Names"]["/EmbeddedFiles"]["/Names"]
            obj_dict = dict(zip(obj_list[0::2],obj_list[1::2]))
            py_idnum = list(obj_dict[pyname]['/EF'].values())[0].idnum
            
        except(KeyError):
            warnings.warn("/PyFile keyword not found, looks like a regular PDF file!")
            py_idnum = -1
            return

        # Write PyFile first:
        py_obj = self._objects[py_idnum - 1]
        if isinstance(py_obj, EncodedStreamObject):
            py_obj.get_data()
            py_obj = py_obj.decoded_self        
        
        object_positions[py_idnum - 1] = stream.tell() - 1 # -1 to account for the '#' at the start of PyPDF file
        stream.write(f"{py_idnum} 0 obj ".encode())

        py_obj[NameObject("/Length")] = NumberObject(len(py_obj._data))
        
        stream.write(b"<< ")
        for key, value in list(py_obj.items()):
            key.write_to_stream(stream)
            stream.write(b" ")
            if key == '/Length':
                space = 10 - len(str(value))
                stream.write(space*b" ")
            value.write_to_stream(stream)
            stream.write(b" ")
        stream.write(b">> stream\n")
        stream.write(py_obj._data)
        stream.write(b"\nendstream\nendobj\n")

        # Write remaining objects
        idnums = list(range(1,len(self._objects)+1))
        idnums.pop(py_idnum-1)
        for idnum in idnums:
            obj = self._objects[idnum-1]
            
            if obj is not None:
                object_positions[idnum - 1] = stream.tell() - 1 # -1 to account for the '#' at the start of PyPDF file
                stream.write(f"{idnum} 0 obj\n".encode())
                if self._encryption and obj != self._encrypt_entry:
                    obj = self._encryption.encrypt_object(obj, idnum, 0)
                
                #PyPDF: decode all encoded objects & encode them as flate
                if isinstance(obj, EncodedStreamObject):
                    obj.get_data()
                    obj = obj.decoded_self
                    obj = obj.flate_encode()
                    
                needs_ascii = False
                if isinstance(obj, EncodedStreamObject):
                    f = obj["/Filter"]
                    if isinstance(f, ArrayObject):
                        f = f[0]

                    if f != '/ASCIIHexDecode':
                        needs_ascii = True 
                else:    
                    try:
                        if obj['/Type'] == '/Metadata':
                            obj = obj.flate_encode()
                            
                        if obj['/Type'] in ['/EmbeddedFile', '/Metadata']:
                            needs_ascii = True    
                            
                    except(KeyError, TypeError):
                        pass

                if needs_ascii:

                    obj.ASCIIHexEncode()

                    #Cut it up to fit the 80 columns PEP requirement
                    temp = b''
                    while len(obj._data) > self.col_width:
                        temp += obj._data[:self.col_width] + b'\n'
                        obj._data = obj._data[self.col_width:]
                    temp += obj._data
                    obj._data = temp
                
                    obj.write_to_stream(stream)

                else:   # all other objects are cropped to fit column size
                    obj_stream = io.BytesIO()
                    obj.write_to_stream(obj_stream)
                    obj_stream.seek(0)        
                    for line in obj_stream:
                        while len(line) > self.col_width + 1:
                            i = line[:self.col_width].rfind(b' ')
                            stream.write(line[:i]+b'\n')
                            line = line[i+1:]
                        stream.write(line)
                
                stream.write(b"\nendobj\n")
                    
            else:
                object_positions.append(-1)
                free_objects.append(idnum)
                
        free_objects.append(0)  # add 0 to loop in accordance with specification
        return object_positions, free_objects

    #overwrite from pypdf:
    def _write_trailer(self, stream: StreamType, xref_location: int) -> None:
        
        super()._write_trailer(stream, xref_location - 1) # -1 to account for the '#' at the start of PyPDF file

        eof = '{:000010d} LF\nPyPDF-' + self.pypdf_version
        eof += '\n"""\n'
        eof = eof.format(stream.tell()+len(eof)).encode()
        stream.write(eof)
            