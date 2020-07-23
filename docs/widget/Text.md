# Text in [widget/text:7](../raw/widget/text.html#L7)

The generic text widget.

A text is meant to be contained inside a
[window](../layout/tag/window.md) tag.  The user can edit the content
of the text area which can be on one or several lines, cleared or
masked like a password.

This is a generic widget which will be converted into a specific widget,
depending on the used GUI toolkit.

## Class summary

This class offers 4 properties.

| Property | Get | Set |
| -------- | --- | --- |
| [cursor](#cursor) | Return the text Cursor object. | **Can't write** |
| [disabled](#disabled) | Return whether the text is disabled or not. | **Can't write** |
| [enabled](#enabled) | Return whether the text is enabled or not. | **Can't write** |
| [hidden](#hidden) | Return whether the text is hidden or not. | **Can't write** |

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

[See the source code](../raw/widget/text.html#L79)

Return the text Cursor object.

### disabled

This property can only get (read-only).

#### Get

[See the source code](../raw/widget/text.html#L74)

Return whether the text is disabled or not.

### enabled

This property can only get (read-only).

#### Get

[See the source code](../raw/widget/text.html#L69)

Return whether the text is enabled or not.

### hidden

This property can only get (read-only).

#### Get

[See the source code](../raw/widget/text.html#L84)

Return whether the text is hidden or not.

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

[See the source code](../raw/widget/text.html#L93)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Text` |  |

Disable the text.

### enable

`enable(self)`

[See the source code](../raw/widget/text.html#L89)

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