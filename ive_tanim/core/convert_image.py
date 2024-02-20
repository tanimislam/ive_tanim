import requests, os, gzip, magic, uuid, pathlib, glob, time
import subprocess, json, re, numpy
from pathos.multiprocessing import Pool, cpu_count
from PIL import Image
from pypdf import PdfReader
from ive_tanim import ivetanim_logger
from ive_tanim.core import autocrop_image

def mp4fromimages( images2mp4dict ):
    """
    Creates an MP4_ file from the low-level input specification :py:class:`dict` that :py:meth:`create_images2mp4dict <ive_tanim.core.convert_image.create_images2mp4dict>` creates. Requires the existence of the ``ffmpeg`` executable, and ``status`` value in the :py:class:`dict` *must* be ``"SUCCESS"``. Otherwise, this method does not create a movie file.

    If ``dirname`` is the directory in which the image files live, and ``PREFIX`` is the prefix of all the image files, the MP4_ file is named ``dirname/PREFIX.mp4``.

    :param dict images2mp4dict: the dictionary specification for creating a specific MP4_ file from a collection of image files as frames.

    .. seealso:: :py:meth:`create_images2mp4dict <ive_tanim.core.convert_image.create_images2mp4dict>`.
    """
    #
    ## barf out if cannot find ffmpeg
    from shutil import which
    ffmpeg_exec = which( 'ffmpeg' )
    if ffmpeg_exec is None:
        raise ValueError("Error, ffmpeg could not be found." )
    assert( images2mp4dict['status'] == 'SUCCESS' )
    def _resize_image( fname ):
        im = Image.open( fname )
        sizeChanged = False
        newWidth, newHeight = im.size
        if newWidth % 2 != 0:
            newWidth += 1
            sizeChanged = True
        if newHeight % 2 != 0:
            newHeight += 1
            sizeChanged = True
        if sizeChanged:
            im = im.resize(( newWidth, newHeight ))
            im.save( fname )
    #
    ## now ensure that these files are of even-width-and-height
    with Pool( processes = cpu_count( ) ) as pool:
        time0 = time.perf_counter( )
        autocrop = images2mp4dict[ 'autocrop' ]
        if not autocrop:
            _ = list(pool.map(_resize_image, images2mp4dict['files'] ) )
        else:
            _ = list(pool.map(lambda fname: autocrop_image.autocrop_image( fname, fixEven = True ),
                              images2mp4dict['files']))
        ivetanim_logger.info('fixed widths and heights of %d images in %0.3f seconds.' % (
            len( images2mp4dict['files'] ), time.perf_counter( ) - time0 ) )
    #
    ## now create the FFMPEG movie file
    ## thank instructions from https://hamelot.io/visualization/using-ffmpeg-to-convert-a-set-of-images-into-a-video/
    ## make MP4 movie, 5 fps, quality = 25
    time0 = time.perf_counter( )
    num_dots = len( images2mp4dict['prefix'].split('.')[:-1] )
    ivetanim_logger.info('NUM DOTS mp4fromimages: %d.' % num_dots )
    if num_dots == 0:
        movie_name = '%s.mp4' % images2mp4dict['prefix']
    else:
        movie_name = '%s.mp4' % '.'.join(images2mp4dict['prefix'].split('.')[:-1])
    stdout_val = subprocess.check_output(
        [ ffmpeg_exec, '-y', '-r', '%d' % images2mp4dict['fps'], '-f', 'image2',
         '-i', images2mp4dict['actual prefix'],
         '-vcodec', 'libx264', '-crf', '25', '-pix_fmt', 'yuv420p', movie_name ],
        stderr = subprocess.STDOUT )        
    ivetanim_logger.info('created movie = %s from %d image frame images in %0.3f seconds.' % (
        movie_name, len( images2mp4dict['files'] ), time.perf_counter( ) - time0 ) )
    
