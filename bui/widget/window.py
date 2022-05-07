"""The Window class.

This class is the main graphical content of any window.  With
[Dialog](dialog.md), chances are you won't need anything else as a
container for your windows.

The Window class contains the controls of your window, as user-defined
methods prefixed with `on`..  It can also contain data models and controls
of the contained widgets (graphical elements) in this window.  Optionally,
it can contain the window layout, though it's recommended to place this
layout in a separate [file](../layout/file.md).

"""

import asyncio
import inspect
from pathlib import Path
import sys
from typing import Optional, Sequence, Tuple, Type, Union

from bui.control.exceptions import StopControl
from bui.control.log import logger as control_logger
from bui.layout.parser import BUILayoutParser
from bui.tasks import cancel_all, run_remaining
from bui.widget.base import Widget
from bui import widget as wg

class MetaWindow(type):

    """
    Metaclass for the window class.

    It only traces the layout attribute for debugging purposes.

    """

    _marks = {}

    def __prepare__(name, bases, **kwargs):
        namespace = {
                "mark": MetaWindow.mark
        }

        # If one of the bases has a `close` method, put it in the namespace
        for base in bases:
            close = getattr(base, "close", None)
            if close:
                namespace["close"] = close
                namespace["stop_control"] = base.stop_control
                break

        return namespace

    @staticmethod
    def mark(layout: str) -> str:
        """Mark layout in the window."""
        frame = sys._getframe().f_back
        file = frame.f_globals["__file__"]
        line = frame.f_lineno
        line = line - len(layout.splitlines())
        qualname = frame.f_locals["__qualname__"]
        MetaWindow._marks[qualname] = (file, line)
        return layout


