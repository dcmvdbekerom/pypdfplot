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

from PyPDF4 import PdfFileWriter,PdfFileReader
from PyPDF4.generic import *
from PyPDF4.utils import isString,formatWarning,PdfReadError,readUntilWhitespace
from binascii import hexlify,unhexlify
from PyPDF4.filters import ASCIIHexDecode
import os

COL_WIDTH = 79

def available_filename(fname):
    base,ext = os.path.splitext(fname)
    i = 1
    fname = base + ext
    while os.path.isfile(fname):
        fname = base + '({:1d})'.format(i) + ext
        i += 1

    return fname

def ASCIIHexEncode(self):
    
    hexdata = hexlify(self._data) + b_('>')

    temp = b_('')
    while len(hexdata) > COL_WIDTH:
        temp += hexdata[:COL_WIDTH] + b_('\n')
        hexdata = hexdata[COL_WIDTH:]
    temp += hexdata
    self._data = temp
 
    f = self["/Filter"]
    if isinstance(f, ArrayObject):
        f.insert(0, NameObject("/ASCIIHexDecode"))
    else:
        newf = ArrayObject()
        newf.append(NameObject("/ASCIIHexDecode"))
        newf.append(f)
        f = newf

    self[NameObject("/Filter")] = f
   
StreamObject.ASCIIHexEncode = ASCIIHexEncode

def decode(data, decodeParms=None):
    bdata = data[:-1].replace(b_('\n'),b_(''))
    return unhexlify(bdata)

ASCIIHexDecode.decode = staticmethod(decode)

