#
## docutils stuff, which I am putting in one spot now because I don't understand what's going on
# from docutils.examples import html_parts
import os, sys, logging, validators, uuid, smtplib, magic
from bs4 import BeautifulSoup
from docutils import core, nodes
from docutils.writers.html4css1 import Writer, HTMLTranslator
#
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.utils import formataddr, parseaddr
from email import message_from_bytes

##
## read  email message into mimemultipart from file in bytes: msg = message_from_bytes( open( 'msg_file.msg', 'rb' ).read( ) )
## write email message as bytes: with open( 'msg_file.msg', 'wb' ) as openfile: openfile.write( msg.as_bytes( ) )
##

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

    .. seealso:: :py:meth:`convert_string_RST <iv_tanim.core.rst2html.convert_string_RST>`

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

    .. seealso:: :py:meth:`check_valid_RST <iv_tanim.core.rst2html.check_valid_RST>`
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

def create_rfc2047_email( email_fullname_dict ):
    """
    Given a :py:class:`dict` containing email address and (optionally) full name, returns the `RFC 2047`_ fully qualified email address.
    
    :param dict email_fullname_dict: the :py:class:`dict` that *should* contain the email and optionally the fully qualified name. Email address is in the ``email`` key, and optional full name is in the ``full name`` key.
    :returns: an `RFC 2047`_ fully qualified email address under the following conditions:

       #. If there is an email address; and

       #. If there is an email address *AND* a fully qualified name.

       Otherwise returns ``None``.
    :rtype: str

    .. seealso:: :py:meth:`parse_rfc2047_email <iv_tanim.core.rst2html.parse_rfc2047_email>`

    .. _`RFC 2047`: https://tools.ietf.org/html/rfc2047.html
    """
    input_tuple = [ '', '' ]
    if 'email' in email_fullname_dict and len( email_fullname_dict[ 'email' ].strip( ) ) > 0:
        input_tuple[1] = email_fullname_dict[ 'email' ]
    if 'full name' in email_fullname_dict and len( email_fullname_dict[ 'full name' ].strip( ) ) > 0:
        input_tuple[0] = email_fullname_dict[ 'full name' ]
    #
    if input_tuple[0] == '' and input_tuple[1] == '':
        logging.error("ERROR, NO VALID EMAIL AND FULL NAME FORM %s." % email_fullname_dict )
        return None
    if input_tuple[1] == '':
        logging.error("ERROR, NO VALID EMAIL FROM %s" % email_fullname_dict )
        return None
    #
    try:
        return formataddr( tuple( input_tuple ) )
    except Exception as e:
        logging.error( "Problem with trying to format as email this tuple: %s. Exception = %s." % (
            input_tuple, str( e ) ) )
        return None

def parse_rfc2047_email( candidate_rfc2047_email ):
    """
    Uses :py:meth:`parseaddr <email.utils.parseaddr>` to create a :py:class:`dict` of candidate email dictionary (keys are ``email`` and optionally ``full name``).

    :param str candidate_rfc2047_email: the input `RFC 2047`_ fully qualified email address.
    :returns: a :py:class:`dict` of candidate email dictionary *only* if there is a valid email address. Otherwise returns ``None``.
    :rtype: dict
    
    .. seealso:: :py:meth:`create_rfc2047_email <iv_tanim.core.rst2html.create_rfc2047_email>`
    """
    output_tuple = parseaddr( candidate_rfc2047_email )
    if output_tuple[1].strip( ) == '':
        logging.error("Error, candidate input email = %s does NOT have a valid email address." % candidate_rfc2047_email )
        return None
    return { 'email' : output_tuple[1].strip( ), 'full name' : output_tuple[0].strip( ) }

def cid_out_mimeMultiMessage( msg, mainHTML ):
    """
    Goes through the HTML email message, and creates a CID-enabled email with additional image attachments inside. Follows ideas found on `this useful stackoverflow article <https://stackoverflow.com/a/20485764>`_.

    :param msg: the message object that will be modified.
    :type msg:  :py:class:`MIMEMultipart <email.mime.multipart.MIMEMultipart>`
    :param str mainHTML: the HTML message that we will parse through for images on disk rather than as external URLs.
    :returns: the :py:class:`dict` of ``cid`` to image file name.
    :rtype: dict
    """
    htmldoc = BeautifulSoup( mainHTML, 'lxml' )
    #
    ## find all img elems that have a "src" in them and that ARE NOT an URL
    valid_imgs = list(filter(lambda elem: 'src' in elem.attrs and not validators.url( elem['src'] ), htmldoc.find_all('img')))
    if len( valid_imgs ) == 0: # don't modify document
        msg.attach( MIMEText( mainHTML, 'html', 'utf-8' ) )
        return dict()
    #
    ## now perform a replacement and create attachments
    ## follow https://stackoverflow.com/a/20485764
    cid_replacement = dict()
    for img_elem in valid_imgs:
        cid = str( uuid.uuid4( ) )
        fname = img_elem['src']
        cid_replacement[ cid ] = fname
        img_elem[ 'src' ] = "cid:%s" % cid
        img_elem[ 'alt' ] = fname
    #
    ## now attach the *changed* message
    msg.attach( MIMEText( htmldoc.prettify( ), 'html', 'utf-8' ) )
    for cid in cid_replacement:
        msg_image = MIMEImage(
            open( cid_replacement[ cid ], 'rb' ).read( ),
            name = os.path.basename( cid_replacement[ cid ] ) )
        msg_image.add_header( 'Content-ID', '<%s>' % cid )
        msg.attach( msg_image )
    return cid_replacement

