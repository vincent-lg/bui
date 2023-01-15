"""The wxPython implementation of a BUI list widget."""

from typing import Sequence, Union
import threading
import wx

from bui.specific.base import *
from bui.specific.base.list import SpecificList
from bui.specific.wx4.shared import WXShared

class WX4List(WXShared, SpecificList):

    """Wx-specific list widget."""

    def _init(self):
        self.lock = threading.RLock()
        self.wx_choices = []
        self.wx_selected = (0, ) if self.generic.multisel else 0
        self.wx_old_selected = self.wx_selected
        window = self.parent
        style = wx.LB_MULTIPLE if self.generic.multisel else wx.LB_SINGLE
        self.wx_add = self.wx_obj = self.wx_list = wx.ListBox(
                window.wx_parent, style=style)
        window.add_widget(self)
        self.wx_list.Bind(wx.EVT_LISTBOX, self.OnSelectionChange)
        self.watch_keyboard(self.wx_list)

    def refresh(self):
        """Refresh the list choices, using the generic widget."""
        with self.lock:
            self.in_main_thread(self.wx_list.Freeze)
            if self.wx_choices:
                self.wx_choices[:] = []
                self.in_main_thread(self.wx_list.Clear)

            for label in self.generic._choices:
                self.wx_choices.append(label)
                self.in_main_thread(self.wx_list.Append, label)

            self.in_main_thread(self.wx_list.Select, 0)
            self.in_main_thread(self.wx_list.Thaw)
            self.wx_selected = (0, ) if self.generic.multisel else 0
            self.wx_old_selected = self.wx_selected

    def select(self, choice: Union[int, Sequence[int]]):
        """Select the specific choice(s)."""
        with self.lock:
            if self.generic.multisel:
                for deselect in (index for index in self.wx_selected
                        if index not in choice):
                    self.in_main_thread(self.wx_list.Deselect, deselect)

                for select in choice:
                    self.in_main_thread(self.wx_list.Select, select)
            else:
                self.in_main_thread(self.wx_list.Select, choice)
            self.wx_selected = choice
            self.wx_old_selected = self.wx_selected

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
        with self.lock:
            indexes = self.wx_list.GetSelections()
            selected = tuple(self.generic._pos[index] for index in indexes)
            self.wx_selected = indexes if self.generic.multisel else index
            if not self.generic.multisel:
                selected = selected[0] if selected else None

        # Skip the event, no matter what
        e.Skip()

        # Call the control asynchronously.  The control can be stopped.
        self.process_control(None, "select", {"selected": selected})

    def process_control_in_thread(self, event, control, options, close=False):
        """Sub-classing, processing the control in the async thread."""
        result = super().process_control_in_thread(event, control, options)
        if control == "select":
            selected = options["selected"]
            if result:
                self.generic.selected = selected
            else:
                self.select(self.wx_old_selected)

        return result
