from matplotlib.backends.backend_pdf import *
import sys
from matplotlib import  __version__, _png
from binascii import hexlify

def ASCIIHexEncode(data,col_width = 79):

    #ASCII encoding:
    hexdata = hexlify(data)

    #Cut up in lines of 79 characters:
    temp = b''
    while len(hexdata) > col_width:
        temp += hexdata[:col_width] + b'\n'
        hexdata = hexdata[col_width:]
    temp += hexdata
    return temp

def __init__(self, id, len, file, extra=None, png=None):
    """
    Parameters
    ----------

    id : int
        Object id of the stream.
    len : Reference or None
        An unused Reference object for the length of the stream;
        None means to use a memory buffer so the length can be inlined.
    file : PdfFile
        The underlying object to write the stream to.
    extra : dict from Name to anything, or None
        Extra key-value pairs to include in the stream header.
    png : dict or None
        If the data is already png encoded, the decode parameters.
    """
    self.id = id            # object id
    self.len = len          # id of length object
    self.pdfFile = file
    self.file = file.fh      # file to which the stream is written
    self.compressobj = None  # compression object
    if extra is None:
        self.extra = dict()
    else:
        self.extra = extra.copy()
    if png is not None:
        self.extra.update({'Filter':[Name('ASCIIHexDecode'),Name('FlateDecode')],
                           'DecodeParms': [None, png]}) #PYPDF

    self.pdfFile.recordXref(self.id)
    if rcParams['pdf.compression'] and not png:
        self.compressobj = zlib.compressobj(rcParams['pdf.compression'])
    if self.len is None:
        self.file = BytesIO()
    else:
        self._writeHeader()
        self.pos = self.file.tell()

def _writeHeader(self):
    write = self.file.write
    write(b"%d 0 obj\n" % self.id)
    dict = self.extra
    dict['Length'] = self.len
    if rcParams['pdf.compression']:
        dict['Filter'] = [Name('ASCIIHexDecode'),Name('FlateDecode')] #PYPDF

    write(pdfRepr(dict))
    write(b"\nstream\n")

def write(self, data):
    """Write some data on the stream."""
    
    if self.compressobj is None:
        self.file.write(data)
    else:
        compressed = self.compressobj.compress(data)

        #PYPDF:
        compressed = ASCIIHexEncode(compressed) 
        if len(compressed):
            compressed += b'\n'
        #/PYPDF

        self.file.write(compressed)

def _flush(self):
    """Flush the compression object."""

    if self.compressobj is not None:
        compressed = self.compressobj.flush()
        compressed = ASCIIHexEncode(compressed) + b'>' #PYPDF
        self.file.write(compressed)
        self.compressobj = None

Stream.__init__ = __init__
Stream._writeHeader = _writeHeader
Stream.write = write
Stream._flush = _flush


