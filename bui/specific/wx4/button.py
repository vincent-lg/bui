"""The wxPython implementation of a BUI button widget."""

import wx

from bui.specific.base import *
from bui.specific.base.button import SpecificButton
from bui.specific.wx4.shared import WXShared

class WX4Button(WXShared, SpecificButton):

    @property
    def name(self):
        """Get the button name."""
        return self.wx_button.GetLabel()

    @name.setter
    def name(self, name):
        """Set the button name."""
        self.wx_button.SetLabel(name)

    def _init(self):
        """Initialize the specific widget."""
        window = self.parent
        label = self.generic.name
        self.wx_add = self.wx_obj = self.wx_button = wx.Button(
                window.wx_parent,label=label, name=label)
        window.add_widget(self)
        self.wx_button.Bind(wx.EVT_BUTTON, self.OnClick)

        self.watch_keyboard(self.wx_button)

    def OnClick(self, e):
        """The menu is seslected, create a click control."""
        self.generic._process_control("click")
