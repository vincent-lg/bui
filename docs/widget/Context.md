# Context in [widget/context:5](../raw/widget/context.html#L5)

The generic context widget.

A context menu is a menu, containing items or other menus, meant
to be popped up (usually on right click, though other situations
may arise as well).

This is a generic widget which will be converted into a specific widget,
depending on the used GUI toolkit.

## Class summary

This class offers 3 methods.

| Method | Signature | Description |
| ------ | --------- | ----------- |
| [create_specific](#create_specific) | `create_specific()` | Create the specific widget, using the `specific_package` attribute. |
| [schedule](#schedule) | `schedule(coroutine)` | Schedule the specified coroutine in the main event loop. |
| [sleep](#sleep) | `sleep(seconds)` | Asynchronous sleep during the specified number of seconds. |

## Methods

### create_specific

`create_specific(self)`

[See the source code](../raw/widget/context.html#L30)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Context` |  |

Create the specific widget, using the `specific_package` attribute.

If the specific object has already been created, don't recreate it and
raise no exception.

### schedule

`schedule(self, coroutine)`

[See the source code](../raw/widget/context.html#L75)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Context` |  |
| coroutine | *Not set* |  |

Schedule the specified coroutine in the main event loop.

### sleep

`sleep(self, seconds)`

[See the source code](../raw/widget/context.html#L79)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Context` |  |
| seconds | *Not set* |  |

Asynchronous sleep during the specified number of seconds.

This method should ONLY be called in an asynchronous control method.
It is a shortcut to `asyncio.sleep`.

Args:
    seconds (int or float): the number of seconds to wait.