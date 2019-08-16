# Dialog in [widget/dialog:10](../raw/widget/dialog.html#L10)

The Dialog main class.

A Dialog is similar to a Window, in that it can contain various
widgets and control methods.  A dialog is popped from a
window, however.

## Class summary

This class offers 1 property.

| Property | Get | Set |
| -------- | --- | --- |
| [usable_surface](#usable_surface) | Return the screen size that can be used, in pixels. | **Can't write** |

This class offers 10 methods.

| Method | Signature | Description |
| ------ | --------- | ----------- |
| [close](#close) | `close()` | Close this window. |
| [create_specific](#create_specific) | `create_specific()` | Create the specific widget, using the `specific_package` attribute. |
| [handle_close](#handle_close) | `handle_close(control)` | The window closes. |
| [mark](#mark) | `mark(layout: str)` | Mark layout in the window. |
| [open_window](#open_window) | `open_window(window: 'Window', child=False)` | Open a new window. |
| [parse_layout](#parse_layout) | `parse_layout(Window, tag_name='window')` | Determine where the layout is and try to parse it, return a window. |
| [pop_dialog](#pop_dialog) | `pop_dialog(dialog: Union[str, Type[ForwardRef('wg.dialog.Dialog')]])` | Pop up a dialog, blocks until the dialog has been closed. |
| [pop_menu](#pop_menu) | `pop_menu(context_id: str)` | Pop a context menu, blocks until the menu is closed. |
| [schedule](#schedule) | `schedule(coroutine)` | Schedule the specified coroutine in the main event loop. |
| [sleep](#sleep) | `sleep(seconds)` | Asynchronous sleep during the specified number of seconds. |

## Properties

### usable_surface

This property can only get (read-only).

#### Get

[See the source code](../raw/widget/dialog.html#L131)

Return the screen size that can be used, in pixels.

This size is returned in a tuple: (width, height), so that
(x, y) follow the exact same pattern.  Both components are integers.

Note that this is the screen surface being "free", that is,
not counting the taskbar on some operating systems, since
we cannot draw on that.  Therefore, the usable surface tends
to be somewhat narrower than the screen resolution.

## Methods

### close

`close(self)`

[See the source code](../raw/widget/dialog.html#L252)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Dialog` |  |

Close this window.

### create_specific

`create_specific(self)`

[See the source code](../raw/widget/dialog.html#L30)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Dialog` |  |

Create the specific widget, using the `specific_package` attribute.

If the specific object has already been created, don't recreate it and
raise no exception.

### handle_close

`handle_close(self, control)`

[See the source code](../raw/widget/dialog.html#L305)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Dialog` |  |
| control | *Not set* |  |

The window closes.

### mark

`mark(layout: str)`

[See the source code](../raw/widget/dialog.html#L50)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| layout | `str` |  |

Mark layout in the window.

### open_window

`open_window(self, window: 'Window', child=False)`

[See the source code](../raw/widget/dialog.html#L291)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Dialog` |  |
| window | `'Window'` |  |
| child | *Not set* | `False` |

Open a new window.

Args:
    window (Window): the window class.
    child (bool): if True, the new window will be a child of the
            current window (closing self will close the new window).

### parse_layout

`parse_layout(Window, tag_name='window')`

[See the source code](../raw/widget/dialog.html#L147)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| Window | *Not set* |  |
| tag_name | *Not set* | `'window'` |

Determine where the layout is and try to parse it, return a window.

Raises:
    ValueError: the layout couldn't be parsed.

### pop_dialog

`pop_dialog(self, dialog: Union[str, Type[ForwardRef('wg.dialog.Dialog')]])`

[See the source code](../raw/widget/dialog.html#L256)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Dialog` |  |
| dialog | `Union[str, Type[ForwardRef('wg.dialog.Dialog')]]` |  |

Pop up a dialog, blocks until the dialog has been closed.

Args:
    dialog (str or Dialog): the dialog layout (as a str) or the
            Dialog class to instantiate from.

Returns:
    dialog (Dialog): the dialog object.

### pop_menu

`pop_menu(self, context_id: str)`

[See the source code](../raw/widget/dialog.html#L280)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Dialog` |  |
| context_id | `str` |  |

Pop a context menu, blocks until the menu is closed.

Args:
    context_id (str): the registered ID of the context menu.

### schedule

`schedule(self, coroutine)`

[See the source code](../raw/widget/dialog.html#L75)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Dialog` |  |
| coroutine | *Not set* |  |

Schedule the specified coroutine in the main event loop.

### sleep

`sleep(self, seconds)`

[See the source code](../raw/widget/dialog.html#L217)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Dialog` |  |
| seconds | *Not set* |  |

Asynchronous sleep during the specified number of seconds.

This method should ONLY be called in an asynchronous control method.
It is a shortcut to `asyncio.sleep`.

Args:
    seconds (int or float): the number of seconds to wait.