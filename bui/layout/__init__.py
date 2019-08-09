"""Package containing layout tags."""

from bui.layout.button import Button
from bui.layout.checkbox import Checkbox
from bui.layout.choice import Choice
from bui.layout.col import Col
from bui.layout.dialog import Dialog
from bui.layout.item import Item
from bui.layout.menu import Menu
from bui.layout.menubar import Menubar
from bui.layout.radio import RadioButton
from bui.layout.table import Table
from bui.layout.text import Text
from bui.layout.window import Window

TAGS = {
    # name: (Class, (should be inside))
    "button": (Button, (Window, Dialog)),
    "checkbox": (Checkbox, (Window, Dialog)),
    "choice": (Choice, RadioButton),
    "col": (Col, Table),
    "dialog": (Dialog, None),
    "item": (Item, (Menu, )),
    "menu": (Menu, (Menubar, Menu)),
    "menubar": (Menubar, None),
    "radio": (RadioButton, (Window, Dialog)),
    "table": (Table, (Window, Dialog)),
    "text": (Text, (Window, Dialog)),
    "window": (Window, None),
}
