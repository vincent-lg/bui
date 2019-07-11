"""Package containing the generic widgets."""

from bui.widget.button import Button
from bui.widget.checkbox import Checkbox
from bui.widget.item import Item
from bui.widget.menu import Menu
from bui.widget.menubar import Menubar
from bui.widget.table import Table
from bui.widget.text import Text
from bui.widget.window import Window

WIDGETS = {
        "button": Button,
        "checkbox": Checkbox,
        "item": Item,
        "menu": Menu,
        "menubar": Menubar,
        "table": Table,
        "text": Text,
        "window": Window,
}
