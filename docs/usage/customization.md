# Customization

It is possible to customize the output of the generated documentation with CSS
and/or by overriding templates.

## CSS classes

Our templates add [CSS](https://www.w3schools.com/Css/) classes to many HTML elements
to make it possible for users to customize the resulting look and feel.

To add CSS rules and style mkdocstrings' output,
put them in a CSS file in your docs folder, for example in `docs/css/mkdocstrings.css`,
and reference this file in [MkDocs' `extra_css` configuration option](https://www.mkdocs.org/user-guide/configuration/#extra_css):

```yaml title="mkdocs.yml"
extra_css:
- css/mkdocstrings.css
```

Example:

```css title="docs/css/mkdocstrings.css"
.doc-section-title {
  font-weight: bold;
}
```

## Symbol types

### Colors

You can customize the colors of the symbol types
(see [`show_symbol_type_heading`][show_symbol_type_heading] and [`show_symbol_type_toc`][show_symbol_type_toc])
by overriding the values of our CSS variables, for example:

```css title="docs/css/mkdocstrings.css"
[data-md-color-scheme="default"] {
  --doc-symbol-data-fg-color: #d1b619;

  --doc-symbol-data-bg-color: #d1b6191a;
}

[data-md-color-scheme="slate"] {
  --doc-symbol-data-fg-color: #46c2cb;

  --doc-symbol-data-bg-color: #46c2cb1a;
}
```

The `[data-md-color-scheme="*"]` selectors work with the [Material for MkDocs] theme.
If you are using another theme, adapt the selectors to this theme
if it supports light and dark themes,
otherwise just override the variables at root level:

```css title="docs/css/mkdocstrings.css"
:root {
  --doc-symbol-data-fg-color: #d1b619;

  --doc-symbol-data-bg-color: #d1b6191a;
}
```

/// admonition | Preview
    type: preview

<div id="preview-symbol-colors">
  <style>
    [data-md-color-scheme="default"] #preview-symbol-colors {
      --doc-symbol-data-fg-color: #d1b619;

      --doc-symbol-data-bg-color: #d1b6191a;
    }

    [data-md-color-scheme="slate"] #preview-symbol-colors {
      --doc-symbol-data-fg-color: #46c2cb;

      --doc-symbol-data-bg-color: #46c2cb1a;
    }
  </style>
  <p>
    Try cycling through the themes to see the colors for each theme:
    <code class="doc-symbol doc-symbol-data"></code
  </p>
</div>

///

### Names

You can also change the actual symbol names.
For example, to use single letters instead of truncated types:

```css title="docs/css/mkdocstrings.css"
.doc-symbol-data::after {
  content: "D";
}
```

/// admonition | Preview
    type: preview

<div id="preview-symbol-names">
  <style>
    #preview-symbol-names .doc-symbol-data::after {
      content: "D";
    }
  </style>
  <ul>
    <li>Data: <code class="doc-symbol doc-symbol-data"></code></li>
  </ul>
</div>

///

## Templates

Templates are organized into the following tree:

```python exec="1" result="tree"
from pathlib import Path

basedir = "src/mkdocstrings_handlers/twincat/templates/material"
print("theme/")
for filepath in sorted(path for path in Path(basedir).rglob("*") if "_base" not in str(path) and path.suffix != ".css"):
    print(
        "    " * (len(filepath.relative_to(basedir).parent.parts) + 1)
        + filepath.name
        + ("/" if filepath.is_dir() else "")
    )
```

See them [in the repository](https://github.com/mkdocstrings/mkdocstrings-twincat/tree/main/src/mkdocstrings_handlers/twincat/templates/).
See the general *mkdocstrings* documentation to learn how to override them: https://mkdocstrings.github.io/theming/#templates.

Each one of these templates extends a base version in `theme/_base`. Example:

```html+jinja title="theme/data.html.jinja"
{% extends "_base/data.html.jinja" %}
```

Some of these templates define [Jinja blocks](https://jinja.palletsprojects.com/en/3.0.x/templates/#template-inheritance).
allowing to customize only *parts* of a template
without having to fully copy-paste it into your project:

```jinja title="templates/theme/data.html"
{% extends "_base/data.html" %}
{% block contents scoped %}
  {{ block.super }}
  Additional contents
{% endblock contents %}
```
