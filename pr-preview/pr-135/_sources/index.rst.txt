Welcome to hwid's documentation!
================================

Extract the ``hwid`` on Windows, Linux, Mac. Cross-platform using Python,
native OS detection.

.. toctree::
   :maxdepth: 2
   :caption: Contents

   installation
   usage
   modules

Motivation
----------

TL;DR I don't want to copy and paste it again...

I have created a bunch of desktop applications for Windows. I needed a way to
license my applications for my users to use without distributing to other
people. I decided to use the hwid of the computer to license my applications,
so I created this module. It has only one purpose: getting the hwid of the
computer. It is cross-platform and does not require any external dependencies.

Features
--------

- Cross-platform
- No external dependencies
- CLI
- Module

Warning
-------

I do not recommend using this module for licensing purposes all alone. You can
use it as a part of your licensing system.

If you are using a server-client architecture, you can send the encrypted hwid
to the server and check if it is valid. But keep in mind, it's easy to intercept
the HTTP requests with `mitmproxy <https://mitmproxy.org/>`_ or other tools.

If you are using a local licensing system, you can encrypt the hwid and store it
in a file, then check if the encrypted hwid is valid. You can use
`pyarmor <https://github.com/dashingsoft/pyarmor>`_ to obfuscate your code to
make it harder to reverse engineer.

Disclaimer
----------

This module is not intended to be used for malicious purposes. The author is not
responsible for any damage caused by this module. Use at your own risk.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
