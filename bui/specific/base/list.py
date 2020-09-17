from abc import abstractmethod

from bui.specific.base import *

class SpecificList(SpecificWidget):

    """Parent class for a specific list widget."""

    widget_name = "list"

    @abstractmethod
    def refresh(self):
        """Refresh the list choices, using the generic widget."""
        pass

    def select(self, choice: int):
        """Select the specific choice."""
        pass

    @abstractmethod
    def update_choice(self, pos: int, choice: str):
        """
        Update a specific choice.

        Args:
            pos (int): the choice position.
            choice (str): the choice label to use.

        """
        pass

    @abstractmethod
    def remove_choice(self, pos: int):
        """
        Remove the specified choice.

        Args:
            pos (int): the choice position.

        """
        pass
