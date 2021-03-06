# Menu in [widget/menu:5](../raw/widget/menu.html#L5)

The generic menu widget.

A menu is meant to be contained inside either a `<menubar>` or
`<toolbar>` tag.  It describes a menu (or a sub-menu), since a
`<menu>` can contain another `<menu>`.  See the [menu](/layout/tag/menu.md)
tag for more details.

This is a generic widget which will be converted into a specific widget,
depending on the used GUI toolkit.

## Class summary

This class offers 2 methods.

| Method | Signature | Description |
| ------ | --------- | ----------- |
| [create_specific](#create_specific) | `create_specific()` | Create the specific widget, using the `specific_package` attribute. |
| [schedule](#schedule) | `schedule(coroutine)` | Schedule the specified coroutine in the main event loop. |

## Methods

### create_specific

`create_specific(self)`

[See the source code](../raw/widget/menu.html#L30)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Menu` |  |

Create the specific widget, using the `specific_package` attribute.

If the specific object has already been created, don't recreate it and
raise no exception.

### schedule

`schedule(self, coroutine)`

[See the source code](../raw/widget/menu.html#L75)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Menu` |  |
| coroutine | *Not set* |  |

Schedule the specified coroutine in the main event loop.