def __init__(self, filename, metadata=None, file_list = []):
        """
        Parameters
        ----------

        filename : str or path-like or file-like
            Output target; if a string, a file will be opened for writing.
        metadata : dict from strings to strings and dates
            Information dictionary object (see PDF reference section 10.2.1
            'Document Information Dictionary'), e.g.:
            `{'Creator': 'My software', 'Author': 'Me',
            'Title': 'Awesome fig'}`.

            The standard keys are `'Title'`, `'Author'`, `'Subject'`,
            `'Keywords'`, `'Creator'`, `'Producer'`, `'CreationDate'`,
            `'ModDate'`, and `'Trapped'`. Values have been predefined
            for `'Creator'`, `'Producer'` and `'CreationDate'`. They
            can be removed by setting them to `None`.
        """
        self._object_seq = itertools.count(1)  # consumed by reserveObject
        self.xrefTable = [[0, 65535, 'the zero object']]
        self.passed_in_file_object = False
        self.original_file_like = None
        self.tell_base = 1 #PYPDF
        fh, opened = cbook.to_filehandle(filename, "wb", return_opened=True)
        if not opened:
            try:
                self.tell_base = filename.tell()
            except IOError:
                fh = BytesIO()
                self.original_file_like = filename
            else:
                fh = filename
                self.passed_in_file_object = True

        self.fh = fh
        self.currentstream = None  # stream object to write to, if any

        
        self.rootObject = self.reserveObject('root')
        self.pagesObject = self.reserveObject('pages')
        self.pageList = []
        self.fontObject = self.reserveObject('fonts')
        self._extGStateObject = self.reserveObject('extended graphics states')
        self.hatchObject = self.reserveObject('tiling patterns')
        self.gouraudObject = self.reserveObject('Gouraud triangles')
        self.XObjectObject = self.reserveObject('external objects')
        self.resourceObject = self.reserveObject('resources')

        #PYPDF
        pyname = os.path.basename(sys.argv[0])
        self.pySpecObject = self.reserveObject('pyfile spec') #PYPDF
        self.pyStreamObject = self.reserveObject('pyfile stream') #PYPDF
        
        self.fileList = [pyname,self.pySpecObject]
        self.fileStreamList = [self.pyStreamObject]
        self.file_list = []
        for fname,i in zip(file_list,range(len(file_list))):
            self.fileList.append(fname)
            self.fileList.append(self.reserveObject('file spec {:d}'.format(i)))
            self.fileStreamList.append(self.reserveObject('file stream {:d}'.format(i)))

        fh.write(b"#%PDF-1.4 ")
        self.recordXref(self.pyStreamObject.id)

        with open(pyname,'r') as fr:
            pyfile = fr.read()
        pyfile += '\n"""'
       
        hdr = "{:d} 0 obj << /Length {:10d} >> stream\n" #/Type /EmbeddedFile 
        fh.write(hdr.format(self.pyStreamObject.id,len(pyfile)).encode())
        fh.write(pyfile.encode())
        fh.write(b'\nendstream\nendobj\n')
        
        
        root = {'Type': Name('Catalog'),
                'Pages': self.pagesObject,
                'PageMode': Name('UseAttachments'),
                'Names':{'EmbeddedFiles':{'Names':self.fileList}},
                }

        self.writeObject(self.rootObject, root)

        for fname, specObject, streamObject, i in zip(self.fileList[0::2],
                                                      self.fileList[1::2],
                                                      self.fileStreamList,
                                                      range(len(file_list)+1)):
            
            file_spec = {'Type':Name('Filespec'),
                         'F':fname,
                         'EF':{'F': streamObject},
                         }
            self.writeObject(specObject,file_spec)
        
            if fname != pyname:
                with open(fname,'rb') as fr:
                    stream = fr.read()
                tmod = os.path.getmtime(fname)
                mod_date = datetime.utcfromtimestamp(tmod).strftime("D:%Y%m%d%H%M%SZ00'00")
                stream_dict = {'Type':Name('EmbeddedFile'),
                               'Params':{'Size':len(stream),
                                         'ModDate':mod_date}
                               }
                self.beginStream(streamObject.id, None, stream_dict)
                self.currentstream.write(stream)
                self.endStream()

        #/PYPDF
        
        # get source date from SOURCE_DATE_EPOCH, if set
        # See https://reproducible-builds.org/specs/source-date-epoch/
        source_date_epoch = os.getenv("SOURCE_DATE_EPOCH")
        if source_date_epoch:
            source_date = datetime.utcfromtimestamp(int(source_date_epoch))
            source_date = source_date.replace(tzinfo=UTC)
        else:
            source_date = datetime.today()

        self.infoDict = {
            'Creator': 'matplotlib %s, http://matplotlib.org' % __version__,
            'Producer': 'matplotlib pypdf backend %s' % __version__, #PYPDF
            'CreationDate': source_date
        }
        if metadata is not None:
            self.infoDict.update(metadata)
        self.infoDict = {k: v for (k, v) in self.infoDict.items()
                         if v is not None}

        self.fontNames = {}     # maps filenames to internal font names
        self._internal_font_seq = (Name(f'F{i}') for i in itertools.count(1))
        self.dviFontInfo = {}   # maps dvi font names to embedding information
        # differently encoded Type-1 fonts may share the same descriptor
        self.type1Descriptors = {}
        self.used_characters = {}

        self.alphaStates = {}   # maps alpha values to graphics state objects
        self._alpha_state_seq = (Name(f'A{i}') for i in itertools.count(1))
        self._soft_mask_states = {}
        self._soft_mask_seq = (Name(f'SM{i}') for i in itertools.count(1))
        self._soft_mask_groups = []
        # reproducible writeHatches needs an ordered dict:
        self.hatchPatterns = collections.OrderedDict()
        self._hatch_pattern_seq = (Name(f'H{i}') for i in itertools.count(1))
        self.gouraudTriangles = []

        self._images = collections.OrderedDict()   # reproducible writeImages
        self._image_seq = (Name(f'I{i}') for i in itertools.count(1))

        self.markers = collections.OrderedDict()   # reproducible writeMarkers
        self.multi_byte_charprocs = {}

        self.paths = []

        self.pageAnnotations = []  # A list of annotations for the current page

        # The PDF spec recommends to include every procset
        procsets = [Name(x)
                    for x in "PDF Text ImageB ImageC ImageI".split()]

        # Write resource dictionary.
        # Possibly TODO: more general ExtGState (graphics state dictionaries)
        #                ColorSpace Pattern Shading Properties
        resources = {'Font': self.fontObject,
                     'XObject': self.XObjectObject,
                     'ExtGState': self._extGStateObject,
                     'Pattern': self.hatchObject,
                     'Shading': self.gouraudObject,
                     'ProcSet': procsets}
        self.writeObject(self.resourceObject, resources)
        
