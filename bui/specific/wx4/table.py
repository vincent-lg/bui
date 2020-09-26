"""The wxPython implementation of a BUI table widget."""

from typing import Callable, List
import wx

from bui.specific.base import *
from bui.specific.base.table import SpecificTable
from bui.specific.wx4.shared import WXShared
from bui.widget.table import AbcRow

class WX4Table(WXShared, SpecificTable):

    """Wx-specific table widget."""

    def _init(self):
        self._wx_rows = []
        window = self.parent
        self.wx_add = self.wx_obj = self.wx_table = wx.ListCtrl(
                window.wx_parent, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)

        for i, (_, name) in enumerate(self.generic.cols):
            self.wx_table.InsertColumn(i, name)
        window.add_widget(self)
        self.watch_keyboard(self.wx_table)
        self.wx_table.Bind(wx.EVT_LIST_ITEM_SELECTED, self._OnSelected)
        self._wx_selected = -1

    def update_row(self, row: AbcRow):
        """
        Update a specific row.

        Args:
            row (Row): the row to update.

        The Row object contains the index of the row to edit.  Therefore,
        a match between the row index and the specific GUI toolkit row index
        is expected.

        """
        num_items = len(self._wx_rows)
        index = row._index
        if index == num_items:
            # Append the row
            self.in_main_thread(self.wx_table.Append, [str(cell) for cell in row])
            row = self.generic.factory(index, *row)
            row._should_update = False
            self._wx_rows.append(row)
        else:
            old = self._wx_rows[index]
            for i, (new_value, old_value) in enumerate(zip(row, old)):
                if new_value != old_value:
                    self.in_main_thread(self.wx_table.SetItem, index, i, str(new_value))
                    old[i] = new_value

    def refresh(self, rows):
        """
        Refresh the entire table, erasing old rows to update if necessary.

        When this method is called, the content of cached rows (`_rows`)
        and the content of the specific GUI toolkit table should match.
        Indexes should be similar.  This method will attempt to perform a
        lazy update, trying to find the first row to edit in the table
        and then updating what needs updating, removing what needs removing
        and adding what needs adding.

        Args:
            rows (list of Row): the collection of rows to update.

        """
        for row in rows:
            self.update_row(row)
        self.delete_additional()

        # Select the first item if nothing is selected
        if len(self._wx_rows) > 0 and self._wx_selected < 0:
            self.in_main_thread(self.wx_table.Select, 0)
            self.in_main_thread(self.wx_table.Focus, 0)

    def remove_row(self, row: AbcRow):
        """
        Remove the specified row.

        Args:
            row (Row): the row to remove.

        The row to remove can be anywhere in the table, not necessarily
        at the end.

        """
        index = row._index
        del self._wx_rows[index]
        self.in_main_thread(self.wx_table.DeleteItem, index)
        for wx_row in self._wx_rows[index:]:
            wx_row._index -= 1
        self.in_main_thread(self.wx_table.Select, index)
        self.in_main_thread(self.wx_table.Focus, index)

    def delete_additional(self):
        """Remove rows that are in generic, not in the wx table."""
        while len(self._wx_rows) > len(self.generic._rows):
            self.in_main_thread(self.wx_table.DeleteItem, len(self._wx_rows) - 1)
            del self._wx_rows[-1]

    def select_row(self, row: int):
        """Select the specified row."""
        self.in_main_thread(self.wx_table.Select, row)
        self.in_main_thread(self.wx_table.Focus, row)

    def sort(self, key: Callable = None, reverse=False):
        """Sort the table."""
        # The generic table has been sorted, so follow it
        for row in self.generic._rows:
            self.update_row(row)

    def _OnSelected(self, e):
        """An item has been selected."""
        self.generic._selected = e.GetIndex()
