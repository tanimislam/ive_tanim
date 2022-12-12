__author__ = 'Tanim Islam'
__email__ = 'tanim.islam@gmail.com'

import sys, os, logging, numpy, requests, urllib3

#
## disable insecure request warnings
requests.packages.urllib3.disable_warnings( )
urllib3.disable_warnings( )

_mainDir = os.path.dirname( os.path.abspath( __file__ ) )
resourceDir = os.path.join( _mainDir, 'resources' )
assert( os.path.isdir( resourceDir ) )

logging_dict = {
    "NONE" : 100,
    "INFO" : logging.INFO,
    "DEBUG": logging.DEBUG,
    "ERROR": logging.ERROR }

def _get_ivetanim_logger( ):
    logging.basicConfig(format = '%(levelname)s %(module)s.%(funcName)s (%(lineno)d): %(message)s' )
    return logging.getLogger( )

# code to handle Ctrl+C, convenience method for command line tools
def signal_handler( signal, frame ):
    print( "You pressed Ctrl+C. Exiting...")
    sys.exit( 0 )

ivetanim_logger = _get_ivetanim_logger( )
