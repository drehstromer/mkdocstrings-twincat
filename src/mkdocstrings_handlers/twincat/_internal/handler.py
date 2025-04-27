
# This module implements a handler for Twincat.

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Dict, List, Optional, Tuple, Union, cast

from mkdocs.exceptions import PluginError
from mkdocstrings import BaseHandler, CollectionError, CollectorItem, get_logger

from mkdocstrings_handlers.twincat._internal.config import TwincatConfig, TwincatOptions

# Import pytwincatparser
from pytwincatparser import (
    TwinCatLoader,
    TcPou,
    TcDut,
    TcItf,
    TcMethod,
    TcProperty,
    TcGet,
    TcSet,
    TcVariable,
    TcVariableSection,
    TcDocumentation,
)

if TYPE_CHECKING:
    from collections.abc import Mapping, MutableMapping

    from mkdocs.config.defaults import MkDocsConfig
    from mkdocstrings import HandlerOptions


_logger = get_logger(__name__)


class TwincatHandler(BaseHandler):
    """The Twincat handler class."""

    name: ClassVar[str] = "twincat"
    """The handler's name."""

    domain: ClassVar[str] = "twincat"
    """The cross-documentation domain/language for this handler."""
    # Typically: the file extension, like `py`, `go` or `rs`.
    # For non-language handlers, use the technology/tool name, like `openapi` or `click`.

    enable_inventory: ClassVar[bool] = False
    """Whether this handler is interested in enabling the creation of the `objects.inv` Sphinx inventory file."""

    fallback_theme: ClassVar[str] = "material"
    """The theme to fallback to."""

    def __init__(self, config: TwincatConfig, base_dir: Path, **kwargs: Any) -> None:
        """Initialize the handler.

        Parameters:
            config: The handler configuration.
            base_dir: The base directory of the project.
            **kwargs: Arguments passed to the parent constructor.
        """
        super().__init__(**kwargs)

        self.config = config
        """The handler configuration."""
        self.base_dir = base_dir
        """The base directory of the project."""
        self.global_options = config.options
        """The global configuration options."""

        self._collected: dict[str, CollectorItem] = {}
        self._loader: Optional[TwinCatLoader] = None
        self._tc_objects: List[Tuple[str, Any]] = []

    def get_options(self, local_options: Mapping[str, Any]) -> HandlerOptions:
        """Get combined default, global and local options.

        Arguments:
            local_options: The local options.

        Returns:
            The combined options.
        """
        extra = {**self.global_options.get("extra", {}), **local_options.get("extra", {})}
        options = {**self.global_options, **local_options, "extra": extra}
        try:
            return TwincatOptions.from_data(**options)
        except Exception as error:
            raise PluginError(f"Invalid options: {error}") from error

    def _initialize_loader(self, options: TwincatOptions) -> None:
        """Initialize the TwinCatLoader if it hasn't been initialized yet.

        Arguments:
            options: The configuration options.
        """
        if self._loader is None:
            search_path = options.extra.get("search_path", "")
            if not search_path:
                raise CollectionError("No search_path specified in options.extra")

            # Convert relative path to absolute path
            if not os.path.isabs(search_path):
                search_path = os.path.join(self.base_dir, search_path)

            _logger.info(f"Initializing TwinCatLoader with search_path: {search_path}")
            self._loader = TwinCatLoader(
                search_path=search_path,
                tcObjects=self._tc_objects
            )
            self._loader.load()
            _logger.info(f"Loaded {len(self._tc_objects)} TwinCAT objects")

    def collect(self, identifier: str, options: TwincatOptions) -> CollectorItem:
        """Collect data given an identifier and selection configuration.

        Arguments:
            identifier: The identifier of the object to collect.
            options: The configuration options.

        Returns:
            The collected data.

        Raises:
            CollectionError: If the object could not be found.
        """
        _logger.info(f"Collecting data for identifier: {identifier}")

        # Initialize the loader if it hasn't been initialized yet
        self._initialize_loader(options)

        # Check if we've already collected this identifier
        if identifier in self._collected:
            return self._collected[identifier]

        # Get the object from the loader
        obj = self._loader.getItemByName(identifier)
        if obj is None:
            raise CollectionError(f"Could not find object with identifier: {identifier}")

        # Create a collector item with the object and its metadata
        item = CollectorItem(
            path=identifier,
            name=identifier.split(".")[-1] if "." in identifier else identifier,
            obj=obj,
            relative_file_path=None,
            relative_line_start=None,
            relative_line_end=None,
        )

        # Store the collected item for later retrieval
        self._collected[identifier] = item

        return item

    def render(self, data: CollectorItem, options: TwincatOptions) -> str:
        """Render a template using provided data and configuration options.

        Arguments:
            data: The data to render.
            options: The configuration options.

        Returns:
            The rendered template.
        """
        obj = data.obj
        template_name = self._get_template_name(obj)

        _logger.info(f"Rendering template {template_name} for {data.path}")

        template = self.env.get_template(template_name)
        return template.render(
            config=options,
            data=obj,
            item=data,
            heading_level=options.heading_level,
            root=True,
        )

    def _get_template_name(self, obj: Any) -> str:
        """Get the template name based on the object type.

        Arguments:
            obj: The object to get the template name for.

        Returns:
            The template name.
        """
        if isinstance(obj, TcPou):
            return "tcpou.html.jinja"
        elif isinstance(obj, TcDut):
            return "tcdut.html.jinja"
        elif isinstance(obj, TcItf):
            return "tcitf.html.jinja"
        elif isinstance(obj, TcMethod):
            return "tcmethod.html.jinja"
        elif isinstance(obj, TcProperty):
            return "tcproperty.html.jinja"
        elif isinstance(obj, TcVariableSection):
            return "tcvariable_section.html.jinja"
        elif isinstance(obj, TcDocumentation):
            return "tcdocumentation.html.jinja"
        else:
            # Default template
            return "index.html.jinja"

    def get_aliases(self, identifier: str) -> tuple[str, ...]:
        """Get aliases for a given identifier.

        Arguments:
            identifier: The identifier to get aliases for.

        Returns:
            A tuple of aliases.
        """
        try:
            data = self._collected[identifier]
            obj = data.obj

            aliases = [data.path]

            # Add additional aliases based on object type
            if isinstance(obj, TcPou):
                # Add aliases for POU
                if obj.name and obj.name != identifier:
                    aliases.append(obj.name)
            elif isinstance(obj, TcDut):
                # Add aliases for DUT
                if obj.name and obj.name != identifier:
                    aliases.append(obj.name)
            elif isinstance(obj, TcItf):
                # Add aliases for ITF
                if obj.name and obj.name != identifier:
                    aliases.append(obj.name)
            elif isinstance(obj, TcMethod):
                # Add aliases for Method
                if obj.name and obj.name != identifier:
                    aliases.append(obj.name)
                    # Also add parent.method_name as an alias
                    if "." in identifier:
                        parent_name = identifier.split(".")[0]
                        aliases.append(f"{parent_name}.{obj.name}")
            elif isinstance(obj, TcProperty):
                # Add aliases for Property
                if obj.name and obj.name != identifier:
                    aliases.append(obj.name)
                    # Also add parent.property_name as an alias
                    if "." in identifier:
                        parent_name = identifier.split(".")[0]
                        aliases.append(f"{parent_name}.{obj.name}")

            return tuple(set(aliases))
        except KeyError:
            return ()

    def update_env(self, config: dict) -> None:  # noqa: ARG002
        """Update the Jinja environment with any custom settings/filters/options for this handler.

        Parameters:
            config: MkDocs configuration, read from `mkdocs.yml`.
        """
        self.env.trim_blocks = True
        self.env.lstrip_blocks = True
        self.env.keep_trailing_newline = False

        # Add custom filters
        self.env.filters["is_pou"] = lambda obj: isinstance(obj, TcPou)
        self.env.filters["is_dut"] = lambda obj: isinstance(obj, TcDut)
        self.env.filters["is_itf"] = lambda obj: isinstance(obj, TcItf)
        self.env.filters["is_method"] = lambda obj: isinstance(obj, TcMethod)
        self.env.filters["is_property"] = lambda obj: isinstance(obj, TcProperty)
        self.env.filters["is_variable_section"] = lambda obj: isinstance(obj, TcVariableSection)
        self.env.filters["is_documentation"] = lambda obj: isinstance(obj, TcDocumentation)

    # You can also implement the `get_inventory_urls` and `load_inventory` methods
    # if you want to support loading object inventories.
    # You can also implement the `render_backlinks` method if you want to support backlinks.


def get_handler(
    handler_config: MutableMapping[str, Any],
    tool_config: MkDocsConfig,
    **kwargs: Any,
) -> TwincatHandler:
    """Simply return an instance of `TwincatHandler`.

    Arguments:
        handler_config: The handler configuration.
        tool_config: The tool (SSG) configuration.

    Returns:
        An instance of `TwincatHandler`.
    """
    base_dir = Path(tool_config.config_file_path or "./mkdocs.yml").parent
    return TwincatHandler(
        config=TwincatConfig.from_data(**handler_config),
        base_dir=base_dir,
        **kwargs,
    )
