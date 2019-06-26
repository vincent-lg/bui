from abc import abstractmethod

from bui.specific.base import *

class SpecificWindow(SpecificWidget):

    """Parent class for a specific window object."""

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
    def create_menubar(self, menubar):
        """Create a menu bar."""
        pass

    @abstractmethod
    def close(self):
        """Close this window, terminate loop if appropriate."""
        pass
