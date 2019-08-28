# Layout tag: col

Create a column inside of a table tag.

A column is a layout component of a [table](./table.md) tag.  A
table should have at least two columns.  Columns are defined in the
layout, contrary to the data (that is, the table rows).
```
<window title="Table demonstration">
  <table id=products x=2 y=4>
    <col>Name</col>
    <col>Quantity</col>
    <col>Cost</col>
  </table<
</window>
```

Using the `<table>` landmark creates an empty table, which will cause
an error.  A table must at least have two columns (if one, use
a simple [list](./list.html).  Use the `<col>` tag inside of the
`<table>` to create a column in the table.

## Attributes

| Name         | Required | Description              | Example     |
| ------------ | -------- | ------------------------ | ----------- |
| `id` | Yes | The column identifier (ID). If not set, use the name specified as data of the `<col>` tag. | `<col id=name>` |

See also the [table](./table.md) tag to set the table in the layout.

Specify the name of the column as data of this tag.  This is a
translatable data, it can contain data to be translated.  In this case,
specifying an ID is required.

If the identifier is not set, use the name specified in the data of
the tag.  For instance:

    <col>Quantity</col>

Will result in a column of ID "quantity" (lowercase).

## Data

The column isn't a proper widget by itself.  It exists in the layout,
but isn't linked to a generic widget.  Interacting on a single column
is not possible with this object, rather, see the
[table tag](./table.md).  Therefore, it has no attribute or methof
of its own.

## Controls

The column isn't a proper widget by itself.  It exists in the layout,
but isn't linked to a generic widget.  Interacting on a single column
is not possible with this object, rather, see the
[table tag](./table.md).  Therefore, it has no control of its own.