def create_images2mp4dict( prefix, image_suffix = 'png', dirname = os.getcwd( ), fps = 5, autocrop = False ):
    """
    This method creates a complicated and low-level :py:class:`dict` of set up, when creating an MP4_ file from a collection of images. Here are things needed to make this work. :py:meth:`mp4fromimages <ive_tanim.core.convert_image.mp4fromimages>` uses this :py:class:`dict` to create the MP4_ file.

    #. The collection of image files exist in a directory named ``dirname``.

    #. The format of the image files as frames of a movie must have a name like ``PREFIX0000.<image_suffix>`` to ``PREFIX0401.<image_suffix>``.

    #. The first image file must have a zero-padded value of zero. There must also be *no* number gaps in the sequence of image files as frames. For example, if there are image files ``PREFIX0200.<image_suffix>`` and ``PREFIX0202.<image_suffix>`` but *no* ``PREFIX0201.<image_suffix>``, this process will fail.
    
    In case of success, this method returns a :py:class:`dict` with these five keys and values.

    * ``status``: the :py:class:`string <str>` ``"SUCCESS"``.
    * ``files``: the sorted :py:class:`list` of image file names as movie frames.
    * ``autocrop``: :py:class:`bool` on whether to autocrop the image files.
    * ``fps``: the :py:class:`int` number of frames per second in the MP4_ file.
    * ``actual prefix``: the input (``ffmpeg -i <arg>``) argument that goes into FFmpeg_ when creating the MP4_ from a collection of image files as frames.

    In case of failure, the ``status`` key contains the reason for the failure. :py:meth:`mp4fromimages <ive_tanim.core.convert_image.mp4fromimages>` returns this failure message and does nothing.

    :param str prefix: the base name of each image file as frame, before the integer frame number and ``.<image_suffix>`` suffix.
    :param str image_suffix: the image suffix through which to look. Default is ``png``.
    :param str dirname: the directory in which these image files live. Default is the current working directory.
    :param int fps: the number of frames per seconds for the movie. Must be :math:`\ge 1`.
    :param bool autocrop: whether to automatically crop out white space in the image files as frames. Default is ``False``.
    :returns: the :py:class:`dict` described above.
    :rtype: dict

    .. seealso:: :py:meth:`mp4fromimages <ive_tanim.core.convert_image.mp4fromimages>`.

    .. FFmpeg_: https://ffmpeg.org
    """
    images2mp4dict = { }
    if fps < 1:
        images2mp4dict['status'] = 'Error, fps = %d is less than 1.' % fps
        return images2mp4dict
    images2mp4dict['fps'] = fps
    images2mp4dict['autocrop'] = autocrop
    #
    ## check that it is a dirname
    if not os.path.isdir( dirname ):
        images2mp4dict['status'] = 'Error, %s is not a directory.' % dirname
        return images2mp4dict
    #
    ## now see if IMAGE files with prefix
    isuffix_lower = image_suffix.strip( ).lower( )
    collection_of_image_files = list(filter(os.path.isfile, glob.glob( os.path.join( dirname, '%s*.%s' % (
        prefix, isuffix_lower ) ) ) ) )
    if not collection_of_image_files:
        images2mp4dict['status'] = 'Error, no %s files with prefix = %s found in %s.' % (
            isuffix_lower.upper( ), prefix, dirname )
        return images2mp4dict
    #
    ## now only those collection of png files that have number suffix
    def _is_numbered_prop( fname ):
        bname = os.path.basename( fname )
        bname = bname.replace( prefix, '' ).strip( )
        bname = re.sub('\.%s$' % isuffix_lower, '', bname ).strip( )
        try:
            val = int( bname )
            return True, val, bname
        except:
            return False, None, bname
    collection_files_valid = sorted(filter(lambda fname: _is_numbered_prop(fname)[0], collection_of_image_files ) )
    sorted_numbers_dict = dict(map(lambda fname: ( _is_numbered_prop( fname )[1], fname ), collection_files_valid ) )
    zero_padded_nums = set(map(lambda fname: _is_numbered_prop( fname )[2], collection_files_valid))
    min_zero_padding = min(map(lambda zpn: len(zpn) - len(zpn.lstrip('0')), zero_padded_nums))
    if not sorted_numbers_dict:
        images2mp4dict['status'] = 'Error, no PNG files with prefix = %s AND PROPER NUMBERING found in %s.' % (
            prefix, dirname )
        return images2mp4dict
    #
    ## now check that the numbers are all ordered from 0 to SOME MAX NUMBER
    set_numbers = set(sorted_numbers_dict)
    should_be_sorted = set(range(len(sorted_numbers_dict)))
    if should_be_sorted != set_numbers:
        numbers_missing = sorted((set_numbers - should_be_sorted) | (should_be_sorted - set_numbers))
        images2mp4dict['status'] = 'Error, XOR operations found these %d numbers mismatched between what SHOULD be there, and what is: %s.' % ( len( numbers_missing ), numbers_missing )
        return images2mp4dict
    #
    ## success?
    images2mp4dict['prefix'] = prefix
    images2mp4dict['files'] = sorted( sorted_numbers_dict.values( ) )
    num_digits = int(numpy.log10(len(set_numbers)-1)) + 1 + min_zero_padding
    images2mp4dict['actual prefix'] = os.path.join( dirname, '%s%%0%dd.%s' % (
        prefix, num_digits, isuffix_lower ) ) # prefix to ffmpeg for images
    images2mp4dict['status'] = 'SUCCESS'
    return images2mp4dict

