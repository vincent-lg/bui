# Table in [widget/table:158](../raw/widget/table.html#L158)

The generic table widget.

A table is to represent a list with several columns.  It needs to be
inside a [window](../layout/tag/window.md) tag.  It should have at
least two columns (see the [col](../layout/tag/col.md) tag) and can
be linked with specific control methods.

This is a generic widget which will be converted into a specific widget,
depending on the used GUI toolkit.

## Class summary

This class offers 3 properties.

| Property | Get | Set |
| -------- | --- | --- |
| [row_classes](#row_classes) | Return a tuple of the valid row classes for this widget. | **Can't write** |
| [rows](#rows) | Return the table rows. | Modify the table rows. |
| [selected](#selected) | Return the currently selected row. | Select the given row or index. |

This class offers 7 methods.

| Method | Signature | Description |
| ------ | --------- | ----------- |
| [add_row](#add_row) | `add_row(*args, **kwargs)` | Add a new row with the specified arguments at the bottom of the table. |
| [create_specific](#create_specific) | `create_specific()` | Create the specific widget, using the `specific_package` attribute. |
| [remove_row](#remove_row) | `remove_row(row: Union[int, bui.widget.table.AbcRow, NoneType])` | Remove a row in the table. |
| [schedule](#schedule) | `schedule(coroutine)` | Schedule the specified coroutine in the main event loop. |
| [sleep](#sleep) | `sleep(seconds)` | Asynchronous sleep during the specified number of seconds. |
| [sort](#sort) | `sort(key: Callable = None, reverse: bool = False)` | Sort the table rows, given an optional key. |
| [update_row](#update_row) | `update_row(row)` | Update the specified row. |

## Properties

### row_classes

This property can only get (read-only).

#### Get

[See the source code](../raw/widget/table.html#L209)

Return a tuple of the valid row classes for this widget.

### rows

This property can get and be set.

#### Get

[See the source code](../raw/widget/table.html#L263)

Return the table rows.

#### Set

[See the source code](../raw/widget/table.html#L268)

Modify the table rows.

Args:
    rows (iterable): an iterable containing representations
            of rows (can be Row objects specific to this table,
            or tuple, list or dict).

### selected

This property can get and be set.

#### Get

[See the source code](../raw/widget/table.html#L300)

Return the currently selected row.

#### Set

[See the source code](../raw/widget/table.html#L310)

Select the given row or index.

Args:
    row (int or Row): the row to select.

## Methods

### add_row

`add_row(self, *args, **kwargs)`

[See the source code](../raw/widget/table.html#L359)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Table` |  |
| args | *Not set* |  |
| kwargs | *Not set* |  |

Add a new row with the specified arguments at the bottom of the table.

You should specify all the table columns as positional or
keyword arguments.

For instance, with a table defining 3 columns (name,
price, and quantity):

    self.add_row("table", 30, 1)

Or:

    self.add_row(name="table", price=30, quantity=1)

### create_specific

`create_specific(self)`

[See the source code](../raw/widget/table.html#L30)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Table` |  |

Create the specific widget, using the `specific_package` attribute.

If the specific object has already been created, don't recreate it and
raise no exception.

### remove_row

`remove_row(self, row: Union[int, bui.widget.table.AbcRow, NoneType])`

[See the source code](../raw/widget/table.html#L398)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Table` |  |
| row | `Union[int, bui.widget.table.AbcRow, NoneType]` |  |

Remove a row in the table.

Args:
    row (int or Row): the Row object to remove, or the
            index of the row to remove.

### schedule

`schedule(self, coroutine)`

[See the source code](../raw/widget/table.html#L75)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Table` |  |
| coroutine | *Not set* |  |

Schedule the specified coroutine in the main event loop.

### sleep

`sleep(self, seconds)`

[See the source code](../raw/widget/table.html#L79)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Table` |  |
| seconds | *Not set* |  |

Asynchronous sleep during the specified number of seconds.

This method should ONLY be called in an asynchronous control method.
It is a shortcut to `asyncio.sleep`.

Args:
    seconds (int or float): the number of seconds to wait.

### sort

`sort(self, key: Callable = None, reverse: bool = False)`

[See the source code](../raw/widget/table.html#L420)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Table` |  |
| key | `Callable` | `None` |
| reverse | `bool` | `False` |

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

### update_row

`update_row(self, row)`

[See the source code](../raw/widget/table.html#L380)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Table` |  |
| row | *Not set* |  |

Update the specified row.