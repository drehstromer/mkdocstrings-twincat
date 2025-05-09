# Configuration and options dataclasses.

from __future__ import annotations

import sys
from dataclasses import field
from typing import TYPE_CHECKING, Annotated, Any, Literal

from mkdocstrings import get_logger

# YORE: EOL 3.10: Replace block with line 2.
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


_logger = get_logger(__name__)


try:
    # When Pydantic is available, use it to validate options (done automatically).
    # Users can therefore opt into validation by installing Pydantic in development/CI.
    # When building the docs to deploy them, Pydantic is not required anymore.

    # When building our own docs, Pydantic is always installed (see `docs` group in `pyproject.toml`)
    # to allow automatic generation of a JSON Schema. The JSON Schema is then referenced by mkdocstrings,
    # which is itself referenced by mkdocs-material's schema system. For example in VSCode:
    #
    # "yaml.schemas": {
    #     "https://squidfunk.github.io/mkdocs-material/schema.json": "mkdocs.yml"
    # }
    import pydantic

    if getattr(pydantic, "__version__", "1.").startswith("1."):
        raise ImportError  # noqa: TRY301

    # YORE: EOL 3.9: Remove block.
    if sys.version_info < (3, 10):
        try:
            import eval_type_backport  # noqa: F401
        except ImportError:
            _logger.debug(
                "Pydantic needs the `eval-type-backport` package to be installed "
                "for modern type syntax to work on Python 3.9. "
                "Deactivating Pydantic validation for Twincat handler options.",
            )
            raise

    from inspect import cleandoc

    from pydantic import Field as BaseField
    from pydantic.dataclasses import dataclass

    _base_url = "https://mkdocstrings.github.io/mkdocstrings-twincat/usage"

    def _Field(  # noqa: N802
        *args: Any,
        description: str,
        group: Literal["general"] | None = None,
        parent: str | None = None,
        **kwargs: Any,
    ) -> None:
        def _add_markdown_description(schema: dict[str, Any]) -> None:
            url = f"{_base_url}/{f'configuration/{group}/' if group else ''}#{parent or schema['title']}"
            schema["markdownDescription"] = f"[DOCUMENTATION]({url})\n\n{schema['description']}"

        return BaseField(
            *args,
            description=cleandoc(description),
            field_title_generator=lambda name, _: name,
            json_schema_extra=_add_markdown_description,
            **kwargs,
        )
except ImportError:
    from dataclasses import dataclass

    def _Field(*args: Any, **kwargs: Any) -> None:  # type: ignore[misc]  # noqa: N802
        pass


if TYPE_CHECKING:
    from collections.abc import MutableMapping


# YORE: EOL 3.9: Remove block.
_dataclass_options = {"frozen": True}
if sys.version_info >= (3, 10):
    _dataclass_options["kw_only"] = True


Order = Literal["alphabetical"]
"""Ordering methods.

- `__all__`: order members according to `__all__` module attributes, if declared;
- `alphabetical`: order members alphabetically;
- `source`: order members as they appear in the source file.
"""

# YORE: EOL 3.9: Replace `**_dataclass_options` with `frozen=True, kw_only=True` within line.
@dataclass(**_dataclass_options)  # type: ignore[call-overload]
class SummaryOption:
    """Summary option."""

    properties: Annotated[
        bool,
        _Field(
            group="members",
            parent="summary",
            description="Whether to render summaries of properties.",
        ),
    ] = False

    methods: Annotated[
        bool,
        _Field(
            group="members",
            parent="summary",
            description="Whether to render summaries of methods.",
        ),
    ] = False

    pous: Annotated[
        bool,
        _Field(
            group="members",
            parent="summary",
            description="Whether to render summaries of pous.",
        ),
    ] = False

    itfs: Annotated[
        bool,
        _Field(
            group="members",
            parent="summary",
            description="Whether to render summaries of itfs.",
        ),
    ] = False

    duts: Annotated[
        bool,
        _Field(
            group="members",
            parent="summary",
            description="Whether to render summaries of duts.",
        ),
    ] = False

    gvls: Annotated[
        bool,
        _Field(
            group="members",
            parent="summary",
            description="Whether to render summaries of gvls.",
        ),
    ] = False

    variables: Annotated[
        bool,
        _Field(
            group="members",
            parent="summary",
            description="Whether to render summaries of variables.",
        ),
    ] = False


