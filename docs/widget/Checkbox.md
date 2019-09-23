# Checkbox in [widget/checkbox:5](../raw/widget/checkbox.html#L5)

The generic checkbox widget.

A checkbox is meant to be contained inside a
[window](../layout/tag/window.md) tag.  It can have a label and can
be checked or not checked.

This is a generic widget which will be converted into a specific widget,
depending on the used GUI toolkit.

## Class summary

This class offers 2 properties.

| Property | Get | Set |
| -------- | --- | --- |
| [disabled](#disabled) | Return whether the checkbox is disabled or not. | **Can't write** |
| [enabled](#enabled) | Return whether the checkbox is enabled or not. | **Can't write** |

This class offers 10 methods.

| Method | Signature | Description |
| ------ | --------- | ----------- |
| [check](#check) | `check()` | Force check this checkbox. |
| [create_specific](#create_specific) | `create_specific()` | Create the specific widget, using the `specific_package` attribute. |
| [disable](#disable) | `disable()` | Disable the checkbox. |
| [enable](#enable) | `enable()` | Force-enable the checkbox. |
| [handle_check](#handle_check) | `handle_check(control)` | Do nothing if a checkbox is clicked. |
| [handle_init](#handle_init) | `handle_init(control)` | Do nothing if a checkbox is pressed. |
| [handle_press](#handle_press) | `handle_press(control)` | Do nothing if a checkbox is pressed. |
| [schedule](#schedule) | `schedule(coroutine)` | Schedule the specified coroutine in the main event loop. |
| [sleep](#sleep) | `sleep(seconds)` | Asynchronous sleep during the specified number of seconds. |
| [uncheck](#uncheck) | `uncheck()` | Force uncheck this checkbox. |

## Properties

### disabled

This property can only get (read-only).

#### Get

[See the source code](../raw/widget/checkbox.html#L68)

Return whether the checkbox is disabled or not.

### enabled

This property can only get (read-only).

#### Get

[See the source code](../raw/widget/checkbox.html#L63)

Return whether the checkbox is enabled or not.

## Methods

### check

`check(self)`

[See the source code](../raw/widget/checkbox.html#L73)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Checkbox` |  |

Force check this checkbox.

### create_specific

`create_specific(self)`

[See the source code](../raw/widget/checkbox.html#L30)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Checkbox` |  |

Create the specific widget, using the `specific_package` attribute.

If the specific object has already been created, don't recreate it and
raise no exception.

### disable

`disable(self)`

[See the source code](../raw/widget/checkbox.html#L85)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Checkbox` |  |

Disable the checkbox.

### enable

`enable(self)`

[See the source code](../raw/widget/checkbox.html#L81)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Checkbox` |  |

Force-enable the checkbox.

### handle_check

`handle_check(self, control)`

[See the source code](../raw/widget/checkbox.html#L89)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Checkbox` |  |
| control | *Not set* |  |

Do nothing if a checkbox is clicked.

### handle_init

`handle_init(self, control)`

[See the source code](../raw/widget/checkbox.html#L93)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Checkbox` |  |
| control | *Not set* |  |

Do nothing if a checkbox is pressed.

### handle_press

`handle_press(self, control)`

[See the source code](../raw/widget/checkbox.html#L97)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Checkbox` |  |
| control | *Not set* |  |

Do nothing if a checkbox is pressed.

### schedule

`schedule(self, coroutine)`

[See the source code](../raw/widget/checkbox.html#L75)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Checkbox` |  |
| coroutine | *Not set* |  |

Schedule the specified coroutine in the main event loop.

### sleep

`sleep(self, seconds)`

[See the source code](../raw/widget/checkbox.html#L79)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Checkbox` |  |
| seconds | *Not set* |  |

Asynchronous sleep during the specified number of seconds.

This method should ONLY be called in an asynchronous control method.
It is a shortcut to `asyncio.sleep`.

Args:
    seconds (int or float): the number of seconds to wait.

### uncheck

`uncheck(self)`

[See the source code](../raw/widget/checkbox.html#L77)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Checkbox` |  |

Force uncheck this checkbox.