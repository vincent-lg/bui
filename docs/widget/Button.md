# Button in [widget/button:5](../raw/widget/button.html#L5)

The generic button widget.

A button is meant to be contained inside a
[window](../layout/tag/window.md) tag.  It can have a label and can
be linked with specific control methods.

This is a generic widget which will be converted into a specific widget,
depending on the used GUI toolkit.

## Class summary

This class offers 2 properties.

| Property | Get | Set |
| -------- | --- | --- |
| [disabled](#disabled) | Return whether the checkbox is disabled or not. | **Can't write** |
| [enabled](#enabled) | Return whether the checkbox is enabled or not. | **Can't write** |

This class offers 7 methods.

| Method | Signature | Description |
| ------ | --------- | ----------- |
| [after_click](#after_click) | `after_click(control)` | Close the dialog if the button was set. |
| [create_specific](#create_specific) | `create_specific()` | Create the specific widget, using the `specific_package` attribute. |
| [disable](#disable) | `disable()` | Disable the checkbox. |
| [enable](#enable) | `enable()` | Force-enable the checkbox. |
| [handle_press](#handle_press) | `handle_press(control)` | Do nothing if a button is pressed. |
| [schedule](#schedule) | `schedule(coroutine)` | Schedule the specified coroutine in the main event loop. |
| [sleep](#sleep) | `sleep(seconds)` | Asynchronous sleep during the specified number of seconds. |

## Properties

### disabled

This property can only get (read-only).

#### Get

[See the source code](../raw/widget/button.html#L61)

Return whether the checkbox is disabled or not.

### enabled

This property can only get (read-only).

#### Get

[See the source code](../raw/widget/button.html#L56)

Return whether the checkbox is enabled or not.

## Methods

### after_click

`after_click(self, control)`

[See the source code](../raw/widget/button.html#L74)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Button` |  |
| control | *Not set* |  |

Close the dialog if the button was set.

### create_specific

`create_specific(self)`

[See the source code](../raw/widget/button.html#L30)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Button` |  |

Create the specific widget, using the `specific_package` attribute.

If the specific object has already been created, don't recreate it and
raise no exception.

### disable

`disable(self)`

[See the source code](../raw/widget/button.html#L70)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Button` |  |

Disable the checkbox.

### enable

`enable(self)`

[See the source code](../raw/widget/button.html#L66)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Button` |  |

Force-enable the checkbox.

### handle_press

`handle_press(self, control)`

[See the source code](../raw/widget/button.html#L86)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Button` |  |
| control | *Not set* |  |

Do nothing if a button is pressed.

### schedule

`schedule(self, coroutine)`

[See the source code](../raw/widget/button.html#L75)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Button` |  |
| coroutine | *Not set* |  |

Schedule the specified coroutine in the main event loop.

### sleep

`sleep(self, seconds)`

[See the source code](../raw/widget/button.html#L79)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Button` |  |
| seconds | *Not set* |  |

Asynchronous sleep during the specified number of seconds.

This method should ONLY be called in an asynchronous control method.
It is a shortcut to `asyncio.sleep`.

Args:
    seconds (int or float): the number of seconds to wait.