def make_aspected_mp4video( input_mp4_file, output_mp4_file, aspect = 'square', background = 'white' ):
    """
    More FFmpeg_ voodoo, this time to create a square (or 9/16 aspect or 16/9 aspect) MP4_ file for upload into Instagram_.

    This requires a working ``ffmpeg`` and ``ffprobe`` executable to work. The input file must be MP4_.

    Here are resources that I used to get this working.

    * `Padding movie file with FFmpeg <padding_movie_>`_.

    * `Using FFPROBE to output JSON format <ffprobe_json_>`_.

    :param str input_mp4_file: the name of the valid input MP4_ file.
    :param str output_mp4_file: the name of the valid output MP4_ file.
    :param str aspect: the aspect ratio to choose. Must be one of "square", "916" is 9/16 (width 9 units, height 16 units), and "169" is 16/9 (width 16 units, height 9 units). Default is "square".
    :param str background: the background color to use for padding. Must be either "white" or "black". Default is "white".

    .. _FFmpeg: https://ffmpeg.org
    .. _MP4: https://en.wikipedia.org/wiki/MPEG-4_Part_14
    .. _MKV: https://en.wikipedia.org/wiki/Matroska
    .. _padding_movie: https://superuser.com/questions/1212106/add-border-to-video-ffmpeg
    .. _ffprobe_json: https://tanimislam.gitlab.io/blog/ffprobe-to-get-output-in-json-format.html
    """
    from shutil import which
    import shutil
    ffmpeg_exec = which( 'ffmpeg' )
    ffprobe_exec = which( 'ffprobe' )
    assert(all(map(lambda tok: tok is not None, ( ffmpeg_exec, ffprobe_exec ))))
    assert( os.path.basename( input_mp4_file ).endswith( '.mp4' ) )
    assert( os.path.isfile( input_mp4_file ) )
    assert( aspect in ('square', '916', '169') )
    assert( background in ('black', 'white') )
    #
    ## first dictionary of multiplication of width to height
    aspect_dict = { 'square' : 1, '916' : 9.0 / 16, '169' : 16.0 / 9 }
    #
    ## assert this is an MP4 file, and output ends in .mp4
    assert( 'ISO Media,' in magic.from_file( input_mp4_file ) )
    assert( os.path.basename( output_mp4_file ).endswith( '.mp4' ) )
    ## get info JSON to get width, fps
    stdout_val = subprocess.check_output(
        [ ffprobe_exec, '-v', 'quiet', '-show_streams',
         '-show_format', '-print_format', 'json', input_mp4_file ],
        stderr = subprocess.STDOUT )
    mp4file_info = json.loads( stdout_val )
    # from dictionary, get width and height
    width_of_mp4 = int( mp4file_info[ 'streams' ][ 0 ][ 'width' ] )
    height_of_mp4 = int( mp4file_info[ 'streams' ][ 0 ][ 'height' ] )
    asp = aspect_dict[ aspect ]
    #
    ## if input video already correctly aspected, copy to output mp4 file
    if int( width_of_mp4 ) == int( asp * height_of_mp4 ):
        shutil.copyfile( input_mp4_file, output_mp4_file )
        return
    #
    ## case #1: asp * height_of_mp4 > width_of_mp4, pad width
    elif asp * height_of_mp4 > width_of_mp4:
        filter_string = 'pad=w=%d:h=%d:x=%d:y=0:color=%s' % (
            width_of_mp4 + int( asp * height_of_mp4 - width_of_mp4 ),
            height_of_mp4, ( asp * height_of_mp4 - width_of_mp4 ) // 2, background )
    #
    ## case #2: asp * height_of_mp4 < width_of_mp4, pad height
    else:
        filter_string = 'pad=w=%d:h=%d:x=0:y=%d:color=%s' % (
            width_of_mp4, height_of_mp4 + int( width_of_mp4 / asp - height_of_mp4 ),
            ( width_of_mp4 / asp - height_of_mp4 ) // 2, background )
    #
    ## now voodoo magic do do
    exec_cmd = [
        ffmpeg_exec, '-y', '-v', 'warning', '-i', input_mp4_file,
        '-vf', filter_string, output_mp4_file ]
    ivetanim_logger.info( 'CMD: %s' % ' '.join( exec_cmd ) )
    stdout_val = subprocess.check_output(
        exec_cmd, stderr = subprocess.STDOUT )
    
def mp4togif( input_mp4_file, gif_file = None, duration = None, scale = 1.0 ):
    """
    This consists of voodoo FFmpeg_ magic that converts MP4_ to animated GIF_ reasonably well. Don't ask me how most of it works, just be on-your-knees-kissing-the-dirt grateful that MILLIONS of people hack onto and into FFmpeg_ so that this information is available, and the workflow works.
    
    This requires a working ``ffmpeg`` and ``ffprobe`` executable to work. If the input file is named ``<input>.mp4``, the output animated GIF file is named ``<input>.gif``.
    
    Here are resources that I used to get this working.
    
    * `Tutorial on high quality movie to animated GIF conversion <movie_2_gif_>`_. I hope this doesn't go away!
    
    * `Using FFPROBE to output JSON format <ffprobe_json_>`_.
    
    :param str input_mp4_file: the name of the valid MP4_ file.
    :param str gif_file: the (optional) name of the animated GIF_ file. If not provided, then creates a GIF file of some default name.
    :param float duration: duration, in seconds, of MP4_ file to use to make the animated GIF_. If ``None`` is provided, use the full movie. If provided, then must be :math:`\ge 1` seconds.
    :param float scale: scaling of input width and height of MP4_ file. Default is 1.0. Must be :math:`\ge 0`.
  
    .. seealso:: :py:meth:`make_aspected_mp4video <ive_tanim.core.convert_image.make_aspected_mp4video>`.
    
    .. _GIF: https://en.wikipedia.org/wiki/GIF
    .. _movie_2_gif: http://blog.pkh.me/p/21-high-quality-gif-with-ffmpeg.html
    """
    from shutil import which
    ffmpeg_exec = which( 'ffmpeg' )
    ffprobe_exec = which( 'ffprobe' )
    assert(all(map(lambda tok: tok is not None, ( ffmpeg_exec, ffprobe_exec ))))
    assert( os.path.basename( input_mp4_file ).endswith( '.mp4' ) )
    assert( os.path.isfile( input_mp4_file ) )
    if duration is not None: assert( duration >= 1.0 )
    assert( scale > 0.0 )
    #
    ## assert this is an MP4 file
    assert( 'ISO Media,' in magic.from_file( os.path.realpath( input_mp4_file ) ) )
    #
    ## GIF output and PALETTE file
    if gif_file is None: gif_file = input_mp4_file.replace('.mp4', '.gif' )
    else: assert( os.path.basename( gif_file ).endswith( '.gif' ) )
    palettefile = '%s.png' % str( uuid.uuid4( ) )
    #
    ## step #0: first scale the image if not X1
    newmp4file = input_mp4_file
    if scale != 1.0:
        newmp4file = '%s.mp4' % str( uuid.uuid4( ) )
        #
        ## motherfucker
        ## thought experiment: you want to scale a (divisible-by-two) MP4 file by some multiplier
        ## the OUTPUT file itself must have width AND height divisible by two
        ## the corporate knowledge is embedded in 'scale=ceil(iw*%0.2f)*2:ceil(ih*%0.2f)*2' % ( scale * 0.5, scale * 0.5 )
        ## intent of that video filter: scale width and height by HALF of scale, round-up width + height, multiple by 2.
        ## by definition this will create a final (scaled) width and height that are divisible by two
        ## solution to impossib-error: https://stackoverflow.com/questions/20847674/ffmpeg-libx264-height-not-divisible-by-2
        ## motherfucker
        cmd = [
            ffmpeg_exec, '-y', '-v', 'warning', '-i', input_mp4_file,
            '-vf', 'scale=ceil(iw*%0.2f)*2:ceil(ih*%0.2f)*2' % ( scale * 0.5, scale * 0.5 ),
            newmp4file ]
        ivetanim_logger.debug('COMMAND TO SCALE = %s.' % ' '.join( cmd ) )
        stdout_val = subprocess.check_output(
            cmd, stderr = subprocess.STDOUT )
        ivetanim_logger.debug( 'OUTPUT FFMPEG SCALE = %s.' % stdout_val )
    
    #
    ## get info JSON to get width, fps
    stdout_val = subprocess.check_output(
        [ ffprobe_exec, '-v', 'quiet', '-show_streams',
         '-show_format', '-print_format', 'json', newmp4file ],
        stderr = subprocess.STDOUT )
    mp4file_info = json.loads( stdout_val )
    ivetanim_logger.debug( 'mp4file_info = %s.' % mp4file_info )
    # from dictionary, get width
    streams_with_width = list(filter(lambda strm: 'width' in strm, mp4file_info[ 'streams' ] ) )
    assert( len( streams_with_width ) != 0 )
    width_of_mp4 = int( streams_with_width[ 0 ][ 'width' ] )
    fps_string = streams_with_width[ 0 ][ 'avg_frame_rate' ]
    fps = int( float( fps_string.split('/')[0] ) * 1.0 /
              float( fps_string.split('/')[1] ) )
    
    #
    ## now do the voodoo magic from resource #1
    ## step #1: create palette, run at fps
    args_mov_before = [ ]
    if duration is not None: args_mov_before = [ '-t', '%0.3f' % duration ]
    cmd = [
        ffmpeg_exec, '-y', '-v', 'warning', ] + args_mov_before + [
            '-i', newmp4file,
            '-vf', 'fps=%d,scale=%d:-1:flags=lanczos,palettegen' % ( fps, width_of_mp4 ),
            palettefile ]
    stdout_val = subprocess.check_output(cmd, stderr = subprocess.STDOUT )
    assert( os.path.isfile( palettefile ) )
    #
    ## step #2: take palette file, MP4 file, create animated GIF
    cmd = [
        ffmpeg_exec, '-y', '-v', 'warning' ] + args_mov_before + [
            '-i', newmp4file,
            '-i', palettefile, '-lavfi', 'fps=%d,scale=%d:-1:flags=lanczos[x];[x][1:v]paletteuse' % (
            fps, width_of_mp4 ), gif_file ]
    stdout_val = subprocess.check_output(cmd, stderr = subprocess.STDOUT )
    #
    ## now batting cleanup
    try:
        if newmp4file != input_mp4_file: os.remove( newmp4file )
        os.remove( palettefile )
    except Exception as e:
        print( 'REASON FAILURE WHY:', e )
        pass


def png2png( input_png_file, newWidth = None, verify = True ):
    """
    Returns an :py:class:`Image <PIL.Image.Image>` object of the PNG_ file produced when the CloudConvert_ server uploaded an input PNG_ file. The output PNG_ file has the same aspect ratio as the input file.

    :param str input_png_file: the input PNG_ file. Filename must end in ``.png``.
    :param int newWidth: optional argument. If specified, the pixel width of the output image.
    :param bool verify: optional argument, whether to verify SSL connections. Default is ``True``.
    
    :returns: the :py:class:`Image <PIL.Image.Image>` object of the PNG_ file from the input PNG_ file.

    .. seealso::

        * :py:meth:`pdf2png <ive_tanim.core.convert_image.pdf2png>`.
    """
    assert( os.path.basename( input_png_file ).endswith( '.png' ) )
    assert( os.path.isfile( input_png_file ) )
    width, height = Image.open( input_png_file ).size
    files = { 'file' : open( input_png_file, 'rb' ).read( ) }
    return _return_image_cc(
        width, height, input_png_file, 'png', files, params.copy( ),
        newWidth = newWidth, verify = verify )

def pdf2png( input_pdf_file, newWidth = None, verify = True ):
    """
    Returns an :py:class:`Image <PIL.Image.Image>` object of the PNG_ file produced when the CloudConvert_ server uploaded an input PDF_ image file. The output PNG_ file has the same aspect ratio as the input file.

    :param str input_png_file: the input PNG_ file. Filename must end in ``.png``.
    :param int newWidth: optional argument. If specified, the pixel width of the output image.
    :param bool verify: optional argument, whether to verify SSL connections. Default is ``True``.
    
    :returns: the :py:class:`Image <PIL.Image.Image>` object of the PNG_ file from the input PNG_ file.

    .. _PDF: https://en.wikipedia.org/wiki/PDF

    .. seealso::

        * :py:meth:`png2png <ive_tanim.core.convert_image.png2png>`.
    """
    assert( os.path.basename( input_pdf_file ).endswith( '.pdf' ) )
    assert( os.path.isfile( input_pdf_file ) )
    ipdf = PdfReader( open( input_pdf_file, 'rb' ) )
    assert( len( ipdf.pages ) == 1 )
    mbox = ipdf.getPage( 0 ).mediabox
    files = { 'file' : open( input_pdf_file, 'rb' ).read( ) }
    width = int( mbox.width )
    height = int( mbox.height )
    return _return_image_cc(
        width, height, input_pdf_file, 'pdf', files,
        newWidth = newWidth, verify = verify )
