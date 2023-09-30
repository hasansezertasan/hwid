<h1 align="center">
    <strong>HWID</strong>
</h1>
<p align="center">
    <em>Extract the `hwid` on Windows, Linux, Mac. Cross-platform using Python, native OS detection.</em>
</p>
<p align="center">
    <a href="https://github.com/hasansezertasan/hwid" target="_blank">
        <img src="https://img.shields.io/github/last-commit/hasansezertasan/hwid" alt="Latest Commit">
    </a>
        <img src="https://img.shields.io/github/workflow/status/hasansezertasan/hwid/Test">
        <img src="https://img.shields.io/codecov/c/github/hasansezertasan/hwid">
    <br />
    <a href="https://pypi.org/project/hwid" target="_blank">
        <img src="https://img.shields.io/pypi/v/hwid" alt="Package version">
    </a>
    <a href="https://pypi.org/project/hwid" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/hwid">
    </a>
    <img src="https://img.shields.io/github/license/hasansezertasan/hwid">
</p>

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

## Why?

I have created a bunch of desktop applications for Windows to sell. I needed a way to license my applications. I decided to use the hwid of the computer to license my applications. I needed a way to get the hwid of the computer, so I created this module. It has only one purpose: getting the hwid of the computer. It is cross-platform and does not require any external dependencies.

I do not recommend using this module for licensing purposes by itself. You can use it as a part of your licensing system.

If you are using server-client architecture, you can send the encrypted hwid to the server and check if it is valid. It's easy to intercept the request to the server. You can check [mitmproxy](https://mitmproxy.org/) for that.

If you are using a local licensing system, you can encrypt the hwid and store it in a file. Then you can check if the encrypted hwid is valid. You can use [pyarmor](https://github.com/dashingsoft/pyarmor) to obfuscate your code. It will make it harder to reverse engineer your code.

## Disclaimer

This module is not intended to be used for malicious purposes. The author is not responsible for any damage caused by this module. Use at your own risk.
