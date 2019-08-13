"""Module containing the generic Item class, a generic menu widget."""

from bui.widget.base import Widget, CachedProperty

class Item(Widget):

    """
    The generic item widget.

    An item is meant to be contained inside a `<menu>` tag.  It represents
    the last leaf of a menubar or toolbar, the one on which the user
    can click.  It is very likely you will associate a specific
    [window control](/control/overview.md) with a menu item.  See the
    [item](/layout/tag/item.md) tag for more details.

    This is a generic widget which will be converted into a specific widget,
    depending on the used GUI toolkit.

    """

    widget = "item"
    class_name = "Item"
    default_controls = {
        "click": "This menu item is being clicked on",
    }
    implicit_control = "click"

    def __init__(self, leaf):
        super().__init__(leaf)
        self.id = leaf.id
        self.data = leaf.data

    @CachedProperty
    def id(self):
        return self.leaf.id

    def handle_click(self, control):
        """Do nothing if a menu item is clicked."""
        pass
