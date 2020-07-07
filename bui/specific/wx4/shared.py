"""Contain the WXShared class."""

from collections import namedtuple

import wx

from bui.control.exceptions import StopControl
from bui.specific.wx4.constants import KEYMAP

class WXShared:

    """Mixin to share wx behavior, to be expected on all BUI widgets."""

    def watch_keyboard(self, wx_obj):
        """Bind to different wx events to watch the keyboard."""
        wx_obj.Bind(wx.EVT_KEY_DOWN, self._OnKeyDown)
        wx_obj.Bind(wx.EVT_CHAR, self._OnChar)
        wx_obj.Bind(wx.EVT_KEY_UP, self._OnKeyUp)

    def _OnKeyDown(self, e):
        """A key was pressed."""
        kwargs = self._get_control_args(e)
        self.process_control(e, "press", kwargs)

    def _OnChar(self, e):
        """A key was pressed leadng to a key type."""
        kwargs = {
                "unicode": chr(e.GetUnicodeKey()),
        }

        self.process_control(e, "type", kwargs)

    def _OnKeyUp(self, e):
        """A key was released."""
        kwargs = self._get_control_args(e)
        self.process_control(e, "release", kwargs)

    def _get_control_args(self, e):
        key_code = e.GetKeyCode()
        key = KEYMAP.get(key_code)

        if key is None:
            if key_code < 256:
                if key_code == 0:
                    key = "nul"
                elif key_code < 27:
                    key = f"ctrl{chr(key_code + 64)}"
                else:
                    key = chr(key_code)
            else:
                key = str(key_code)

        key = key.lower()

        # Add modifiers
        kwargs = {"raw_key": key}
        modified = ""
        modifiers = (
                (e.ControlDown(), "ctrl"),
                (e.AltDown(), "alt"),
                (e.ShiftDown(), "shift"),
        )

        for on, attr in modifiers:
            kwargs[attr] = on
            if on:
                if modified:
                    modified += "_"
                modified += attr

        if modified:
            if key:
                key = f"{modified}_{key}"
            else:
                key = modified

        kwargs["key"] = key
        return kwargs

    def process_control(self, e, control, options=None):
        """Process the control.

        Args:
            e (wx.Event): the wxPython event.
            control (str): the control name to call.
            options (optional, dict): the control options.

        If the generic widget is not subscribed to this control,
        look for the parent widget and so on.

        """
        widget = self
        while control not in widget.generic.default_controls:
            widget = widget.parent
            if widget is None:
                break

        if widget:
            try:
                widget.generic._process_control(control, options)
            except StopControl:
                return

        e.Skip()
