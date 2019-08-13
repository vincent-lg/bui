from abc import abstractmethod

from bui.specific.base import *

class SpecificRadioButton(SpecificWidget):

    """Parent class for a specific radio button widget."""

    widget_name = "radio"

    @abstractmethod
    def refresh(self):
        """Refresh the available choices."""
        pass
