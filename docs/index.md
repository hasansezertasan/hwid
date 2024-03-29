# HWID

[![Coverage](https://img.shields.io/codecov/c/github/hasansezertasan/hwid)](https://codecov.io/gh/hasansezertasan/hwid)
[![PyPI - Version](https://img.shields.io/pypi/v/hwid.svg)](https://pypi.org/project/hwid)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hwid.svg)](https://pypi.org/project/hwid)
[![License](https://img.shields.io/github/license/hasansezertasan/hwid.svg)](https://github.com/hasansezertasan/hwid/blob/main/LICENSE)
[![Latest Commit](https://img.shields.io/github/last-commit/hasansezertasan/hwid)](https://github.com/hasansezertasan/hwid)

[![Downloads](https://pepy.tech/badge/hwid)](https://pepy.tech/project/hwid)
[![Downloads/Month](https://pepy.tech/badge/hwid/month)](https://pepy.tech/project/hwid)
[![Downloads/Week](https://pepy.tech/badge/hwid/week)](https://pepy.tech/project/hwid)

Extract the `hwid` on Windows, Linux, Mac. Cross-platform using Python, native OS detection.

---

## Table of Contents

- [HWID](#hwid)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Motivation](#motivation)
  - [Features](#features)
  - [Warning](#warning)
  - [Author](#author)
  - [Disclaimer](#disclaimer)
  - [License](#license)

## Installation

``` bash
pip install hwid
```

## Usage

Module:

```python
import hwid
print(hwid.get_hwid())
# 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
```

CLI:

```bash
hwid
XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
```

## Motivation

TL;DR I don't want to copy and paste it again...

I have created a bunch of desktop applications for Windows. I needed a way to license my applications for my users to use it without distributing to other people. I decided to use the hwid of the computer to license my applications. I needed a way to get the hwid of the computer, so I created this module. It has only one purpose: getting the hwid of the computer. It is cross-platform and does not require any external dependencies.

## Features

- Cross-platform
- No external dependencies
- CLI
- Module

## Warning

I do not recommend using this module for licensing purposes all alone. You can use it as a part of your licensing system.

If you are using server-client architecture, you can send the encrypted hwid to the server and check if it is valid. But keep in mind, It's easy to intercept the http requests with [mitmproxy] or other tools.

If you are using a local licensing system, you can encrypt the hwid and store it in a file. Then you can check if the encrypted hwid is valid. You can use [pyarmor] to obfuscate your code. It will make it harder to reverse engineer your code. Here is a [NeuralNine Tutorial][neuralnine-tutorial] using [Oxyry][oxyry]

## Author

- [hasansezertasan](https://www.github.com/hasansezertasan)

## Disclaimer

This module is not intended to be used for malicious purposes. The author is not responsible for any damage caused by this module. Use at your own risk.

## License

`hwid` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

<!-- Links -->
[mitmproxy]: https://mitmproxy.org/
[pyarmor]:https://github.com/dashingsoft/pyarmor
[neuralnine-tutorial]: https://www.youtube.com/watch?v=k4bLhDolLf0
[oxyry]: https://pyob.oxyry.com/
