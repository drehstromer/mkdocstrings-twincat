# Usage

This page explains how to use the TwinCAT handler for mkdocstrings.

## Configuration

To use the TwinCAT handler, you need to configure it in your `mkdocs.yml` file:

```yaml
plugins:
  - mkdocstrings:
      handlers:
        twincat:
          options:
            extra:
              search_path: path/to/your/twincat/files
```

The `search_path` option is required and should point to the directory containing your TwinCAT files. This can be an absolute path or a path relative to your mkdocs.yml file.

## Documenting TwinCAT Objects

To document TwinCAT objects in your Markdown files, use the `::: twincat` directive followed by the identifier of the object you want to document:

```markdown
::: twincat:FB_Example
```

This will include documentation for the `FB_Example` POU. You can also document methods and properties:

```markdown
::: twincat:FB_Example.Method1
```

## Supported TwinCAT Objects

The TwinCAT handler supports the following types of objects:

- POUs (Program Organization Units): Function Blocks, Functions, Programs
- DUTs (Data Unit Types): Structures, Enumerations, Unions
- Interfaces
- Methods
- Properties

## Documentation Comments

The TwinCAT handler extracts documentation from comments in your TwinCAT code. It supports both single-line (`//`) and multi-line (`(* *)`) comments.

You can use the following tags in your comments:

- `@details`: Detailed description of the object
- `@usage`: Usage examples
- `@return`: Description of the return value (for methods)
- Custom tags: Any other tag will be included in the documentation

Example:

```
(*
    @details This is a detailed description of the function block.
    @usage Example of how to use this function block.
    @author John Doe
*)
FUNCTION_BLOCK FB_Example
```

## Requirements

This handler uses the `pytwincatparser` package to parse TwinCAT files. This package is automatically installed as a dependency when you install `mkdocstrings-twincat`.
