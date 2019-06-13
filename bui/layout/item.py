"""Item object represented in layout."""

from bui.layout.attr import Attr
from bui.layout.component import Component

class Item(Component):

    tag_name = "item"
    attrs = (
        Attr("id", help="The widget identifier", default=""),
    )
    must_have_data = True

    def __init__(self, layout, parent, id):
        super().__init__(layout, parent)
        self.id = id

    def complete(self):
        """Complete the widet, when all the layout has been set."""
        if not self.id:
            self.id = self.deduce_id(self.data)
