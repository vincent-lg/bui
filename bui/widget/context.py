"""Module containing the generic Context class, a generic context widget."""

from bui.widget.base import Widget

class Context(Widget):

    """
    The generic context widget.

    A context menu is a menu, containing items or other menus, meant
    to be popped up (usually on right click, though other situations
    may arise as well).

    This is a generic widget which will be converted into a specific widget,
    depending on the used GUI toolkit.

    """

    widget = "context"
    class_name = "Context"

    def __init__(self, leaf):
        super().__init__(leaf)
        self.id = leaf.id
