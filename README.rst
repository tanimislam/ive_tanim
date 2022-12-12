###################################################################
IVE_TANIM - Image-Video-Email Functionality from Tanim, for Tanim
###################################################################
NPRSTUFF_ is a repository that started off with tools that downloaded public radio programs like `NPR Fresh Air`_, `Wait Wait...Don't Tell
Me <waitwait_>`_, and `This American Life`_. I then expanded it to become a grab bag of altogether different types of functionalities. Dependency managament was *stupidly onerous*.

This repository, |ivetanim| (pronounced ``ivy``), carves out the image-video-email low-level functionality and command line executables into their own repository. This functionality continues and deprecated-land lives for now in NPRSTUFF_, but in the relatively immediate big-rock-candy-mountain future I will move the older "relying on NPRSTUFF_" dependencies into |ivetanim|. Single but obvious big benefit:

* |ivetanim| contains a few, easy-to-meet Python module dependencies.

The comprehensive documentation lives in HTML created with `Sphinx <https://www.sphinx-doc.org/en/master/>`_, and now in the `IVE_TANIM Sphinx Page <ive_tanim_doc_>`_ for this project. To generate the documentation, go to the ``docsrc`` subdirectory. In that directory, run ``make html``. Load ``docsrc/build/html/index.html`` into a browser to see the documentation.

There's also a demonstration presentation! I am/have (depending on whether you're from the past/future) made a presentation to the `Sacramento Python Meetup <sacpy_>`_ on Thursday, ``3 NOVEMBER 2022``.

* Link to the `powerpoint presentation <https://tanimislam.gitlab.io/blog/pages/presentation_stuff/IV_TANIM_MULTIMEDIA.pptx>`_.

* Link to the `keynote presentation <https://tanimislam.gitlab.io/blog/pages/presentation_stuff/IV_TANIM_MULTIMEDIA.key>`_.

* Link to the `YouTube presentation <https://youtu.be/FwbIzATyboE>`_.

* Link to the `full video  <https://drive.google.com/file/d/11g-mWTpWeFvNrb32l-n1oCIlUROr4z8Y/view?usp=sharing>`_.

Installation Instructions
^^^^^^^^^^^^^^^^^^^^^^^^^^
Installing this Python module is easy.

* If you want to get it from Github_, then run this command,

  .. code-block:: console

     python3 -m pip install --user git+https://github.com/tanimislam/ive_tanim#egginfo=ive_tanim

* If you want to have more control, follow these several steps.

  .. code-block:: console

     git clone https://github.com/tanimislam/ive_tanim
     cd ive_tanim
     python3 -m pip install --user -e .

Both installation workflows install |ivetanim| into your user Python folder (``~/.local`` by default on Linux and Mac OS X systems). Its executables are installed into ``~/.local/bin`` by default on Linux or Mac OS X systems.

.. _`NPR Fresh Air`: https://freshair.npr.org
.. _waitwait: https://waitwait.npr.org
.. _`This American Life`: https://www.thisamericanlife.org
.. _LibAV: https://libav.org
.. _FFMPEG: https://ffmpeg.org
.. _HandBrakeCLI: https://handbrake.fr
.. _`older NPR API`: https://www.npr.org/api/index
.. _`NPR One API`: https://dev.npr.org/api
.. _ive_tanim_doc: https://tanimislam.github.io/ive_tanim
.. _M4A: https://en.wikipedia.org/wiki/MPEG-4_Part_14
.. _MP3: https://en.wikipedia.org/wiki/MP3
.. _PNG: https://en.wikipedia.org/wiki/Portable_Network_Graphics
.. _JPEG: https://en.wikipedia.org/wiki/JPEG
.. _TIFF: https://en.wikipedia.org/wiki/TIFF
.. _PDF: https://en.wikipedia.org/wiki/PDF
.. _MOV: https://en.wikipedia.org/wiki/QuickTime_File_Format
.. _OGG: https://en.wikipedia.org/wiki/Vorbis
.. _FLAC: https://en.wikipedia.org/wiki/FLAC
.. _SVG: https://en.wikipedia.org/wiki/Scalable_Vector_Graphics
.. _Github: https://github.com
.. _NPRSTUFF: https://github.com/tanimislam/nprstuff
.. _sacpy: http://sacpy.org


.. |ivetanim| replace:: ``IVE_TANIM``

..
.. these are magazine URLS
..

.. _`Lightspeed Magazine`: http://www.lightspeedmagazine.com
.. _Medium: https://medium.com/>
.. _`The New Yorker`: https://www.newyorker.com
.. _`The New York Times`: https://www.nytimes.com
.. _`Virginia Quarterly Review`: https://www.vqronline.org
