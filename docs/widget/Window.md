# Window in [widget/window:65](../raw/widget/window.html#L65)

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

This class offers 13 methods.

| Method | Signature | Description |
| ------ | --------- | ----------- |
| [close](#close) | `close()` | Close this window. |
| [create_specific](#create_specific) | `create_specific()` | Create the specific widget, using the `specific_package` attribute. |
| [handle_close](#handle_close) | `handle_close(control)` | The window closes. |
| [mark](#mark) | `mark(layout: str)` | Mark layout in the window. |
| [open_window](#open_window) | `open_window(window: 'Window', child=False)` | Open a new window. |
| [parse_layout](#parse_layout) | `parse_layout(Window, tag_name='window', **kwargs)` | Determine where the layout is and try to parse it, return a window. |
| [pop_alert](#pop_alert) | `pop_alert(title: str, message: str, danger: Union[str, NoneType] = 'error', ok: Union[bool, str, NoneType] = True, cancel: Union[bool, str, NoneType] = False, yes: Union[bool, str, NoneType] = False, no: Union[bool, str, NoneType] = False, default: Union[str, NoneType] = 'ok')` | Display a default message box for inforiation or errors. |
| [pop_dialog](#pop_dialog) | `pop_dialog(dialog: Union[str, Type[ForwardRef('wg.dialog.Dialog')]], **kwargs)` | Pop up a custom dialog, blocks until the dialog has been closed. |
| [pop_menu](#pop_menu) | `pop_menu(context_id: str)` | Pop a context menu, blocks until the menu is closed. |
| [pop_open_file](#pop_open_file) | `pop_open_file(message: str, location: pathlib.Path = None, filters: Sequence[Union[str, Tuple[str, str]]] = (), default: str = None, multiple: bool = False, preview: bool = True, hidden: bool = False)` | Display a system dialog to select one or several files. |
| [schedule](#schedule) | `schedule(coroutine)` | Schedule the specified coroutine in the main event loop. |
| [sleep](#sleep) | `sleep(seconds)` | Asynchronous sleep during the specified number of seconds. |
| [stop_control](#stop_control) | `stop_control()` | Stop the control, and the control method that called it. |

## Properties

### usable_surface

This property can only get (read-only).

#### Get

[See the source code](../raw/widget/window.html#L137)

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

[See the source code](../raw/widget/window.html#L256)

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

[See the source code](../raw/widget/window.html#L408)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Window` |  |
| control | *Not set* |  |

The window closes.

### mark

`mark(layout: str)`

[See the source code](../raw/widget/window.html#L53)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| layout | `str` |  |

Mark layout in the window.

### open_window

`open_window(self, window: 'Window', child=False)`

[See the source code](../raw/widget/window.html#L392)

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

`parse_layout(Window, tag_name='window', **kwargs)`

[See the source code](../raw/widget/window.html#L153)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| Window | *Not set* |  |
| tag_name | *Not set* | `'window'` |
| kwargs | *Not set* |  |

Determine where the layout is and try to parse it, return a window.

Raises:
    ValueError: the layout couldn't be parsed.

### pop_alert

`pop_alert(self, title: str, message: str, danger: Union[str, NoneType] = 'error', ok: Union[bool, str, NoneType] = True, cancel: Union[bool, str, NoneType] = False, yes: Union[bool, str, NoneType] = False, no: Union[bool, str, NoneType] = False, default: Union[str, NoneType] = 'ok')`

[See the source code](../raw/widget/window.html#L306)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Window` |  |
| title | `str` |  |
| message | `str` |  |
| danger | `Union[str, NoneType]` | `'error'` |
| ok | `Union[bool, str, NoneType]` | `True` |
| cancel | `Union[bool, str, NoneType]` | `False` |
| yes | `Union[bool, str, NoneType]` | `False` |
| no | `Union[bool, str, NoneType]` | `False` |
| default | `Union[str, NoneType]` | `'ok'` |

Display a default message box for inforiation or errors.

Args:
    title (str): the dialog title.
    message (str): the message title, can be on several lines.
    danger (str): the type of the dialog which will influence
            how noisy it is, what icon it displays and so on.
            Possible values are:
            "info": informative dialog, just to be polite.
            "warning": warning message, danger increases.
            "error": error message, probably can't go on.
            "quesiton": just a question to ask the user.
    ok (bool or str, optional): should a OK butotn appear?
    cancel (bool or str, optional): should a cancel button appear?
    yes (bool or str, optional): should a yes butotn appear?
    no (bool or str, optional): should a no butotn appear?
    default (str, optional): the name of the default button.

The button can either be set to True (only ok is set to True
by default), or contain a string of the button label to display.  A button with False will not appear.  For isntance:

    answer = await self.pop_alert(..., danger="question",
            ok="Go on anyway", cancel="Don't even try")
    if answer == "ok":
        # Go on

Returns:
    clicked button (str): the clicked button as a string,
            either "ok", "cancel", "yes", "no".
            Even if a different label has been set for these
            buttons, the string identifiers do not change.

### pop_dialog

`pop_dialog(self, dialog: Union[str, Type[ForwardRef('wg.dialog.Dialog')]], **kwargs)`

[See the source code](../raw/widget/window.html#L358)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Window` |  |
| dialog | `Union[str, Type[ForwardRef('wg.dialog.Dialog')]]` |  |
| kwargs | *Not set* |  |

Pop up a custom dialog, blocks until the dialog has been closed.

Args:
    dialog (str or Dialog): the dialog layout (as a str) or the
            Dialog class to instantiate from.

Returns:
    dialog (Dialog): the dialog object.  This object could
            contain "filled" information by the user.

### pop_menu

`pop_menu(self, context_id: str)`

[See the source code](../raw/widget/window.html#L381)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Window` |  |
| context_id | `str` |  |

Pop a context menu, blocks until the menu is closed.

Args:
    context_id (str): the registered ID of the context menu.

### pop_open_file

`pop_open_file(self, message: str, location: pathlib.Path = None, filters: Sequence[Union[str, Tuple[str, str]]] = (), default: str = None, multiple: bool = False, preview: bool = True, hidden: bool = False)`

[See the source code](../raw/widget/window.html#L264)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Window` |  |
| message | `str` |  |
| location | `pathlib.Path` | `None` |
| filters | `Sequence[Union[str, Tuple[str, str]]]` | `()` |
| default | `str` | `None` |
| multiple | `bool` | `False` |
| preview | `bool` | `True` |
| hidden | `bool` | `False` |

Display a system dialog to select one or several files.

This method displays a file system dialog, where the user can browse directories and select one or several files.  The selected file(s) will be returned if the user presses on the 'open' button in the dialog.  You can catch the result of this dialog to perform whatever operation you need.

Args:
    message (str): the message to display to the user.
    location (Path, optional): if not set, use the current
            directory.  Otherwise, you need to specify a
            `pathlib.Path` object.
    filters (sequence): a sequence of filters to apply to the file
            system list.  Each filter can be a string containing,
            between parenthesis, the pattern to apply.  Optionally
            a filter can be a tuple of two information:
            the pattern, and what to display to the user.  See
            the examples below of valid filters.
    default (str, optional): the default (selected) file, if any.
    multiple (bool, optional): allow to select several files
            (default False).
    preview (bool, optional): display a previoew of the file (default
            True).
    hidden (bool, optional): display hidden files (default False).

Returns:
    If `multiple` is not set, returns either `None` or the
    selected file, as a `pathlib.Path` object.
    If `multiple` is set to `True`, returns either an empty tuple,
    or a tuple of selected files, where each file is a
    `pathlib.Path` object.
    Returning `None` or an empty tuple indicates the user
    cancelled the operation (pressed on the Cancel button in
    the file system dialog).

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

[See the source code](../raw/widget/window.html#L79)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Window` |  |
| seconds | *Not set* |  |

Asynchronous sleep during the specified number of seconds.

This method should ONLY be called in an asynchronous control method.
It is a shortcut to `asyncio.sleep`.

Args:
    seconds (int or float): the number of seconds to wait.

### stop_control

`stop_control(self)`

[See the source code](../raw/widget/window.html#L260)

| Parameter | Type | Default |
| --------- | ---- | ------- |
| self | `Window` |  |

Stop the control, and the control method that called it.