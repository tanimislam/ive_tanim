import signal
from ive_tanim import signal_handler
signal.signal( signal.SIGINT, signal_handler )
#
import os, sys, numpy, json, logging
from tabulate import tabulate
from ive_tanim import configFile, ivetanim_logger
from ive_tanim.core import rst2html
from argparse import ArgumentParser

def display_aliases( show_emails = True ):
    configData = json.load( open( configFile, 'r' ) )
    data_to_show = list(map(lambda alias: ( alias, configData[ 'aliases' ][ alias ] ), sorted( configData[ 'aliases' ] ) ) )
    if len( data_to_show ) == 0:
        print( 'FOUND NO EMAIL ALIASES' )
        return
    print( 'FOUND %02d EMAIL ALIASES' % len( configData[ 'aliases' ] ) )
    print( '' )
    if show_emails:
        print( '%s\n' % tabulate( data_to_show, headers = [ 'ALIAS', 'FULL EMAIL ADDRESS' ] ) )
        return
    print( '%s\n' % tabulate( list(map(lambda alias: ( alias, ), sorted( configData[ 'aliases' ] ) ) ),
                              headers = [ 'ALIAS', ] ) )

def display_me( ):
    configData = json.load( open( configFile, 'r' ) )
    data_me_email = configData[ 'me' ]
    if data_me_email.strip( ) == '':
        print( 'FOUND NO EMAIL ADDRESS' )
        return
    print( 'DEFAULT EMAIL ADDRESS: %s.' % data_me_email )

def display_smtp( ):
    configData = json.load( open( configFile, 'r' ) )
    data_me_smtp = configData[ 'smtp' ]
    print( 'DEFAULT SMTP SERVER: %s.' % data_me_smtp[ 'server' ] )
    print( 'DEFAULT SMTP PORT: %d.' % data_me_smtp[ 'port' ] )

def main( ):
    parser = ArgumentParser( )
    parser.add_argument('--info', dest='do_info', action='store_true', default = False,
                        help = 'If chosen, then print out INFO level logging statements.' )
    #
    subparsers = parser.add_subparsers(
        help = '\n'.join([
            "Choose one of these six options (stuff before the first colon):",
            "show_aliases: show the list of email aliases I have.",
            "show_me: show whether I have a default sender (me). If so, then show sender's default email identity.",
            "show_smtp: show the settings for the SMTP server I have identified.",
            "add_alias: add an email alias.",
            "set_me: set up the default sender's identity.",
            "set_smtp: set up the default SMTP server." ]),
        dest = 'choose_option' )
    #
    ## show_aliases
    parser_showaliases = subparsers.add_parser( 'show_aliases', help = 'If chosen, show the list of email aliases I have.' )
    parser_showaliases.add_argument( '-H', '--hidealiases', dest = 'parser_showaliases_showemails', action = 'store_false', default = True,
                                     help = 'If chosen, then HIDE the email addresses when showing the list of aliases. Default is to SHOW.' )
    #
    ## show_me
    parser_showme = subparsers.add_parser( 'show_me', help = "show whether I have a default sender (me). If so, then show sender's default email identity." )
    #
    ## show_smtp
    parser_showsmtp = subparsers.add_parser( 'show_smtp', help = "show the settings for the SMTP server I have identified." )
    #
    ## add_alias
    parser_addalias = subparsers.add_parser( 'add_alias', help = 'add an email alias.' )
    parser_addalias.add_argument( '-a', '--alias', dest = 'parser_addalias_alias', type = str, required = True,
                                 help = 'Name of the alias to use for an emailer.' )
    parser_addalias.add_argument( '-e', '--email', dest = 'parser_addalias_email', type = str, required = True,
                                 help = 'The RFC 5322 email format of the emailer.' )
    #
    ## set_me
    parser_setme = subparsers.add_parser( 'set_me', help = "set up the default sender's identity." )
    parser_setme.add_argument( '-e', '--email', dest = 'parser_setme_email', type = str, required = True,
                              help = 'The RFC 5322 email format of the sender.' )
    #
    ## set_smtp
    parser_smtp = subparsers.add_parser( 'set_smtp', help = "set up the default SMTP server." )
    parser_smtp.add_argument( '-S', '--server', dest = 'parser_smtp_server', type = str, default = 'localhost',
                             help = "The name of the default SMTP server. Default is 'localhost'." )
    parser_smtp.add_argument( '-p', '--port', dest = 'parser_smtp_port', type = int, default = 25,
                             help = "The port number of the default SMTP server. Default is 25." )
    #
    ##
    args = parser.parse_args( )
    if args.do_info: ivetanim_logger.setLevel( logging.INFO )
    #
    ## if show_aliases
    if args.choose_option == 'show_aliases':
        display_aliases( args.parser_showaliases_showemails )
        return
    #
    ## if show_me
    if args.choose_option == 'show_me':
        display_me( )
        return
    #
    ## if show_smtp
    if args.choose_option == 'show_smtp':
        display_smtp( )
        return
    #
    ## if add_alias
    if args.choose_option == 'add_alias':
        alias = args.parser_addalias_alias.strip( ).lower( )
        email = args.parser_addalias_email.strip( )
        status = rst2html.config_email_alias( alias, email )
        if status == False:
            print('ERROR, COULD NOT ADD ALIAS = %s, EMAIL = %s.' % ( alias, email ) )
        else:
            print('SUCCESSFULLY ADDED ALIAS = %s, EMAIL = %s.' % ( alias, email ) )
        return
    #
    ## if set_me
    if args.choose_option == 'set_me':
        email = args.parser_setme_email.strip( )
        status = rst2html.config_email_default_sender( email )
        if status == False:
            print('ERROR, COULD NOT SET DEFAULT SENDER EMAIL TO %s.' % email )
        else:
            print('SUCCESSFULLY SET DEFAULT SENDET EMAIL TO %s.' % email )
        return
    #
    ## if set_smtp
    if args.choose_option == 'set_smtp':
        server = args.parser_smtp_server.strip( )
        port = args.parser_smtp_port
        assert( port >= 10 ) # port number MUST be >= 10
        rst2html.config_email_default_smtp( server = server, port = port )
        print( 'SUCCESSFULLY SET DEFAULT SMTP SERVER = %s AND PORT = %d.' % (
            server, port ) )
        return
