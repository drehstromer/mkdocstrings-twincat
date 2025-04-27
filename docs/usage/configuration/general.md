# General Options

This page explains the general options available for the TwinCAT handler.

## extra

The `extra` option is a dictionary of additional options for the TwinCAT handler.

```yaml
extra:
  search_path: path/to/your/twincat/files
```

### search_path

The `search_path` option is required and should point to the directory containing your TwinCAT files. This can be an absolute path or a path relative to your mkdocs.yml file.

```yaml
search_path: path/to/your/twincat/files
```

## heading

The `heading` option allows you to override the heading text for the object being documented.

```yaml
heading: "Custom Heading"
```

By default, the heading is the name of the object being documented.

## heading_level

The `heading_level` option sets the initial heading level for the object being documented.

```yaml
heading_level: 2
```

The default value is `2`, which means the object's name will be rendered as an `<h2>` heading. Child elements will use higher heading levels.
