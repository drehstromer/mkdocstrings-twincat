# Heading Options

This page explains the heading-related options available for the TwinCAT handler.

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

## show_symbol_type_heading

The `show_symbol_type_heading` option controls whether the symbol type (e.g., POU, DUT, Method) is shown in the heading.

```yaml
show_symbol_type_heading: true
```

When set to `true`, the symbol type will be shown in the heading. For example, "FB_Example (POU)". The default value is `false`.

## show_symbol_type_toc

The `show_symbol_type_toc` option controls whether the symbol type (e.g., POU, DUT, Method) is shown in the table of contents.

```yaml
show_symbol_type_toc: true
```

When set to `true`, the symbol type will be shown in the table of contents. For example, "FB_Example (POU)". The default value is `false`.

## toc_label

The `toc_label` option allows you to override the label used in the table of contents for the object being documented.

```yaml
toc_label: "Custom TOC Label"
```

By default, the TOC label is the name of the object being documented.
