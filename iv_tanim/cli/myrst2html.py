import os, sys
from iv_tanim.core import rst2html
from argparse import ArgumentParser

# class MyHTMLTranslator(HTMLTranslator):
#     mathjax_script = '<script type="text/javascript" src="{}"></script>\n'
#     mathjax_url = 'https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'

#     def visit_math(self, node, math_env=''):
#         if self.math_output != 'mathjax':
#             super().visit_math(node, math_env)
#             return

#         if self.math_output == 'mathjax' and not self.math_header:
#             if self.math_output_options:
#                 self.mathjax_url = self.math_output_options[0]
#             self.math_header = [self.mathjax_script.format(self.mathjax_url)]

#         math_code = node.astext().translate(unichar2tex.uni2tex_table)
#         math_code = self.encode(math_code)
#         # Don't wrap the mathematics with div or span
#         if math_env:
#             self.body.append('\[{}\]\n'.format(math_code))
#         else:
#             self.body.append('\({}\)'.format(math_code))
#         raise nodes.SkipNode

def _main( ):
    #htmlwriter = Writer()
    # htmlwriter.translator_class = MyHTMLTranslator
    #publish_cmdline(writer=htmlwriter)

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
