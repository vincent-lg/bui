"""The wxPython implementation of a BUI menu widget."""

import wx

from bui.specific.base import *
from bui.specific.base.menu import SpecificMenu
from bui.specific.wx4.shared import WXShared

class WX4Menu(WXShared, SpecificMenu):

    def _init(self):
        """Initialize the menu."""
        self.wx_menu = wx.Menu()
        parent = self.parent
        while parent and parent.widget_name != "window":
            parent = parent.parent
        parent.wx_menus.append(self)

    def _complete(self, window):
        """Complete the menu."""
        parent = self.parent
        if parent.widget_name in ("context", "menu"):
            parent.wx_menu.AppendSubMenu(self.wx_menu, self.generic.name)
        else:
            parent.wx_menubar.Append(self.wx_menu, self.generic.name)
