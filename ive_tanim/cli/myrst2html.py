import os, sys
from ive_tanim.core import rst2html
from argparse import ArgumentParser

def _main( ):
    parser = ArgumentParser( )
    parser.add_argument('-i', '--input', dest='inputfile', type = str, action = 'store', required = True,
                        help = 'Name of the input RST file. Required argument.' )
    parser.add_argument('-M', '--mathjax', dest='do_mathjax', action = 'store_true', default = False,
                        help = 'If chosen, then use the MathJAX JS CDN to display LaTeX formulae. Default is turned off.' )
    args = parser.parse_args( )
    #
    fname = os.path.abspath( os.path.expanduser( args.inputfile ) )
    outputfilename = os.path.basename( fname ).replace('.rst', '.html' )
    try:
        status = rst2html.check_valid_RST( str( open( fname, 'r' ).read( ) ), use_mathjax = args.do_mathjax )
        if not status:
            print("ERROR, %s IS NOT A VALID RST INPUT." % fname )
            return
        print( '%s\n' % rst2html.convert_string_RST(
            str( open( fname, 'r' ).read( ) ),
            use_mathjax = args.do_mathjax,
            outputfilename = outputfilename ) )
    except Exception as e:
        print( str( e ) )
        print( "ERROR, %s IS NOT A VALID RST INPUT." % fname )
        return
