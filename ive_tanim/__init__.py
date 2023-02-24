__author__ = 'Tanim Islam'
__email__ = 'tanim.islam@gmail.com'

import sys, os, logging, numpy, requests, urllib3, json

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

baseConfDir = os.path.abspath( os.path.expanduser( '~/.config/ive_tanim' ) )
"""
the directory where ``IVE_TANIM`` user data is stored -- ``~/.config/ive_tanim``.
"""

configFile = os.path.join( baseConfDir, 'config.json' )
"""
The configuration file location of ``IVE_TANIM`` configuration data -- ``~/.config/ive_tanim/config.json``.
"""

def create_config( ):
    """
    Creates the necessary JSON configuration file into ``~/.config/ive_tanim/config.json``, AND to create the ``~/.config/ive_tanim`` if not there. The configuration file contains three empty keys by default.

    * ``me`` with an empty string "" value.
    * ``aliases`` with an empty :py:class:`dict` value.
    * ``smtp`` with a :py:class:`dict` describing a default SMTP server.
      
      .. code-block:: console

         { 'server' : 'localhost',
           'port' : 25 }

    Useful methods in :py:mod:`rst2html <ive_tanim.core.rst2html>` will do the following:

    * Set the default sender (owned by the ``me`` key).

    * Add aliases (key-value pairs into the :py:class:`dict` owned by the the ``aliases`` key).

    * Set the default SMTP server settings (changing the ``server`` name and changing the default port).
    """
    #
    ## don't do anuthing if in READTHEDOCS
    if os.environ.get( 'READTHEDOCS' ): return
    #
    ## if directory not exists create it.
    if not os.path.isdir( baseConfDir ): os.mkdir( baseConfDir )
    #
    ## if JSON config file not exist create one with top-level keys with 'me' and 'aliases'
    if os.path.exists( configFile ): return
    json.dump( {
        'me' : '',
        'aliases' : dict(),
        'smtp' : { 'server' : 'localhost', 'port' : 25 } },
              open( configFile, 'w' ), indent = 1 )

create_config( ) # OK now create the config directory and everything
    
ivetanim_logger = _get_ivetanim_logger( )
