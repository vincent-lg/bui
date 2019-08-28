# Menubar in [widget/menubar:5](../raw/widget/menubar.html#L5)

The generic menubar widget.

A menubar is a top-level widget, meaning it is not defined inside a
`<window>` or `<dialog>` tag, but is a root element on the layout
description.  It usually contains `<menu>` which can contain other
`<menu>` or `<item>` widgets.  See more information on the
[menubar](/layout/tag/menubar.md) tag.

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

[See the source code](../raw/widget/menubar.html#L30)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Menubar` |  |

Create the specific widget, using the `specific_package` attribute.

If the specific object has already been created, don't recreate it and
raise no exception.

### schedule

`schedule(self, coroutine)`

[See the source code](../raw/widget/menubar.html#L75)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Menubar` |  |
| coroutine | *Not set* |  |

Schedule the specified coroutine in the main event loop.