def _writePng(self, data):
    """
    Write the image *data* into the pdf file using png
    predictors with Flate compression.
    """
    buffer = BytesIO()
    _png.write_png(data, buffer)
    buffer.seek(8)
    while True:
        length, type = struct.unpack(b'!L4s', buffer.read(8))
        if type == b'IDAT':
            data = buffer.read(length)
            if len(data) != length:
                raise RuntimeError("truncated data")
            self.currentstream.write(ASCIIHexEncode(data)+b'>') #PYPDF
        elif type == b'IEND':
            break
        else:
            buffer.seek(length, 1)
        buffer.seek(4, 1)   # skip CRC

def writeTrailer(self):
    """Write out the PDF trailer."""

    self.write(b"trailer\n")
    self.write(pdfRepr(
        {'Size': len(self.xrefTable),
         'Root': self.rootObject,
         'Info': self.infoObject}))
    # Could add 'ID'
    self.write(b"\nstartxref\n%d\n%%%%EOF\n" % self.startxref)
    self.write('{:010d}\n"""\n'.format(self.fh.tell() + 15).encode()) #PYPDF

PdfFile.__init__ = __init__
PdfFile._writePng = _writePng
PdfFile.writeTrailer = writeTrailer


def print_pdf(self, filename, *,
                  dpi=72,  # dpi to use for images
                  bbox_inches_restore=None, metadata=None,
                  file_list=[], #PYPDF
                  **kwargs):
        
        self.figure.set_dpi(72)            # there are 72 pdf points to an inch
        width, height = self.figure.get_size_inches()
        if isinstance(filename, PdfPages):
            file = filename._file
        else:
            file = PdfFile(filename, metadata=metadata, file_list=file_list)
        try:
            file.newPage(width, height)
            renderer = MixedModeRenderer(
                self.figure, width, height, dpi,
                RendererPdf(file, dpi, height, width),
                bbox_inches_restore=bbox_inches_restore)
            self.figure.draw(renderer)
            renderer.finalize()
            if not isinstance(filename, PdfPages):
                file.finalize()
        finally:
            if isinstance(filename, PdfPages):  # finish off this page
                file.endStream()
            else:            # we opened the file above; now finish it off
                file.close()

            #Do file manupulations here

FigureCanvasPdf.print_pdf = print_pdf
