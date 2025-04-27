# mkdocstrings-twincat

[![documentation](https://img.shields.io/badge/docs-mkdocs-708FCC.svg?style=flat)](https://drehstromer.github.io/mkdocstrings-twincat/)
[![pypi version](https://img.shields.io/pypi/v/mkdocstrings-twincat.svg)](https://pypi.org/project/mkdocstrings-twincat/)

A Twincat handler for mkdocstrings that uses pytwincatparser to parse TwinCAT PLC files.

## Installation

```bash
pip install mkdocstrings-twincat
```

## Usage

To use this handler, you need to configure it in your `mkdocs.yml` file:

```yaml
plugins:
  - mkdocstrings:
      handlers:
        twincat:
          options:
            extra:
              search_path: path/to/your/twincat/files
```

Then, in your Markdown files, you can use the `::: twincat` directive to include documentation for TwinCAT objects:

```markdown
::: twincat:FB_Example
```

This will include documentation for the `FB_Example` POU. You can also document methods and properties:

```markdown
::: twincat:FB_Example.Method1
```

## Requirements

This handler requires the `pytwincatparser` package, which is automatically installed as a dependency.

## Development

### Building and Publishing

This project uses [uv](https://github.com/astral-sh/uv) for building and publishing. To build and publish the package, you can use one of the provided scripts:

#### Windows

```powershell
.\build_uv.ps1
```

#### Python Script

```bash
python build_uv.py
```

These scripts will:
1. Clean up previous builds
2. Build the package using uv
3. Ask if you want to publish the package to PyPI
4. Publish the package if you choose to do so