# The input config class is useful to generate a JSON schema, see scripts/mkdocs_hooks.py.
# YORE: EOL 3.9: Replace `**_dataclass_options` with `frozen=True, kw_only=True` within line.
@dataclass(**_dataclass_options)
class TwincatInputOptions:
    """Accepted input options."""

    extra: Annotated[
        dict[str, Any],
        _Field(
            group="general",
            description="Extra options.",
        ),
    ] = field(default_factory=dict)

    heading: Annotated[
        str,
        _Field(
            group="headings",
            description="A custom string to override the autogenerated heading of the root object.",
        ),
    ] = ""

    heading_level: Annotated[
        int,
        _Field(
            group="headings",
            description="The initial heading level to use.",
        ),
    ] = 2

    show_symbol_type_heading: Annotated[
        bool,
        _Field(
            group="headings",
            description="Show the symbol type in headings (e.g. mod, class, meth, func and attr).",
        ),
    ] = False

    show_symbol_type_toc: Annotated[
        bool,
        _Field(
            group="headings",
            description="Show the symbol type in the Table of Contents (e.g. mod, class, methd, func and attr).",
        ),
    ] = False

    show_root_members_full_path: Annotated[
        bool,
        _Field(
            group="headings",
            description="Show the full twincat path of the root members.",
        ),
    ] = False

    show_object_full_path: Annotated[
        bool,
        _Field(
            group="docstrings",
            description="Show the full twincat path of every object.",
        ),
    ] = False

    show_root_heading: Annotated[
        bool,
        _Field(
            group="headings",
            description="""Show the heading of the object at the root of the documentation tree.

            The root object is the object referenced by the identifier after `:::`.
            """,
        ),
    ] = False

    show_symbol_type_heading: Annotated[
        bool,
        _Field(
            group="headings",
            description="Show the symbol type in headings (e.g. mod, class, meth, func and attr).",
        ),
    ] = False

    show_symbol_type_toc: Annotated[
        bool,
        _Field(
            group="headings",
            description="Show the symbol type in the Table of Contents (e.g. mod, class, methd, func and attr).",
        ),
    ] = False

    show_source: Annotated[
        bool,
        _Field(
            group="general",
            description="Show the source code of this object.",
        ),
    ] = True

    show_implements: Annotated[
        bool,
        _Field(
            group="general",
            description="if the pou implements something.",
        ),
    ] = True

    show_extends: Annotated[
        bool,
        _Field(
            group="general",
            description="show if the pou extends something",
        ),
    ] = True

    show_access_modifier: Annotated[
        bool,
        _Field(
            group="general",
            description="show the access modifier of the method",
        ),
    ] = True

    show_return: Annotated[
        bool,
        _Field(
            group="general",
            description="show the return of the method",
        ),
    ] = True

    show_root_toc_entry: Annotated[
        bool,
        _Field(
            group="headings",
            description="If the root heading is not shown, at least add a ToC entry for it.",
        ),
    ] = True

    show_labels: Annotated[
        bool,
        _Field(
            group="docu",
            description="Whether to show labels of the members.",
        ),
    ] = True

    variable_headings: Annotated[
        bool,
        _Field(
            group="headings",
            description="Whether to render headings for variables (therefore showing variables in the ToC).",
        ),
    ] = False

    toc_label: Annotated[
        str,
        _Field(
            group="headings",
            description="A custom string to override the autogenerated toc label of the root object.",
        ),
    ] = ""

    summary: Annotated[
        bool | SummaryOption,
        _Field(
            group="members",
            description="Whether to render summaries of tcplc proj, pous, duts, itfs, methods.",
        ),
    ] = field(default_factory=SummaryOption)

    show_category_heading: Annotated[
        bool,
        _Field(
            group="headings",
            description="When grouped by categories, show a heading for each category.",
        ),
    ] = False



    variable_section_style: Annotated[
        Literal["table", "list"],
        _Field(
            group="variable",
            description="The style used to render variable sections.",
        ),
    ] = "table"

    summary_section_style: Annotated[
        Literal["table", "list"],
        _Field(
            group="variable",
            description="The style used to render summarys.",
        ),
    ] = "table"

    @classmethod
    def coerce(cls, **data: Any) -> MutableMapping[str, Any]:
        """Coerce data."""
        if "summary" in data:
            summary = data["summary"]
            if summary is True:
                summary = SummaryOption(properties=True, methods=True, pous=True, itfs=True, duts=True, gvls=True, variables=True)
            elif summary is False:
                summary = SummaryOption(properties=False, methods=False, pous=False, itfs=False, duts=False, gvls=False, variables=False)
            else:
                summary = SummaryOption(**summary)
            data["summary"] = summary
        return data

    @classmethod
    def from_data(cls, **data: Any) -> Self:
        """Create an instance from a dictionary."""
        return cls(**cls.coerce(**data))


# YORE: EOL 3.9: Replace `**_dataclass_options` with `frozen=True, kw_only=True` within line.
@dataclass(**_dataclass_options)
class TwincatOptions(TwincatInputOptions):  # type: ignore[override,unused-ignore]
    """Final options passed as template context."""

    # Re-declare any field to modify/narrow its type.
    summary: SummaryOption = field(default_factory=SummaryOption)
    """Whether to render summaries of modules, classes, functions (methods) and attributes."""

    @classmethod
    def coerce(cls, **data: Any) -> MutableMapping[str, Any]:
        """Create an instance from a dictionary."""
        # Coerce any field into its final form.
        return super().coerce(**data)


# The input config class is useful to generate a JSON schema, see scripts/mkdocs_hooks.py.
# YORE: EOL 3.9: Replace `**_dataclass_options` with `frozen=True, kw_only=True` within line.
@dataclass(**_dataclass_options)
class TwincatInputConfig:

    """Twincat handler configuration."""
    paths: Annotated[
        list[str],
        _Field(description="The paths to the twincat files."),
    ] = field(default_factory=lambda: ["."])

    default_strategy: Annotated[
        str | None,
        _Field(description="Strategy to parse the files"),
    ] = None

    # We want to validate options early, so we load them as `TwincatInputOptions`.
    options: Annotated[
        TwincatInputOptions,
        _Field(description="Configuration options for collecting and rendering objects."),
    ] = field(default_factory=TwincatInputOptions)

    @classmethod
    def coerce(cls, **data: Any) -> MutableMapping[str, Any]:
        """Coerce data."""
        return data

    @classmethod
    def from_data(cls, **data: Any) -> Self:
        """Create an instance from a dictionary."""
        return cls(**cls.coerce(**data))


# YORE: EOL 3.9: Replace `**_dataclass_options` with `frozen=True, kw_only=True` within line.
@dataclass(**_dataclass_options)
class TwincatConfig(TwincatInputConfig):  # type: ignore[override,unused-ignore]
    """Twincat handler configuration."""




    options: Annotated[
        dict[str, Any],
        _Field(description="Configuration options for collecting and rendering objects."),
    ] = field(default_factory=dict)  # type: ignore[assignment]

    @classmethod
    def coerce(cls, **data: Any) -> MutableMapping[str, Any]:
        """Coerce data."""
        return super().coerce(**data)
