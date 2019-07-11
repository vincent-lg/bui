"""Package containing layout tags."""

from bui.layout.button import Button
from bui.layout.checkbox import Checkbox
from bui.layout.col import Col
from bui.layout.item import Item
from bui.layout.menu import Menu
from bui.layout.menubar import Menubar
from bui.layout.table import Table
from bui.layout.text import Text
from bui.layout.window import Window

TAGS = {
    # name: (Class, (should be inside))
    "button": (Button, Window),
    "checkbox": (Checkbox, Window),
    "col": (Col, Table),
    "item": (Item, (Menu, )),
    "menu": (Menu, (Menubar, Menu)),
    "menubar": (Menubar, None),
    "table": (Table, Window),
    "text": (Text, Window),
    "window": (Window, None),
}
