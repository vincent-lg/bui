"""The wxPython implementation of a BUI context menu widget."""

import wx

from bui.specific.base import *
from bui.specific.base.context import SpecificContext

class WX4Context(SpecificContext):

    def _init(self):
        """Initialize the context menu."""
        self.wx_menu = wx.Menu()
