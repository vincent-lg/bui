"""The Blind user Interface (BUI) package.

This package makes an internal bridge between simple, portable Python
code and a GUI toolkit installed on your system.

BUI documentation: https://vincent-lg.github.io/bui/

Package content:
    start: the start function, needing a Window class or str as argument.
    Window: the Window class.  Creating one will create a specific Window
            from a GUI toolkit, depending on what is available and on other
            considerations.

Additionally, importing this package will do some extra work to guess the
available GUI toolkit.  Therefore, if none is available, an exception will
be raised right when the module is imported, before anything can be done (or
attempted) with its classes.

"""

from bui.geometry import Point, Rectangle, Size
from bui.tools import start, PACKAGE
from bui.widget.base import Widget
from bui.widget.dialog import Dialog
from bui.widget.window import Window
Widget.specific_package = PACKAGE
name = "BUI"
version = "0.3.3"
