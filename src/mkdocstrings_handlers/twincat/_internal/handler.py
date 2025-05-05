# This module implements a handler for Twincat.

from __future__ import annotations

import glob
import os
import posixpath
import sys
from contextlib import suppress
from pathlib import Path, PureWindowsPath
from typing import TYPE_CHECKING, Any, ClassVar, List

from pytwincatparser import Loader,get_strategy, TcObjects, BaseStrategy, get_default_strategy

from mkdocs.exceptions import PluginError
from mkdocstrings import BaseHandler, CollectionError, CollectorItem, get_logger
from mkdocstrings_handlers.twincat._internal import rendering
from mkdocstrings_handlers.twincat._internal.config import TwincatConfig, TwincatOptions

if TYPE_CHECKING:
    from collections.abc import Mapping, MutableMapping

    from mkdocs.config.defaults import MkDocsConfig
    from mkdocstrings import HandlerOptions

# YORE: EOL 3.10: Replace block with line 2.
if sys.version_info >= (3, 11):
    from contextlib import chdir
else:
    from contextlib import contextmanager

    @contextmanager
    def chdir(path: str) -> Iterator[None]:
        old_wd = os.getcwd()
        os.chdir(path)
        try:
            yield
        finally:
            os.chdir(old_wd)


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

        self._collected: dict[str, TcObjects] = {}
        self._strategy: BaseStrategy = None
        if config.default_strategy is not None:
            strategy = get_strategy(config.default_strategy)
        else:
            strategy = get_default_strategy()


        self._strategy = strategy()
        self._loader: Loader = Loader(loader_strategy=self._strategy)
        
        paths:List[Path] = []

        for path in config.paths:
            _path = Path(PureWindowsPath(path))
            if _path.resolve().is_file():
                paths.append(_path.resolve())
                _logger.info(f"filepath: {_path.resolve()} is appended and resolved")
            else:
                _logger.info(f"filepath: {_path.resolve()} is not appended and resolved")
                _logger.error("No directories are supported, specify a file!")



        self._paths = paths
        _logger.info(f"Search Paths: {self._paths}")
        self.load_all_objects(paths=self._paths)
        _logger.info(f"Parsed {len(self._collected)} twincat objects")
        


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
        

    def load_all_objects(self, paths:List[Path], strategy:BaseStrategy|None = None):
        if strategy is not None:
            self._loader.strategy = strategy()

        for path in paths:
            tcobjects = self._loader.load_objects(path=path)
            for tcobject in tcobjects:
                if not tcobject.get_identifier() in self._collected:
                    self._collected[tcobject.get_identifier()] = tcobject



    def collect(self, identifier: str, options: TwincatOptions) -> CollectorItem:  # noqa: ARG002
        """Collect data given an identifier and selection configuration."""
        # In the implementation, you either run a specialized tool in a subprocess
        # to capture its JSON output, that you load again in Python data structures,
        # or you parse the source code directly, for example with tree-sitter.
        #
        # The `identifier` argument is the fully qualified name of the object to collect.
        # For example, in Python, it would be 'package.module.function' to collect documentation
        # for this function. Other languages have different conventions.
        #
        # The `options` argument is the configuration options for loading/rendering the data.
        # It contains both the global and local options, combined together.
        #
        # You might want to store collected data in `self._collected`, for easier retrieval later,
        # typically when mkdocstrings will try to get aliases for an identifier through your `get_aliases` method.

  
        try:
            doc_object = self._collected[identifier]
        except KeyError as error:
            raise CollectionError(f"{identifier} could not be found") from error

        return doc_object  


    def render(self, data: CollectorItem, options: TwincatOptions) -> str:
        """Render a template using provided data and configuration options."""
        # The `data` argument is the data to render, that was collected above in `collect()`.
        # The `options` argument is the configuration options for loading/rendering the data.
        # It contains both the global and local options, combined together.

        template_name = rendering.do_get_template(self.env, data)
        template = self.env.get_template(template_name)

        # All the following variables will be available in the Jinja templates.
        return template.render(
            config=options,
            data=data,  # You might want to rename `data` into something more specific.
            heading_level=options.heading_level,
            root=True,
        )

    def get_aliases(self, identifier: str) -> tuple[str, ...]:
        """Get aliases for a given identifier."""
        try:
            data = self._collected[identifier]
        except KeyError:
            return ()
        
        aliases = []

        parts = identifier.split(".")

        aliases.append(identifier)

        if len(parts) >= 3:
            aliases.append(f"{parts[1]}.{parts[-1]}")  # z. B. Lib.Fb_base.Do_something() -> Fb_Base.DoSomething()

        return tuple(aliases)


    def update_env(self, config: dict) -> None:  # noqa: ARG002
        """Update the Jinja environment with any custom settings/filters/options for this handler.

        Parameters:
            config: MkDocs configuration, read from `mkdocs.yml`.
        """
        self.env.trim_blocks = True
        self.env.lstrip_blocks = True
        self.env.keep_trailing_newline = False

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
