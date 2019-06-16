from abc import abstractmethod

from bui.specific.base import *

class SpecificButton(SpecificWidget):

    """Parent class for a specific button widget."""

    @property
    @abstractmethod
    def name(self):
        """Get the button name."""
        pass

    @name.setter
    @abstractmethod
    def name(self, name):
        """Set the button name."""
        pass
