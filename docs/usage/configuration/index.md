# Configuration

This page explains how to configure the TwinCAT handler for mkdocstrings.

## Handler Configuration

The TwinCAT handler is configured in your `mkdocs.yml` file under the `mkdocstrings` plugin configuration:

```yaml
plugins:
  - mkdocstrings:
      handlers:
        twincat:
          options:
            # Global options for the TwinCAT handler
            heading_level: 2
            show_symbol_type_heading: true
            show_symbol_type_toc: true
            extra:
              search_path: path/to/your/twincat/files
```

## Required Options

### search_path

The `search_path` option is required and should point to the directory containing your TwinCAT files. This can be an absolute path or a path relative to your mkdocs.yml file.

```yaml
extra:
  search_path: path/to/your/twincat/files
```

## Global vs. Local Options

Options can be set globally for all TwinCAT objects in your `mkdocs.yml` file, or locally for specific objects in your Markdown files.

### Global Options

Global options are set in your `mkdocs.yml` file:

```yaml
plugins:
  - mkdocstrings:
      handlers:
        twincat:
          options:
            heading_level: 2
            show_symbol_type_heading: true
            show_symbol_type_toc: true
```

### Local Options

Local options are set in your Markdown files:

```markdown
::: twincat:FB_Example
    options:
      heading_level: 3
      show_symbol_type_heading: false
```

Local options override global options for the specific object being documented.

## Available Options

See the following pages for details on the available options:

- [General Options](general.md): Options for controlling the general behavior of the handler.
- [Heading Options](headings.md): Options for controlling the headings in the generated documentation.
