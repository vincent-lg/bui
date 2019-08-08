"""The wxPython implementation of a BUI table widget."""

from typing import List
import wx

from bui.specific.base import *
from bui.specific.base.table import SpecificTable
from bui.widget.table import AbcRow

class WX4Table(SpecificTable):

    """Wx-specific table widget."""

    def _init(self):
        self._wx_rows = []
        window = self.parent
        self.wx_add = self.wx_obj = self.wx_table = wx.ListCtrl(
                window.wx_parent, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)

        for i, (_, name) in enumerate(self.generic.cols):
            self.wx_table.InsertColumn(i, name)
        window.add_widget(self)

    def update_row(self, row: AbcRow):
        """
        Update a specific row.

        Args:
            row (Row): the row to update.

        The Row object contains the index of the row to edit.  Therefore,
        a match between the row index and the specific GUI toolkit row index
        is expected.

        """
        num_items = self.wx_table.GetItemCount()
        index = row.index
        if index == num_items:
            # Append the row
            self.wx_table.Append([str(cell) for cell in row])
            self._wx_rows.append(self.generic.factory(index, *row))
        else:
            old = self._wx_rows[index]
            for i, (new_value, old_value) in enumerate(zip(row, old)):
                if new_value != old_value:
                    self.wx_table.SetItem(index, i, str(new_value))
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
        if len(self._wx_rows) > 0 and self.wx_table.GetFirstSelected() < 0:
            self.wx_table.Select(0)
            self.wx_table.Focus(0)

    def remove_row(self, row: AbcRow):
        """
        Remove the specified row.

        Args:
            row (Row): the row to remove.

        The row to remove can be anywhere in the table, not necessarily
        at the end.

        """
        index = row.index
        del self._wx_rows[index]
        self.wx_table.DeleteItem(index)
        for wx_row in self._wx_rows[index:]:
            wx_row.index -= 1

    def delete_additional(self):
        """Remove rows that are in generic, not in the wx table."""
        while len(self._wx_rows) > len(self.generic._rows):
            self.wx_table.DeleteItem(len(self._wx_rows) - 1)
            del self._wx_rows[-1]
