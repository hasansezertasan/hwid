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

Library:

- Cross-platform (Windows, Linux, macOS) with native OS detection
- No external runtime dependencies
- Usable as a module or a CLI

Engineering:

- **Type Safety**: Full type hints checked by mypy, basedpyright, ty, pyrefly,
  and zuban
- **Code Quality**: Comprehensive linting and formatting with ruff, plus
  architecture-contract enforcement with import-linter
- **Testing**: pytest with coverage reporting and parallel execution
- **Documentation**: Sphinx documentation with the Shibuya theme, GitHub Pages
  deployment, and live per-PR documentation previews
- **CI/CD**: Automated testing, building, and publishing across multiple
  platforms
- **Security**: CodeQL, OpenSSF Scorecard, dependency review, secret scanning
  (gitleaks), dependency auditing (pip-audit), GitHub Actions static analysis
  (zizmor — a blocking prek/CI gate plus a Security-tab dashboard, over hardened
  least-privilege workflows), and a CycloneDX SBOM attached to every release
- **Managed** ``.gitignore``: kept in sync with the upstream
  `github/gitignore <https://github.com/github/gitignore>`_ templates by
  `cobo <https://github.com/hasansezertasan/cobo>`_, with a weekly drift check
- **Modern Python**: uv for dependency management, hatch for building

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
