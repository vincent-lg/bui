"""Module containing the generic Table class, a generic table widget."""

from typing import Dict, Iterable, List, Sequence, Tuple, Union

from bui.widget.base import Widget, CachedProperty

NO_VALUE = object()

class AbcRow:

    """
    Abstract row object.

    When a table widget is created, it holds a definition of a row
    (expected information in the table, deduced from the list of columns).
    A row object is a generic object representation of a table row.
    Each table has a different row object.  Do not create row objects
    manually, use the table methods to do so.

    """

    def __init__(self):
        raise TypeError("cannot instantiate abstract row")


Row = Union[dict, list, tuple, AbcRow]

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
        self.width = leaf.width
        self.height = leaf.height
        self.cols = []
        self.factory = None

    def __len__(self):
        return len(self._rows)

    def __getitem__(self, item):
        return self._rows[item]

    def __setitem__(self, item, row: Union[Row, Sequence[Row]]):
        if isinstance(item, int):
            items = slice(item, item + 1, 1)
            rows = [row]
        else:
            items = item
            rows = row

        cur_rows = self._rows[items]
        try:
            iter(rows)
            if len(rows) != len(cur_rows):
                raise TypeError
        except TypeError:
            raise TypeError("the number of rows doesn't match "
                    "the speicified indices") from None

        for cur_row, row in zip(cur_rows, rows):
            if isinstance(row, AbcRow) and not isinstance(row, self.factory):
                raise TypeError("the specified row isn't of the proper table")
            elif isinstance(row, dict):
                row = self.factory(cur_row.index, **row)
            else:
                row = self.factory(cur_row.index, *row)
            row.index = cur_row.index
            self.update_row(row)

    @CachedProperty
    def id(self):
        return self.leaf.id

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, rows: Iterable[Row]):
        """
        Modify the table rows.

        Args:
            rows (iterable): an iterable containing representations
                    of rows (can be Row objects specific to this table,
                    or tuple, list or dict).

        """
        try:
            iter(rows)
        except TypeError:
            raise TypeError("'rows' isn't a valid iterable")

        if not isinstance(rows, list):
            rows = list(rows)

        for i, row in enumerate(rows):
            if isinstance(row, (tuple, list)):
                row = self.factory(i, *row)
            elif isinstance(row, (dict)):
                row = self.factory(i, **row)
            elif not isinstance(row, self.factory):
                raise TypeError(f"invalid row type ({type(row)})")
            rows[i] = row

        self._rows[:] = rows
        self.specific.refresh(rows)
        return rows

    def _init(self):
        """Widget initialization."""
        self._rows = []
        for tag in self.leaf.children:
            if tag.tag_name == "col":
                self.cols.append((tag.id, tag.data))

        if len(self.cols) < 2:
            raise ValueError("a table must have at least two columns.  "
                    "Represent a table with one column using the "
                    "<list> tag instead.")

        self.factory = build_factory(self, self.cols)
        return super()._init()

    def add_row(self, *args, **kwargs):
        """
        Add a new row with the specified arguments at the bottom of the table.

        You should specify all the table columns as positional or
        keyword arguments.

        For instance, with a table defining 3 columns (name,
        price, and quantity):

            self.add_row("table", 30, 1)

        Or:

            self.add_row(name="table", price=30, quantity=1)

        """
        row = self.factory(len(self._rows), *args, **kwargs)
        self.update_row(row)
        return row

    def update_row(self, row):
        """Update the specified row."""
        index = row.index
        if index == len(self._rows):
            # Append the row
            self._rows.append(row)
        elif index > len(self._rows):
            for i in range(len(self._rows), index + 1):
                row = self._rows[i]
                self.update_row(row)
        else:
            old = self._rows[index]
            for i, (new_value, old_value) in enumerate(zip(row, old)):
                if new_value != old_value:
                    old[i] = new_value

        self.specific.update_row(row)

    def remove_row(self, row: Union[int, AbcRow]):
        """
        Remove a row in the table.

        Args:
            row (int or Row): the Row object to remove, or the
                    index of the row to remove.

        """
        if isinstance(row, int):
            row = self._rows[row]

        index = row.index
        del self._rows[index]
        for row in self._rows[index:]:
            row.index -= 1

        self.specific.remove_row(row)


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
                            f"{kwargs[col]!r} in keyword arguments.  You "
                            f"might be better off using either only "
                            f"positional, or only keyword arguments when "
                            f"creating a row")
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

    def row__getitem__(self, item):
        if isinstance(item, int):
            item = tuple(self._cols.keys())[item]

        return self._cols[item]

    def row__setitem__(self, item, value):
        if isinstance(item, int):
            item = tuple(self._cols.keys())[item]

        self._cols[item] = value

    def row__eq__(self, other):
        if isinstance(other, (tuple, list)):
            other = self.widget.factory(self.index, *other)
        elif isinstance(other, dict):
            other = self.widget.factory(self.index, **other)
        elif not isinstance(other, self.widget.factory):
            raise TypeError(f"cannot compare to {type(other)}")

        return self._cols == other._cols

    factory = type("Row", (AbcRow, ), {
            "widget": widget,
            "columns": [tup[0] for tup in cols],
            "__init__": row__init__,
            "__repr__": row__repr__,
            "__str__": row__str__,
            "__iter__": row__iter__,
            "__getattr__": row__getattr__,
            "__setattr__": row__setattr__,
            "__getitem__": row__getitem__,
            "__setitem__": row__setitem__,
            "__eq__": row__eq__,
    })
    return factory
