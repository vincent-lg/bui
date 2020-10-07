"""Col object represented in layout."""

from bui.layout.attr import Attr
from bui.layout.component import Component

class Col(Component):

    """
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

    Using the `<table>` tag creates an empty table, which will cause
    an error.  A table must at least have two columns (if one, use
    a simple [list](./list.html).  Use the `<col>` tag inside of the
    `<table>` to create a column in the table.

    ## Attributes

    | Name         | Required | Description              | Example     |
    | ------------ | -------- | ------------------------ | ----------- |
    | `id`         | Yes      | The column identifier    | `<col       |
    |              |          | (ID). If not set, use    | id=name>`   |
    |              |          | the name specified as    |             |
    |              |          | data of the `<col>` tag. |             |
    | `hidden`     | No       | If present, this column  | `<col       |
    |              |          | will not appear to the   | hidden>`    |
    |              |          | user.  This can be       |             |
    |              |          | useful to store          |             |
    |              |          | identifiers or data to   |             |
    |              |          | be accessed by the       |             |
    |              |          | developer, but not       |             |
    |              |          | visible to the end user. |             |

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

    """

    tag_name = "col"
    attrs = (
        Attr("id", help="The widget identifier", default=""),
        Attr("hidden", help="The column is hidden to the user",
                default=False, if_present=True),
    )
    must_have_data = True
    has_widget = False

    def __init__(self, layout, parent, id, hidden=False):
        super().__init__(layout, parent)
        self.id = id
        self.hidden = hidden

    def complete(self):
        """Complete the tag, when all the layout has been set."""
        if not self.id:
            self.id = self.deduce_id(self.data)
