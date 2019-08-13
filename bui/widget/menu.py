"""Module containing the generic Menu class, a generic menu widget."""

from bui.widget.base import Widget

class Menu(Widget):

    """
    The generic menu widget.

    A menu is meant to be contained inside either a `<menubar>` or
    `<toolbar>` tag.  It describes a menu (or a sub-menu), since a
    `<menu>` can contain another `<menu>`.  See the [menu](/layout/tag/menu.md)
    tag for more details.

    This is a generic widget which will be converted into a specific widget,
    depending on the used GUI toolkit.

    """

    widget = "menu"
    class_name = "Menu"

    def __init__(self, leaf):
        super().__init__(leaf)
        self.name = leaf.name
