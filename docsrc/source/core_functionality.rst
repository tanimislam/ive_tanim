.. include:: urls.rst

.. _core_functionality_label:
	     
Core Functionality
^^^^^^^^^^^^^^^^^^^
This consists of the *main* functionality of |ivetanim|.

.. _autoCropImage_label:

autoCropImage
==================
``autoCropImage`` automatically crops image (PNG_, JPEG_, TIFF_, etc.) and PDF_ files to remove whitespace. The default whitespace color is ``white``. The help screen for this command line tool is here,

.. code-block:: console

   usage: autoCropImage [-h] --input INPUT [--output OUTPUT] [--color COLOR] [--trans] [--newwidth NEWWIDTH] [--show]

   optional arguments:
     -h, --help           show this help message and exit
     --input INPUT        Name of the input file.
     --output OUTPUT      Name of the output file. Optional.
     --color COLOR        Name of the color over which to autocrop. Default is white.
     --trans              If chosen, also remove the transparency wrapping around the image. Works only for non-PDF images.
     --newwidth NEWWIDTH  New width of the image.
     --show               If chosen, then show the final image after cropped.

In the two examples shown here, I use only *white* (default) background. The first example, :numref:`fig_autocrop_png` demonstrates how this tool autocrops a PNG_ image file.

.. _fig_autocrop_png:

.. figure:: images/iwanttobelieve_uncropped_cropped.png
   :width: 100%
   :align: left

   On the left (with dark black borders) is the uncropped file, :download:`iwanttobelieve_uncropped.png <images/iwanttobelieve_uncropped.png>`, and on the right is the cropped-without-any-whitespace (with dark black borders) file, :download:`iwanttobelieve_cropped.png <images/iwanttobelieve_cropped.png>`.

You can generate :download:`iwanttobelieve_cropped.png <images/iwanttobelieve_cropped.png>` from :download:`iwanttobelieve_uncropped.png <images/iwanttobelieve_uncropped.png>` by running,

.. code-block:: console

   autoCropImage --input=iwanttobelieve_uncropped.png --output=iwanttobelieve_cropped.png

The second example, :numref:`fig_autocrop_pdf` demonstrates how this tool autocrops a PDF_ image file.

.. _fig_autocrop_pdf:

.. figure:: images/cumulative_plot_emission_uncropped_cropped.png
   :width: 100%
   :align: left

   On the left (with dark black borders) is the uncropped file, :download:`cumulative_plot_emission_uncropped.pdf <images/cumulative_plot_emission_uncropped.pdf>`, and on the right is the cropped-without-any-whitespace (with dark black borders) file, :download:`cumulative_plot_emission_cropped.pdf <images/cumulative_plot_emission_cropped.pdf>`.

You can generate :download:`cumulative_plot_emission_cropped.pdf <images/cumulative_plot_emission_cropped.pdf>` from :download:`cumulative_plot_emission_uncropped.pdf <images/cumulative_plot_emission_uncropped.pdf>` by running,

.. code-block:: console

   autoCropImage --input=cumulative_plot_emission_uncropped.pdf --output=cumulative_plot_emission_cropped.pdf

.. _convertImage_label:

convertImage
================
``convertImage`` does *three* things, as seen when running ``convertImage -h``.

.. code-block:: console

   usage: convertImage [-h] [--noverify] [--info] {movie,aspected,fromimages} ...

   Now does five different things, where only "image" operates on image files!

   positional arguments:
     {movie,aspected,fromimages}
			   Choose whether to convert a video or an image
       movie               If chosen, convert an MP4 into an animated GIF.
       aspected            If chosen, create an aspected MP4 file from an input MP4 file.
       fromimages          If chosen, then convert a sequence of PNG/JPEG/TIF images into an MP4 file.

   optional arguments:
     -h, --help            show this help message and exit
     --noverify            If chosen, do not verify the SSL connection.
     --info                If chosen, then print out INFO level logging.

There are two optional top-level flags.

* ``--info`` prints out :py:const:`INFO <logging.INFO>` level :py:mod:`logging` output.

* ``--noverify`` ignores verification of SSL transactions. It is optional and defaults to ``False``.

