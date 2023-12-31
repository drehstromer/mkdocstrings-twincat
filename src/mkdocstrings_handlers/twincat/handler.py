"""This module implements a handler for the Twincat language."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Mapping, MutableMapping

from contextlib import chdir
import glob
import os
import sys
import pathlib

from mkdocs.exceptions import PluginError
from mkdocstrings.handlers.base import BaseHandler, CollectorItem
from mkdocstrings.loggers import get_logger

import blark.parse
import blark.summary
import blark.util
import blark.input

from mkdocstrings_handlers.twincat import rendering

if TYPE_CHECKING:
    from markdown import Markdown


logger = get_logger(__name__)


class TwincatHandler(BaseHandler):
    """The Twincat handler class."""

    domain: str = "twincat"
    """The cross-documentation domain/language for this handler."""


    enable_inventory: bool = False
    """Whether this handler is interested in enabling the creation of the `objects.inv` Sphinx inventory file."""

    fallback_theme = "material"
    """The theme to fallback to."""

    fallback_config: ClassVar[dict] = {"fallback": True}
    """The configuration used to collect item during autorefs fallback."""

    default_config: ClassVar[dict] = {
        "show_root_heading": False,
        "show_root_toc_entry": True,
        "heading_level": 2,
        "inoutput_rendering_style": "list",
    }
    """The default configuration options.

    Option | Type | Description | Default
    ------ | ---- | ----------- | -------
    **`show_root_heading`** | `bool` | Show the heading of the object at the root of the documentation tree. | `False`
    **`show_root_toc_entry`** | `bool` | If the root heading is not shown, at least add a ToC entry for it. | `True`
    **`heading_level`** | `int` | The initial heading level to use. | `2`
    """

    def __init__(self,  
                *args: Any, 
                config_file_path: str | None = None,
                path: str ="",
                **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._config_file_path = config_file_path
        self.path = None
        acceptedFileEndings = [".tsproj",".plcproj",".sln"]
        for FileEnding in acceptedFileEndings:
            if path.endswith(FileEnding):
                if not os.path.isabs(path) and config_file_path:
                    path = os.path.abspath(os.path.join(os.path.dirname(config_file_path), path))  # noqa: PLW2901
                self.path = path
                logger.info(f"load: {self.path}")

        if self.path is not None:
            parsed = list(blark.parse.parse(self.path))
            self._CodeSummary = blark.summary.CodeSummary.from_parse_results(parsed)
            logger.info(f"CodeSummary loaded")
        else:
            self._CodeSummary = None
            logger.warning("no Codesummary loaded")
            
        


   

    def collect(self, identifier: str, config: MutableMapping[str, Any]) -> CollectorItem:  # noqa: ARG002
        """Collect data given an identifier and selection configuration.

        In the implementation, you typically call a subprocess that returns JSON, and load that JSON again into
        a Python dictionary for example, though the implementation is completely free.

        Parameters:
            identifier: An identifier that was found in a markdown document for which to collect data. For example,
                in Python, it would be 'mkdocstrings.handlers' to collect documentation about the handlers module.
                It can be anything that you can feed to the tool of your choice.
            config: All configuration options for this handler either defined globally in `mkdocs.yml` or
                locally overridden in an identifier block by the user.

        Returns:
            Anything you want, as long as you can feed it to the `render` method.
        """
        self.test =self._CodeSummary.find(identifier)
     
        return(self._CodeSummary.find(identifier))


    def render(self, data: CollectorItem, config: Mapping[str, Any]) -> str:  # noqa: ARG002
        """Render a template using provided data and configuration options.

        Parameters:
            data: The data to render that was collected above in `collect()`.
            config: All configuration options for this handler either defined globally in `mkdocs.yml` or
                locally overridden in an identifier block by the user.

        Returns:
            The rendered template as HTML.
        """
        # final_config = {**self.default_config, **config}
        # heading_level = final_config["heading_level"]
        # template = self.env.get_template(f"{data...}.html")
        # return template.render(
        #     **{"config": final_config, data...: data, "heading_level": heading_level, "root": True},
        # )
        #raise PluginError("Implement me!")

        templatename = self.do_get_template(data)
        template = self.env.get_template(templatename)

        final_config = {**self.default_config, **config}
        heading_level = final_config["heading_level"]

        return template.render(
            **{"config": final_config, "data": data, "heading_level": heading_level, "root": True})






        

    def do_get_template(self, summaryType):
        return f"{type(summaryType).__name__}.html"


    def update_env(self, md: Markdown, config: dict) -> None:
        """Update the Jinja environment with any custom settings/filters/options for this handler.

        Parameters:
            md: The Markdown instance. Useful to add functions able to convert Markdown into the environment filters.
            config: Configuration options for `mkdocs` and `mkdocstrings`, read from `mkdocs.yml`. See the source code
                of [mkdocstrings.plugin.MkdocstringsPlugin.on_config][] to see what's in this dictionary.
        """
        super().update_env(md, config)  # Add some mkdocstrings default filters such as highlight and convert_markdown
        self.env.filters["do_sort_extended_methods"] = rendering.do_sort_extended_methods
        self.env.filters["do_sort_extended_properties"] = rendering.do_sort_extended_properties
        self.env.trim_blocks = True
        self.env.lstrip_blocks = True
        self.env.keep_trailing_newline = False


def get_handler(
    *,
    theme: str,
    custom_templates: str | None = None,
    config_file_path: str | None = None,  # noqa: ARG001
    path: str = "",
    **config: Any,  # noqa: ARG001
) -> TwincatHandler:
    """Simply return an instance of `TwincatHandler`.

    Parameters:
        theme: The theme to use when rendering contents.
        custom_templates: Directory containing custom templates.
        config_file_path: The MkDocs configuration file path.
        **config: Configuration passed to the handler.

    Returns:
        An instance of the handler.
    """
    return TwincatHandler(
        handler="twincat",
        theme=theme,
        custom_templates=custom_templates,
        config_file_path=config_file_path,
        path=path,
    )
