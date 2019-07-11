"""The wxPython implementation of a BUI checkbox widget."""

import wx

from bui.specific.base import *
from bui.specific.base.checkbox import SpecificCheckbox

class WX4Checkbox(SpecificCheckbox):

    @property
    def name(self):
        """Get the checkbox name."""
        return self.wx_checkbox.GetName()

    @name.setter
    def name(self, name):
        """Set the checkbox name."""
        self.wx_checkbox.SetName(name)

    @property
    def checked(self):
        """Get the checkbox checked status."""
        return self.wx_checkbox.GetValue()

    @checked.setter
    def checked(self, checked):
        """Set the checkbox checked status."""
        self.wx_checkbox.SetValue(checked)

    @property
    def enabled(self):
        """Return whether the checkbox is enabled or not."""
        return self.wx_checkbox.Enabled

    def enable(self):
        """Force-enable the checkbox."""
        self.wx_checkbox.Enable()

    def disable(self):
        """Force-disable the checkbox."""
        self.wx_checkbox.Disable()

    def _init(self):
        """Initialize the specific widget."""
        window = self.generic.leaf.parent.widget.specific
        frame = window._wx_frame
        panel = window._wx_panel
        grid = window._wx_grid
        label = self.generic.leaf.name
        self.wx_checkbox = wx.CheckBox(panel, label=label, name=label)
        self.wx_checkbox.SetValue(self.generic.checked)
        grid.Add(self.wx_checkbox, (self.generic.leaf.y, self.generic.leaf.x))
        self.wx_checkbox.Bind(wx.EVT_CHECKBOX, self.OnCheck)

    def focus(self):
        self.wx_checkbox.SetFocus()

    def OnCheck(self, e):
        """The checkbox is clicked, create a click control."""
        state = 'checked' if e.IsChecked() else 'unchecked'
        self.generic._process_control("check", {'checked': e.IsChecked(), 'state': state})
        self.generic.cached_checked = e.IsChecked()