:ref:`convertImage fromimages <convertImage_fromimages>` creates an MP4_ file from a sequence of PNG_ as frames. :ref:`convertImage movie <convertImage_movie>` creates an animated GIF_ file from an MP4_ file. Finally, :ref:`convertImage aspected <convertImage_aspected>` creates an *aspected* MP4_ file from an input MP4_ file.

:ref:`convertImage movie <convertImage_movie>`, and :ref:`convertImage fromimages <convertImage_fromimages>` use FFmpeg_ underneath the hood, using a :py:mod:`subprocess.check_output <subprocess.check_output>` that implements this `tutorial on high quality movie to animated GIF conversion <movie_2_gif_>`_.

.. note::

   A recent `Medium article`_ describes two ways to produce similarly high quality animated GIF_ files.

   * create the animated GIF_ from a frame-by-frame list of PNG_ files, such as those used to create the MP4_ file.
     
   * Use `Gifsicle <http://www.lcdf.org/gifsicle>`_ to optimize (make smaller but same quality) the initial animated GIF_ file.
   
.. _convertImage_movie:

convertImage movie
--------------------
``convertImage movie`` converts an MP4_ file into an animated GIF_. Its help screen, when running ``convertImage movie -h``, is,

.. code-block:: console

   usage: convertImage movie [-h] -f filename [-s scale] [-d PARSER_MOVIE_DIRNAME]

   optional arguments:
     -h, --help            show this help message and exit
     -f filename, --filename filename
			   Name of the input video (MP4) file.
     -s scale, --scale scale
			   Multiply the width and height of the input MP4 file into the output GIF. Default is 1.0 (GIF file has same dimensions as input MP4 file).
			   Must be greater than 0.
     -d PARSER_MOVIE_DIRNAME, --dirname PARSER_MOVIE_DIRNAME
			   Optional argument. If defined, the directory into which to store the file.

The required flag is ``-f`` or ``--filename``, to specify the input MP4_ file. There are two optional flags.

* ``-s`` or ``--scale`` resizes the width and height of the input MP4_ file by some factor. Its default is 1.0, and it must be greater than zero.

* ``-d`` or ``--dirname`` specifies the directory into which to store the output animated GIF_. By default, it is the *same* directory as the MP4_ file.

For example, when we run ``convertImage movie`` on :download:`covid19_conus_LATEST.mp4 <images/covid19_conus_LATEST.mp4>` (2.6 MB in size) with a scale factor of 0.5 with this command,

.. code-block:: console

   convertImage movie -f covid19_conus_LATEST.mp4 -s 0.5

Then we get this animated GIF_ in :numref:`covid19_conus_LATEST_gif` (13M in size).

.. _covid19_conus_LATEST_gif:

.. figure:: images/covid19_conus_LATEST.gif
   :width: 100%
   :align: left

   The animated GIF_ of COVID-19 cumulative cases and deaths in the `CONUS <https://en.wikipedia.org/wiki/Contiguous_United_States>`_, as of 11 February 2021: nearly 27.1 million cases, and over 470k deaths.
   
.. _convertImage_aspected:

convertImage aspected
-----------------------
``convertImage aspected`` *symmetrically letterboxes* a non-square input MP4_ file, so that the output MP4_ file is either *square*, or *9/16* aspect ratio (9 width units and 16 height units), or *16/9* aspect ratio (16 width units and 9 height units). This letterboxing color can be either *black* or *white*. If the input MP4_ file's *width is greater than the aspect ratio times height*, the output MP4_ file will have equal width padding on the top and bottom to get the correct aspect ratio. If the input MP4_ file's *width is smaller than the aspect ratio times height*, the output MP4_ file will have equal width padding on the left and right to get the correct aspect ratio.

Its help screen, when running ``convertImage aspected -h``, is,

.. code-block:: console

   usage: convertImage aspected [-h] -f filename -o OUTPUTFILENAME [-a {square,916,169}] [-b]

   optional arguments:
     -h, --help            show this help message and exit
     -f filename, --filename filename
			   Name of the input video (MP4) file.
     -o OUTPUTFILENAME, --output OUTPUTFILENAME
			   Name of the output MP4 video that will be square.
     -a {square,916,169}, --aspect {square,916,169}
			   The aspect ratio to choose for the final video. Can be one of three: "square" is 1:1, "916" is 9/16 (width 9 units, height 16 units), and
			   "169" is 16/9 (width 16 units, height 9 units). Default is "square".
     -b, --black           If chosen, then pad the sides OR the top and bottom with BLACK instead of WHITE. Default is to do WHITE.

