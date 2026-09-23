Installation
============

``hwid`` is both an importable library and a command-line tool. To use it as a
dependency, add it to your project (``uv add hwid`` or ``pip install hwid``) and
call :func:`hwid.get_hwid` from Python. To use the ``hwid`` command directly,
install it as a standalone tool as shown below.

Stable release
--------------

Install ``hwid`` into an isolated environment with your
preferred tool installer:

.. code-block:: sh

   uv tool install hwid

.. code-block:: sh

   pipx install hwid

Or run it without installing:

.. code-block:: sh

   uvx hwid

Homebrew (macOS/Linux):

.. code-block:: sh

    brew install hasansezertasan/tap/hwid

Scoop (Windows):

.. code-block:: sh

    scoop bucket add hasansezertasan https://github.com/hasansezertasan/scoop-bucket
    scoop install hasansezertasan/hwid

From source
-----------

The source files for ``hwid`` can be downloaded from the
`GitHub repo <https://github.com/hasansezertasan/hwid>`_.

You can either clone the public repository:

.. code-block:: sh

   git clone https://github.com/hasansezertasan/hwid.git

Or download the
`tarball <https://github.com/hasansezertasan/hwid/tarball/main>`_:

.. code-block:: sh

   mkdir hwid
   curl -fL https://github.com/hasansezertasan/hwid/tarball/main | tar -xz --strip-components=1 -C hwid

Once you have a copy of the source, you can install it with:

.. code-block:: sh

   cd hwid
   uv tool install .
