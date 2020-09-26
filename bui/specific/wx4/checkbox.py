"""The wxPython implementation of a BUI checkbox widget."""

import wx

from bui.specific.base import *
from bui.specific.base.checkbox import SpecificCheckbox
from bui.specific.wx4.shared import WXShared

class WX4Checkbox(WXShared, SpecificCheckbox):

    @property
    def name(self):
        """Get the checkbox name."""
        raise ValueError("cannot get the name")

    @name.setter
    def name(self, name):
        """Set the checkbox name."""
        self.in_main_thread(self.wx_checkbox.SetName, name)

    @property
    def checked(self):
        """Get the checkbox checked status."""
        raise ValueError("cannot query the checked status")

    @checked.setter
    def checked(self, checked):
        """Set the checkbox checked status."""
        self.in_main_thread(self.wx_checkbox.SetValue, checked)

    def enable(self):
        """Force-enable the checkbox."""
        self.in_main_thread(self.wx_checkbox.Enable)

    def disable(self):
        """Force-disable the checkbox."""
        self.in_main_thread(self.wx_checkbox.Disable)

    def _init(self):
        """Initialize the specific widget."""
        window = self.parent
        label = self.generic.name
        self.wx_add = self.wx_obj = self.wx_checkbox = wx.CheckBox(
                window.wx_parent, label=label, name=label)
        self.wx_checkbox.SetValue(self.generic.cached_checked)
        window.add_widget(self)
        self.wx_checkbox.Bind(wx.EVT_CHECKBOX, self.OnCheck)
        self.watch_keyboard(self.wx_checkbox)

    def OnCheck(self, e):
        """The checkbox is clicked, create a click control."""
        state = 'checked' if e.IsChecked() else 'unchecked'
        self.process_control(e, "check", {'checked': e.IsChecked(), 'state': state})
        self.generic.cached_checked = e.IsChecked()
