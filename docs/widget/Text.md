# Text in [widget/text:7](../raw/widget/text.html#L7)

The generic text widget.

A text is meant to be contained inside a
[window](../layout/tag/window.md) tag.  The user can edit the content
of the text area which can be on one or several lines, cleared or
masked like a password.

This is a generic widget which will be converted into a specific widget,
depending on the used GUI toolkit.

## Class summary

This class offers 3 properties.

| Property | Get | Set |
| -------- | --- | --- |
| [cursor](#cursor) | Return the text Cursor object. | **Can't write** |
| [disabled](#disabled) | Return whether the text is disabled or not. | **Can't write** |
| [enabled](#enabled) | Return whether the text is enabled or not. | **Can't write** |

This class offers 5 methods.

| Method | Signature | Description |
| ------ | --------- | ----------- |
| [create_specific](#create_specific) | `create_specific()` | Create the specific widget, using the `specific_package` attribute. |
| [disable](#disable) | `disable()` | Disable the text. |
| [enable](#enable) | `enable()` | Force-enable the text. |
| [schedule](#schedule) | `schedule(coroutine)` | Schedule the specified coroutine in the main event loop. |
| [sleep](#sleep) | `sleep(seconds)` | Asynchronous sleep during the specified number of seconds. |

## Properties

### cursor

This property can only get (read-only).

#### Get

[See the source code](../raw/widget/text.html#L78)

Return the text Cursor object.

### disabled

This property can only get (read-only).

#### Get

[See the source code](../raw/widget/text.html#L73)

Return whether the text is disabled or not.

### enabled

This property can only get (read-only).

#### Get

[See the source code](../raw/widget/text.html#L68)

Return whether the text is enabled or not.

## Methods

### create_specific

`create_specific(self)`

[See the source code](../raw/widget/text.html#L30)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Text` |  |

Create the specific widget, using the `specific_package` attribute.

If the specific object has already been created, don't recreate it and
raise no exception.

### disable

`disable(self)`

[See the source code](../raw/widget/text.html#L87)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Text` |  |

Disable the text.

### enable

`enable(self)`

[See the source code](../raw/widget/text.html#L83)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Text` |  |

Force-enable the text.

### schedule

`schedule(self, coroutine)`

[See the source code](../raw/widget/text.html#L75)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Text` |  |
| coroutine | *Not set* |  |

Schedule the specified coroutine in the main event loop.

### sleep

`sleep(self, seconds)`

[See the source code](../raw/widget/text.html#L79)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Text` |  |
| seconds | *Not set* |  |

Asynchronous sleep during the specified number of seconds.

This method should ONLY be called in an asynchronous control method.
It is a shortcut to `asyncio.sleep`.

Args:
    seconds (int or float): the number of seconds to wait.