.. include:: urls.rst

================================================
Core APIs
================================================

This document describes the |ivtanim| core API, which provides the low-level back-end for the CLI front ends described in :ref:`Core Functionality`. These modules live under ``iv_tanim.core``.

I have redesigned the Python logging functionality in the following way,

* custom format of the logging output, formatted as ``'%(levelname)s %(module)s.%(funcName)s (%(lineno)d): %(message)s'``. See the `logging cookbook`_ for more information on what this format means.

* Some of the :ref:`Core Functionality` command line tools have an extra argument flag, ``--level``, that specifies whether to print out logging output and the following debug levels: ``DEBUG``, ``INFO``, or ``ERROR``.
		
autocrop_image module
------------------------------------
This module provides low-level functionality that implements automatic cropping of lossy (PNG_, JPEG_, TIFF_) and PDF_ images.

This PDF_ autocropping functionality is copied over from `this repo`_. That repository is based off `pdfcrop.pl`_ to calculate the BoundingBox_. This functionality requires a working ghostscript_ (using the ``gs`` executable) to calculate the bounding box, and the PyPDF2_ module to read and manipulate PDF_ files.

.. image:: https://upload.wikimedia.org/wikipedia/commons/2/2a/PDF_BOX_01.svg
   :width: 100%

Three methods -- :py:meth:`get_boundingbox <iv_tanim.core.autocrop_image.get_boundingbox>`, :py:meth:`crop_pdf <iv_tanim.core.autocrop_image.crop_pdf>`, and  :py:meth:`crop_pdf_singlepage <iv_tanim.core.autocrop_image.crop_pdf_singlepage>` -- are the higher level hooks to the PDF_ autocropping functionality.

.. automodule:: iv_tanim.core.autocrop_image
   :members:

convert_image module
-----------------------------------
This module provides the low-level functionality that uses utility functions to create MP4_ movies from a sequence of images, creates animated GIF_ files, and creates square movies (useful for upload to Instagram_).

.. automodule:: iv_tanim.core.convert_image
   :members:

rst2html module
----------------------------------
This module provides low-level functionality that converts reStructuredText_ into HTML, with the option of using MathJax_ to render LaTeX formulae in HTML. This also consists of methods to create a properly CID-converted :py:class:`MIMEMultiPart <email.mime.multipart.MIMEMultiPart>` low-level message object for other, external modules that convert RST documents into HTML emails that most email servers will work on.

.. automodule:: iv_tanim.core.rst2html
   :members:

.. _CloudConvert: https://cloudconvert.com
.. _GIF: https://en.wikipedia.org/wiki/GIF
.. _PyPI: https://pypi.org
.. _Ubuntu: https://ubuntu.com
.. _MP4: https://en.wikipedia.org/wiki/MPEG-4_Part_14
.. _RealMedia: https://en.wikipedia.org/wiki/RealMedia
.. _`logging cookbook`: https://docs.python.org/3/howto/logging-cookbook.html
.. _QtSVG: https://doc.qt.io/qt-5/qtsvg-index.html
.. _`this repo`: https://gist.github.com/jpscaletti/7321281
.. _BoundingBox: https://upload.wikimedia.org/wikipedia/commons/2/2a/PDF_BOX_01.svg
.. _ghostscript: https://www.ghostscript.com
.. _pdfcrop.pl: https://github.com/ho-tex/pdfcrop
