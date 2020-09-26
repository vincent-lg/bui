"""The wxPython implementation of a BUI menubar widget."""

import wx

from bui.specific.base import *
from bui.specific.base.menubar import SpecificMenubar
from bui.specific.wx4.shared import WXShared

class WX4Menubar(WXShared, SpecificMenubar):

    def _init(self):
        """Create a menu bar."""
        self.wx_menubar = wx.MenuBar()
        self.parent.wx_menus.append(self)

    def _complete(self, window):
        """Complete the widget."""
        window.wx_frame.SetMenuBar(self.wx_menubar)
