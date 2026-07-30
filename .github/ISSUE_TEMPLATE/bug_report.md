---
name: Bug report
about: Report a bug in `hwid`
title: 'Bug: '
labels: bug
assignees: 'hasansezertasan'
---
## Bug Description

<!-- A clear and concise description of what the bug is. -->

## How to Reproduce

<!--
The exact code or command you ran. For example, as a library:

```python
import hwid

print(hwid.get_hwid())
```

Or as a CLI:

```sh
hwid
# or
python -m hwid
```
-->

## Expected Behavior

<!-- What you expected to happen (e.g. a valid hardware ID was returned). -->

## Actual Behavior

<!--
What actually happened. Include the full traceback if an exception was raised:

```text
Traceback (most recent call last):
  ...
```

`hwid` reads the hardware ID from a native OS tool (PowerShell on Windows,
`system_profiler` on macOS, `dmidecode` on Linux). If the returned value looks
wrong, or an `UnsupportedOSError` / `InvalidHWIDError` was raised, paste the raw
output of the underlying command if you can.
-->

## Environment

<!-- Please complete the following: -->

- hwid version: <!-- e.g. 0.3.0 -->
- Python version: <!-- e.g. 3.12 -->
- OS and version: <!-- e.g. Windows 11, macOS 14, Ubuntu 24.04 -->
- Installation method: <!-- e.g. pip, uv, uvx, from source -->

## Additional Context

<!-- Add any other context about the problem here. -->