``-f`` or ``--filename`` specifies the input MP4_ file. ``-o`` or ``--output`` specifies the output file name.

The aspect ratio is specified with the ``-a`` or ``--aspect`` flag. It can be either ``square`` (equal width and height), ``916`` (final width is 9/16 of height), or ``169`` (final width is 16/9 of height). The default aspect ratio is ``square``.

The letterboxing color is by default ``white``. However, the ``-b`` or ``--black`` flag sets the letterboxing color to be ``black``.

Here are two examples, for the default *square* aspect ratio and *white* letterboxing.

1. For an MP4_ file wider than it is high, this command,

   .. code-block:: console

      convertImage aspected -f covid19_conus_LATEST.mp4 -o covid19_conus_LATEST_square.mp4

   Converts :download:`covid19_conus_LATEST.mp4 <images/covid19_conus_LATEST.mp4>` into :download:`covid19_conus_LATEST_square.mp4 <images/covid19_conus_LATEST_square.mp4>`, which has black letterboxes on its top and bottom.

2. For an MP4_ file higher than it is wide, this command,

   .. code-block:: console

      convertImage aspected -f covid19_california_LATEST.mp4 -o covid19_california_LATEST_square.mp4

   Converts :download:`covid19_california_LATEST.mp4 <images/covid19_california_LATEST.mp4>` into :download:`covid19_california_LATEST_square.mp4 <images/covid19_california_LATEST_square.mp4>`, which has black letterboxes on its left and right.

.. _convertImage_fromimages:

convertImage fromimages
------------------------
``convertImage fromimages`` creates an MP4_ movie file from a collection of image files as frames. Say the files live in a directory ``dirname``, the prefix of the image files is ``PREFIX``, and the suffix of the image files is ``png`` so that the PNG_ images are named, say, ``PREFIX0000.png`` sequentially to ``PREFIX0401.png``. This command will create an MP4_ file, named ``PREFIX.mp4``, in ``dirname``.

Its help screen, when running ``convertImage fromimages -h``, is,

.. code-block:: console

   usage: convertImage fromimages [-h] [-d dirname] -p prefix [-s suffix] [-f fps] [--autocrop]

   optional arguments:
     -h, --help            show this help message and exit
     -d dirname, --dirname dirname
			   The name of the directory to look for a sequence of PNG/JPEG/TIF images. Default is <CURRENT_DIRECTORY>.
     -p prefix, --prefix prefix
			   The prefix of PNG/JPEG/TIF files through which to go.
     -s suffix, --imagesuffix suffix
			   The suffix of the image files. Default is png.
     -f fps, --fps fps     The number of frames per second in the MP4 file. Default is 5.
     --autocrop            If chosen, then perform an autocrop, and then (where necessary) resize each image so that their widths and heights are multiples of 2.

Here are the command line arguments.
			   
* ``-d`` or ``--dirname`` specifies the directory where the image files live. By default it is the current working directory.

* ``-p`` or ``--prefix`` is the prefix to the collection of image files as frames.
  
* ``-s`` or ``--imagesuffix`` is the suffix of the image files. By default it is ``png``, but could be anything that ffmpeg_ can read.

* ``-f`` or ``--fps`` is the frames per second for the output MP4_ file. The default is 5, but it must be :math:`\ge 1`.

* ``--autocrop`` specifies whether you want to automatically crop out white space from the image files.

``<CURRENT_DIRECTORY>`` refers to the current working directory in which ``convertImage fromImages`` has been launched.

.. _myrst2html_desc:

myrst2html
=================
``myrst2html`` acts *almost* like rst2html_. In default mode, it uses ``math.css`` for LaTeX math formulae. However, one can also specify it to use  MathJax_ with the correct CDN_, which in this case is https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML. I borrow shamelessly from `this GitHub gist`_ with some slight modifications.

