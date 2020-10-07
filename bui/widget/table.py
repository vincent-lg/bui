"""Module containing the generic Table class, a generic table widget."""

from operator import itemgetter
from typing import (Any, Callable, Dict, Iterable, List, Optional,
        Sequence, Tuple, Union)

from bui.widget.base import Widget, CachedProperty

NO_VALUE = object()

class AbcRow:

    """
    Abstract row object.

    When a table widget is created, it holds a definition of a row
    (expected information in the table, deduced from the list of columns).
    A row object is a generic object representation of a table row.
    Each table has a different row class.  Do not create row objects
    manually, use the table methods to do so.  You can override the default
    row class for a table, but in this case, your row class should
    inherit `AbcRow`.

    """

    widget = None
    columns = ()

    def __init__(self, index, *args, **kwargs):
        if type(self) is AbcRow:
            raise TypeError("cannot instantiate abstract row")

        self._index = index
        self._cols = {}
        self._should_update = True
        used_args = 0
        ids = [tup[0] for tup in type(self).columns]
        for col, value in zip(ids, args):
            self._update(col, value)
            self._cols[col] = value
            used_args += 1

        for col in ids:
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
                    value = kwargs[col]
                    self._update(col, value)
                    self._cols[col] = value

        if not all(key in self._cols.keys() for key in ids):
            forgotten = [key for key in self.columns if key not in ids]
            raise ValueError(f"not all columns were specified: missing "
                    f"{', '.join(forgotten)}")

        if len(args) > used_args:
            unused = args[used_args:]
            unused = [str(arg) for arg in unused]
            raise ValueError(f"too many position arguments: {', '.join(unused)}")

        if any(key not in ids for key in kwargs.keys()):
            unused = [key for key in kwargs.keys() if key not in ids]
            raise ValueError(f"unused keyword arguments: {', '.join(unused)}")

    @property
    def index(self):
        return self._index

    def __repr__(self):
        args = [f"{key}={value!r}" for key, value in self._cols.items()]
        return f"<{type(self).__name__}({', '.join(args)})>"

    def __str__(self):
        args = [f"{key}={value}" for key, value in self._cols.items()]
        return f"{type(self).__name__} {', '.join(args)}"

    def __iter__(self):
        return iter(self._cols.values())

    @property
    def _visible(self):
        """Return only the visible columns."""
        visible = []
        for id, _, hidden in type(self).columns:
            if hidden:
                continue

            value = self._cols[id]
            visible.append(value)

        return tuple(visible)

    def __getattr__(self, attr):
        cols = object.__getattribute__(self, "_cols")
        value = cols.get(attr, NO_VALUE)
        if value is NO_VALUE:
            raise AttributeError(f"no {attr} column or attribute in this row")

        return value

    def __setattr__(self, attr, value):
        try:
            cols = object.__getattribute__(self, "_cols")
        except AttributeError:
            object.__setattr__(self, attr, value)
        else:
            if attr in cols:
                self._update(attr, value)
                cols[attr] = value
                if self._should_update:
                    self.widget.update_row(self)
            else:
                object.__setattr__(self, attr, value)

    def __getitem__(self, item):
        if isinstance(item, int):
            item = tuple(self._cols.keys())[item]

        return self._cols[item]

    def __setitem__(self, item, value):
        if isinstance(item, int):
            item = tuple(self._cols.keys())[item]

        self._update(item, value)
        self._cols[item] = value
        if self._should_update:
            self.widget.update_row(self)

    def __eq__(self, other):
        if isinstance(other, (tuple, list)):
            other = self.widget.factory(self._index, *other)
        elif isinstance(other, dict):
            other = self.widget.factory(self._index, **other)
        elif not isinstance(other, self.widget.row_classes):
            raise TypeError(f"cannot compare to {type(other)}")

        return self._cols == other._cols

    def _update(self, column: str, value: Any):
        if not self._should_update:
            return

        method = getattr(self, f"update_{column}", None)
        if method:
            method(value)


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
        "press": "The user presses on a key while the table is focused.",
        "select": "The table selection changes.",
        "release": "The user releases a key while the table is focused.",
        "type": "The user types a character while the table is focused.",
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
        self.row_class = None
        self._rows = []
        self._selected = 0

    def __str__(self):
        """Return a nice display of the table."""
        desc = super().__str__()
        rows = self.rows
        if rows:
            desc += "\nrows ("
            for row in rows:
                desc += f"\n    {row}"
            desc += "\n)"

        return desc

    @property
    def row_classes(self):
        """Return a tuple of the valid row classes for this widget."""
        if self.row_class:
            return (self.factory, self.row_class)

        return (self.factory, )

    def __len__(self):
        return len(self._rows)

    def __getitem__(self, item):
        row = self._rows[item]
        if isinstance(row, AbcRow):
            return row

        ret = []
        rows = row
        for row in rows:
            ret.append(row)

        return ret

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
            if isinstance(row, AbcRow) and not isinstance(row, self.row_classes):
                raise TypeError("the specified row isn't of the proper table")
            elif isinstance(row, dict):
                row = self.factory(cur_row._index, **row)
            else:
                row = self.factory(cur_row._index, *row)
            row._index = cur_row._index
            self.update_row(row)

    @CachedProperty
    def id(self):
        return self.leaf.id

    @property
    def rows(self):
        """Return the table rows."""
        return list(self._rows)

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
                row = self._create_row(i, *row)
            elif isinstance(row, (dict)):
                row = self._create_row(i, **row)
            elif not isinstance(row, self.row_classes):
                raise TypeError(f"invalid row type ({type(row)})")
            rows[i] = row

        self._rows[:] = rows
        self.specific.refresh(rows)
        return rows

    @property
    def selected(self):
        """Return the currently selected row."""
        try:
            row = self._rows[self._selected]
        except IndexError:
            row = None

        return row

    @selected.setter
    def selected(self, row: Union[int, Row]):
        """
        Select the given row or index.

        Args:
            row (int or Row): the row to select.

        """
        if isinstance(row, AbcRow):
            row = row._index
        self._selected = row
        self.specific.select_row(row)

    def _init(self):
        """Widget initialization."""
        for tag in self.leaf.children:
            if tag.tag_name == "col":
                self.cols.append((tag.id, tag.data, tag.hidden))

        if len(self.cols) < 2:
            raise ValueError("a table must have at least two columns.  "
                    "Represent a table with one column using the "
                    "<list> tag instead.")

        self.factory = build_factory(self, self.cols)
        return super()._init()

    def _create_row(self, index, *args, **kwargs):
        """
        Return a new row, either using the row factory or row class.

        The row factory is used to create generic rows without extra information beyond their column.  The row class, however, can be specified to change the default row class used by the rows.  If the row class hasn't been specified, use the factory.

        Args:
            index (int): the row index, mandatory no matter the row class.
            Extra arguments (either positional or optional) hold the
                    row columns.

        Raises:
            ValueError: the row couldn't be created.

        """
        if self.row_class:
            self.row_class.widget = self

        row_class = self.row_class or self.factory
        return row_class(index, *args, **kwargs)

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
        row = self._create_row(len(self._rows), *args, **kwargs)
        self.update_row(row)
        return row

    def update_row(self, row):
        """Update the specified row."""
        index = row._index
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

    def remove_row(self, row: Optional[Union[int, AbcRow]]):
        """
        Remove a row in the table.

        Args:
            row (int or Row): the Row object to remove, or the
                    index of the row to remove.

        """
        if row is None:
            return

        if isinstance(row, int):
            row = self._rows[row]

        index = row._index
        del self._rows[index]
        for next_row in self._rows[index:]:
            next_row._index -= 1

        self.specific.remove_row(row)

    def sort(self, key: Callable = None, reverse: bool = False):
        """
        Sort the table rows, given an optional key.

        This method is similar to the sort method of a list.  You
        can use it to sort using, by default, the first column, or by
        specifying a column key.

        Args:
            key (callable, optional): the key to call on every row.
            reverse (bool, optional): sort in reverse order.

        Example:
            >>> from operator import attrgetter
            >>> table.sort(key=attrgetter("grade"))

        """
        if key is None:
            key = itemgetter(0)

        selected = self._rows[self._selected]
        self._rows.sort(key=key, reverse=reverse)
        for index, row in zip(range(len(self._rows)), self._rows):
            row._index = index

        self.specific.sort(key=key, reverse=reverse)
        self.selected = selected


def build_factory(widget, cols):
    """Build a factory (dynamic class) for the specified columns."""
    factory = type("Row", (AbcRow, ), {
            "widget": widget,
            "columns": tuple(cols),
    })
    return factory
