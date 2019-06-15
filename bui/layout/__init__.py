"""Package containing layout tags."""

from bui.layout.button import Button
from bui.layout.item import Item
from bui.layout.menu import Menu
from bui.layout.menubar import Menubar
from bui.layout.window import Window

TAGS = {
    # name: (Class, (should be inside))
    "button": (Button, Window),
    "item": (Item, (Menu, )),
    "menu": (Menu, (Menubar, Menu)),
    "menubar": (Menubar, None),
    "window": (Window, None),
}
