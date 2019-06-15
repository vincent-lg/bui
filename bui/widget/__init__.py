"""Package containing the generic widgets."""

from bui.widget.button import Button
from bui.widget.item import Item
from bui.widget.menu import Menu
from bui.widget.menubar import Menubar
from bui.widget.window import Window

WIDGETS = {
        "button": Button,
        "item": Item,
        "menu": Menu,
        "menubar": Menubar,
        "window": Window,
}
