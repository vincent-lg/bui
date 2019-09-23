"""Table object represented in layout."""

from bui.layout.attr import Attr
from bui.layout.component import Component

class Table(Component):

    """
    Create a table with columns.

    A table is a list, except each item in the list is a
    [row](../../topic/table-row.md) in the table.
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

    Using the `<table>` tag creates an empty table, which will
    cause an error.  A table must at least have two columns (if one,
    use a simple [list](./list.html).  Use the `<col>` tag inside of the
    `<table>` to create a column in the table.

    Afterward, you will use methods on the
    [Table widget](../../widget/Table.md) directly to add, remove, sort
    [rows](./../topic/table-row.md), and optionally override the
    [row class](../../topic/table-row.md#customize-the-row-class)
    for this widget.

    ## Attributes

    | Name         | Required | Description              | Example     |
    | ------------ | -------- | ------------------------ | ----------- |
    | `x`          | Yes      | The widget's horizontal  | `<table     |
    |              |          | position in columns (0   | x=5>`       |
    |              |          | is left). This position  |             |
    |              |          | is relative to the       |             |
    |              |          | window width.            |             |
    | `y`          | Yes      | The widget's vertical    | `<table     |
    |              |          | position in rows (0      | y=2>`       |
    |              |          | is at the top). This     |             |
    |              |          | position is relative to  |             |
    |              |          | the window height.       |             |
    | `id`         | Yes      | The table identifier     | `<table     |
    |              |          | (ID). Contrary to most   | id=quit>`   |
    |              |          | other tags, you need to  |             |
    |              |          | set this attribute.      |             |
    | `width`      | No       | The widget width, that   | `<table     |
    |              |          | is, the number of        | width=2>`   |
    |              |          | columns it will use in   |             |
    |              |          | the window grid. A       |             |
    |              |          | widget with a width of   |             |
    |              |          | 2 will stretch one       |             |
    |              |          | additional column to the |             |
    |              |          | right. A widget with `x` |             |
    |              |          | set to 2 and `width` set |             |
    |              |          | to 3 will span `x=2`,    |             |
    |              |          | `x=3`, and `x=4`.  The   |             |
    |              |          | default is 1, so a       |             |
    |              |          | widget will remain in    |             |
    |              |          | its `x` column.          |             |
    | `height`     | No       | The widget height, that  | `<table     |
    |              |          | is, the number of        | height=2>`  |
    |              |          | rows it will use in      |             |
    |              |          | the window grid. A       |             |
    |              |          | widget with a height of  |             |
    |              |          | 2 will stretch one       |             |
    |              |          | additional row downward. |             |
    |              |          | A widget with `y` set    |             |
    |              |          | to 2 and `height` set    |             |
    |              |          | to 3 will span `y=2`,    |             |
    |              |          | `y=3`, and `y=4`.  The   |             |
    |              |          | default is 1, so a       |             |
    |              |          | widget will remain in    |             |
    |              |          | its `y` row.             |             |

    See also the [col](./col.md) tag to define the columns in a table.
    This tag will need more information.

    > Note: the table identifier is mandatory.  You cannot create
      a table without valid a identifier.  The reason for this constraint
      is that this widget, in particular, will be edited
      in your application.  Lacking an identifier, you won't be able
      to do that.

    ## Data

    The [table widget](../../widget/Table.md) can be manipulated to add
    and remove rows and perform additional operations.

    | Attribute      | Meaning and type | Example                     |
    | -------------- | ---------------- | --------------------------- |
    | `rows`         | The rows (list)  | `self.rows = (("col 1",     |
    |                |                  | "col 2"))`                  |
    | `selected`     | The selected     | `self.selected = 5`         |
    |                | row. Use this    |                             |
    |                | property to      |                             |
    |                | query the        |                             |
    |                | selected row or  |                             |
    |                | change the       |                             |
    |                | current          |                             |
    |                | selection.

    The [Table widget](../../widget/Table.md) also implements methods:

    | Method                            | Description                |
    | --------------------------------- | -------------------------- |
    | `add_row(*args, **kwargs)`        | Add a new row. The         |
    |                                   | arguments depend on the    |
    |                                   | number of columns in the   |
    |                                   | table and can be either    |
    |                                   | positional or keyword      |
    |                                   | arguments.  See [adding    |
    |                                   | rows](#adding-rows) for    |
    |                                   | more information.          |
    | `remove_row(row)`                 | Remove an existing row.    |
    |                                   | Specify either the row     |
    |                                   | index (as an `int`) or the |
    |                                   | `Row` object to remove.    |
    |                                   | See [removing              |
    |                                   | rows](#removing-rows) for  |
    |                                   | more information.          |
    | `sort(key=None, reverse=False)`   | Sort the table according   |
    |                                   | to the given key, or the   |
    |                                   | first column if no key is  |
    |                                   | given. See [sorting        |
    |                                   | rows](#sorting-rows) for   |
    |                                   | more information.          |

    ### Resetting the table

    The table rows are not present in the layout.  As a developer, you
    will have to fill the table using methods, with
    [init](../../control/init.md) control for instance.

    The most frequent way to reset an entire table is to use the
    `rows` property.  Just set the `rows` property on the
    [table widget](../../widget/Table.md) instance:

        def on_click_update(self):
            \"\"\"A button of ID 'update' was clicked.\"\"\"
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
    [Row objects](../../topic/table-row.md) or dict instances.  In either
    case, you should use the column name (or identifier) to represent
    a column content.

        def on_click_update(self):
            \"\"\"A button of ID 'update' was clicked.\"\"\"
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
    [row object](../../topic/table-row.md), dictionary, tuple or list.

        table[2] = ("Lemon", 15, 2)
        # Or replace a row with another
        table[3] = table[1]
        # Now table[1] (row 2) and table[3] (row 4) will contain
        # the same data
        # You can also update multiple rows with the slice notation
        table[:2] = (
            ("Lemon", 15, 2),
            ("Apple", 20, 1),
        )
        # However, this might not be as easy to read.

    ### Adding rows

    You also can use the `add_row` instance method on the
    [table widget](../../widget/Table.md) to add one row:

        def on_click_update(self):
            \"\"\"A button of ID 'update' was clicked.\"\"\"
            # There is a table of ID 'products' in the window
            table = self["products"]
            table.add_row("Apple", 25, 3.15)
            # Or, more rreadable
            table.add_row(name="Apple", quantity=25, cost=3.15)

    Use the method arguments to add a [row](../../topic/table-row.md)
    (that is to say, if your table has 5 columns, you should specify
    5 arguments to the method).
    Simiarly, you can use named arguments to add a row.  If you need
    to add a row from a list or dictionary, use the `*` or `**` syntax:

        def on_click_update(self):
            \"\"\"A button of ID 'update' was clicked.\"\"\"
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

    To remove rows, you can use either the row index (its position) or
    the [row object](../../topic/table-row.md) itself.

        def on_click_delete(self):
            \"\"\"A button of ID 'delete' was clicked.\"\"\"
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
      the "Apple" after the call to `sort`, even though the "apple" might
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

    ### Custom row class

    Sometimes, beyond the data we want to display in the table, we would
    like to associate data that is not visible to the user, but
    can be useful for the developer.  An example can be found in the
    [download example](../example/download.md) window: the download
    table contains columns that should be displayed to the user.  But
    it also contains additional data (like the URL associated with
    each file) that shouldn't be displayed to the user but would
    be used by the developer.  It's a bit like associating a row
    with a given object.

    BUI does it by allowing to override the default row class:
    each time a row is added in the table, a row object is created,
    behaving like a [namedtuple](https://docs.python.org/3/library/collections.html#collections.namedtuple).

    By default, these row objects are created from a dynamic class
    (one per table widget) containing the table structure.  You can,
    however, override this row class to create your own rows: these rows
    must contain exactly the expected data by the table (each row
    column), but they can contain additional data for each row too.

    This is a complex topic and is described in
    [its very own section](../../topic/table-row-class.md#customize-the-row-class).

    ## Controls

    | Control                         | Method       | Description      |
    | ------------------------------- | ------------ | ---------------- |
    | [focus](../../control/focus.md) | `on_focus`   | The table is     |
    |                                 |              | focused or lose  |
    |                                 |              | focus.           |
    | [init](../../control/init.md)   | `on_init`    | The table is     |
    |                                 |              | ready to be      |
    |                                 |              | displayed, but   |
    |                                 |              | is not displayed |
    |                                 |              | just yet.        |
    | [press](../../control/press.md) | `on_press`   | The user presses |
    |                                 |              | on a key from her|
    |                                 |              | keyboard. This   |
    |                                 |              | control can have |
    |                                 |              | sub-controls.    |
    | [release](../../                | `on_release` | The user         |
    | control/release.md)             |              | relases a key on |
    |                                 |              | her keyboard.    |
    |                                 |              | This control can |
    |                                 |              | have sub-        |
    |                                 |              | controls.        |
    | [select](../../                 | `on_select`  | The table        |
    | control/select.md)              |              | selection has    |
    |                                 |              | changed.         |
    | [type](../../control/type.md)   | `on_type`    | The user types   |
    |                                 |              | a character      |
    |                                 |              | using her        |
    |                                 |              | keyboard. This   |
    |                                 |              | control can have |
    |                                 |              | sub-controls.    |

        class MainWindow(Window):

            def on_select_products(self, widget, row):
                print(f"The user selected the row {row} in the table.")

    """

    tag_name = "table"
    attrs = (
        Attr("x", help="The widget horizontal position", type=int),
        Attr("y", help="The widget vertical position", type=int),
        Attr("id", help="The widget identifier"),
        Attr("width", help="The widget width", type=int, default=1),
        Attr("height", help="The widget height", type=int, default=1),
    )

    def __init__(self, layout, parent, x, y, id, width=1, height=1):
        super().__init__(layout, parent)
        self.x = x
        self.y = y
        self.id = id
        self.width = width
        self.height = height
