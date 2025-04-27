# Customization

This page explains how to customize the TwinCAT handler for mkdocstrings.

## Templates

The TwinCAT handler uses Jinja2 templates to render the documentation. You can customize these templates to change the appearance of the generated documentation.

### Template Structure

The templates are organized in a hierarchical structure:

- `base.html.jinja`: The base template that defines the overall structure of the documentation.
- `tcpou.html.jinja`: Template for POUs (Program Organization Units).
- `tcdut.html.jinja`: Template for DUTs (Data Unit Types).
- `tcitf.html.jinja`: Template for Interfaces.
- `tcmethod.html.jinja`: Template for Methods.
- `tcproperty.html.jinja`: Template for Properties.
- `tcvariable_section.html.jinja`: Template for Variable Sections.
- `tcdocumentation.html.jinja`: Template for Documentation.

### Customizing Templates

To customize the templates, you need to create your own templates in your project's `docs/templates` directory. The templates should have the same names as the original templates.

For example, to customize the POU template, create a file at `docs/templates/tcpou.html.jinja`.

Then, configure mkdocstrings to use your custom templates in your `mkdocs.yml` file:

```yaml
plugins:
  - mkdocstrings:
      handlers:
        twincat:
          options:
            template_dir: templates
```

### Template Variables

The following variables are available in the templates:

- `config`: The configuration options for the handler.
- `data`: The object being documented (e.g., a TcPou, TcDut, TcItf, etc.).
- `item`: The collector item containing metadata about the object.
- `heading_level`: The initial heading level for the object.
- `root`: A boolean indicating whether the object is the root object being documented.

## CSS Styling

You can customize the appearance of the generated documentation by adding your own CSS styles.

### Adding Custom CSS

To add custom CSS, create a CSS file in your project's `docs/css` directory, for example `docs/css/custom.css`.

Then, add the CSS file to your `mkdocs.yml` file:

```yaml
extra_css:
  - css/custom.css
```

### CSS Classes

The following CSS classes are used in the generated documentation:

- `.doc-section`: A section of the documentation.
- `.doc-section-title`: The title of a section.
- `.doc-subsection`: A subsection of the documentation.
- `.doc-subsection-title`: The title of a subsection.
- `.doc-item`: An item in the documentation.
- `.doc-item-name`: The name of an item.
- `.doc-item-type`: The type of an item.
- `.doc-item-description`: The description of an item.
- `.doc-item-attributes`: The attributes of an item.
- `.doc-item-value`: The value of an item.
- `.doc-tag`: A documentation tag.
- `.doc-tag-name`: The name of a documentation tag.
- `.doc-tag-value`: The value of a documentation tag.
- `.badge`: A badge.
- `.badge-primary`: A primary badge.
- `.badge-secondary`: A secondary badge.
- `.badge-success`: A success badge.
- `.badge-info`: An info badge.
- `.badge-warning`: A warning badge.
- `.badge-danger`: A danger badge.
