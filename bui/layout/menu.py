"""Menu object represented in layout."""

from bui.layout.attr import Attr
from bui.layout.component import Component

class Menu(Component):

    tag_name = "menu"
    attrs = (
        Attr("name", help="The menu name"),
    )

    def __init__(self, layout, parent, name):
        super().__init__(layout, parent)
        self.name = name
