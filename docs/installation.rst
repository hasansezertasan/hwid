Installation
============

``hwid`` is a library. Add it to your project as a dependency.

Stable release
--------------

To add ``hwid`` to your project, run this command in your
terminal:

.. code-block:: sh

   uv add hwid

Or if you prefer to use ``pip``:

.. code-block:: sh

   pip install hwid

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
   uv pip install .
