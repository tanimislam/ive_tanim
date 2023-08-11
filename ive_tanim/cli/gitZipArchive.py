import os, sys, subprocess, time, logging, zipfile, re
from pathos.multiprocessing import Pool, cpu_count
from shutil import which
from argparse import ArgumentParser

_git_exec = which( 'git' )
assert( _git_exec is not None )

def find_all_submodules( git_archive_dir ):
    try:
        assert( os.path.isdir( git_archive_dir ) )
        stdout_val = subprocess.check_output(
            [ _git_exec, '-C', git_archive_dir, 'submodule', 'foreach' ],
            stderr = subprocess.PIPE ).decode( 'utf8' )
        return set(map(
            lambda line: line.split("'")[1].strip( ),
            filter(lambda line: len( line.strip( ) ) > 0, stdout_val.split("\n"))))
    except Exception as e:
        logging.info( str( e ) )
        return( set([ ]) )

def zip_out_archive( git_archive_dir, zip_archive_name, current_dir, prefix = None ):
    try:
        if prefix is not None:
            stdout_val = subprocess.check_output(
                [ _git_exec, '-C', git_archive_dir, 'archive', '--format=zip', '--prefix=%s/' % prefix,
                 'HEAD', '-o', os.path.join( current_dir, zip_archive_name ) ],
                stderr = subprocess.STDOUT )
        else:
            stdout_val = subprocess.check_output(
                [ _git_exec, '-C', git_archive_dir, 'archive', '--format=zip',
                 'HEAD', '-o', os.path.join( current_dir, zip_archive_name ) ],
                stderr = subprocess.STDOUT )
        return zip_archive_name
    except Exception as e:
        logging.info( str( e ) )
        return None

def zip_out_submodules_into_main( vals_entries ):
    time0 = time.perf_counter( )
    main_zip_archive = list(filter(lambda entry: entry[ 'prefix' ] is not None, vals_entries ) )
    assert( len( main_zip_archive ) == 1 )
    main_zip_archive_entry = main_zip_archive[ 0 ]
    main_prefix = main_zip_archive_entry[ 'prefix' ]
    with zipfile.ZipFile( main_zip_archive_entry[ 'final_name' ], 'a' ) as zipFileMain:
        for other_archive in filter(lambda entry: entry[ 'prefix' ] is None, vals_entries ):
            submodule_name = other_archive[ 'submodule_name' ]
            with zipfile.ZipFile( other_archive[ 'final_name' ], 'r' ) as zipFileSub:
                for entry in zipFileSub.namelist( ):
                    with zipFileSub.open( entry ) as openfile:
                        zipFileMain.writestr( os.path.join(
                            main_prefix, submodule_name, os.path.basename( entry ) ), openfile.read( ) )
    logging.info( 'took %0.3f seconds to move %d submodules into 1 main zip archive.' % (
        time.perf_counter( ) - time0, len( vals_entries ) - 1 ) )
            
                        
def create_stuff_to_zipout( git_archive_dir, zip_archive_name_main, prefix ):
    submodule_name_dirs = find_all_submodules( git_archive_dir )
    stuff_to_zipout = list(map(lambda tup: {
        'git_archive_dir' : os.path.join( git_archive_dir, tup[1] ),
        'zip_archive_name' : os.path.join(
            os.path.dirname( zip_archive_name_main ),
            '%s.%02d.zip' % ( re.sub( '\.zip$', '', os.path.basename( zip_archive_name_main ) ).strip( ), tup[ 0 ] ) ),
        'prefix' : None,
        'submodule_name' : tup[1] }, enumerate( sorted( submodule_name_dirs ) ) ) )
    stuff_to_zipout += [
        { 'git_archive_dir' : git_archive_dir,
         'zip_archive_name' : zip_archive_name_main,
         'prefix' : prefix } ]
    return stuff_to_zipout

def delete_submodule_zip_archives( stuff_to_zipout ):
    time0 = time.perf_counter( )
    for entry in filter(lambda entry: entry['prefix'] is None, stuff_to_zipout ):
        try: os.remove( entry[ 'zip_archive_name' ] )
        except: pass
    logging.info( 'took %0.3f seconds to remove %d submodules zip archives.' % (
        time.perf_counter( ) - time0, len( stuff_to_zipout ) - 1 ) )

def create_archives_val_entries( stuff_to_zipout ):
    time0 = time.perf_counter( )
    # num_submodules = len(list(filter(lambda entry: 'submodule_name' in entry, stuff_to_zipout ) ) )
    with Pool( processes = min( cpu_count( ), len( stuff_to_zipout ) ) ) as pool:
        vals_entries = list(
            pool.map(lambda entry: dict(list( entry.items()) + [ (
                'final_name', zip_out_archive(
                    entry[ 'git_archive_dir' ],
                    entry[ 'zip_archive_name' ],
                    os.getcwd( ),
                    prefix = entry[ 'prefix' ] ) ), ] ), stuff_to_zipout ) )
        assert( len( stuff_to_zipout ) == len( vals_entries ) )
        assert( all( filter(lambda entry: entry[ 'final_name' ] is not None, vals_entries ) ) )
        logging.info( 'took %0.3f seconds to move %d submodules into 1 main zip archive.' % (
            time.perf_counter( ) - time0, len( stuff_to_zipout ) - 1 ) )
        return vals_entries                    

def main( ):
    parser = ArgumentParser( )
    parser.add_argument( '-D', '--dirname', dest = 'dirname', type = str, action = 'store', default = os.getcwd( ),
                        help = 'Name of the nominal git archive directory to zip archive out. Default is %s.' % os.getcwd( ) )
    parser.add_argument( '-z', '--zipfile', dest = 'zipfile', type = str, action = 'store', required = True,
                        help = 'Name of the ZIP ARCHIVE into which to store everything.' )
    parser.add_argument( '-p', '--prefix', dest = 'prefix', type = str, action = 'store', required = True,
                        help = 'Name of the ZIP ARCHIVE prefix into which to store everything. This is the top level directory in the zip archive.' )
    parser.add_argument( '-I', '--info', dest = 'do_info', action = 'store_true', default = False,
                        help = 'If chosen, then turn on INFO logging.' )
    #
    args = parser.parse_args( )
    logger = logging.getLogger( )
    if args.do_info: logger.setLevel( logging.INFO )
    #
    git_archive_dir = os.path.expanduser( args.dirname )
    assert( os.path.isdir( git_archive_dir ) )
    zip_archive_name_main = os.path.expanduser( args.zipfile )
    assert( os.path.basename( zip_archive_name_main ).endswith( '.zip' ) )
    stuff_to_zipout = create_stuff_to_zipout( git_archive_dir, zip_archive_name_main, args.prefix )
    #
    ## first delete all
    for entry in stuff_to_zipout:
        try: os.remove( entry[ 'zip_archive_name' ] )
        except: pass
    #
    ## now perform the creation of the archives
    vals_entries = create_archives_val_entries( stuff_to_zipout )
    #
    ## now move the stuff from the submodules into the main archive
    zip_out_submodules_into_main( vals_entries )
    #
    ## now delete the submodule entries zip archives
    delete_submodule_zip_archives( stuff_to_zipout )
