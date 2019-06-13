"""The wxPython implementation of a BUI item widget."""

import wx

from bui.specific.base import *
from bui.specific.base.item import SpecificItem

class WX4Item(SpecificItem):

    def OnMenu(self, e):
        """The menu is seslected, create a click control."""
        self.generic._process_control("click")
