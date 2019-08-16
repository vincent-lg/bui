# Button in [widget/button:5](../raw/widget/button.html#L5)

The generic button widget.

A button is meant to be contained inside a
[window](../layout/tag/window.md) tag.  It can have a label and can
be linked with specific control methods.

This is a generic widget which will be converted into a specific widget,
depending on the used GUI toolkit.

## Class summary

This class offers 4 methods.

| Method | Signature | Description |
| ------ | --------- | ----------- |
| [create_specific](#create_specific) | `create_specific()` | Create the specific widget, using the `specific_package` attribute. |
| [handle_click](#handle_click) | `handle_click(control)` | Do nothing if a button is clicked. |
| [handle_press](#handle_press) | `handle_press(control)` | Do nothing if a button is pressed. |
| [schedule](#schedule) | `schedule(coroutine)` | Schedule the specified coroutine in the main event loop. |

## Methods

### create_specific

`create_specific(self)`

[See the source code](../raw/widget/button.html#L30)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Button` |  |

Create the specific widget, using the `specific_package` attribute.

If the specific object has already been created, don't recreate it and
raise no exception.

### handle_click

`handle_click(self, control)`

[See the source code](../raw/widget/button.html#L53)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Button` |  |
| control | `inspect._empty` |  |

Do nothing if a button is clicked.

### handle_press

`handle_press(self, control)`

[See the source code](../raw/widget/button.html#L65)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Button` |  |
| control | `inspect._empty` |  |

Do nothing if a button is pressed.

### schedule

`schedule(self, coroutine)`

[See the source code](../raw/widget/button.html#L75)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Button` |  |
| coroutine | `inspect._empty` |  |

Schedule the specified coroutine in the main event loop.