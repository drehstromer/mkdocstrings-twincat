# mkdocstrings-twincat

[![documentation](https://img.shields.io/badge/docs-mkdocs-708FCC.svg?style=flat)](https://drehstromer.github.io/mkdocstrings-twincat/)
[![pypi version](https://img.shields.io/pypi/v/mkdocstrings-twincat.svg)](https://pypi.org/project/mkdocstrings-twincat/)

A Twincat handler for mkdocstrings.

## Installation

```bash
pip install mkdocstrings-twincat
```

This handler is using pytwincatparser to parse Twincatfiles. Currently supported are:

- .plcproj
- .tcio
- .tcpou
- .tcgvl
- .tcdut

The handler can load recursivly all objects. You just have to add the .plcproj file, and it generates the documentation for all Function Blocks etc.


## Demo
At the project page you can find a demo of this handler. It parses the source code of the famous [TcUnit](https://github.com/tcunit/TcUnit) TwinCAT unit testing framework and displays it. The documentation is not optimal, but this is because the tags are not used by tcunit.


## Used packages
- mkdocstrings
- mkdocstrings-python (heavily as inspiration. really great code!)
- pytwincatparser


## Be aware
I am a plc programmer. I usually dont code in python. if you find bugs, flaws, mistakes or if you have an idea how to improve or make a new feature, do not hesitate to contact me!
