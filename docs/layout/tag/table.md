# Layout tag: table

Create a table with columns.

A table is a list, except each item in the list is a row in the table.
A table has several columns with names.  The user can scroll through
this table and select either only row or several rows at the same time.

```
<window title="Table demonstration">
  <table id=products x=2 y=4>
    <col>Name</col>
    <col>Quantity</col>
    <col>Cost</col>
  </table<
</window>
```

## Usage

Using the `<table>` landmark creates an empty table, which will
cause an error.  A table must at least have two columns (if one,
use a simple [list](./list.html).  Use the `<col>` tag inside of the
`<table>` to create a column in the table.

Afterward, you will use methods on the
[Table widget](../../widget/Table.md) directly to add, remove, sort
rows, and associate objects to rows.

## Attributes

| Name         | Required | Description              | Example     |
| ------------ | -------- | ------------------------ | ----------- |
| `x` | Yes | The widget's horizontal position in columns (0 is left). This position is relative to the window width. | `<table x=5>` |
| `y` | Yes | The widget's vertical position in rows (0 is at the top). This position is relative to the window height. | `<table y=2>` |
| `id` | Yes | The table identifier (ID). Contrary to most other tags, you need to set this attribute. | `<table id=quit>` |
| `width` | No | The widget width, that is, the number of columns it will use in the window grid. A widget with a width of 2 will stretch one additional column to the right. A widget with `x` set to 2 and `width` set to 3 will span `x=2`, `x=3`, and `x=4`.  The default is 1, so a widget will remain in its `x` column. | `<table width=2>` |
| `height` | No | The widget height, that is, the number of rows it will use in the window grid. A widget with a height of 2 will stretch one additional row downward. A widget with `y` set to 2 and `height` set to 3 will span `y=2`, `y=3`, and `y=4`.  The default is 1, so a widget will remain in its `y` row. | `<table height=2>` |

See also the [col](./col.md) tag to define the columns in a table.
This tag will need more information.

> Note : the table identifier is mandatory.  You cannot dcreate
  a table without validt identifier.  The reason for this constraint
  is due to the fact that this widget, in particular, will be edited
  in your application.  Lacking an identifier, you won't be able
  to do that.

## Data

The [table widget](../../widget/Table.md) can be manipulated to add
and remove rows and peform additional operations.

| Attribute      | Meaning and type | Example                     |
| -------------- | ---------------- | --------------------------- |
| `rows` | The rows (list) | `self.rows = (("col 1", "col 2"))` |
| `selected` | The selected row. Use this property to query the selected row or change the current | `self.selected = 5` |
| `can_associate` | A boolean (`False` by default).  If set to `True`, associating objects with rows is the default bheavior (see [row association](#row -association)). | `self.can_associate = True` |

The [Table widget](../../widget/Table.md) also implements methods:

| Method                            | Description                |
| --------------------------------- | -------------------------- |
| `add_row(*args, **kwargs)` | Add a new row. The arguments depend on the number of columns in the table and can be either positional or keyword arguments.  See [adding rows](#adding-rows) for more information. |
| `remove_row(row)` | Remove an existing row. Specify either the row index (as an `int`) or the `Row` object to remove. See [removing rows](#removing-rows) for more information. arguments depend on the number of columns in the table and can be either positional or keyword arguments.  See [adding rows](#adding-rows) for more information. |
| `sort(key=None, reverse=False)` | Sort the table according to the given key, or the first column if no key is given. See [sorting rows](#sorting-rows) for more information. |
| `associate(row, obj)` | Associate a row with an arbitrary object. See [row association](#row -association) for more information. |

### Resetting the table

The table rows are not present in the layout.  As developer, you
will have to fill the table using methods, with
[init](../../control/init.md) controls for instance.

The most frequent way to reset an entire table is to use the
`rows` property.  Just set the `rows` property on the
[table widget](../../widget/Table.md) instance:

    def on_click_update(self):
        """A button of ID 'update' was clicked."""
        # There is a table of ID 'products' in the window
        table = self["products"]
        table.rows = (
            ("Pear", 10, 3.22),
            ("Minced beef", 2, 8.5),
            # ...
        )

The `rows` property can be a tuple of tuples (with each row being
defined in an inside tuple).  It can be a list of lists as well,
or another ordered sequence.  Rows can be
[Row objects](../../widget/Row.md) or dict instances.  In either case,
you should use the column name (or identifier) to represent
a column content.

    def on_click_update(self):
        """A button of ID 'update' was clicked."""
        # There is a table of ID 'products' in the window
        table = self["products"]
        table.rows = (
            {"name": "Pear", "quantity": 10, "cost": 3.22},
            {"name": "Minced beef", "quantity": 2, "cost": 8.5},
            # ...
        )

### Updating rows

To update a row, you can use the `[]` operator.  This is also
useful to query specific rows (or slices) from the table.

    row = table[0]
    print(row)
    # Or all the rows before table[4]
    rows = table[:4]

Again, when updating a row, you can use a
[row object](../../widget/Row.md), dictionary, tuple or list.

    table[2] = ("Lemon", 15, 2)
    # Or replace a row with another
    table[3] = table[1]
    # Now table[1] (row 2) and table[3] (row 4) will contain
    # the same data
    # You can also update multiple rows with this notation
    table[:2] = (
        ("Lemon", 15, 2),
        ("Apple", 20, 1),
    )
    # However, this might not be as easy to read.

### Adding rows

You also can use the `add_row` instance method on the
[table widget](../../widget/Table.md) to add one row:

    def on_click_update(self):
        """A button of ID 'update' was clicked."""
        # There is a table of ID 'products' in the window
        table = self["products"]
        table.add_row("Apple", 25, 3.15)
        # Or, more rreadable
        table.add_row(name="Apple", quantity=25, cost=3.15)

Use the method arguments to add a row (that is to say, if your table
has 5 columsns, you should specify 5 arguments to the method).
Simiarly, you can use named arguments to add a row.  If you need
to add a row from a list or dictionary, use the `*` or `**` syntax:

    def on_click_update(self):
        """A button of ID 'update' was clicked."""
        # There is a table of ID 'products' in the window
        table = self["products"]
        row = ("Apple", 25, 3.15)
        table.add_row(*row)
        # Or, more readable
        row = {"name": "Apple", "quantity": 25, "cost": 3.15}
        table.add_row(**row)

> Note: you cannot add columns to the table.  This constraint is
  made more logicial by the clear separation (columns are
  defined in layout, rows in code).

### Removing rows

To remove rows, you can use either the row indice (its position) or
the [row object](../../widget/Row.md) itself.

    def on_click_delete(self):
        """A button of ID 'delete' was clicked."""
        # There is a table of ID 'products' in the window
        table = self["products"]
        # Remove the first row
        table.remove_row(0)
        # Or use the row object
        row = table[0]
        table.remove_row(row)

### Sorting rows

The [table widget](../../widget/Table.md) also offers a `sort`
method, very much like a list.  It can be used in a similar pattern:

    from operator import attrgetter
    table.sort(key=attrgetter("price"), reverse=True)
    # Sort with the more expensive objects above

> Note: this method will make sure the selection in the table is
  not affected.  If the user was on the "Apple", then she will be on
  the "Apple" after the call to  sort`, even though the "apple" might
  have changed position in the table.

### Row selection

The [table widget](../../widget/Table.md) has a `selected`
property which you should use to know and change the
current selection.

By default, use this property to query the selected row in the table:

    row = table.selected

You can also change the selection:

    table.selected = 8 # select the ninth row
    # Or, using the row object
    row = table[3]
    table.selected = row

### Row association

BUI offers a quick way to associate a row with an object.  This
is often very useful when the table rows represent objects (which,
admittedly, can often be the case).  The concept of association
allows you to associate an object with a row, but not display the
said object to the user.

Consider this example from the [download
example]../../example/download.md).  You have a list of files
to download.  Files to download are objects of type `File`:

    class File:

        def __init__(self, name, url):
            self.name = name
            self.url = url
            self.progress = 0
            self.status = "unknown"
            # ...

When creating rows on these objects, you can display part of
the information, but keep the original objects because you will need
them in your code:

```python
table = self["download"]
for filename, url in FILES:
    file = File(filename, url)
    row = table.add_row(file.name, file.url, file.progress, file.status)
    table.associate(row, file)
```

When you browse the list of rows in the table, you will also have
access to their `File` object:

```python
table.can_associate = True # This is necessary
for row, file in table.rows:
    # file is the File object
    # while row is the information displayed to the user
```

To use this feature, first set the `can_associate` attribute of
table from `False` to `True`.  `can_associate` is `False` by
default.  While this will not prevent you from using the `associate`
method, it will affect return values of other methods.

Then use `associate`, specifying as first argument the
[row object](../../widget/Row.md) and as second argument, the
object to associate with it.

The `rows` property will return a list, not of rows, but of
`(row, associated object)` for each row:

    for row, file in table.rows:

Similarly, the `selected` property will return the selected row
and the associated object in a tuple:

    row, file = table.selected

When using the `rows` and `selected` property as setters (to
change data), they will work as usual:

    table.selected = 2

If this concept sounds extremely odd, you might want to first
associate a row with a dictionary: assuming you have some data,
associated with your rows, but you don't want to display them to
the user, how could you do it?

## Controls

| Control                         | Method       | Description      |
| ------------------------------- | ------------ | ---------------- |
| [focus](../../control/focus.md) | `on_focus` | The table is focused or lose focus. |
| [init](../../control/init.md) | `on_init` | The table is ready to be displayed, but is not displayed just yet. |
| [press](../../control/press.md) | `on_press` | The user presses on a key from her keyboard. This control can have sub-controls. |
| [release](../../ control/release.md) | `on_release` | The user relases a key on her keyboard. This control can have sub- controls. |
| [select](../../ control/select.md) | `on_select` | The table selection has changed. |
| [type](../../control/type.md) | `on_type` | The user types a character using her keyboard. This control can have sub-controls. |

    class MainWindow(Window):

        def on_select_products(self, widget, row):
            print(f"The user selected the row {row} in the table.")

