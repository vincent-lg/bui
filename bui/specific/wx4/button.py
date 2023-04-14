"""The wxPython implementation of a BUI button widget."""

import wx

from bui.specific.base import *
from bui.specific.base.button import SpecificButton
from bui.specific.wx4.shared import WXShared

NAV_KEYS = (
    "left right up down pageup pagedown home end tab return space"
).split()

class WX4Button(WXShared, SpecificButton):

    @property
    def name(self):
        """Get the button name."""
        raise ValueError("cannot modify the label like this")

    @name.setter
    def name(self, name):
        """Set the button name."""
        self.in_main_thread(self.wx_button.SetLabel, name)

    def enable(self):
        """Force-enable the button."""
        self.generic._enabled = True
        self.in_main_thread(self.wx_button.Enable)

    def disable(self):
        """Force-disable the button."""
        self.generic._enabled = True
        self.in_main_thread(self.wx_button.Disable)

    def _init(self):
        """Initialize the specific widget."""
        window = self.parent
        label = self.generic.name
        self.wx_add = self.wx_obj = self.wx_button = wx.Button(
                window.wx_parent, label=label)
        window.add_widget(self)
        if self.generic.leaf.disabled:
            self.wx_button.Disable()

        self.wx_button.Bind(wx.EVT_BUTTON, self.OnClick)

        self.watch_keyboard(self.wx_button)

    def OnClick(self, e):
        """The menu is seslected, create a click control."""
        self.process_control(e, "click")

    def should_process_control(self, event, name, options=None):
        """Returns whether this widget can perform this control.

        Args:
            event (wx): the WX event.
            name (str): the control name.
            options (dict, optional): the control options.

        """
        options = {} if options is None else options
        if name == "press":
            if options.get("hook", False):
                if options.get("raw_key") not in NAV_KEYS:
                    return False

        return True
