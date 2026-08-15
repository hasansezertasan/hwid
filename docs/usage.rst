Usage
=====

As a library
------------

To use ``hwid`` in a project:

.. code-block:: python

   import hwid

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
