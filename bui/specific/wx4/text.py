"""The wxPython implementation of a BUI text widget."""

import wx

from bui.specific.base import *
from bui.specific.base.text import SpecificText

class WX4Text(SpecificText):

    @property
    def label(self):
        """Get the text label."""
        return self.wx_label.GetLabel()

    @label.setter
    def label(self, label):
        """Set the text label."""
        self.wx_label.SetLabel(label)

    @property
    def value(self):
        """Get the text value status."""
        return self.wx_text.GetValue()

    @value.setter
    def value(self, value):
        """Set the text value status."""
        self.wx_text.SetValue(value)

    @property
    def enabled(self):
        """Return whether the text is enabled or not."""
        return self.wx_text.Enabled

    def enable(self):
        """Force-enable the text."""
        self.wx_text.Enable()

    def disable(self):
        """Force-disable the text."""
        self.wx_text.Disable()

    def _init(self):
        """Initialize the specific widget."""
        window = self.generic.leaf.parent.widget.specific
        frame = window._wx_frame
        panel = window._wx_panel
        grid = window._wx_grid
        label = self.generic.leaf.label
        self.wx_label = wx.StaticText(panel, label=label)
        self.wx_text = wx.TextCtrl(panel, value=self.generic.leaf.value)
        self.wx_text.generic = self.generic
        grid.Add(self.wx_label, (self.generic.leaf.y - 1, self.generic.leaf.x))
        grid.Add(self.wx_text, (self.generic.leaf.y, self.generic.leaf.x))
        self.wx_text.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.wx_text.Bind(wx.EVT_TEXT, self.OnTextChanged)

    def focus(self):
        self.wx_text.SetFocus()

    def OnTextChanged(self, e):
        text = e.GetString()
        self.generic._process_control("change", {"text": text})
        self.generic.cached_value = text

    def OnKeyDown(self, e):
        window = self.generic.leaf.parent.widget.specific
        if "press" in self.generic.controls:
            window._OnKeyDown(e, self)
        else:
            window._OnKeyDown(e)

        e.Skip()
