"""Module containing the generic Table class, a generic table widget."""

from bui.widget.base import Widget, CachedProperty

NO_VALUE = object()

class Table(Widget):

    """
    The generic table widget.

    A table is to represent a list with several columns.  It needs to be
    inside a [window](../layout/tag/window.md) tag.  It should have at
    least two columns (see the [col](../layout/tag/col.md) tag) and can
    be linked with specific control methods.

    This is a generic widget which will be converted into a specific widget,
    depending on the used GUI toolkit.

    """

    widget = "table"
    class_name = "Table"
    default_controls = {
        #"focus": "The table gets or loses focus",
        "init": "The window is initialized",
        #"press": "The user presses on a key while the table is focused.",
        #"select": "The table selection changes.",
    }

    def __init__(self, leaf):
        super().__init__(leaf)
        self.x = leaf.x
        self.y = leaf.y
        self.id = leaf.id
        self.rows = []

        # Look for the <col> sub-tags
        self.cols = []
        self.factory = None
        self.length = 0

    @CachedProperty
    def id(self):
        return self.leaf.id

    @CachedProperty
    def rows(self):
        return self.specific.rows

    @rows.setter
    def rows(self, rows):
        if isinstance(rows, tuple):
            rows = list(rows)

        for i, row in enumerate(rows):
            if isinstance(row, (tuple, list)):
                row = self.factory(i, *row)
            elif isinstance(row, (dict)):
                row = self.factory(i, **row)
            rows[i] = row

        self.specific.rows = rows
        self.length = len(rows)
        return rows

    def _init(self):
        """Widget initialization."""
        for tag in self.leaf.children:
            if tag.tag_name == "col":
                self.cols.append((tag.id, tag.data))
        self.factory = build_factory(self, self.cols)
        super()._init()

    def add_row(self, *args, **kwargs):
        """Add a new row."""
        row = self.factory(self.length, *args, **kwargs)
        self.update_row(row)
        return row

    def update_row(self, row):
        """Update the specified row."""
        self.specific.update_row(row)
        self.length = len(self.rows)

    def handle_click(self, control):
        """Do nothing if a button is clicked."""
        pass

    def handle_press(self, control):
        """Do nothing if a button is pressed."""
        pass


def build_factory(widget, cols):
    """Build a factory (dynamic class) for the specified columns."""
    def row__init__(self, index, *args, **kwargs):
        self.index = index
        self._cols = {}
        used_args = 0
        for col, value in zip(self.columns, args):
            self._cols[col] = value
            used_args += 1

        for col in self.columns:
            if col in kwargs:
                if col in self._cols:
                    arg = self._cols[col]
                    raise ValueError(f"two values were specified for column "
                            f"{col!r}: {arg!r} in positional arguments, and "
                            f"{kwargs[col]} in keyword arguments. You might "
                            f"be better off using either only positional, "
                            f"or only keyword arguments when creating a row")
                else:
                    self._cols[col] = kwargs[col]

        if not all(key in self._cols.keys() for key in self.columns):
            forgotten = [key for key in self.columns if key not in self._cols.keys()]
            raise ValueError(f"not all columns were specified: missing "
                    f"{', '.join(forgotten)}")

        if len(args) > used_args:
            unused = args[used_args:]
            unused = [str(arg) for arg in unused]
            raise ValueError(f"too many position alguments: {', '.join(unused)}")
        if any(key not in self.columns for key in kwargs.keys()):
            unused = [key for key in kwargs.keys() if key not in self.columns]
            raise ValueError(f"unused keyword arguments: {', '.join(unused)}")

    def row__repr__(self):
        args = [f"{key}={value!r}" for key, value in self._cols.items()]
        return f"<Row({', '.join(args)})>"

    def row__str__(self):
        args = [f"{key}={value}" for key, value in self._cols.items()]
        return f"Row {', '.join(args)}"

    def row__iter__(self):
        return iter(self._cols.values())

    def row__getattr__(self, attr):
        cols = object.__getattribute__(self, "_cols")
        value = cols.get(attr, NO_VALUE)
        if value is NO_VALUE:
            raise AttributeError(f"no {attr} column or attribute in this row")

        return value

    def row__setattr__(self, attr, value):
        try:
            cols = object.__getattribute__(self, "_cols")
        except AttributeError:
            object.__setattr__(self, attr, value)
        else:
            if attr in cols:
                cols[attr] = value
                self.widget.update_row(self)
            else:
                object.__setattr__(self, attr, value)

    factory = type("Row", (), {
            "widget": widget,
            "columns": [tup[0] for tup in cols],
            "__init__": row__init__,
            "__repr__": row__repr__,
            "__str__": row__str__,
            "__iter__": row__iter__,
            "__getattr__": row__getattr__,
            "__setattr__": row__setattr__,
    })
    return factory
