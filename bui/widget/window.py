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

from pathlib import Path
import sys

from bui.widget.base import Widget

from bui.layout.parser import BUILayoutParser

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
                break

        return namespace

    @staticmethod
    def mark(layout: str) -> str:
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
        "press": "The user presses a key anywhere in the window",
    }

    # Can be overrideen by subclasses
    layout = ""
    bui = ""

    # Class attributes, to be overridden by instance attributes
    parsed_layout = None

    def __init__(self, leaf):
        super().__init__(leaf)
        self.control_methods = {}

    def __getitem__(self, item):
        for child in self.leaf.children:
            if child.id == item:
                return child.widget

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
    def parse_layout(cls, Window):
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
                filename = Path(__name__)
                bui = f"{filename.stem}.bui"

            with open(bui, 'r', encoding="utf-8") as file:
                layout = file.read()

            parser = BUILayoutParser(bui)

        parser.feed(layout)
        parsed_layout = parser.layout
        window_leaf = parsed_layout.get("window")
        if window_leaf is None:
            raise ValueError("the specified layout doesn't contain a <window> description")

        # Creates all the leafs
        from bui.widget import WIDGETS
        widgets = []
        for leaf in parsed_layout.flat:
            leaf.complete()
            if leaf is window_leaf:
                Generic = Window
            else:
                Generic = WIDGETS[leaf.tag_name]

            widget = Generic(leaf)
            leaf.widget = widget
            widget.create_specific()
            widgets.append(widget)
            if leaf is window_leaf:
                window = widget

        # Call the `_init` method on all generic widgets
        for widget in widgets:
            widget._bind_controls(window)
            widget._init()

            if widget.widget == "window":
                break

        window.parsed_layout = parsed_layout
        return window

    def _init(self):
        """Private method to initialize the generic and specific window."""
        self.specific._init()
        layout = self.leaf.layout

        # If the layout defines a menubar
        menubar = layout.get("menubar")
        if menubar:
            self.specific.create_menubar(menubar)

    def _start(self):
        """Start the window, block execution."""
        return self.specific._start()

    def close(self):
        """Close the window, terminate the loop if no window remain."""
        self.specific.close()
