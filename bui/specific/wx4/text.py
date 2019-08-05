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
        self._nl_offset = 0
        self.cached_position = -1
        window = self.parent
        label = self.generic.label
        self.wx_add = self.wx_sizer = wx.BoxSizer(wx.VERTICAL)
        self.wx_label = wx.StaticText(window.wx_parent, label=label)
        style = 0
        if self.generic.multiline:
            style |= wx.TE_MULTILINE
        self.wx_obj = self.wx_text = wx.TextCtrl(window.wx_parent,
                value=self.generic.value, style=style, name=label)
        self.wx_sizer.Add(self.wx_label)
        self.wx_sizer.Add(self.wx_text, proportion=5)
        #self.wx_text.generic = self.generic
        window.add_widget(self)
        self.wx_text.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.wx_text.Bind(wx.EVT_TEXT, self.OnTextChanged)
        self.wx_text.Bind(wx.EVT_LEFT_UP, self.OnUpdateCursor)
        self.wx_text.Bind(wx.EVT_KEY_UP, self.OnUpdateCursor)

    def OnTextChanged(self, e):
        text = e.GetString()
        self.generic._process_control("change", {"text": text})
        self.generic.cached_value = text

        # Update the cursor position
        self.UpdateCursorPosition(text)

    def OnKeyDown(self, e):
        window = self.parent
        if "press" in self.generic.controls:
            window._OnKeyDown(e, self)
        else:
            window._OnKeyDown(e)

        e.Skip()

    def UpdateCursorPosition(self, text=None):
        """Check the cursor position."""
        text = text if text else self.wx_text.GetValue()
        position = self.wx_text.GetInsertionPoint()
        if position != self.cached_position:
            self.cached_position = position
            # Calculate line offset if necessary
            # wxPython coupled with Windows break the one-character-per-line-break
            # convention, so BUI tries to apply a patch.
            num_nl = text.count("\n")
            if not self._nl_offset:
                last = self.wx_text.GetLastPosition()
                if num_nl > 0:
                    self._nl_offset = int((last - len(text)) / num_nl) + 1

            # If the text contains new lines, we should have a valid NL offset
            # (usually 1 for Linux or Mac, 2 for Windows)
            if num_nl > 0:
                offset_pos = pos = 0
                for character in text:
                    if pos == self.cached_position:
                        break

                    if character == "\n":
                        pos += self._nl_offset
                    else:
                        pos += 1
                    offset_pos += 1
                else:
                    offset_pos += 1
            else:
                offset_pos = position

            cursor = self.generic.cursor
            cursor._pos = offset_pos
            print(f"Update cursor: {cursor.pos} {cursor.text_before!r} {cursor.text_after!r}")

    async def AsyncUpdateCursor(self, text=None):
        self.UpdateCursorPosition(text)

    def OnUpdateCursor(self, e):
        self.generic.schedule(self.AsyncUpdateCursor())
