# Layout tag: table

Create a table with columns.

A table is a list, except each item in the list is a row in the table.  A table has several columns with names.  The user can scroll through this table and select either only row or several rows at the same time.

```
<window title="Table demonstration">
  <table id=products x=2 y=4>
    <col>Name</col>
    <col>Quantity</col>
    <col>Cost</col>
  </table<
</window>
```

Using the `<table>` landmark creates an empty table, which will cause an error.  A table must at least have two columns (if one, use a simple [list](./list.html).  Use the `<col>` tag inside of the `<table>` to create a column in the table.

## Attributes

| Name         | Required | Description              | Example     |
| ------------ | -------- | ------------------------ | ----------- |
| `x` | Yes | The widget's horizontal position in columns (0 is left). This position is relative to the window width. | `<table x=5>` |
| `y` | Yes | The widget's vertical position in rows (0 is at the top). This position is relative to the window height. | `<table y=2>` |
| `id` | Yes | The table identifier (ID). Contrary to most other tags, you need to set this attribute. | `<table id=quit>` |

See also the [col](./col.md) tag to define the columns in a table.  This tag will need more information.

> Note : the table identifier is mandatory.  You cannot dcreate a table without validt identifier.  The reason for this constraint is due to the fact that this widget, in particular, will be edited in your application.  Lacking an identifier, you won't be able to do that.

## Data

The [table widget](../../widget/Table.md) can be manipulated to add and remove columsn, as well as add or remove rows.

| Attribute      | Meaning and type | Example                     |
| -------------- | ---------------- | --------------------------- |
| `rows` | The rows (list) | `self.rows = (("col 1", "col 2"))` |

You can easily update the entire table this way.  Just set the `rows` property on the [table widget](../../widget/Table.md) instance:

    def on_click_update(self):
        # A button of ID 'update' was clicked
        # There is a table of ID 'products' in the window
        table = self["products"]
        table.rows = (
            ("Pear", 10, 3.22),
            ("Minced beef", 2, 8.5),
            # ...
        )

The `rows` property can be a tuple of tuples (wich each row being defined in an inside tuple).  It can be a list of lists as well, or another ordered sequence.  Rows can be [Row objects](../../widget/Row.md) or dict instances.  In either case, you should use the column name (or identifier) to represent a column content.
    def on_click_update(self):
        # A button of ID 'update' was clicked
        # There is a table of ID 'products' in the window
        table = self["products"]
        table.rows = (
            {"name": "Pear", "quantity": 10, "cost": 3.22},
            {"name": "Minced beef", "quantity": 2, "cost": 8.5},
            # ...
        )

This will reset the entire table.  Alternatively, you can use the `add_row` or `add_column` instance methods on the [table widget](../../widget/Table.md):

    def on_click_update(self):
        # A button of ID 'update' was clicked
        # There is a table of ID 'products' in the window
        table = self["products"]
        table.add_row("Apple", 25, 3.15)
        # Or, more rreadable
        table.add_row(name="Apple", quantity=25, cost=3.15)

Use the method arguments to add a row (that is to say, if your table has 5 columsns, you should specify 5 arguments to the function).  Simiarly, you can use named arguments to add a row.  If you need to add a row from a list or dictionary, use the `*` or `**` syntax:

    def on_click_update(self):
        # A button of ID 'update' was clicked
        # There is a table of ID 'products' in the window
        table = self["products"]
        row = ("Apple", 25, 3.15)
        table.add_row(*row)
        # Or, more readable
        row = {"name": "Apple", "quantity": 25, "cost": 3.15}
        table.add_row(**row)

Use `add_column` indicating the name of the column to add to the table.  This should be discouraged, as the table structure should be indicated in thei layout and not modified afterward.

Use the indice of the row to remove it, or the [row object](../../class/Row.md) corresponding to it:

    def on_click_delete(self):
        # A button of ID 'delete' was clicked
        # There is a table of ID 'products' in the window
        table = self["products"]
        # Remove the first row
        del table.rows[0]
        # Or the last
        del table.rows[1]
        # Or, if you have a Row object
        row = table.rows[0]
        table.remove_row(row)
        # Or the last
        row = table.rows[-1]
        table.remove_row(row)

> A [Row object](../../class/Row.md) is a glorified named tuple.  It is used to represent a row but will also allow editing:

    def on_click_edit(self):
        # A button of ID 'edit' was clicked
        # There is a table of ID 'products' in the window
        table = self["products"]
        # Change the first row, update the second column
        table.rows[0][1] = 25
        # Or, more readable
        table.rows[0].quantity = 30

## Controls

| Control                           | Method       | Description    |
| --------------------------------- | ------------ | -------------- |
| [focus](../../control/focus.md) | `on_focus` | The table is focused or lose focus. |
| [select](../../control/select.md] | `on_select` | The table selection has changed. |

    class MainWindow(Window):

        def on_select_products(self, widget, row):
            print(f"The user selected the row {row} in the table.")

