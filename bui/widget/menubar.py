"""Module containing the generic MenuBar class, a generic menubar widget."""

from bui.widget.base import Widget

class Menubar(Widget):

    """
    The generic menubar widget.

    A menubar is a top-level widget, meaning it is not defined inside a
    `<window>` or `<dialog>` tag, but is a root element on the layout
    description.  It usually contains `<menu>` which can contain other
    `<menu>` or `<item>` widgets.  See more information on the
    [menubar](/layout/tag/menubar.md) tag.

    This is a generic widget which will be converted into a specific widget,
    depending on the used GUI toolkit.

    """

    widget = "menubar"
    class_name = "Menubar"
