from abc import abstractmethod

from bui.specific.base import *
from bui.specific.base.window import SpecificWindow

class SpecificDialog(SpecificWindow):

    """Parent class for a specific dialog."""

    widget_name = "dialog"