def create_collective_email_full(
    mainHTML, subject, fromEmail, to_emails, cc_emails = [ ], bcc_emails = [ ], attachments = [ ] ):
    """
    Creates a :py:class:`MIMEMultiPart <email.mime.multipart.MIMEMultiPart>` email that *also* contains the following

    * the body of the message as an HTML document.

    * sender.

    * ``TO`` recipients.

    * ``CC`` recipients.

    * ``BCC`` recipients.

    * explicitly included attachments.

    * soft-conventioned ``cid`` of embedded and inlined images (PNG_, JPEG_, TIFF_, GIF_, etc.).

    Go easy on me, it's my first day!

    :param str mainHTML: the email body as an HTML :py:class:`string <str>` document.
    :param str subject: the email subject.
    :param str fromEmail: the :py:class:`dict` of email and optional full name of sender.
    :param list to_emails: the :py:class:`list` of :py:class:`dict` of ``TO`` recipients. Each ``TO`` recipient is a :py:class:`dict` of ``email`` and optionally ``full name``.
    :param list cc_emails: the :py:class:`list` of :py:class:`dict` of ``CC`` recipients. Each ``CC`` recipient is a :py:class:`dict` of ``email`` and optionally ``full name``.
    :param list bcc_emails: the :py:class:`list` of :py:class:`dict` of ``BCC`` recipients. Each ``BCC`` recipient is a :py:class:`dict` of ``email`` and optionally ``full name``.
    :param list attachments: the collection of attachments to send out.
    :returns: the message object, with soft-conventioned ``cid`` of images included.
    :rtype: :py:class:`MIMEMultipart <email.mime.multipart.MIMEMultipart>`
    """
    #
    ## get the RFC 2047 sender stuff
    msg = MIMEMultipart( )
    fq_fromEmail = create_rfc2047_email( fromEmail )
    assert( fq_fromEmail is not None )        
    msg[ 'From' ] = fq_fromEmail
    msg[ 'Subject' ] = subject
    msg[ 'To' ] = ', '.join( sorted(set(filter(None, map(create_rfc2047_email,  to_emails))))).strip( )
    msg[ 'Cc' ] = ', '.join( sorted(set(filter(None, map(create_rfc2047_email,  cc_emails))))).strip( )
    msg[ 'Bcc'] = ', '.join( sorted(set(filter(None, map(create_rfc2047_email, bcc_emails))))).strip( )
    logging.info( 'from_email: %s' % msg[ 'From' ] )
    logging.info( 'to_emails: %s.' % msg['To'] )
    logging.info( 'cc_emails: %s.' % msg['Cc'] )
    logging.info('bcc_emails: %s.' % msg['Bcc'])
    #msg.attach( MIMEText( mainHTML, 'html', 'utf-8' ) )
    cid_out_mimeMultiMessage( msg, mainHTML )
    #
    ##
    if len( attachments ) == 0: return msg
    #
    for attach in attachments:
        name = attach[ 'name' ]
        mimetype = attach[ 'mimetype' ]
        filepath = attach[ 'filepath' ]
        mainType, subtype = mimetype.split('/')[:2]
        if mainType == 'application':
            att = MIMEApplication( open( filepath, 'rb' ).read( ), _subtype = subtype )
        elif mainType == 'text':
            att = MIMEText( open( filepath, 'r' ).read( ), _subtype = subtype )
        elif mainType == 'image':
            att = MIMEImage( open( filepath, 'rb' ).read( ), _subtype = subtype )
        elif mainType == 'audio':
            att = MIMEAudio( open( filepath, 'rb' ).read( ), _subtype = subtype )
        else:
            att = MIMEApplication( open( filepath, 'rb' ).read( ) )
        att.add_header( 'content-disposition', 'attachment', filename = name )
        msg.attach( att )
    return msg

def get_attachment_object( full_file_path ):
    """
    Create the attachment :py:class:`dict` given the input file.
    
    :param str full_file_path: the location of the file on-disk.
    :returns: a :py:class:`dict` of ``name`` (which is file base name), ``mimetype``, and ``filepath`` (which is ``full_file_path``). If file does not exist, then function returns ``None``.
    :rtype: dict
    """
    if not os.path.exists( full_file_path ): return None
    mime = magic.Magic(mime=True)
    return {
        'name' : os.path.basename( full_file_path ),
        'mimetype' : mime.from_file( full_file_path ),
        'filepath' : full_file_path }

def send_email_localsmtp( msg, server = 'localhost', portnumber = 25 ):
    """
    Sends the email using the :py:class:`SMTP <smtplib.SMTP>` Python functionality to send through a local SMTP_ server.

    `This blog post`_ describes how I set up a GMail relay using my local SMTP_ server on my Ubuntu_ machine.
    
    :param msg: the email message object to send. At a high level, this is an email with body, sender, recipients, and optional attachments.
    :type msg:  :py:class:`MIMEMultipart <email.mime.multipart.MIMEMultipart>`
    :param str server: the SMTP_ server to use. Default is ``localhost``.
    :param int portnumber: the port number to use to send the email to the local SMTP_ server. Default is port 25.
    
    .. _SMTP: https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol
    .. _`This blog post`: https://tanimislam.gitlab.io/blog/sendmail-relay-setup-and-implementation.html
    """
    assert( portnumber > 0 )
    assert( len( server.strip( ) ) > 0 )
    smtp_conn = smtplib.SMTP( server.strip( ), portnumber )
    smtp_conn.ehlo( 'test' )
    smtp_conn.sendmail( msg['From'], [ msg["To"], ], msg.as_string( ) )
    smtp_conn.quit( )
