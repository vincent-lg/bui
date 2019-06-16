"""The wxPython implementation of a BUI button widget."""

import wx

from bui.specific.base import *
from bui.specific.base.button import SpecificButton

class WX4Button(SpecificButton):

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
        window = self.generic.leaf.parent.widget.specific
        frame = window._wx_frame
        panel = window._wx_panel
        grid = window._wx_grid
        label = self.generic.leaf.name
        self.wx_button = wx.Button(panel, label=label, name=label)
        grid.Add(self.wx_button, (self.generic.leaf.y, self.generic.leaf.x))
        if "click" in self.generic.controls:
            frame.Bind(wx.EVT_BUTTON, self.OnClick, self.wx_button)

        self.wx_button.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    def OnClick(self, e):
        """The menu is seslected, create a click control."""
        self.generic._process_control("click")

    def OnKeyDown(self, e):
        window = self.generic.leaf.parent.widget.specific
        if "press" in self.generic.controls:
            window._OnKeyDown(e, self)
        else:
            window._OnKeyDown(e)

    def focus(self):
        self.wx_button.SetFocus()
