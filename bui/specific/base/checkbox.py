from abc import abstractmethod

from bui.specific.base import *

class SpecificCheckbox(SpecificWidget):

    """Parent class for a specific checkbox widget."""

    @property
    @abstractmethod
    def name(self):
        """Get the checkbox name."""
        pass

    @name.setter
    @abstractmethod
    def name(self, name):
        """Set the checkbox name."""
        pass

    @property
    @abstractmethod
    def checked(self):
        """Get the checkbox checked status."""
        pass

    @checked.setter
    @abstractmethod
    def checked(self, checked):
        """Set the checkbox checked status."""
        pass
