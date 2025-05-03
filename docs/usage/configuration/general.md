# General options

[](){ #option-extra }
## `extra`

- **:octicons-package-24: Type [`dict`][] :material-equal: `{}`{ title="default value" }**

The `extra` option lets you inject additional variables into the Jinja context used when rendering templates. You can then use this extra context in your overridden templates.

Local `extra` options will be merged into the global `extra` option:

```yaml title="in mkdocs.yml (global configuration)"
plugins:
- mkdocstrings:
    handlers:
      twincat:
        options:
          extra:
            hello: world
```

```md title="in docs/some_page.md (local configuration)"
::: your_package.your_module.your_func
    options:
      extra:
        foo: bar
```

...will inject both `hello` and `foo` into the Jinja context when rendering `your_package.your_module.your_func`.
