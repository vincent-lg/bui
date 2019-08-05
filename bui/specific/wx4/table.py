"""The wxPython implementation of a BUI table widget."""

import wx

from bui.specific.base import *
from bui.specific.base.table import SpecificTable

class WX4Table(SpecificTable):

    """Wx-specific table widget."""

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, rows):
        self.refresh(rows)

    def _init(self):
        self._rows = []
        window = self.parent
        self.wx_add = self.wx_obj = self.wx_table = wx.ListCtrl(
                window.wx_parent, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)

        for i, (_, name) in enumerate(self.generic.cols):
            self.wx_table.InsertColumn(i, name)
        window.add_widget(self)

    def row_at(self, index):
        """
        Return the Row object at the specified index.

        If the index is invalid, raise IndexError.  Otherwise, the
        returned Row object will have the same definition as the table
        columns.

        Unlike the `rows` property, this method communicates with the
        specific GUI toolkit to get accurate and updated content.
        Therefore, it is not a good idea to use it on a frequent basis.
        Updating the `rows` property will actually call this method but
        the content will be cached as much as possible.

        Args:
            index (int): the row index (starts at 0).

        Returns:
            row (Row): the row object, if successfully found and created.

        Raises:
            IndexError if the index is out of range.
            ValueError if the row doesn't have a logical structure
            matching the table columns.

        """
        texts = [self.wx_table.GetItem(index, col).GetText()
                for col in range(len(self.generic.cols))]
        row = self.generic.factory(index, *texts)
        if index < len(self._rows):
            self._rows[index] = row
        else:
            # Force-update the previous indexes
            i = len(self._rows)
            while i < index:
                self.row_at(i)
                i += 1

            self._rows.append(row)

    def update_row(self, row):
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
            self.wx_table.Append(list(row))
            self.row_at(index)
            return
        elif index > len(self._rows):
            old = self.row_at(index)
        else:
            old = self._rows[index]

        for i, (new_value, old_value) in enumerate(zip(row, old)):
            if new_value != old_value:
                self.wx_table.SetItem(index, i, new_value)

        self._rows[index] = self.generic.factory(index, *row)

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
        num_items = self.wx_table.GetItemCount()
        index = 0
        while index < num_items:
            self.row_at(index)
            index += 1

        # By then, the specific GUI toolkit and the _rows should match,
        # at least in number
        for row in rows:
            self.update_row(row)

        # Select the first item if nothing is selected
        if self.wx_table.GetFirstSelected() < 0:
            self.wx_table.Select(0)
            self.wx_table.Focus(0)
