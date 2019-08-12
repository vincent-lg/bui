"""The wxPython implementation of a BUI list widget."""

import wx

from bui.specific.base import *
from bui.specific.base.list import SpecificList

class WX4List(SpecificList):

    """Wx-specific list widget."""

    def _init(self):
        self.wx_choices = []
        window = self.parent
        self.wx_add = self.wx_obj = self.wx_list = wx.ListBox(
                window.wx_parent, style=wx.LB_SINGLE)
        window.add_widget(self)
        self.wx_list.Bind(wx.EVT_LISTBOX, self.OnSelectionChange)
        self.wx_list.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    def refresh(self):
        """Refresh the list choices, using the generic widget."""
        self.wx_list.Freeze()
        if self.wx_choices:
            self.wx_choices[:] = []
            self.wx_list.Clear()

        for label in self.generic._choices:
            self.wx_choices.append(label)
            self.wx_list.Append(label)

        self.wx_list.Select(0)
        self.wx_list.Thaw()

    def update_choice(self, pos: int, choice: str):
        """
        Update a specific choice.

        Args:
            pos (int): the choice position.
            choice (str): the choice label to use.

        """
        self.refresh()

    def remove_choice(self, pos: int):
        """
        Remove the specified choice.

        Args:
            pos (int): the choice position.

        """
        self.refresh()

    def OnSelectionChange(self, e):
        """When the selection changes."""
        indice = self.wx_list.GetSelection()
        self.generic.selected = indice

    def OnKeyDown(self, e):
        window = self.parent
        if "press" in self.generic.controls:
            window._OnKeyDown(e, self)
        else:
            window._OnKeyDown(e)

        e.Skip()
