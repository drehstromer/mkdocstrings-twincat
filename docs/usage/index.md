## Installation


```toml title="pyproject.toml"
# PEP 621 dependencies declaration
# adapt to your dependencies manager
[project]
dependencies = [
    "mkdocstrings-twincat",
]
```

If you just use the twincat handler you can set it to default

```yaml title="mkdocs.yml"
plugins:
- mkdocstrings:
    default_handler: twincat
```

## Injecting documentation

With the Twincat handler installed and configured as default handler,
you can inject documentation for a plc project, functionblock, gvl, itf,...

```md
::: path.to.object
```

If another handler was defined as default handler,
you can explicitely ask for the Twincat handler to be used when injecting documentation
with the `handler` option:

```md
::: path.to.object
    handler: twincat
```

## Configuration

You can configure the twincat handler in `mkdocs.yml`:

```yaml title="mkdocs.yml"
plugins:
- mkdocstrings:
    handlers:
      twincat:
        ...  # the twincat handler configuration
```

### Global-only options

Some options are **global only**, and go directly under the handler's name.

[](){#setting-paths}
#### `paths`

This option is used to provide filesystem paths in which to search for a twincat file.
it is important that you specify a file, not a folder. It is currently not supported to load a whole folder. 

```yaml title="mkdocs.yml"
plugins:
- mkdocstrings:
    handlers:
      twincat:
        paths: [twincatproject\TcUnit.plcproj]
```


[](){#setting-options}
### Global/local options

The other options can be used both globally *and* locally, under the `options` key.
For example, globally:

```yaml title="mkdocs.yml"
plugins:
- mkdocstrings:
    handlers:
      twincat:
        options:
          do_something: true
```

...and locally, overriding the global configuration:

```md title="docs/some_page.md"
::: package.module.class
    options:
      do_something: false
```

These options affect how the documentation is collected from sources and rendered.
See the following tables summarizing the options, and get more details for each option
in the following pages:

- [General options](configuration/general.md): various options that do not fit in the other categories
- [Headings options](configuration/headings.md): options related to headings and the table of contents
    (or sidebar, depending on the theme used)
- [Documentation options](configuration/documentation.md): options related to documentation

