"""The wxPython implementation of a BUI window.

In order to represent a BUI window with a grid, a wx.Window object is
created, containing a wx.Panel, containing a wx.GridBagSizer.  This
sizer is then used to place the BUI components on the window and
account for spanning that might occur.

"""

import wx

from bui.specific.base import *
from bui.specific.base.window import SpecificWindow
from bui.specific.wx4.app import AsyncApp
from bui.specific.wx4.constants import KEYMAP

class WX4Window(SpecificWindow):

    def __init__(self, generic):
        super().__init__(generic)
        self.wx_app = None
        self.wx_display = None

    @property
    def usable_surface(self):
        self._wx_init()
        rect = self.wx_display.ClientArea
        return Rectangle((rect.x, rect.y), (rect.width, rect.height))

    def _wx_init(self):
        """Initialize wx (creating a wx.App) if necessary."""
        if not self.wx_app:
            self.wx_app = AsyncApp()
            self.wx_display = wx.Display()

    @property
    def title(self):
        """Return the current title, override in child class."""
        return self.wx_frame.GetTitle()

    @title.setter
    def title(self, new_title):
        """Set the window's title, override in child class."""
        self.wx_frame.SetTitle(new_title)

    def _init(self):
        """Initialize the specific widget."""
        self._wx_init()
        title = self.generic.title
        self.wx_frame = wx.Frame(None, title=title, name=title)
        self.wx_app.top_window = self.wx_frame
        self.wx_parent = self.wx_panel = wx.Panel(self.wx_frame)
        self.wx_sizer = wx.BoxSizer(wx.VERTICAL)

        # Bind press and type controls
        if "press" in self.generic.controls:
            self.wx_panel.Bind(wx.EVT_KEY_DOWN, self._OnKeyDown)

        self.wx_panel.SetSizerAndFit(self.wx_sizer)
        self.wx_frame.SetClientSize(self.wx_panel.GetSize())

    def add_widget(self, widget: SpecificWidget):
        """
        Add a widget on the window.

        Args:
            widget (SpecificWidget): the specific widget to add.

        """
        generic = widget.generic
        (top_x, top_y), (bottom_x, bottom_y) = self.usable_surface
        x = top_x + (generic.x / (self.generic.width + 1)) * (bottom_x - top_x)
        y = top_y + (generic.y / (self.generic.height + 1)) * (bottom_y - top_y)
        width = (bottom_x - top_x) * (generic.width / (self.generic.width + 1)) - 5
        height = (bottom_y - top_y) * (generic.height / (self.generic.height + 1)) - 5
        widget.wx_obj.SetSize(int(x), int(y), int(width), int(height))
        self.wx_sizer.Add(widget.wx_add)

    def _start(self, loop):
        """
        Start the window, watch events and allow async loop.

        Args:
            loop (AsyncLoop): the asynchronous event loop (see asyncio).

        """
        self.wx_frame.Show()
        self.wx_app.loop = loop
        return self.wx_app.MainLoop()

    def create_menubar(self, menubar):
        """Create a menu bar."""
        wx_menubar = wx.MenuBar()

        # Create menus and then meny items in each menu
        for menu in menubar.children:
            wx_menu = wx.Menu()
            for item in menu.children:
                wx_item = wx_menu.Append(wx.ID_ANY, item.data)
                self.wx_frame.Bind(wx.EVT_MENU, item.widget.specific.OnMenu, wx_item)
            wx_menubar.Append(wx_menu, menu.name)
        self.wx_frame.SetMenuBar(wx_menubar)

    def close(self):
        """Close this window, terminate loop if appropriate."""
        if self.wx_frame:
            self.wx_frame.Destroy()

    def _OnKeyDown(self, e, widget=None):
        """A KeyDown event has been sent, create a control."""
        key_code = e.GetKeyCode()
        key = KEYMAP.get(key_code)

        if key is None:
            if key_code < 256:
                if key_code == 0:
                    key = "nul"
                elif key_code < 27:
                    key = f"ctrl{chr(key_code + 64)}"
                else:
                    key = chr(key_code)
            else:
                key = str(key_code)

        key = key.lower()

        # Add modifiers
        kwargs = {"raw_key": key}
        modified = ""
        modifiers = (
                (e.ControlDown(), "ctrl"),
                (e.AltDown(), "alt"),
                (e.ShiftDown(), "shift"),
        )

        for on, attr in modifiers:
            kwargs[attr] = on
            if on:
                if modified:
                    modified += "_"
                modified += attr

        if modified:
            key = f"{modified}_{key}"

        kwargs["key"] = key
        print(f"Process command key: {kwargs}")
        if widget:
            widget.generic._process_control("press", kwargs)
        else:
            self.generic._process_control("press", kwargs)

    def pop_dialog(self, dialog: SpecificWidget):
        """Pop up a dialog."""
        return dialog.pop()
