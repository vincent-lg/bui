"""Helper functions for BUI widgets."""

from unittest.mock import MagicMock

MOCKED = (None, None)

def mock_specific(widget, mock):
    """
    Mock the specified widget.

    Args:
        widget (str): the widget name (its class name).

    """
    global MOCKED
    from bui.tools import PACKAGE
    MOCKED = (widget, getattr(PACKAGE, widget))
    setattr(PACKAGE, widget, mock)

def unmock_specific():
    """Unmock the specific widget."""
    global MOCKED
    from bui.tools import PACKAGE
    widget, specific = MOCKED
    setattr(PACKAGE, widget, specific)
    MOCKED = (None, None)
