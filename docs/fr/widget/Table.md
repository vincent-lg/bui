# Table in [widget/table:29](../raw/widget/table.html#L29)

The generic table widget.

A table is to represent a list with several columns.  It needs to be
inside a [window](../layout/tag/window.md) tag.  It should have at
least two columns (see the [col](../layout/tag/col.md) tag) and can
be linked with specific control methods.

This is a generic widget which will be converted into a specific widget,
depending on the used GUI toolkit.

## Class summary

This class offers 2 properties.

| Property | Get | Set |
| -------- | --- | --- |
| [rows](#rows) | Return the table rows with optional associated objects. | Modify the table rows. |
| [selected](#selected) | Return the row and its associated object if needed. | Select the given row or index. |

This class offers 7 methods.

| Method | Signature | Description |
| ------ | --------- | ----------- |
| [add_row](#add_row) | `add_row(*args, **kwargs)` | Add a new row with the specified arguments at the bottom of the table. |
| [associate](#associate) | `associate(row: bui.widget.table.AbcRow, obj: Any)` | Associate the given row with an arbitrary object. |
| [create_specific](#create_specific) | `create_specific()` | Create the specific widget, using the `specific_package` attribute. |
| [remove_row](#remove_row) | `remove_row(row: Union[int, bui.widget.table.AbcRow])` | Remove a row in the table. |
| [schedule](#schedule) | `schedule(coroutine)` | Schedule the specified coroutine in the main event loop. |
| [sort](#sort) | `sort(key: Callable = None, reverse: bool = False)` | Sort the table rows, given an optional key. |
| [update_row](#update_row) | `update_row(row)` | Update the specified row. |

## Properties

### rows

This property can get and be set.

#### Get

[See the source code](../raw/widget/table.html#L121)

Return the table rows with optional associated objects.

#### Set

[See the source code](../raw/widget/table.html#L135)

Modify the table rows.

Args:
    rows (iterable): an iterable containing representations
            of rows (can be Row objects specific to this table,
            or tuple, list or dict).

### selected

This property can get and be set.

#### Get

[See the source code](../raw/widget/table.html#L167)

Return the row and its associated object if needed.

#### Set

[See the source code](../raw/widget/table.html#L176)

Select the given row or index.

Args:
    row (int or Row): the row to select.

## Methods

### add_row

`add_row(self, *args, **kwargs)`

[See the source code](../raw/widget/table.html#L204)

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

### associate

`associate(self, row: bui.widget.table.AbcRow, obj: Any)`

[See the source code](../raw/widget/table.html#L293)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Table` |  |
| row | `bui.widget.table.AbcRow` |  |
| obj | `Any` |  |

Associate the given row with an arbitrary object.

The given object can contain extra information that won't
be displayed on the table, but can be useful for the developer.
You can associate a row to an object and retrieve it,
either using the `selected` property, or the `associations`
generator.

Args:
    row (Row): the row to associate with the object.
    obj (any): the python object to associate with the row.

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

`remove_row(self, row: Union[int, bui.widget.table.AbcRow])`

[See the source code](../raw/widget/table.html#L243)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Table` |  |
| row | `Union[int, bui.widget.table.AbcRow]` |  |

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

### sort

`sort(self, key: Callable = None, reverse: bool = False)`

[See the source code](../raw/widget/table.html#L265)

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

[See the source code](../raw/widget/table.html#L225)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Table` |  |
| row | *Not set* |  |

Update the specified row.