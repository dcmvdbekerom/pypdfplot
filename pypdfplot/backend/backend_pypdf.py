from matplotlib.backends.backend_pdf import *
from pypdfplot.functions import write_pypdf

print_pdf = FigureCanvasPdf.print_pdf
        
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
