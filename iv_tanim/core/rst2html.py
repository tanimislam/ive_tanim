#
## docutils stuff, which I am putting in one spot now because I don't understand what's going on
# from docutils.examples import html_parts
import os, sys, logging, copy
from bs4 import BeautifulSoup
from docutils import core, nodes
from docutils.writers.html4css1 import Writer, HTMLTranslator

class MyHTMLTranslator( HTMLTranslator ):
    """
    I am copying this code *without* any real understanding from `this GitHub gist`_. This class seems to extend :py:class:`HTMLTranslator <docutils.writers.html4css1.HTMLTranslator>`, but I don't know what that means.

    The usage in that gist is as follows, because the gist is an enhancement of ``rst2html.py`` called ``myrst2html.py``.

    .. code-block:: python

       htmlwriter = Writer( )
       htmlwriter.translator_class = MyHTMLTranslator
       publish_cmdline(writer=htmlwriter)

    I imagine I will have to modify the methods :py:meth:`check_valid_RST <iv_tanim.core.rst2html.check_valid_RST>` and :py:meth:`convert_string_RST <iv_tanim.core.rst2html.convert_string_RST>` to represent more *correct* functionality. There, I am following what I inferred from :py:meth:`publish_parts <docutils.core.publish_parts>` and the included code block in this object's description.

    .. _`this GitHub gist`: https://gist.github.com/Matherunner/c0397ae11cc72f2f35ae
    """
    mathjax_script = '<script type="text/javascript" src="{}"></script>\n'
    #mathjax_url = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'
    mathjax_url = 'https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'

    def visit_math(self, node, math_env=''):
        from docutils.utils.math import unichar2tex
        if self.math_output != 'mathjax':
            super().visit_math(node, math_env)
            return

        if self.math_output == 'mathjax' and not self.math_header:
            if self.math_output_options:
                self.mathjax_url = self.math_output_options[0]
            self.math_header = [self.mathjax_script.format(self.mathjax_url)]

        math_code = node.astext().translate(unichar2tex.uni2tex_table)
        math_code = self.encode(math_code)
        # Don't wrap the mathematics with div or span
        if math_env:
            self.body.append('\[{}\]\n'.format(math_code))
        else:
            self.body.append('\({}\)'.format(math_code))
        raise nodes.SkipNode

def check_valid_RST( myString, use_mathjax = False ):
    """
    Checks to see whether the input string is valid reStructuredText_.

    :param str myString: the candidate reStructuredText_ input.
    :param bool use_mathjax: if ``True``, then use MathJax_ for math formulae. Default is ``False``.
    :returns: ``True`` if valid, otherwise ``False``.
    :rtype: bool

    .. seealso:: :py:meth:`convert_string_RST <iv_tanim.core.rst2html.convert_string_RST>`.

    .. _MathJax: https://www.mathjax.org
    """
    overrides = {
        'input_encoding': 'unicode',
        'doctitle_xform': True,
        'initial_header_level': 1 }
    if use_mathjax:
        overrides[ 'math_output' ] = 'mathjax'
    htmlwriter = Writer( )
    htmlwriter.translator_class = MyHTMLTranslator
    parts = core.publish_parts(
        source = myString, source_path = None,
        destination_path = None,
        writer_name = 'html', writer = htmlwriter,
        settings_overrides = overrides )
    body = parts[ 'body' ]
    html = BeautifulSoup( body, 'lxml' )
    error_messages = html.find_all('p', { 'class' : 'system-message-title' } )
    return len( error_messages) == 0

def convert_string_RST( myString, use_mathjax = False, outputfilename = None ):
    """
    Converts a valid reStructuredText_ input string into rich HTML.

    :param str myString: the candidate reStructuredText_ input.
    :param bool use_mathjax: if ``True``, then use MathJax_ for math formulae. Default is ``False``.
    :param str outputfilename: if not ``None``, then sets the HTML document *title* to this value.
    :returns: If the input string is valid reStructuredText_, returns the rich HTML as a :py:class:`string <str>`. Otherwise emits a :py:meth:`logging error message <logging.error>` and returns ``None``.
    :rtype: str

    .. seealso:: :py:meth:`check_valid_RST <iv_tanim.core.rst2html.check_valid_RST>`.
    """
    if not check_valid_RST( myString ):
        logging.error( "Error, could not convert %s into RST." % myString )
        return None
    overrides = {
        'input_encoding': 'unicode',
        'doctitle_xform': True,
        'initial_header_level': 1 }
    if use_mathjax:
        overrides[ 'math_output' ] = 'mathjax'
    htmlwriter = Writer( )
    htmlwriter.translator_class = MyHTMLTranslator
    parts = core.publish_parts(
        source = myString, source_path = None,
        destination_path = None,
        writer_name = 'html', writer = htmlwriter,
        settings_overrides = overrides )
    html_body = parts[ 'whole' ]
    html = BeautifulSoup( html_body, 'lxml' )
    #
    def _fix_title_elem( html ):
        if outputfilename is None: return html
        #
        head_elem = html.find_all( 'head' )
        if len( head_elem ) == 0: return html
        head_elem = head_elem[ 0 ]
        #
        title_elem = head_elem.find_all('title' )
        if len( title_elem ) == 0: return html
        #
        title_elem = title_elem[ 0 ]
        title_elem.string = outputfilename
        return html
    #
    html = _fix_title_elem( html )
    return html.prettify( )
