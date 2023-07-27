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
from pypdf._utils import read_until_whitespace as readUntilWhitespace
import pypdf._utils as utils
import warnings

from binascii import hexlify
import sys
import io
import os
import struct

__PYPDFVERSION__ = '1.0'
_pyfile_appendix = b'\n"""\n--- Do not edit below ---'

def ASCIIHexEncode(self):

    self._data = hexlify(self._data) + b'>'
 
    f = self["/Filter"]
    if isinstance(f, ArrayObject):
        f.insert(0, NameObject("/ASCIIHexDecode"))
    else:
        newf = ArrayObject()
        newf.append(NameObject("/ASCIIHexDecode"))
        newf.append(f)
        f = newf

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
    
    def __init__(self, read_buf):
        ##Fix XREF table, obj length, etc.:
        in_stream = self.sanitizePDF(read_buf)

        ##From this point we have a plain old regular PDF file
        super(PyPdfFileReader,self).__init__(in_stream)

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
    def __init__(self, after_page_append=None): # in_stream,  out_stream,

       
        super(PyPdfFileWriter,self).__init__()
        self._stream = io.BytesIO()
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
        self._root_object[NameObject("/PageMode")] = NameObject("/UseAttachments")
        self._root_object[NameObject('/PyFile')] = create_string_object(fname)

    def setPyPDFVersion(self,version):
        
        self.pypdf_version = version

        major_str, minor_str = version.split('.')[:2]
        self.major_pypdf_version = int(major_str)
        self.minor_pypdf_version = int(minor_str)

        root_dict = dict(self._root_object)
        root_dict[NameObject('/PyPDFVersion')] = create_string_object(version)
        self._root_object = DictionaryObject(root_dict)

##    def setNewlineChar(self,newline_char):
##        self._root_object[NameObject('/PyPDFNewlineChar')] = create_string_object(newline_char)


    def write(self,fstream):
        """
        Writes the collection of pages added to this object out as a PDF file.

        :param stream: An object to write the file to.  The object must support
            the write method and the tell method, similar to a file object.
        """

        self.setPyPDFVersion(__PYPDFVERSION__)
        
        if hasattr(self._stream, 'mode') and 'b' not in self._stream.mode:
            warnings.warn("File <%s> to write to is not in binary mode. It may not be written to correctly." % self._stream.name)

        if not self._root:
            self._root = self._add_object(self._root_object)

        externalReferenceMap = {}

        # PDF objects sometimes have circular references to their /Page objects
        # inside their object tree (for example, annotations).  Those will be
        # indirect references to objects that we've recreated in this PDF.  To
        # address this problem, PageObject's store their original object
        # reference number, and we add it to the external reference map before
        # we sweep for indirect references.  This forces self-page-referencing
        # trees to reference the correct new object location, rather than
        # copying in a new copy of the page object.

        # BUT for pypdfplot we don't have to worry about this happening,
        # because we only ever get matplotlib outputs, which behave nicely.
        
##        for objIndex in range(len(self._objects)):
##            obj = self._objects[objIndex]
##            if isinstance(obj, PageObject) and obj.indirectRef != None:
##                print 'case0'
##                data = obj.indirectRef
##                if data.pdf not in externalReferenceMap:
##                    print 'case1'
##                    externalReferenceMap[data.pdf] = {}
##                if data.generation not in externalReferenceMap[data.pdf]:
##                    print 'case2'
##                    externalReferenceMap[data.pdf][data.generation] = {}
##                externalReferenceMap[data.pdf][data.generation][data.idnum] = IndirectObject(objIndex + 1, 0, self)

        self.stack = []
        if debug: print(("ERM:", externalReferenceMap, "root:", self._root))
        self._sweep_indirect_references(self._root)
        del self.stack

        # Begin writing:
        offsets = {}
        self._header = b"%PDF-1.4"
        self._stream.write(b'#' + self._header + b" ")

        ## Find the object number of the Python script and rearrange write order

        oi = list(range(len(self._objects)))
        try:
            pyname = self._root_object['/PyFile']
            name_list = self._root.get_object()["/Names"]["/EmbeddedFiles"]["/Names"]
            name_dict = dict(zip(name_list[0::2],name_list[1::2]))
            py_oi = list(name_dict[pyname].get_object()['/EF'].values())[0].idnum - 1
            
            oi.pop(py_oi)
            oi = [py_oi] + oi
            
        except(KeyError):
            warnings.warn("/PyFile keyword not found, looks like a regular PDF file!")
            py_oi = -1
 
        for i in oi:
