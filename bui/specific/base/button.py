from abc import abstractmethod

from bui.specific.base import *

class SpecificButton(SpecificWidget):

    """Parent class for a specific button widget."""

    widget_name = "button"

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

    @property
    @abstractmethod
    def enabled(self):
        """Return whether the button is enabled or not."""
        pass

    @property
    def disabled(self):
        """Return whether the button is disabled or not."""
        return not self.enabled

    @abstractmethod
    def enable(self):
        """Force-enable the button."""
        pass

    @abstractmethod
    def disable(self):
        """Disable the button."""
        pass
