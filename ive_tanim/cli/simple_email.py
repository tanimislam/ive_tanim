import signal
from ive_tanim import signal_handler
signal.signal( signal.SIGINT, signal_handler )
#
import os, sys, logging, re, json
from itertools import chain
from ive_tanim import ivetanim_logger, configFile
from ive_tanim.core import rst2html
from argparse import ArgumentParser

_configData = json.load( open( configFile, 'r' ) )

def _get_valid_email_recipients_with_aliases( email_addresses ):
    set_of_emails = set(map(lambda tok: tok.strip( ), email_addresses ) )
    aliases = set(map(lambda tok: tok.lower( ), set_of_emails ) ) & set( _configData[ 'aliases' ] )
    try_act_emails = set_of_emails - set( _configData[ 'aliases' ] )
    final_emails = list(filter(None, map(
        rst2html.parse_rfc2047_email,
        sorted( set(chain.from_iterable([
            map(lambda alias: _configData[ 'aliases' ][ alias ], aliases ),
            try_act_emails ]) ) ) ) ) )
    ivetanim_logger.info( 'FOUND THESE %d ACTUAL EMAIL ADDRESSES: %s.' % (
        len( final_emails ), ', '.join(map(rst2html.create_rfc2047_email, final_emails ) ) ) )
    return final_emails

def _main( ):
    parser = ArgumentParser( )
    parser.add_argument( '-f', '--emailfile', dest = 'emailfile', type = str, action = 'store', required = True,
                        help = 'Name of the restructuredtext email file to convert into HTML, THEN email out.' )
    parser.add_argument( '-s', '--subject', dest = 'subject', type = str, action = 'store', default = 'test subject',
                        help = 'Email subject. Default is "test subject".' )
    #
    ## now check if default sender defined
    if _configData[ 'me' ].strip( ) == '':
        parser.add_argument( '-F', '--from', dest = 'sender', type = str, action = 'store', required = True,
                            help = 'Email and/or name of the sender. Use RFC 5322 email format.' )
    else:
        parser.add_argument( '-F', '--from', dest = 'sender', type = str, action = 'store', default = _configData[ 'me' ].strip( ),
                            help = 'Email and/or name of the sender. Use RFC 5322 email format. Default is "%s".' % _configData[ 'me' ].strip( ) )
    parser.add_argument( '-T', '--to', dest = 'to', type = str, nargs = '*', required = True,
                        help = 'List of email and/or names of the recipients.  Use RFC 5322 email format.' )
    parser.add_argument( '-C', '--cc', dest = 'cc', type = str, nargs = '*', default = [ ],
                        help = 'List of CC email and/or names. Use RFC 5322 email format.' )
    parser.add_argument( '-B', '--bcc', dest = 'bcc', type = str, nargs = '*', default = [ ],
                        help = 'List of BCC email and/or names. Use RFC 5322 email format.' )
    parser.add_argument( '-A', '--attach', dest = 'attach', type = str, nargs = '*', default = [ ],
                        help = 'List of files to attach to this email.' )
    parser.add_argument( '-p', '--smtpport', dest = 'smtpport', type = int, default = _configData[ 'smtp' ][ 'port' ],
                        help = 'The port number for the SMTP server to send the SMTP email. Default is %d.' % _configData[ 'smtp' ][ 'port' ] )
    parser.add_argument( '-S', '--smtpserver', dest = 'smtpserver', type = str, default = _configData[ 'smtp' ][ 'server' ],
                        help = "The name of the SMTP server to send the SMTP email. Default is '%s'." % _configData[ 'smtp' ][ 'server' ] )
    parser.add_argument( '-I', '--info', dest = 'do_info', action = 'store_true', default = False,
                        help = 'If chosen, then do INFO logging.' )
    #
    args = parser.parse_args( )
    #
    if args.do_info: ivetanim_logger.setLevel( logging.INFO )
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
    ivetanim_logger.info( 'SUBJECT = %s.' % subject )
    #
    ## sender
    from_address_cand = _get_valid_email_recipients_with_aliases( [ args.sender, ] )
    if len( from_address_cand ) == 0:
        print( "ERROR, INPUT CANDIDATE SENDER = %s CANNOT BE CONVERTED INTO APPROPRIATE EMAIL FORMAT." % args.sender )
        return
    from_address = from_address_cand[ 0 ]
    ivetanim_logger.info( 'FROM ADDRESS = %s.' % from_address )
    #
    ## recipients
    to_addresses = _get_valid_email_recipients_with_aliases( args.to )
    ivetanim_logger.info( '%d TO ADDRESSES = %s.' % (
        len( to_addresses ),
        '\n'.join(map(lambda entry: '%s' % entry, to_addresses ) ) ) )
    if len( to_addresses ) == 0:
        print( "ERROR, INPUT RECIPIENTS = %s DID NOT WORK. FOUND NO VALID RECIPIENTS." % ( args.to ) )
        return
    #
    ## CC
    cc_addresses = _get_valid_email_recipients_with_aliases( args.cc )
    ivetanim_logger.info( '%d CC ADDRESSES = %s.' % (
        len( cc_addresses ),
        '\n'.join(map(lambda entry: '%s' % entry, cc_addresses ) ) ) )
    #
    ## BCC
    bcc_addresses = _get_valid_email_recipients_with_aliases( args.bcc )
    if _configData[ 'me' ].strip( ) != '':
        bcc_addresses += [ rst2html.parse_rfc2047_email( _configData[ 'me' ] ), ]
    ivetanim_logger.info( '%d BCC ADDRESSES = %s.' % (
        len( bcc_addresses ),
        '\n'.join(map(lambda entry: '%s' % entry, bcc_addresses ) ) ) )
    #
    ## ATTACHMENTS
    attaches = list(filter(None, map(
        rst2html.get_attachment_object,
        filter( os.path.exists, map(lambda entry: os.path.abspath( os.path.expanduser( entry ) ), args.attach ) ) ) ) )
    ivetanim_logger.info( '%d ATTACHMENTS = %s.' % (
        len( attaches ), '\n'.join(map(lambda attach: '%s' % attach, attaches))))
    #
    ## PORT NUMBER
    assert( args.smtpport > 0 )
    ivetanim_logger.info( 'SMTP PORT NUMBER = %d.' % args.smtpport )
    #
    ## SMTP SERVER
    smtpserver = args.smtpserver.strip( )
    assert( len( smtpserver ) > 0 )
    ivetanim_logger.info( 'SMTP SERVER = %s.' % smtpserver )
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