Its help screen, when running ``myrst2html -h``, is,

.. code-block:: console

   usage: myrst2html [-h] -i INPUTFILE [-M]

   options:
     -h, --help            show this help message and exit
     -i INPUTFILE, --input INPUTFILE
			   Name of the input RST file. Required argument.
     -M, --mathjax         If chosen, then use the MathJAX JS CDN to display LaTeX formulae. Default is turned off.

This generates the HTML file, ``filename.html``, from the RST markup file, ``filename.rst``, but now with MathJax_ if you run with ``-M`` or ``--mathjax``.

simple_email_config
=====================
I gave birth to a new CLI, ``simple_email_config``, to *simplify* sending (use much-much-much-fewer typing characters and smaller chances of fat-fingeritis) technical emails with :ref:`simple_email`. Here one can set default identity for sending email; set the default SMTP_ server; and add or remove email **aliases**. Likewise, one can do the following: show the default identity for sending email; show the default SMTP_ server and port; and show the list of email **aliases** with and without the full email address (showing just the list of ordered email **aliases**).

An email alias is a lower-case non-spaced string that identifies an email address or an RFC 5322 full email address. For example, I have identified the **alias** ``tanimg`` with the full email address, ``Tanim Islam <tanim.islam@gmail.com>``.

The full help command demonstrating all the commands by running, ``simple_email_config -h``.

.. code-block:: console

   positional arguments:
     {show_aliases,show_me,show_smtp,add_alias,remove_aliases,set_me,set_smtp}
			   Choose one of these six options (stuff before the first colon): show_aliases: show the list of email aliases I have. show_me: show whether I have a default sender (me). If so, then show sender's default email identity.
			   show_smtp: show the settings for the SMTP server I have identified. add_alias: add an email alias. remove_aliases: remove email aliases. set_me: set up the default sender's identity. set_smtp: set up the default SMTP server.
       show_aliases        If chosen, show the list of email aliases I have.
       show_me             show whether I have a default sender (me). If so, then show sender's default email identity.
       show_smtp           show the settings for the SMTP server I have identified.
       add_alias           add an email alias.
       remove_aliases      remove email aliases.
       set_me              set up the default sender's identity.
       set_smtp            set up the default SMTP server.

   optional arguments:
     -h, --help            show this help message and exit
     --info                If chosen, then print out INFO level logging statements.

As of ``4 MARCH 2023``, **7 choices**. Subsequent functionalities are in separate subsections under :ref:`simple_email_config`.

.. _simple_email_config_set_show_me:

simple_email_config show_me and set_me
------------------------------------------
You *set* the **default** sender information by running ``simple_email_config set_me``. Its help screen is ``simple_email_config set_me -h``,

.. code-block:: console

   usage: simple_email_config set_me [-h] -e PARSER_SETME_EMAIL

   optional arguments:
     -h, --help            show this help message and exit
     -e PARSER_SETME_EMAIL, --email PARSER_SETME_EMAIL
			   The RFC 5322 email format of the sender.

So for example, running ``simple_email_config set_me -e "Tanim Islam <tanim.islam@gmail.com>"`` sets the default RFC 5322 email to ``Tanim Islam <tanim.islam@gmail.com>``.

You *show* the **default** sender information by running ``simple_email_config show_me``. In the example below,

.. code-block:: console

   $ simple_email_config show_me
   DEFAULT EMAIL ADDRESS: Tanim Islam <tanim.islam@gmail.com>.

And that's it!

.. _simple_email_config_set_show_smtp:

simple_email_config set_smtp and show_smtp
--------------------------------------------------
You *set* the **default** SMTP_ server information by running ``simple_email_config set_smtp``. Its help screen, ``simple_email_config set_smtp -h`` is,

.. code-block:: console

   usage: simple_email_config set_smtp [-h] -S SMTP_SERVER -p SMTP_PORT

   optional arguments:
     -h, --help            show this help message and exit
     -S SMTP_SERVER, --server SMTP_SERVER
			   The name of the default SMTP server.
     -p SMTP_PORT, --port SMTP_PORT
			   The port number of the default SMTP server.

I go through each command line argument like so.