class PyPdfFileReader(PdfFileReader):
    """
    Initializes a PdfFileReader object.  This operation can take some time, as
    the PDF stream's cross-reference tables are read into memory.

    :param stream: A File object or an object that supports the standard read
        and seek methods similar to a File object. Could also be a
        string representing a path to a PDF file.
    :param bool strict: Determines whether user should be warned of all
        problems and also causes some correctable problems to be fatal.
        Defaults to ``True``.
    :param warndest: Destination for logging warnings (defaults to
        ``sys.stderr``).
    :param bool overwriteWarnings: Determines whether to override Python's
        ``warnings.py`` module with a custom implementation (defaults to
        ``True``).
    """
    def __init__(self, stream, strict=True, warndest = None, overwriteWarnings = True):
        if overwriteWarnings:
            # have to dynamically override the default showwarning since there are no
            # public methods that specify the 'file' parameter
            def _showwarning(message, category, filename, lineno, file=warndest, line=None):
                if file is None:
                    file = sys.stderr
                try:
                    file.write(formatWarning(message, category, filename, lineno, line))
                except IOError:
                    pass
            warnings.showwarning = _showwarning
        self.strict = strict
        self.flattenedPages = None
        self.resolvedObjects = {}
        self.xrefIndex = 0
        self._pageId2Num = None # map page IndirectRef number to Page Number
        if hasattr(stream, 'mode') and 'b' not in stream.mode:
            warnings.warn("PdfFileReader stream/file object is not in binary mode. It may not be read correctly.", utils.PdfReadWarning)
        if isString(stream):
            fileobj = open(stream, 'rb')
            stream = BytesIO(b_(fileobj.read()))
            fileobj.close()
        self.read(stream)
        self.stream = stream
        self.pyObj = self.getGeneratingScriptObject()
        self._override_encryption = False

    def read(self, stream):
        debug = False
        if debug: print(">>read", stream)
        
        # start at the end:
        stream.seek(-1, 2)
        file_end = stream.tell()
        if not file_end:
            raise utils.PdfReadError('Cannot read an empty file')

        # locate %PDF: 
        stream.seek(0,0)
        first1K = min(1024,file_end)
        line = b_('')
        pdf_start = -1
        while pdf_start < 0:
            if stream.tell() > first1K:
                raise utils.PdfReadError("%PDF marker not found")
            line = stream.readline()
            pdf_start = line.find(b_("%PDF"))
            if pdf_start < 0:
                raise utils.PdfReadError("%PDF marker not found")
            try:
                self.pyId, self.pyGen = map(int,line.split()[1:3])
            except:
                warnings.warn("No object header found, file does not comply with PyPDF standard")
                pass
            if debug: print("  line:",line,"pdf_start:",pdf_start)

        # locate %%EOF
        stream.seek(-1, 2)
        last1K = stream.tell() - 1024 + 1 # offset of last 1024 bytes of stream
        line = b_('')
        while line[:5] != b_("%%EOF"):
            if stream.tell() < last1K:
                raise utils.PdfReadError("%%EOF marker not found")
            line = self.readNextEndLine(stream)
            if debug: print("  line:",line)

        # Determine if file has changed and by how much
        try:
            eof_addr = stream.tell()
            stream.readline()
            stream.readline()
            old_size,self.revision = map(int,stream.readline().split())
            stream.seek(eof_addr)
            self.offset_diff = file_end + 1 - old_size
            
        except:
            self.offset_diff = 0
            warnings.warn("Could not find original file size in trailer, file does not comply with PyPDF standard")
            
        # find startxref entry - the location of the xref table
        line = self.readNextEndLine(stream)
        try:
            startxref = pdf_start + int(line)
        except ValueError:
            # 'startxref' may be on the same line as the location
            if not line.startswith(b_("startxref")):
                raise utils.PdfReadError("startxref not found")
            startxref = pdf_start + int(line[9:].strip())
            warnings.warn("startxref on same line as offset")
        else:
            line = self.readNextEndLine(stream)
            if line[:9] != b_("startxref"):
                raise utils.PdfReadError("startxref not found")

        # Fix position if file has been edited after publication
        startxref += self.offset_diff
                
        # read all cross reference tables and their trailers
        self.xref = {}
        self.xref_objStm = {}
        self.trailer = DictionaryObject()
        while True:
            # load the xref table
            stream.seek(startxref, 0)
            x = stream.read(1)
            if x == b_("x"):
                # standard cross-reference table
                ref = stream.read(4)
                if ref[:3] != b_("ref"):
                    raise utils.PdfReadError("xref table read error")
                readNonWhitespace(stream)
                stream.seek(-1, 1)
                firsttime = True; # check if the first time looking at the xref table
                while True:
                    num = readObject(stream, self)
                    if firsttime and num != 0:
                         self.xrefIndex = num
                         if self.strict:
                            warnings.warn("Xref table not zero-indexed. ID numbers for objects will be corrected.", utils.PdfReadWarning)
                            #if table not zero indexed, could be due to error from when PDF was created
                            #which will lead to mismatched indices later on, only warned and corrected if self.strict=True
                    firsttime = False
                    readNonWhitespace(stream)
                    stream.seek(-1, 1)
                    size = readObject(stream, self)
                    readNonWhitespace(stream)
                    stream.seek(-1, 1)
                    cnt = 0
                    while cnt < size:
                        line = stream.read(20)

                        # It's very clear in section 3.4.3 of the PDF spec
                        # that all cross-reference table lines are a fixed
                        # 20 bytes (as of PDF 1.7). However, some files have
                        # 21-byte entries (or more) due to the use of \r\n
                        # (CRLF) EOL's. Detect that case, and adjust the line
                        # until it does not begin with a \r (CR) or \n (LF).
                        while line[0] in b_("\x0D\x0A"):
                            stream.seek(-20 + 1, 1)
                            line = stream.read(20)

                        # On the other hand, some malformed PDF files
                        # use a single character EOL without a preceeding
                        # space.  Detect that case, and seek the stream
                        # back one character.  (0-9 means we've bled into
                        # the next xref entry, t means we've bled into the
                        # text "trailer"):
                        if line[-1] in b_("0123456789t"):
                            stream.seek(-1, 1)

                        offset, generation = line[:16].split(b_(" "))
                        offset, generation = int(offset), int(generation)

                        # Fix position if file has been edited after publication

                        if num:
                            offset += pdf_start                      
                            if (num,generation) != (self.pyId,self.pyGen):
                                offset += self.offset_diff
                                                
                        if generation not in self.xref:
                            self.xref[generation] = {}
                        if num in self.xref[generation]:
                            # It really seems like we should allow the last
                            # xref table in the file to override previous
                            # ones. Since we read the file backwards, assume
                            # any existing key is already set correctly.
                            pass
                        else:
                            self.xref[generation][num] = offset
                        cnt += 1
                        num += 1
                    readNonWhitespace(stream)
                    stream.seek(-1, 1)
                    trailertag = stream.read(7)
                    if trailertag != b_("trailer"):
                        # more xrefs!
                        stream.seek(-7, 1)
                    else:
                        break
                readNonWhitespace(stream)
                stream.seek(-1, 1)
                newTrailer = readObject(stream, self)
                for key, value in list(newTrailer.items()):
                    if key not in self.trailer:
                        self.trailer[key] = value
                if "/Prev" in newTrailer:
                    startxref = newTrailer["/Prev"]
                else:
                    break
            elif x.isdigit():
                # PDF 1.5+ Cross-Reference Stream
                stream.seek(-1, 1)
                idnum, generation = self.readObjectHeader(stream)
                xrefstream = readObject(stream, self)
                assert xrefstream["/Type"] == "/XRef"
                self.cacheIndirectObject(generation, idnum, xrefstream)
                streamData = BytesIO(b_(xrefstream.getData()))
                # Index pairs specify the subsections in the dictionary. If
                # none create one subsection that spans everything.
                idx_pairs = xrefstream.get("/Index", [0, xrefstream.get("/Size")])
                if debug: print(("read idx_pairs=%s"%list(self._pairs(idx_pairs))))
                entrySizes = xrefstream.get("/W")
                assert len(entrySizes) >= 3
                if self.strict and len(entrySizes) > 3:
                    raise utils.PdfReadError("Too many entry sizes: %s" %entrySizes)

                def getEntry(i):
                    # Reads the correct number of bytes for each entry. See the
                    # discussion of the W parameter in PDF spec table 17.
                    if entrySizes[i] > 0:
                        d = streamData.read(entrySizes[i])
                        return convertToInt(d, entrySizes[i])

                    # PDF Spec Table 17: A value of zero for an element in the
                    # W array indicates...the default value shall be used
                    if i == 0:  return 1 # First value defaults to 1
                    else:       return 0

                def used_before(num, generation):
                    # We move backwards through the xrefs, don't replace any.
                    return num in self.xref.get(generation, []) or \
                            num in self.xref_objStm

                # Iterate through each subsection
                last_end = 0
                for start, size in self._pairs(idx_pairs):
                    # The subsections must increase
                    assert start >= last_end
                    last_end = start + size
                    for num in range(start, start+size):
                        # The first entry is the type
                        xref_type = getEntry(0)
                        # The rest of the elements depend on the xref_type
                        if xref_type == 0:
                            # linked list of free objects
                            next_free_object = getEntry(1)
                            next_generation = getEntry(2)
                        elif xref_type == 1:
                            # objects that are in use but are not compressed
                            byte_offset = getEntry(1)
                            generation = getEntry(2)
                            if generation not in self.xref:
                                self.xref[generation] = {}
                            if not used_before(num, generation):
                                self.xref[generation][num] = byte_offset
                                if debug: print(("XREF Uncompressed: %s %s"%(
                                                num, generation)))
                        elif xref_type == 2:
                            # compressed objects
                            objstr_num = getEntry(1)
                            obstr_idx = getEntry(2)
                            generation = 0 # PDF spec table 18, generation is 0
                            if not used_before(num, generation):
                                if debug: print(("XREF Compressed: %s %s %s"%(
                                        num, objstr_num, obstr_idx)))
                                self.xref_objStm[num] = (objstr_num, obstr_idx)
                        elif self.strict:
                            raise utils.PdfReadError("Unknown xref type: %s"%
                                                        xref_type)

                trailerKeys = "/Root", "/Encrypt", "/Info", "/ID"
                for key in trailerKeys:
                    if key in xrefstream and key not in self.trailer:
                        self.trailer[NameObject(key)] = xrefstream.raw_get(key)
                if "/Prev" in xrefstream:
                    startxref = xrefstream["/Prev"]
                else:
                    break
            else:
                # bad xref character at startxref.  Let's see if we can find
                # the xref table nearby, as we've observed this error with an
                # off-by-one before.
                stream.seek(-11, 1)
                tmp = stream.read(20)
                xref_loc = tmp.find(b_("xref"))
                if xref_loc != -1:
                    startxref -= (10 - xref_loc)
                    continue
                # No explicit xref table, try finding a cross-reference stream.
                stream.seek(startxref, 0)
                found = False
                for look in range(5):
                    if stream.read(1).isdigit():
                        # This is not a standard PDF, consider adding a warning
                        startxref += look
                        found = True
                        break
                if found:
                    continue
                # no xref table found at specified location
                raise utils.PdfReadError("Could not find xref table at specified location")
        #if not zero-indexed, verify that the table is correct; change it if necessary
        if self.xrefIndex and not self.strict:
            loc = stream.tell()
            for gen in self.xref:
                if gen == 65535: continue
                for id in self.xref[gen]:
                    stream.seek(self.xref[gen][id], 0)
                    try:
                        pid, pgen = self.readObjectHeader(stream)
                    except ValueError:
                        break
                    if pid == id - self.xrefIndex:
                        self._zeroXref(gen)
                        break
                    #if not, then either it's just plain wrong, or the non-zero-index is actually correct
            stream.seek(loc, 0) #return to where it was

    def getGeneratingScriptObject(self):
        """
        Since the generating script object may have been changed since last time,
        the /Length in its dictionary may not match the actual stream length.
        That's why we treat it separately so that we can fix the length
        before running into problems.
        """

        indirectReference = IndirectObject(self.pyId,self.pyGen,self)
       
        start = self.xref[indirectReference.generation][indirectReference.idnum]
        self.stream.seek(start,0)

        idnum, generation = self.readObjectHeader(self.stream)
        if idnum != indirectReference.idnum and self.xrefIndex:
            # Xref table probably had bad indexes due to not being zero-indexed
            if self.strict:
                raise utils.PdfReadError("Expected object ID (%d %d) does not match actual (%d %d); xref table not zero-indexed." \
                                 % (indirectReference.idnum, indirectReference.generation, idnum, generation))
            else: pass # xref table is corrected in non-strict mode
        elif idnum != indirectReference.idnum:
            # some other problem
            raise utils.PdfReadError("Expected object ID (%d %d) does not match actual (%d %d)." \
                                     % (indirectReference.idnum, indirectReference.generation, idnum, generation))
        assert generation == indirectReference.generation
                
        ## Following is copied from DictionaryObject.readFromStream(), just to add the patch for the changed length
        pdf = self
        stream = self.stream
        
        debug = False
        tmp = stream.read(2)
        if tmp != b_("<<"):
            raise utils.PdfReadError("Dictionary read error at byte %s: stream must begin with '<<'" % utils.hexStr(stream.tell()))
        data = {}
        while True:
            tok = readNonWhitespace(stream)
            if tok == b_('\x00'):
                continue
            elif tok == b_('%'):
                stream.seek(-1, 1)
                skipOverComment(stream)
                continue
            if not tok:
                # stream has truncated prematurely
                raise PdfStreamError("Stream has ended unexpectedly")

            if debug: print(("Tok:", tok))
            if tok == b_(">"):
                stream.read(1)
                break
            stream.seek(-1, 1)
            key = readObject(stream, pdf)
            tok = readNonWhitespace(stream)
            stream.seek(-1, 1)
            value = readObject(stream, pdf)
            if not data.get(key):
                data[key] = value
            elif pdf.strict:
                # multiple definitions of key not permitted
                raise utils.PdfReadError("Multiple definitions in dictionary at byte %s for key %s" \
                                           % (utils.hexStr(stream.tell()), key))
            else:
                warnings.warn("Multiple definitions in dictionary at byte %s for key %s" \
                                           % (utils.hexStr(stream.tell()), key), utils.PdfReadWarning)

        pos = stream.tell()
        s = readNonWhitespace(stream)
        if s == b_('s') and stream.read(5) == b_('tream'):
            eol = stream.read(1)
            # odd PDF file output has spaces after 'stream' keyword but before EOL.
            # patch provided by Danial Sandler
            while eol == b_(' '):
                eol = stream.read(1)
            assert eol in (b_("\n"), b_("\r"))
            if eol == b_("\r"):
                # read \n after
                if stream.read(1)  != b_('\n'):
                    stream.seek(-1, 1)
            # this is a stream object, not a dictionary
            assert "/Length" in data
            length = data["/Length"]
            # And here is the patch:
            length += self.offset_diff
            if debug: print(data)
            if isinstance(length, IndirectObject):
                t = stream.tell()
                length = pdf.getObject(length)
                stream.seek(t, 0)
            data["__streamdata__"] = stream.read(length)
            if debug: print("here")
            #if debug: print(binascii.hexlify(data["__streamdata__"]))
            e = readNonWhitespace(stream)
            ndstream = stream.read(8)
            if (e + ndstream) != b_("endstream"):
                # (sigh) - the odd PDF file has a length that is too long, so
                # we need to read backwards to find the "endstream" ending.
                # ReportLab (unknown version) generates files with this bug,
                # and Python users into PDF files tend to be our audience.
                # we need to do this to correct the streamdata and chop off
                # an extra character.
                pos = stream.tell()
                stream.seek(-10, 1)
                end = stream.read(9)
                if end == b_("endstream"):
                    # we found it by looking back one character further.
                    data["__streamdata__"] = data["__streamdata__"][:-1]
                else:
                    if debug: print(("E", e, ndstream, debugging.toHex(end)))
                    stream.seek(pos, 0)
                    raise utils.PdfReadError("Unable to find 'endstream' marker after stream at byte %s." % utils.hexStr(stream.tell()))
        else:
            stream.seek(pos, 0)
        if "__streamdata__" in data:
            retval = StreamObject.initializeFromDictionary(data)
        else:
            retval = DictionaryObject()
            retval.update(data)

        self.cacheIndirectObject(indirectReference.generation,
                    indirectReference.idnum, retval)

        return retval





