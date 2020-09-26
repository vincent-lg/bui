"""The wxPython implementation of a BUI text widget."""

from itertools import count

import wx

from bui.specific.base import *
from bui.specific.base.text import SpecificText
from bui.specific.wx4.shared import WXShared

class WX4Text(WXShared, SpecificText):

    @property
    def label(self):
        """Get the text label."""
        raise ValueError("can't read the label")

    @label.setter
    def label(self, label):
        """Set the text label."""
        self.in_main_thread(self.wx_label.SetLabel, label)

    @property
    def value(self):
        """Get the text value status."""
        raise ValueError("can't read the value")

    @value.setter
    def value(self, value):
        """Set the text value status."""
        old_value = getattr(self.generic, "cached_value", "")
        if old_value:
            # Find the first different character, not updating everything
            off_pos = pos = None
            for i, (old_char, new_char) in enumerate(zip(old_value, value)):
                if old_char != new_char:
                    pos = i
                    off_pos = pos + value[:i].count("\n") * (self._nl_offset - 1)
                    break
            else:
                smaller = value if len(value) < len(old_value) else old_value
                pos = len(smaller)
                off_pos = pos + smaller.count("\n") * (self._nl_offset - 1)

            self.in_main_thread(self.wx_text.Remove, off_pos, self.wx_text.GetLastPosition())
            to_add = value[pos:]
            if to_add:
                self.in_main_thread(self.wx_text.AppendText, to_add)
        else:
            self.in_main_thread(self.wx_text.SetValue, value)

    @property
    def enabled(self):
        """Return whether the text is enabled or not."""
        return self.wx_text.Enabled

    @property
    def hidden(self):
        """Return whether the text is hidden or not."""
        return self.wx_text.GetStyle(0, wx.TE_PASSWORD)

    def enable(self):
        """Force-enable the text."""
        self.wx_text.Enable()

    def disable(self):
        """Force-disable the text."""
        self.wx_text.Disable()

    def _init(self):
        """Initialize the specific widget."""
        self._nl_offset = 0
        self._update_counter = count()
        self._last_updated = next(self._update_counter)
        self._last_checked = self._last_updated
        window = self.parent
        label = self.generic.label
        self.wx_add = self.wx_sizer = wx.BoxSizer(wx.VERTICAL)
        self.wx_label = wx.StaticText(window.wx_parent, label=label)
        style = 0
        if self.generic.multiline:
            style |= wx.TE_MULTILINE
        if self.generic._hidden:
            style |= wx.TE_PASSWORD
        if self.generic.read_only:
            style |= wx.TE_READONLY

        self.wx_obj = self.wx_text = wx.TextCtrl(window.wx_parent,
                size=window.size_for(self), style=style, name=label)
        self.wx_text.SetPosition(window.position_for(self))

        # Try to infer the NL offset by a simple update
        self.wx_text.Freeze()
        if self.generic.multiline:
            self.wx_text.SetValue("\n")
            self._nl_offset = self.wx_text.GetLastPosition()
        else:
            self._nl_offset = 1
        self.wx_text.SetValue(self.generic.value)
        self.wx_text.Thaw()
        self.wx_sizer.Add(self.wx_label)
        self.wx_sizer.Add(self.wx_text, proportion=5)
        window.add_widget(self)
        self.watch_keyboard(self.wx_text)
        self.wx_text.Bind(wx.EVT_TEXT, self.OnTextChanged)
        self.wx_text.Bind(wx.EVT_LEFT_UP, self.OnUpdateCursor)
        self.wx_text.Bind(wx.EVT_KEY_UP, self.OnUpdateCursor)

    def OnTextChanged(self, e):
        text = e.GetString()
        self.generic._process_control("change", {"text": text})
        self.generic.cached_value = text
        self._last_checked = next(self._update_counter)

        # Update the cursor position
        self.UpdateCursorPosition(text)

    def UpdateCursorPosition(self, text=None):
        """Check the cursor position."""
        text = text if text else self.wx_text.GetValue()
        position = self.wx_text.GetInsertionPoint()
        if self._last_updated != self._last_checked:
            self._last_updated = self._last_checked
            self.cached_position = position
            num_nl = text.count("\n")
            lineno, col = 0, 0
            if num_nl > 0:
                offset_pos = pos = 0
                for character in text:
                    if pos == self.cached_position:
                        break

                    if character == "\n":
                        pos += self._nl_offset
                        lineno += 1
                        col = 0
                    else:
                        pos += 1
                        col += 1
                    offset_pos += 1
                else:
                    offset_pos += 1
                    col += 1
            else:
                offset_pos = position
                col = position

            cursor = self.generic.cursor
            cursor._pos = offset_pos
            cursor._lineno = lineno
            cursor._col = col

    async def AsyncUpdateCursor(self, text=None):
        if self.wx_text:
            self.UpdateCursorPosition(text)

    def OnUpdateCursor(self, e):
        self.generic.schedule(self.AsyncUpdateCursor())
        e.Skip()

    def move(self, position: int):
        """Move the cursor to the given position.

        Args:
            position (int): the cursor position.

        """
        offset_pos = 0
        lineno, col = 0, 0
        cursor = self.generic.cursor
        text = self.generic.value
        for i, char in enumerate(text):
            if i == position:
                cursor._pos = i
                cursor._lineno = lineno
                cursor._col = col
                self.wx_text.SetInsertionPoint(offset_pos)
                break

            if char == "\n":
                offset_pos += self._nl_offset
                lineno += 1
                col = 0
            else:
                offset_pos += 1
                col += 1
        else:
            num_nl = text.count("\n")
            if num_nl > 0:
                lineno = num_nl - 1
                col = len(text) - text.rfind("\n")
            else:
                lineno = 0
                col = len(text)

            cursor._pos = len(text)
            cursor._lineno = lineno
            cursor._col = col
            self.wx_text.SetInsertionPoint(self.wx_text.GetLastPosition())

    def vertical_move(self, lineno: int, col: int):
        """
        Move the cursor to the given vertiical position.

        Args:
            lineno (int): the line number.
            col (int): the column.

        """
        text = self.generic.value
        _lineno, _col = 0, 0
        for pos, char in enumerate(text):
            if lineno == _lineno and col == _col:
                self.move(pos)
                break

            if char == "\n":
                _lineno += 1
                _col = 0
            else:
                _col += 1
        else:
            self.move(len(text))
