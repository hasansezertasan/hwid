Usage
=====

As a library
------------

Look up the installed distribution version:

.. literalinclude:: examples/version_lookup.py
   :language: python
   :caption: examples/version_lookup.py

For short interactive snippets embedded in prose, the ``docs-doctest`` task
executes ``>>>`` blocks too:

.. doctest::

   >>> from hwid.__metadata__ import PROJECT_NAME
   >>> PROJECT_NAME
   'hwid'

   print(hwid.get_hwid())

As a command-line tool
----------------------

Run it without installing, straight from PyPI:

.. code-block:: sh

   uvx hwid

Or, once installed, invoke the console script. The bare command prints the
machine's hardware ID:

.. code-block:: sh

   hwid

The ``version`` and ``info`` subcommands report the package version and
environment:

.. code-block:: sh

   hwid version
   hwid info
