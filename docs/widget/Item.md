# Item in [widget/item:5](../raw/widget/item.html#L5)

The generic item widget.

An item is meant to be contained inside a `<menu>` tag.  It represents
the last leaf of a menubar or toolbar, the one on which the user
can click.  It is very likely you will associate a specific
[window control](/control/overview.md) with a menu item.  See the
[item](/layout/tag/item.md) tag for more details.

This is a generic widget which will be converted into a specific widget,
depending on the used GUI toolkit.

## Class summary

This class offers 3 methods.

| Method | Signature | Description |
| ------ | --------- | ----------- |
| [create_specific](#create_specific) | `create_specific()` | Create the specific widget, using the `specific_package` attribute. |
| [handle_click](#handle_click) | `handle_click(control)` | Do nothing if a menu item is clicked. |
| [schedule](#schedule) | `schedule(coroutine)` | Schedule the specified coroutine in the main event loop. |

## Methods

### create_specific

`create_specific(self)`

[See the source code](../raw/widget/item.html#L30)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Item` |  |

Create the specific widget, using the `specific_package` attribute.

If the specific object has already been created, don't recreate it and
raise no exception.

### handle_click

`handle_click(self, control)`

[See the source code](../raw/widget/item.html#L37)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Item` |  |
| control | *Not set* |  |

Do nothing if a menu item is clicked.

### schedule

`schedule(self, coroutine)`

[See the source code](../raw/widget/item.html#L75)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Item` |  |
| coroutine | *Not set* |  |

Schedule the specified coroutine in the main event loop.