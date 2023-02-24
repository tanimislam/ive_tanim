.. include:: urls.rst

================================================
Initialization API
================================================
This document describes the |ivetanim| initialization API, which initializes the configuration settings for the custom logger and initializes the |ivetanim| configuration file, which is JSON_ file that lives in ``~/.config/ive_tanim/config.json``.

The logger has a custom format: ``'%(levelname)s %(module)s.%(funcName)s (%(lineno)d): %(message)s'``. See the `logging cookbook`_ for more information on what this format means.

Some of the :ref:`Core Functionality` command line tools have an extra argument flag, ``--level``, that specifies whether to print out logging output and the following debug levels: ``DEBUG``, ``INFO``, or ``ERROR``.

.. automodule:: ive_tanim
   :members:

.. _`logging cookbook`: https://docs.python.org/3/howto/logging-cookbook.html
