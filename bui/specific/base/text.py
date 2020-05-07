from abc import abstractmethod

from bui.specific.base import *

class SpecificText(SpecificWidget):

    """Parent class for a specific text widget."""

    widget_name = "text"

    @property
    @abstractmethod
    def label(self):
        """Get the text label."""
        pass

    @label.setter
    @abstractmethod
    def label(self, label):
        """Set the text label."""
        pass

    @property
    @abstractmethod
    def value(self):
        """Get the text value."""
        pass

    @value.setter
    @abstractmethod
    def value(self, value):
        """Set the text value."""
        pass

    @property
    @abstractmethod
    def enabled(self):
        """Return whether the text is enabled or not."""
        pass

    @property
    def disabled(self):
        """Return whether the text is disabled or not."""
        return not self.enabled

    @property
    @abstractmethod
    def hidden(self):
        """Return whether the text is hidden or not."""
        pass

    @abstractmethod
    def enable(self):
        """Force-enable the text."""
        pass

    @abstractmethod
    def disable(self):
        """Disable the text."""
        pass

    @abstractmethod
    def move(self, position: int):
        """Move the cursor to the given position.

        Args:
            position (int): the cursor position.

        """
        pass

    @abstractmethod
    def vertical_move(self, lineno: int, col: int):
        """
        Move the cursor to the given vertiical position.

        Args:
            lineno (int): the line number.
            col (int): the column.

        """
        pass
