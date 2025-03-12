"""mkdocstrings-twincat package.

A Twincathandler for mkdocstrings
"""

from __future__ import annotations

from mkdocstrings_twincat._internal.cli import get_parser, main

__all__: list[str] = ["get_parser", "main"]
