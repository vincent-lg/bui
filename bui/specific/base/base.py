from abc import ABCMeta

class SpecificWidget(metaclass=ABCMeta):

    """Parent class for a specific widget."""

    def __init__(self, generic):
        self.generic = generic
        self.parent = generic.parent.specific if generic.parent is not None else None

    def _init(self):
        """Initialize the specific widget."""
        pass
