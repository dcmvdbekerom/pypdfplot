from matplotlib.backend_bases import _Backend, FigureManagerBase
from matplotlib.backends.backend_pdf import FigureCanvasPdf
from pypdfplot.functions import write_pypdf
from io import BytesIO
from copy import deepcopy

mpl_print_pdf = deepcopy(FigureCanvasPdf.print_pdf)
       
def print_pypdf(self, filename, *vargs,
                bbox_inches_restore=None, metadata=None,
                **kwargs):

    plot_bytes = BytesIO()
    mpl_print_pdf(self, plot_bytes, *vargs,
              bbox_inches_restore=bbox_inches_restore,
              metadata=metadata)

    write_pypdf(plot_bytes,
                output_fname = filename,
                **kwargs)

FigureCanvasPdf.print_pdf = print_pypdf

FigureManagerPdf = FigureManagerBase

@_Backend.export
class _BackendPdf(_Backend):
    FigureCanvas = FigureCanvasPdf
