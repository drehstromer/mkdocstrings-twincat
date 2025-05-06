# This module implements rendering utilities.

from __future__ import annotations

import random
import re
import string
import subprocess
import sys
import warnings
from collections import defaultdict
from contextlib import suppress
from dataclasses import replace
from functools import lru_cache
from pathlib import Path
from re import Match, Pattern
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Literal, TypeVar


from jinja2 import TemplateNotFound, pass_context, pass_environment
from markupsafe import Markup
from mkdocs_autorefs import AutorefsHookInterface, Backlink, BacklinkCrumb
from mkdocstrings import get_logger

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator, Sequence


    from jinja2 import Environment
    from jinja2.runtime import Context
    from mkdocstrings import CollectorItem

_logger = get_logger(__name__)


# YORE: Bump 2: Remove line.
@pass_environment
# YORE: Bump 2: Replace `env: Environment, ` with `` within line.
# YORE: Bump 2: Replace `str | ` with `` within line.
def do_get_template(env: Environment, obj: CollectorItem) -> str:
    """Get the template name used to render an object.

    Parameters:
        env: The Jinja environment, passed automatically.
        obj: A Griffe object, or a template name.

    Returns:
        A template name.
    """

   
    name = obj.kind


    try:
        template = env.get_template(f"{name}.html")
    except TemplateNotFound:
        return f"{name}.html.jinja"
    our_template = Path(template.filename).is_relative_to(Path(__file__).parent.parent)  # type: ignore[arg-type]
    if our_template:
        return f"{name}.html.jinja"
    _logger.warning(
        f"DeprecationWarning: Overriding '{name}.html' is deprecated, override '{name}.html.jinja' instead. ",
        once=True,
    )
    return f"{name}.html"