class Window(Widget, metaclass=MetaWindow):

    """
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

    """

    widget = "window"
    class_name = "Window"
    default_controls = {
        "close": "The window is ready to be closed",
        "init": "The window is ready to be displayed",
        "press": "The user presses a key anywhere in the window",
        "release": "The user releases a key anywhere in the window",
        "right_click": "The user right clicks in the window",
        "type": "The user types a character anywhere in the window",
    }

    # Can be overrideen by subclasses
    layout = ""
    bui = ""

    # Class attributes, to be overridden by instance attributes
    parsed_layout = None
    _bui_parent = None

    def __init__(self, leaf):
        super().__init__(leaf)
        self.control_methods = {}
        self.title = leaf.title
        self.width = leaf.width
        self.height = leaf.height
        self._ids = {}

    def __getitem__(self, item):
        try:
            return self._ids[item]
        except KeyError:
            raise KeyError(f"{item!r} isn't a known or valid "
                    "widget identifier") from None

    @property
    def usable_surface(self):
        """
        Return the screen size that can be used, in pixels.

        This size is returned in a tuple: (width, height), so that
        (x, y) follow the exact same pattern.  Both components are integers.

        Note that this is the screen surface being "free", that is,
        not counting the taskbar on some operating systems, since
        we cannot draw on that.  Therefore, the usable surface tends
        to be somewhat narrower than the screen resolution.

        """
        return self.specific.usable_surface

    @classmethod
    def parse_layout(cls, Window, tag_name="window", **kwargs):
        """
        Determine where the layout is and try to parse it, return a window.

        Raises:
            ValueError: the layout couldn't be parsed.

        """
        if cls.layout:
            layout = cls.layout

            # Try to find the first line and the proper file,
            # since the layout is defined in code
            qualname = cls.__qualname__
            file, line = MetaWindow._marks.get(qualname, ("__unknown__", 0))
            parser = BUILayoutParser(file, line)
        else:
            bui = cls.bui
            if not bui:
                filename = Path(inspect.getsourcefile(cls))
                if filename.is_absolute():
                    relative = filename.relative_to(Path().absolute())
                    bui = f"{relative.parent}/{relative.stem}.bui"
                else:
                    bui = f"{filename.parent}/{filename.stem}.bui"

            with open(bui, 'r', encoding="utf-8") as file:
                layout = file.read()

            parser = BUILayoutParser(bui)

        parser.feed(layout)
        parsed_layout = parser.layout
        window_leaf = parsed_layout.get(tag_name)
        if window_leaf is None:
            raise ValueError("the specified layout doesn't contain a <window> description")

        # Creates all the leafs
        from bui.widget import WIDGETS
        widgets = []
        ids = {}
        for leaf in parsed_layout.flat:
            leaf.complete()
            if not leaf.has_widget:
                continue
            elif leaf is window_leaf:
                Generic = Window
            else:
                Generic = WIDGETS[leaf.tag_name]

            widget = Generic(leaf)
            if leaf is window_leaf:
                for key, value in kwargs.items():
                    setattr(widget, key, value)

            leaf.widget = widget
            widget.create_specific()
            widgets.append(widget)
            if leaf is window_leaf:
                window = widget

            widget_id = getattr(widget, "id", None)
            if widget_id:
                ids[widget_id] = widget

        window._ids = ids

        # Call the `_init` method on all generic widgets
        control_logger.debug("  Binding control methods...")

        for widget in widgets:
            widget._bind_controls(window)
            widget._init()

        window.parsed_layout = parsed_layout
        for widget in widgets:
            widget.specific.process_control(None, "init")

        return window

    def _init(self):
        """Private method to initialize the generic and specific window."""
        self.specific._init()

    def _start(self, loop):
        """
        Start the window, watch events and allow async loop.

        Args:
            loop (AsyncLoop): the asynchronous event loop (see asyncio).

        """
        self.specific.show()
        return self.specific._start(loop)

    async def _stop(self):
        """Stop the window toolkit."""
        cancel_all()
        self.specific.process_control(None, "close", close=True)
        self.close()

    def close(self):
        """Close this window."""
        self.specific.close()

    def stop_control(self):
        """Stop the control, and the control method that called it."""
        raise StopControl()

    def pop_open_file(self, message: str, location: Path = None,
            filters: Sequence[Union[str, Tuple[str, str]]] = (),
            default: str = None, multiple: bool = False,
            preview: bool = True, hidden: bool = False
            ) -> Optional[Union[Path, Tuple[Path]]]:
        """
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

        """



    async def pop_alert(self, title: str, message: str,
            danger: Optional[str] = "error",
            ok: Optional[Union[bool, str]] = True,
            cancel: Optional[Union[bool, str]] = False,
            yes: Optional[Union[bool, str]] = False,
            no: Optional[Union[bool, str]] = False,
            default: Optional[str] = "ok"):
        """
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

        """
        buttons = {}
        if ok: buttons["ok"] = ok
        if cancel: buttons["cancel"] = cancel
        if yes: buttons["yes"] = yes
        if no: buttons["no"] = no
        if default not in buttons.keys():
            raise ValueError(f"{default!r} isn't in this alert box buttons")

        return await self.specific.pop_alert(title=title, message=message,
                danger=danger, buttons=buttons, default=default)

    async def pop_dialog(self, dialog: Union[str, Type['wg.dialog.Dialog']],
            **kwargs) -> 'wg.dialog.Dialog':
        """
        Pop up a custom dialog, blocks until the dialog has been closed.

        Args:
            dialog (str or Dialog): the dialog layout (as a str) or the
                    Dialog class to instantiate from.

        Returns:
            dialog (Dialog): the dialog object.  This object could
                    contain "filled" information by the user.

        """
        from bui.widget.dialog import Dialog
        if isinstance(dialog, str):
            class NewDialog(Dialog):
                layout = mark(dialog)
            dialog = NewDialog
        assert issubclass(dialog, wg.dialog.Dialog)
        dialog.window = self
        return await self.specific.pop_dialog(dialog, **kwargs)

    def pop_menu(self, context_id: str):
        """
        Pop a context menu, blocks until the menu is closed.

        Args:
            context_id (str): the registered ID of the context menu.

        """
        context = self[context_id]
        self.specific.pop_menu(context.specific)

    def open_window(self, window: "Window", child=False):
        """
        Open a new window.

        Args:
            window (Window): the window class.
            child (bool): if True, the new window will be a child of the
                    current window (closing self will close the new window).

        """
        if child:
            window._bui_parent = self

        self.specific.open_window(window, child=child)
        return window

    def handle_close(self, control):
        """The window closes."""
        pass
