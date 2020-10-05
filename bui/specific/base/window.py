from abc import abstractmethod
from typing import Dict, Optional, Union

from bui.specific.base import *

class SpecificWindow(SpecificWidget):

    """Parent class for a specific window object."""

    widget_name = "window"

    @property
    @abstractmethod
    def usable_surface(self):
        """
        Return the screen size that can be used, in pixels.

        This size is returned in a tuple: (width, height), so that
        (x, y) follow the exact same pattern.  Both components are integers.

        Note that this is the screen surface being "free", that is,
        not counting the taskbar on some operating systems, since
        we cannot draw on that.  Therefore, the usable surface tends
        to be somewhat narrower than the screen resolution.

        """
        pass

    @property
    @abstractmethod
    def title(self):
        """Return the current title, override in child class."""
        pass

    @title.setter
    @abstractmethod
    def title(self, new_title):
        """Set the window's title, override in child class."""
        pass

    def _init(self):
        """Initialize the specific widget."""
        self.title = self.generic.leaf.title

    @abstractmethod
    def _start(self, loop):
        """
        Start the window, watch events and allow async loop.

        Args:
            loop (AsyncLoop): the asynchronous event loop (see asyncio).

        """
        pass

    @abstractmethod
    @abstractmethod
    def close(self):
        """Close this window, terminate loop if appropriate."""
        pass

    @abstractmethod
    def add_widget(self, widget: SpecificWidget):
        """
        Add a widget on the window.

        Args:
            widget (SpecificWidget): the specific widget to add.

        """
        pass

    @abstractmethod
    def pop_dialog(self, dialog: SpecificWidget, **kwargs):
        """Pop up a dialog."""
        pass

    @abstractmethod
    def pop_menu(self, context: SpecificWidget):
        """Pop a context menu, blocks until the menu is closed."""
        pass

    @abstractmethod
    def pop_alert(self, title: str, message: str,
            danger: str, buttons: Dict[str, Union[bool, str]],
            default: str):
        """
        Display an alert message.

        Args:
            title (str): the alert title.
            message (str): the alert message.
            danger (str): the alert danger (dialog type).
            buttons (dict): the buttons of this dialog.
            default (str): the default button for this dialog.

        """
        pass
