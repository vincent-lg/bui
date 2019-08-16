# Window in [widget/window:62](../raw/widget/window.html#L62)

The Window main class.

Instanciating it (with `Window()`) will attempt to create and return an
object of a specific GUI toolkit.  This object will inherit from `Window`
and will have the exact same methods and attributes.  You should remain
blessfully ignorant of the real class you use.  BUI is designed in such
a way that you can ignore how it does its magic for a particular
GUI toolkit, except if you're coding for such a toolkit.

Class attributes:
    layout (str, optional): the optional window layout, if it is not
            defined in a separate [file](../layout/file.md).  It is
            recommended to not use this class attribute, but you still
            can do so, if you have your reasons.
    bui (str, optional): the path leading to the `.bui` file
            containing your layout.  By default, this is in the same
            folder and has the same name as the Python file containing
            your Window class, except it has the `.bui` extension.  If
            you use this naming convention, you don't have to override
            the `bui` class attribute.  Otherwise, give it a relative
            or absolute path: absolute paths consider their root to be
            the user directory when the Python application started
            (which might not be the same as the directory in which
            your Python file is contained).

[Controls]../control/overview.md] are defined as methods on this
class.  By convention, their name starts with `on_`, like `on_focus` or
`on_quit`.  You can also watch for widget controls (execute a method
when a button is pressed, for instance).  In this case, you can create
`on_{control verb}_{control ID}` like `on_click_button`.  BUI will
attempt to connect `on*` methods with controls and will tell you if
it fails, or has a doubt.

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

[See the source code](../raw/widget/window.html#L133)

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

[See the source code](../raw/widget/window.html#L258)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Window` |  |

Close this window.

### create_specific

`create_specific(self)`

[See the source code](../raw/widget/window.html#L30)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Window` |  |

Create the specific widget, using the `specific_package` attribute.

If the specific object has already been created, don't recreate it and
raise no exception.

### handle_close

`handle_close(self, control)`

[See the source code](../raw/widget/window.html#L311)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Window` |  |
| control | *Not set* |  |

The window closes.

### mark

`mark(layout: str)`

[See the source code](../raw/widget/window.html#L50)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| layout | `str` |  |

Mark layout in the window.

### open_window

`open_window(self, window: 'Window', child=False)`

[See the source code](../raw/widget/window.html#L297)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Window` |  |
| window | `'Window'` |  |
| child | *Not set* | `False` |

Open a new window.

Args:
    window (Window): the window class.
    child (bool): if True, the new window will be a child of the
            current window (closing self will close the new window).

### parse_layout

`parse_layout(Window, tag_name='window')`

[See the source code](../raw/widget/window.html#L149)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| Window | *Not set* |  |
| tag_name | *Not set* | `'window'` |

Determine where the layout is and try to parse it, return a window.

Raises:
    ValueError: the layout couldn't be parsed.

### pop_dialog

`pop_dialog(self, dialog: Union[str, Type[ForwardRef('wg.dialog.Dialog')]])`

[See the source code](../raw/widget/window.html#L262)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Window` |  |
| dialog | `Union[str, Type[ForwardRef('wg.dialog.Dialog')]]` |  |

Pop up a dialog, blocks until the dialog has been closed.

Args:
    dialog (str or Dialog): the dialog layout (as a str) or the
            Dialog class to instantiate from.

Returns:
    dialog (Dialog): the dialog object.

### pop_menu

`pop_menu(self, context_id: str)`

[See the source code](../raw/widget/window.html#L286)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Window` |  |
| context_id | `str` |  |

Pop a context menu, blocks until the menu is closed.

Args:
    context_id (str): the registered ID of the context menu.

### schedule

`schedule(self, coroutine)`

[See the source code](../raw/widget/window.html#L75)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Window` |  |
| coroutine | *Not set* |  |

Schedule the specified coroutine in the main event loop.

### sleep

`sleep(self, seconds)`

[See the source code](../raw/widget/window.html#L223)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Window` |  |
| seconds | *Not set* |  |

Asynchronous sleep during the specified number of seconds.

This method should ONLY be called in an asynchronous control method.
It is a shortcut to `asyncio.sleep`.

Args:
    seconds (int or float): the number of seconds to wait.