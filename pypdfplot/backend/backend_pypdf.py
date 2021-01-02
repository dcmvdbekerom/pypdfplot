from matplotlib.backend_bases import _Backend, FigureManagerBase
from matplotlib.backends.backend_pdf import (
    FigureCanvasPdf, PdfPages, PdfFile, RendererPdf)
from matplotlib.backends.backend_mixed import MixedModeRenderer
import matplotlib.pyplot as plt
from pypdfplot.functions import write_pypdf

def print_pdf(self, filename, *,
              dpi=72,  # dpi to use for images
              bbox_inches_restore=None, metadata=None,
              **kwargs):

    self.figure.set_dpi(72) # there are 72 pdf points to an inch
    width, height = self.figure.get_size_inches()
    file = PdfFile(filename, metadata=metadata)

    try:
        file.newPage(width, height)
        renderer = MixedModeRenderer(
            self.figure, width, height, dpi,
            RendererPdf(file, dpi, height, width),
            bbox_inches_restore=bbox_inches_restore)
        self.figure.draw(renderer)
        renderer.finalize()
        file.finalize()
        
    finally:
        file.close()

       
def print_pypdf(self, filename, *,
                  dpi=72,  # dpi to use for images
                  bbox_inches_restore=None, metadata=None,
                  **kwargs):

    def write_plot_func(fh,**kwargs):
        print_pdf(self, fh, dpi=dpi,
                  bbox_inches_restore=bbox_inches_restore,
                  metadata=metadata,
                  **kwargs)

    write_pypdf(write_plot_func,
                output_fname = filename,
                **kwargs)

FigureCanvasPdf.print_pdf = print_pypdf

FigureManagerPdf = FigureManagerBase

@_Backend.export
class _BackendPdf(_Backend):
    FigureCanvas = FigureCanvasPdf