class PyPdfFileWriter(PdfFileWriter):
    def __init__(self, stream, revision = 0, after_page_append=None):

        super(PyPdfFileWriter,self).__init__()

        reader = PdfFileReader(stream)        

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
        debug = False
        if debug:
            print("Number of Objects: %d" % len(self._objects))
            for obj in self._objects:
                print("\tObject is %r" % obj)
                if hasattr(obj, "indirectRef") and obj.indirectRef != None:
                    print("\t\tObject's reference is %r %r, at PDF %r" % (obj.indirectRef.idnum, obj.indirectRef.generation, obj.indirectRef.pdf))

        # Variables used for after cloning the root to
        # improve pre- and post- cloning experience

        mustAddTogether = False
        newInfoRef = self._info
        oldPagesRef = self._pages
        oldPages = self.getObject(self._pages)

        # If there have already been any number of pages added

        if oldPages[NameObject("/Count")] > 0:

            # Keep them

            mustAddTogether = True
        else:

            # Through the page object out

            if oldPages in self._objects:
                newInfoRef = self._pages
                self._objects.remove(oldPages)

        # Clone the reader's root document

        self.cloneReaderDocumentRoot(reader)
        if not self._root:
            self._root = self._addObject(self._root_object)

        # Sweep for all indirect references

        externalReferenceMap = {}
        self.stack = []
        newRootRef = self._sweepIndirectReferences(externalReferenceMap, self._root)

        # Delete the stack to reset

        del self.stack

        #Clean-Up Time!!!

        # Get the new root of the PDF

        realRoot = self.getObject(newRootRef)

        # Get the new pages tree root and its ID Number

        tmpPages = realRoot[NameObject("/Pages")]
        newIdNumForPages = 1 + self._objects.index(tmpPages)

        # Make an IndirectObject just for the new Pages

        self._pages = IndirectObject(newIdNumForPages, 0, self)

        # If there are any pages to add back in

        if mustAddTogether:

            # Set the new page's root's parent to the old
            # page's root's reference

            tmpPages[NameObject("/Parent")] = oldPagesRef

            # Add the reference to the new page's root in
            # the old page's kids array

            newPagesRef = self._pages
            oldPages[NameObject("/Kids")].append(newPagesRef)

            # Set all references to the root of the old/new
            # page's root

            self._pages = oldPagesRef
            realRoot[NameObject("/Pages")] = oldPagesRef

            # Update the count attribute of the page's root

            oldPages[NameObject("/Count")] = NumberObject(oldPages[NameObject("/Count")] + tmpPages[NameObject("/Count")])

        else:

            # Bump up the info's reference b/c the old
            # page's tree was bumped off

            self._info = newInfoRef
            self.revision = revision

    def addAttachment(self,fname,fdata):
        ## This method fixes updating the EmbeddedFile dictionary when multiple files are attached
        try:
            old_list = self._root_object["/Names"]["/EmbeddedFiles"]["/Names"] 
        except(KeyError):
            old_list = ArrayObject([])
        
        super(PyPdfFileWriter,self).addAttachment(fname,fdata)
        
        new_list = self._root_object["/Names"]["/EmbeddedFiles"]["/Names"]
        file_list = ArrayObject(old_list + new_list)
        self._root_object[NameObject("/Names")][NameObject("/EmbeddedFiles")][NameObject("/Names")] = file_list
        self._root_object[NameObject("/PageMode")] = NameObject("/UseAttachments")
          
    def write(self, stream):
        """
        Writes the collection of pages added to this object out as a PDF file.

        :param stream: An object to write the file to.  The object must support
            the write method and the tell method, similar to a file object.
        """
        if hasattr(stream, 'mode') and 'b' not in stream.mode:
            warnings.warn("File <%s> to write to is not in binary mode. It may not be written to correctly." % stream.name)
        debug = False
        import struct

        if not self._root:
            self._root = self._addObject(self._root_object)

        externalReferenceMap = {}

        # PDF objects sometimes have circular references to their /Page objects
        # inside their object tree (for example, annotations).  Those will be
        # indirect references to objects that we've recreated in this PDF.  To
        # address this problem, PageObject's store their original object
        # reference number, and we add it to the external reference map before
        # we sweep for indirect references.  This forces self-page-referencing
        # trees to reference the correct new object location, rather than
        # copying in a new copy of the page object.
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
        self._sweepIndirectReferences(externalReferenceMap, self._root)
        del self.stack

        # Begin writing:
        object_positions = {}
        stream.write(b_('#') + self._header + b_("\n"))
        obji = list(range(len(self._objects)))
        for i in obji[-1:]+obji[:-1]:
            idnum = (i + 1)
            obj = self._objects[i]
            object_positions[i] = stream.tell()
            stream.write(b_(str(idnum) + " 0 obj\n"))
            key = None
