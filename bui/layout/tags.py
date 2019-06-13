"""Module containing a list of tags, maching with the layout classes."""

from bui.layout.item import Item
from bui.layout.menu import Menu
from bui.layout.menubar import Menubar
from bui.layout.window import Window

TAGS = {
    # name: (Class, (should be inside))
    "item": (Item, (Menu, )),
    "menu": (Menu, (Menubar, Menu)),
    "menubar": (Menubar, None),
    "window": (Window, None),
}