##        for i in list(range(len(self._objects))):
            idnum = i + 1
            obj = self._objects[i]
            offsets[i] = self._stream.tell()
            encryption_key = None
            
##            if hasattr(self, "_encrypt") and idnum != self._encrypt.idnum:
##                pack1 = struct.pack("<i", i + 1)[:3]
##                pack2 = struct.pack("<i", 0)[:2]
##                key = self._encrypt_key + pack1 + pack2
##                assert len(key) == (len(self._encrypt_key) + 5)
##                md5_hash = md5(key).digest()
##                key = md5_hash[:min(16, len(self._encrypt_key) + 5)]

            if i == py_oi:
                
                ##decode if necessary (in case of severed PyPDF file):
                if isinstance(obj,EncodedStreamObject):
                    obj.get_data()
                    obj = obj.decoded_self
                
                self._stream.write(str(idnum).encode() + b" 0 obj ")

                obj[NameObject("/Length")] = NumberObject(len(obj._data))
                
                self._stream.write(b"<< ")
                for key, value in list(obj.items()):
                    key.write_to_stream(self._stream, encryption_key)
                    self._stream.write(b" ")
                    if key == '/Length':
                        space = 10 - len(str(value))
                        self._stream.write(space*b" ")
                    value.write_to_stream(self._stream, encryption_key)
                    self._stream.write(b" ")
                self._stream.write(b">>")

                del obj["/Length"]
                self._stream.write(b" stream\n")
                data = obj._data
                
                self._stream.write(data)
                self._stream.write(b"\nendstream")
                self._stream.write(b"\nendobj\n")

            else:
                self._stream.write(str(idnum).encode() + b" 0 obj\n")

                # Try to compress every object:
                if type(obj) == DecodedStreamObject:
                    obj = obj.flate_encode()

                # Hex encode object to make it compatible with Python interpreter:
                if type(obj) == EncodedStreamObject: #TO-DO: isn't this always True?
                    f = obj["/Filter"]
                    if isinstance(f, ArrayObject):
                        f = f[0]

                    if f not in ['/ASCIIHexDecode','/ASCII85Decode']:
                        #TO-DO: upgrade to /ASCII85Encode at some point
                        obj.ASCIIHexEncode()
                        
                        #Cut it up to fit the 80 columns PEP requirement
                        temp = b''
                        while len(obj._data) > self.col_width:
                            temp += obj._data[:self.col_width] + b'\n'
                            obj._data = obj._data[self.col_width:]
                        temp += obj._data
                        obj._data = temp
            
                obj.write_to_stream(self._stream, encryption_key)
                self._stream.write(b"\nendobj\n")

        # xref table
        xref_location = self._stream.tell()-1
        self._stream.write(b"xref\n")
        self._stream.write(("0 %s\n" % (len(self._objects) + 1)).encode())
        self._stream.write(("%010d %05d f \n" % (0, 65535)).encode())
        for i in range(len(self._objects)):
            self._stream.write(("%010d %05d n \n" % (offsets[i]-1, 0)).encode())

        # trailer
        self._stream.write(b"trailer\n")
        trailer = DictionaryObject()
        trailer.update({
                NameObject("/Size"): NumberObject(len(self._objects) + 1),
                NameObject("/Root"): self._root,
                NameObject("/Info"): self._info
                })
        if hasattr(self, "_ID"):
            trailer[NameObject("/ID")] = self._ID
        if hasattr(self, "_encrypt"):
            trailer[NameObject("/Encrypt")] = self._encrypt
        trailer.write_to_stream(self._stream, None)

        eof  = '\nstartxref\n{:d}\n%%EOF'.format(xref_location)
        eof += '\n{:000010d} LF\nPyPDF-' + self.pypdf_version
        eof += '\n"""\n'
        eof = eof.format(self._stream.tell()+len(eof)).encode()
        self._stream.write(eof)
            
        ## Write bytes object to fstream:
        
        self._stream.seek(0)        
        for line in self._stream:
            while len(line) > self.col_width + 1:
                i = line[:self.col_width].rfind(b' ')
                fstream.write(line[:i]+b'\n')
                line = line[i+1:]
            fstream.write(line)