#. ``-S`` or ``--server`` specifies the *required* address or name of the default SMTP_ server. A common default choice is ``localhost``.

#. ``-p`` or ``-port`` specifies the *required* port number of the default SMTP_ server. A common default choice is 25.

You can then *show* the **default** SMTP_ server information by running ``simple_email_config show_smtp``. In the example below,

.. code-block:: console

   $ simple_email_config show_smtp
   DEFAULT SMTP SERVER: localhost.
   DEFAULT SMTP PORT: 25.

And that's it!

.. _simple_email_config_add_show_remove_alias:

simple_email_config show_aliases, add_alias, remove_aliases
--------------------------------------------------------------------
An enhancement to :ref:`simple_email` is that one can *also* specify ``TO/CC/BCC`` recipients with *aliases* in addition to their email addresses or full RFC 5322 email addresses. I use *anonymized* examples from aliases that I (`Tanim Islam <https://tanimislam.gitlab.io/blog/i-exist.html#biography-section>`_) have set up as of ``5 MARCH 2023``.

#. You can **show email aliases** by running ``simple_email_config show_aliases``. Its help screen is ``simple_email_config add_aliases -h``,

   .. code-block:: console

      usage: simple_email_config show_aliases [-h] [-H]

      optional arguments:
	-h, --help         show this help message and exit
	-H, --hidealiases  If chosen, then HIDE the email addresses when showing the list of aliases. Default is to SHOW.

   The ``-H`` or ``--hidealiases`` flag is useful to demonstrate the list of **email aaliases** that you have, because it *hides* the email or RFC 5322 email address for each **alias**. For example, for me (`Tanim Islam <https://tanimislam.gitlab.io/blog/i-exist.html#biography-section>`_

   .. code-block:: console

      $ simple_email_config show_aliases -H
      FOUND 14 EMAIL ALIASES

      ALIAS
      ------------
      bcohan
      chrismay
      cschroder
      drflask
      dstrozzi
      dstrozzig
      marinak
      mehulp
      tanimg
      tanimv
      tanimw
      tbailey
      tipton
      woodyh_sacpy
      
   This displays the **email aliases** in alphabetical order.

#. You can **add an email alias** by running ``simple_email_config add_alias``. Its help screen is ``simple_email_config add_alias -h``,

   .. code-block:: console

      usage: simple_email_config add_alias [-h] -a ALIAS -e EMAIL

      optional arguments:
	-h, --help            show this help message and exit
	-a ALIAS, --alias ALIAS
			      Name of the alias to use for an emailer.
	-e EMAIL, --email EMAIL
			      The RFC 5322 email format of the emailer.

   I go through each command line argument like so.

   #. ``-a`` or ``--alias`` specifies the *required* **email alias**, which is a no-spaces string. **Any string that has uppercase characters will be lowercased**.

   #. ``-e`` or ``--email`` specifies the *required* email address or RFC 5322 email address for that **email alias**.

   For example, let's look at the anonymized **email aliases** *before* adding the **alias** ``tanimg``.

   .. code-block:: console

      FOUND 13 EMAIL ALIASES

      ALIAS
      ------------
      bcohan
      chrismay
      cschroder
      drflask
      dstrozzi
      dstrozzig
      marinak
      mehulp
      tanimv
      tanimw
      tbailey
      tipton
      woodyh_sacpy
   
   Next, let us add an **email alias** ``tanimg`` for ``Tanim Islam <tanim.islam@gmail.com>`` with this command,

   .. code-block:: console

      $ simple_email_config add_alias -a tanimg -e "Tanim Islam <tanim.islam@gmail.com>"
      SUCCESSFULLY ADDED ALIAS = tanimg, EMAIL = Tanim Islam <tanim.islam@gmail.com>.

   Finally, look at the anonymized **email aliases** *after* adding this **alias**.

   .. code-block:: console
      :linenos:
      :emphasize-lines: 13
   
      FOUND 14 EMAIL ALIASES

      ALIAS
      ------------
      bcohan
      chrismay
      cschroder
      drflask
      dstrozzi
      dstrozzig
      marinak
      mehulp
      tanimg
      tanimv
      tanimw
      tbailey
      tipton
      woodyh_sacpy

   Notice ``tanimg`` in line 13.

#. You can **remove email aliases** by running ``simple_email_config remove_aliases``. Its help screen is ``simple_email_config remove_aliases -h``,

   .. code-block:: console

      usage: simple_email_config remove_aliases [-h] [-r [ALIAS ...]]

      optional arguments:
	-h, --help            show this help message and exit
	-r [ALIAS ...], --removealias [ALIAS ...]
			      The set of aliases to REMOVE.

   You can specify *multiple* **email aliases** to remove. Example with removing ``tanimg`` follows.

   First, look at the set of anonymized **email aliases** that *also* contain and emphasize ``tanimg``.
   
   .. code-block:: console
      :linenos:
      :emphasize-lines: 13
   
      FOUND 14 EMAIL ALIASES

      ALIAS
      ------------
      bcohan
      chrismay
      cschroder
      drflask
      dstrozzi
      dstrozzig
      marinak
      mehulp
      tanimg
      tanimv
      tanimw
      tbailey
      tipton
      woodyh_sacpy

   Run this command to remove the **email alias** ``tanimg``.

   .. code-block:: console

      $ simple_email_config remove_aliases -r tanimg
      set of aliases to remove: ['tanimg'].

   Finally, check that ``tanimg`` is no longer of the **email aliases**.

   
   .. code-block:: console
      :linenos:
   
      FOUND 13 EMAIL ALIASES

      ALIAS
      ------------
      bcohan
      chrismay
      cschroder
      drflask
      dstrozzi
      dstrozzig
      marinak
      mehulp
      tanimv
      tanimw
      tbailey
      tipton
      woodyh_sacpy

   And that's it.

simple_email
===============
``simple_email`` is the *simplest* SMTP_ based email sender I could make! One specifies the reStructuredText_ file; (optional) attachments; sender; ``TO`` recipients; (optionally) ``CC`` and ``BCC`` recipients; and (optional) details of the SMTP_ server. Its help screen is ``simple_email -h``,

.. code-block:: console

   usage: simple_email [-h] -f EMAILFILE [-s SUBJECT] [-F SENDER] -T [TO ...] [-C [CC ...]] [-B [BCC ...]] [-A [ATTACH ...]] [-p SMTPPORT] [-S SMTPSERVER] [-I]

   optional arguments:
     -h, --help            show this help message and exit
     -f EMAILFILE, --emailfile EMAILFILE
			   Name of the restructuredtext email file to convert into HTML, THEN email out.
     -s SUBJECT, --subject SUBJECT
			   Email subject. Default is "test subject".
     -F SENDER, --from SENDER
			   Email and/or name of the sender. Use RFC 5322 email format. Default is "Tanim Islam <tanim.islam@gmail.com>".
     -T [TO ...], --to [TO ...]
			   List of email and/or names of the recipients. Use RFC 5322 email format OR email alias.
     -C [CC ...], --cc [CC ...]
			   List of CC email and/or names. Use RFC 5322 email format OR email alias.
     -B [BCC ...], --bcc [BCC ...]
			   List of BCC email and/or names. Use RFC 5322 email format OR email alias.
     -A [ATTACH ...], --attach [ATTACH ...]
			   List of files to attach to this email.
     -p SMTPPORT, --smtpport SMTPPORT
			   The port number for the SMTP server to send the SMTP email. Default is 25.
     -S SMTPSERVER, --smtpserver SMTPSERVER
			   The name of the SMTP server to send the SMTP email. Default is 'localhost'.
     -I, --info            If chosen, then do INFO logging.

I go through each command line argument like so. ``-I`` or ``--info`` turns on ``INFO`` logging, which is right now *extremely useful* to figure out what happened to your email if something went wrong!

#. ``-f`` or ``emailfiles`` specifies the reStructuredText_ file, which has the same structure as I describe in the :ref:`myrst2html description <myrst2html_desc>`.

#. Email stuff consists of the following:

   * ``-s`` or ``--subject`` specifies the non-default email subject. Default is ``test subject``.

   * ``-F`` or ``-from`` specifies the sender. This is in the format of email address only, such as ``tanim.islam@gmail.com``, or in the standard email-with-name format, such as ``Tanim Islam <tanim.islam@gmail.com>``. If not specified, this uses the *default* sender address defined or shown in :numref:`simple_email_config_set_show_me`.

   * ``-T`` or ``--to`` specifies the list of recipients (can be multiple ones). This is in the format of email address only, in the standard email-with-name format (RFC 5322), or as an email alias.
     
   * ``-C`` or ``-cc`` *optionally* specifies the list of `CC recipients`_ (can be multiple ones). This is in the format of email address only, or in the standard email-with-name format (RFC 5322), or as an email alias.

   * ``-B`` or ``--bcc`` *optionally* specifies the list of `BCC recipients`_ (can be multiple ones). This is in the format of email address only, or in the standard email-with-name format (RFC 5322), or as an email alias.

     .. note::

	``simple_email`` implements an *implicit* BCC add of the sender email address, so that the sender (like  ``Tanim Islam <tanim.islam@gmail.com>``) also receives an email showing that they have sent this email to the TO/CC/BCC recipients.

   * ``-A`` or ``--attach`` *optionally* specifies the list of files to attach to this email.

#. SMTP_ server stuff consists of the following:

   * ``-p`` or ``--smtpport`` specifies the port to use for SMTP_ email sending. Default is whatever is the default SMTP_ port set or shown in :numref:`simple_email_config_set_show_smtp`.

   * ``-S`` or ``--smtpserver`` specifies the name of the SMTP_ server. Default is Default is whatever is the default SMTP_ server set or shown in :numref:`simple_email_config_set_show_smtp`.

To help myself and others, I have the following elements needed to send a demonstration email.

* The email file, :download:`demo_email.rst <input/demo_email.rst>`, whose source I have included below,

  .. literalinclude:: input/demo_email.rst
     :language: rst
     :linenos:

* The three images files: :download:`covid19_7day_conus_LATEST_CLIPPED.gif <input/covid19_7day_conus_LATEST_CLIPPED.gif>`, :download:`iwanttobelieve_uncropped_cropped.png <input/iwanttobelieve_uncropped_cropped.png>`, and :download:`turn_cartoon.png <input/turn_cartoon.png>`.

* You will also need an SMTP_ server with valid SMTP_ port.

Example of ``simple_email`` functionality is mocked up below. I assume your SMTP_ server is ``localhost`` and it operates off port 25.

.. code-block:: console

   simple_email -f demo_email.rst -F <email_sender> -T <email_recip_1> <email_recip_2> \
     -C <cc_recip_1> <email_recip_2> -B <bcc_recip_1> <bcc_recip_2> \
     -A demo_email.rst

If everything email-wise *and* SMTP_ wise goes right, then your ``TO`` and ``CC`` and ``BCC`` recipients should receive the email with attachment.
     
.. _rst2html: https://manpages.debian.org/testing/docutils-common/rst2html.1.en.html
.. _CDN: https://en.wikipedia.org/wiki/Content_delivery_network
.. _`this GitHub gist`: https://gist.github.com/Matherunner/c0397ae11cc72f2f35ae
.. _`git bisect`: https://git-scm.com/docs/git-bisect
.. _GIF: https://en.wikipedia.org/wiki/GIF
.. _YouTube: https://www.youtube.com
.. _FFmpeg: https://ffmpeg.org
.. _movie_2_gif: http://blog.pkh.me/p/21-high-quality-gif-with-ffmpeg.html
.. _pdftocairo: http://manpages.ubuntu.com/manpages/trusty/man1/pdftocairo.1.html
.. _cairosvg: http://manpages.ubuntu.com/manpages/focal/en/man1/cairosvg.1.html
.. _MP4: https://en.wikipedia.org/wiki/MPEG-4_Part_14
.. _`Medium article`: https://medium.com/@Peter_UXer/small-sized-and-beautiful-gifs-with-ffmpeg-25c5082ed733

.. _`CC recipients`: https://en.wikipedia.org/wiki/Carbon_copy#Email
.. _`BCC recipients`: https://en.wikipedia.org/wiki/Blind_carbon_copy#cite_note-1

.. _`Tanim Islam`: https://tanimislam.gitlab.io/blog/i-exist.html#biography-section
