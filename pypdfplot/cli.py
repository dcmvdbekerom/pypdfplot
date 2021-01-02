import argparse
from pypdfplot.functions import fix_pypdf

parser = argparse.ArgumentParser()

parser.add_argument('fname',
                    metavar = 'filename',
                    help = 'filename of the severed PyPDF file that needs fixing')

parser.add_argument(
                    '-o',
                    '--output',
                    metavar = 'filename',
                    help = ('specifies the output filename; '+
                            'if omitted the conversion will be done in place'),
                    )


##parser.add_argument('-v',
##                    '--verbose',
##                    action ='store_const',
##                    const = True, 
##                    default = False,
##                    dest ='verbose',
##                    help = 'toggles verbosity')

def main():
    args = parser.parse_args()
    fix_pypdf(args.fname,
              args.output,
              #args.verbose, #Might as well have it always on
              )


if __name__ == '__main__':
    main()
