from abc import ABCMeta

class SpecificWidget(metaclass=ABCMeta):

    """Parent class for a specific widget."""

    def __init__(self, generic):
        self.generic = generic

    def _init(self):
        """Initialize the specific widget."""
        pass
