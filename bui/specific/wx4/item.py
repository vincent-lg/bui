"""The wxPython implementation of a BUI item widget."""

import wx

from bui.specific.base import *
from bui.specific.base.item import SpecificItem
from bui.specific.wx4.shared import WXShared

class WX4Item(WXShared, SpecificItem):

    def _init(self):
        """Initialize the menu."""
        window = self.parent
        while window and window.widget_name != "window":
            window = window.parent
        window.wx_menus.append(self)

    def _complete(self, window):
        """Complete the menu item."""
        self.wx_item = self.parent.wx_menu.Append(wx.ID_ANY, self.generic.data)
        window.wx_frame.Bind(wx.EVT_MENU, self.OnItem, self.wx_item)

    def OnItem(self, e):
        """The menu is seslected, create a click control."""
        self.process_control(e, "click")
