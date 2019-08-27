"""The wxPython implementation of a BUI checkbox widget."""

import wx

from bui.specific.base import *
from bui.specific.base.checkbox import SpecificCheckbox
from bui.specific.wx4.shared import WXShared

class WX4Checkbox(WXShared, SpecificCheckbox):

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
        window = self.parent
        label = self.generic.name
        self.wx_add = self.wx_obj = self.wx_checkbox = wx.CheckBox(
                window.wx_parent, label=label, name=label)
        self.wx_checkbox.SetValue(self.generic.checked)
        window.add_widget(self)
        self.wx_checkbox.Bind(wx.EVT_CHECKBOX, self.OnCheck)
        self.watch_keyboard(self.wx_checkbox)

    def OnCheck(self, e):
        """The checkbox is clicked, create a click control."""
        state = 'checked' if e.IsChecked() else 'unchecked'
        self.generic._process_control("check", {'checked': e.IsChecked(), 'state': state})
        self.generic.cached_checked = e.IsChecked()
