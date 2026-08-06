.. A 7-character "=" underline (the length of "Modules") is treated as a
   merge-conflict separator by ``git diff --check`` / ``check-merge-conflict``;
   keep this underline longer than the title to avoid the false positive.

Modules
=========

An overview of the modules that make up ``hwid``.
The API reference below is generated automatically from the source docstrings.

Public API (``hwid.core``)
--------------------------

The package exposes :func:`hwid.get_hwid` at the top level.

.. automodule:: hwid.core

Exceptions (``hwid.exceptions``)
--------------------------------

.. automodule:: hwid.exceptions

Logging (``hwid.logger``)
-------------------------

.. automodule:: hwid.logger