##            if hasattr(self, "_encrypt") and idnum != self._encrypt.idnum:
##                pack1 = struct.pack("<i", i + 1)[:3]
##                pack2 = struct.pack("<i", 0)[:2]
##                key = self._encrypt_key + pack1 + pack2
##                assert len(key) == (len(self._encrypt_key) + 5)
##                md5_hash = md5(key).digest()
##                key = md5_hash[:min(16, len(self._encrypt_key) + 5)]

            if i != obji[-1]:
                
                if type(obj) == DecodedStreamObject:
                    obj = obj.flateEncode()
                
                if type(obj) == EncodedStreamObject:
                    f = obj["/Filter"]
                    if isinstance(f, ArrayObject):
                        f = f[0]

                    if f not in ['/ASCIIHexDecode','/ASCII85Decode']:
                        obj.ASCIIHexEncode()
            
            obj.writeToStream(stream, key)

            if i == obji[-1]:
                stream.seek(0)
                temp_buf = stream.read()
                addr = temp_buf.find(b_('stream')) + len('stream')
                temp_buf = temp_buf[:addr].replace(b_('\n'),b_(' ')) + temp_buf[addr:]

                stream.seek(0)
                stream.write(temp_buf)
            
            stream.write(b_("\nendobj\n"))

        # xref table
        xref_location = stream.tell()-1
        stream.write(b_("xref\n"))
        stream.write(b_("0 %s\n" % (len(self._objects) + 1)))
        stream.write(b_("%010d %05d f \n" % (0, 65535)))
        for i in range(len(self._objects)):
            stream.write(b_("%010d %05d n \n" % (object_positions[i]-1, 0)))

        # trailer
        stream.write(b_("trailer\n"))
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
        trailer.writeToStream(stream, None)

        eof  = '\nstartxref\n{:d}\n%%EOF'.format(xref_location)
        eof += '\n{:00010d} {:05d} \n"""\n'
        eof = b_(eof.format(stream.tell()+len(eof),self.revision))
        stream.write(eof)



