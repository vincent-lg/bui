from abc import abstractmethod
from typing import List

from bui.widget.table import AbcRow
from bui.specific.base import *

class SpecificTable(SpecificWidget):

    """Parent class for a specific table widget."""

    widget_name = "table"

    @abstractmethod
    def refresh(self, rows: List[AbcRow]):
        """
        Refresh the table rows, using the specified row objects.

        Args:
            rows (list of Row): list of row objects.

        """
        pass

    @abstractmethod
    def update_row(self, row: AbcRow):
        """
        Update a specific row.

        Args:
            row (Row): the row to update.

        The Row object contains the index of the row to edit.  Therefore,
        a match between the row index and the specific GUI toolkit row index
        is expected.

        """
        pass

    @abstractmethod
    def remove_row(self, row: AbcRow):
        """
        Remove the specified row.

        Args:
            row (Row): the row to remove.

        The row to remove can be anywhere in the table, not necessarily
        at the end.

        """
        pass
