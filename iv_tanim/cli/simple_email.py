import os, sys, logging, re
from iv_tanim.core import rst2html
from argparse import ArgumentParser

def _main( ):
    parser = ArgumentParser( )
    parser.add_argument( '-f', '--emailfile', dest = 'emailfile', type = str, action = 'store', required = True,
                        help = 'Name of the restructuredtext email file to convert into HTML, THEN email out.' )
    parser.add_argument( '-s', '--subject', dest = 'subject', type = str, action = 'store', default = 'test subject',
                        help = "Email subject. Default is 'test subject'." )
    parser.add_argument( '-F', '--from', dest = 'sender', type = str, action = 'store', required = True,
                        help = 'Email and/or name of the sender. Use RFC 5322 email format.' )
    parser.add_argument( '-T', '--to', dest = 'to', type = str, nargs = '*', required = True,
                        help = 'List of email and/or names of the recipients.  Use RFC 5322 email format.' )
    parser.add_argument( '-C', '--cc', dest = 'cc', type = str, nargs = '*', default = [ ],
                        help = 'List of CC email and/or names. Use RFC 5322 email format.' )
    parser.add_argument( '-B', '--bcc', dest = 'bcc', type = str, nargs = '*', default = [ ],
                        help = 'List of BCC email and/or names. Use RFC 5322 email format.' )
    parser.add_argument( '-A', '--attach', dest = 'attach', type = str, nargs = '*', default = [ ],
                        help = 'List of files to attach to this email.' )
    parser.add_argument( '-p', '--smtpport', dest = 'smtpport', type = int, default = 25,
                        help = 'The port number for the SMTP server to send the SMTP email. Default is 25.' )
    parser.add_argument( '-S', '--smtpserver', dest = 'smtpserver', type = str, default = 'localhost',
                        help = "The name of the SMTP server to send the SMTP email. Default is 'localhost'." )
    parser.add_argument( '-I', '--info', dest = 'do_info', action = 'store_true', default = False,
                        help = 'If chosen, then do INFO logging.' )
    #
    args = parser.parse_args( )
    #
    logger = logging.getLogger( )
    if args.do_info: logger.setLevel( logging.INFO )
    #
    ## now perform the construction of all the crap
    emailfile = os.path.abspath( os.path.expanduser( args.emailfile ) )
    assert( os.path.exists( emailfile ) )
    status = rst2html.check_valid_RST( open( emailfile, 'r' ).read( ) )
    if not status:
        print( "ERROR, CANDIDATE EMAIL RST FILE = %s DID NOT WORK. TRY IT OUT BY RUNNING 'myrst2html -i %s' AND INSPECT HTML OUTPUT." % (
            emailfile, emailfile ) )
        return
    #
    ## now do the needful!

    #
    ## subject
    subject = args.subject.strip( )
    logging.info( 'SUBJECT = %s.' % subject )
    #
    ## sender
    from_address = rst2html.parse_rfc2047_email( args.sender )
    logging.info( 'FROM ADDRESS = %s.' % from_address )
    if args.sender is None:
        print( "ERROR, INPUT CANDIDATE SENDER = %s CANNOT BE CONVERTED INTO APPROPRIATE EMAIL FORMAT." % args.sender )
        return
    #
    ## recipients
    to_addresses = list(filter(None, map(rst2html.parse_rfc2047_email, args.to ) ) )
    logging.info( '%d TO ADDRESSES = %s.' % (
        len( to_addresses ),
        '\n'.join(map(lambda entry: '%s' % entry, to_addresses ) ) ) )
    if len( to_addresses ) == 0:
        print( "ERROR, INPUT RECIPIENTS = %s DID NOT WORK. FOUND NO VALID RECIPIENTS." % ( args.to ) )
        return
    #
    ## CC
    cc_addresses = list(filter(None, map(rst2html.parse_rfc2047_email, args.cc ) ) )
    logging.info( '%d CC ADDRESSES = %s.' % (
        len( cc_addresses ),
        '\n'.join(map(lambda entry: '%s' % entry, cc_addresses ) ) ) )
    #
    ## BCC
    bcc_addresses = list(filter(None, map(rst2html.parse_rfc2047_email, args.bcc ) ) )
    logging.info( '%d BCC ADDRESSES = %s.' % (
        len( bcc_addresses ),
        '\n'.join(map(lambda entry: '%s' % entry, bcc_addresses ) ) ) )
    #
    ## ATTACHMENTS
    attaches = list(filter(None, map(
        rst2html.get_attachment_object,
        filter( os.path.exists, map(lambda entry: os.path.abspath( os.path.expanduser( entry ) ), args.attach ) ) ) ) )
    logging.info( '%d ATTACHMENTS = %s.' % (
        len( attaches ), '\n'.join(map(lambda attach: '%s' % attach, attaches))))
    #
    ## PORT NUMBER
    assert( args.smtpport > 0 )
    logging.info( 'SMTP PORT NUMBER = %d.' % args.smtpport )
    #
    ## SMTP SERVER
    smtpserver = args.smtpserver.strip( )
    assert( len( smtpserver ) > 0 )
    logging.info( 'SMTP SERVER = %s.' % smtpserver )
    #
    ## FINALLY CREATE THE EMAIL!!!
    msg = rst2html.create_collective_email_full(
        rst2html.convert_string_RST( open( emailfile, 'r' ).read( ) ),
        subject,
        from_address,
        to_addresses,
        cc_emails = cc_addresses,
        bcc_emails = bcc_addresses,
        attachments = attaches )
    if args.do_info:
        dirname = os.path.dirname( emailfile )
        bname = re.sub('\.rst$', '.msg', os.path.basename( emailfile  ).strip( ) )
        with open( os.path.join( dirname, bname ), 'wb' ) as openfile:
            openfile.write( msg.as_bytes( ) )
    #
    ## NOW SEND THE EMAIL!!!
    rst2html.send_email_localsmtp( msg, portnumber = args.smtpport, server = smtpserver )
                  
        
