"""The wxPython implementation of a BUI text widget."""

from itertools import count

import wx
import wx.lib.newevent

from bui.specific.base import *
from bui.specific.base.text import SpecificText
from bui.specific.wx4.shared import WXShared

# Constants
EvtWatchCursor, EVT_WATCH_CURSOR = wx.lib.newevent.NewEvent()

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

            start = off_pos
            value = value[pos:]
        else:
            start = None

        self.in_main_thread(self.wx_SetValue, value, start)

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
        self.wx_text.Bind(wx.EVT_LEFT_UP, self.OnPrepareUpdateCursor)
        self.wx_text.Bind(wx.EVT_KEY_UP, self.OnPrepareUpdateCursor)
        self.wx_text.Bind(EVT_WATCH_CURSOR, self.OnWatchCursor)

    def OnTextChanged(self, e):
        text = e.GetString()
        self.generic._process_control("change", {"text": text})
        self.generic.cached_value = text
        self._last_checked = next(self._update_counter)

        # Update the cursor position
        self.UpdateCursorPosition(text)

    def OnPrepareUpdateCursor(self, e):
        """
        Prepare to update the cursor.

        Notice that this method is the first link of a chain which will
        require some time to proceed.  There is no event to watch
        the cursor position, so this method will generate another
        event which is supposed to run after the cursor has moved.
        This second event, `WatchCursor`, will then generate a coroutine
        that will only be executed in the asynchronous loop, thus
        generating another constraint in time.  However, it is
        worth noting these methods don't contain complicated calculation,
        they just postpone each operation to a later date while
        the cursor might be updated again.  In theory, this does
        not affect BUI's performance.

        """
        e.Skip()
        wx.PostEvent(self.wx_text, EvtWatchCursor())

    def OnWatchCursor(self, e):
        """
        The cursor has supposedly changed position.

        This is the second link in the chain of events.  This method
        should be called after the cursor has moved.

        """
        e.Skip()
        pos = self.wx_text.GetInsertionPoint()
        self.UpdateCursorPosition()

    def UpdateCursorPosition(self, text=None):
        """Check the cursor position."""
        text = text if text else self.wx_text.GetValue()
        position = self.wx_text.GetInsertionPoint()
        self.in_async_thread(self.async_update_cursor_position, text, position)

    def async_update_cursor_position(self, text, position):
        """
        Update the cursor position in the asynchronous thread.

        Args:
            position (int): the new position (with offset).

        """
        num_nl = text.count("\n")
        lineno, col = 0, 0
        if num_nl > 0:
            offset_pos = pos = 0
            for character in text:
                if pos == position:
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

    def wx_SetValue(self, text, start=None):
        """
        Update the text value.

        Args:
            text (str): the text to set as value.
            start (optional, int): the starting index.  If not set,
                    replace everything.  If set, let whatever
                    was before the index and replace whatever
                    comes after.

        Note:
            If specified, the start index should be aware of the
            offset imposed by wxPython on Windows, that is, new lines
            (\n) might need two characters instead of one.  This
            method will apply the start with no consideration on this
            offset, whatsoever.

        This method should be called in the main thread.

        """
        if start is None:
            self.wx_text.SetValue(text)
        else:
            self.wx_text.Remove(start, self.wx_text.GetLastPosition())
            self.wx_text.AppendText(text)

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
                self.in_main_thread(self.wx_set_insertion_point, offset_pos)
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
            self.in_main_thread(self.wx_set_insertion_point, offset_pos)

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

    def wx_set_insertion_point(self, pos):
        """Set the wxPython insertion point."""
        self.wx_text.SetInsertionPoint(pos)
