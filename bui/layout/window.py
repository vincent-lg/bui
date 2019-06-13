"""Window object represented in layout."""

from bui.layout.attr import Attr
from bui.layout.component import Component

class Window(Component):

    tag_name = "window"
    attrs = (
        Attr("title", help="The window title"),
        Attr("width", help="The window width", type=int, default=100),
        Attr("height", help="The window height", type=int, default=100),
    )

    def __init__(self, layout, parent, title, width=0, height=0):
        super().__init__(layout, parent)
        self.title = title
        self.width = width
        self.height = height
