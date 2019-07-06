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
        self._wx_app = None
        self._wx_display = None

    @property
    def usable_surface(self):
        self._wx_init()
        rect = self._wx_display.ClientArea
        return Rectangle((rect.x, rect.y), (rect.width, rect.height))

    def _wx_init(self):
        """Initialize wx (creating a wx.App) if necessary."""
        if not self._wx_app:
            self._wx_app = AsyncApp()
            self._wx_display = wx.Display()

    @property
    def title(self):
        """Return the current title, override in child class."""
        return self._wx_frame.GetTitle()

    @title.setter
    def title(self, new_title):
        """Set the window's title, override in child class."""
        self._wx_frame.SetTitle(new_title)

    def _init(self):
        """Initialize the specific widget."""
        self._wx_init()
        title = self.generic.leaf.title
        self._wx_frame = wx.Frame(None, title=title, name=title)
        self._wx_window = wx.Window(self._wx_frame)
        self._wx_panel = wx.Panel(self._wx_window, style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN | wx.FULL_REPAINT_ON_RESIZE)
        self._wx_grid = wx.GridBagSizer(vgap=5, hgap=5)

        # Bind press and type controls
        if "press" in self.generic.controls:
            self._wx_window.Bind(wx.EVT_KEY_DOWN, self._OnKeyDown)

        for child in self.generic.leaf.children:
            widget = child.widget
            widget._bind_controls(self.generic)
            widget._init()

        children = self.generic.leaf.children
        if children:
            children[0].widget.specific.focus()


        box = wx.BoxSizer()
        box.Add(self._wx_grid, 1, wx.EXPAND, 10)

        self._wx_panel.SetSizerAndFit(box)
        self._wx_frame.SetClientSize(self._wx_panel.GetSize())

    def _start(self, loop):
        """
        Start the window, watch events and allow async loop.

        Args:
            loop (AsyncLoop): the asynchronous event loop (see asyncio).

        """
        self._wx_frame.Show()
        self._wx_app.loop = loop
        return self._wx_app.MainLoop()

    def create_menubar(self, menubar):
        """Create a menu bar."""
        wx_menubar = wx.MenuBar()

        # Create menus and then meny items in each menu
        for menu in menubar.children:
            wx_menu = wx.Menu()
            for item in menu.children:
                wx_item = wx_menu.Append(wx.ID_ANY, item.data)
                self._wx_frame.Bind(wx.EVT_MENU, item.widget.specific.OnMenu, wx_item)
            wx_menubar.Append(wx_menu, menu.name)
        self._wx_frame.SetMenuBar(wx_menubar)

    def close(self):
        """Close this window, terminate loop if appropriate."""
        self._wx_frame.Destroy()

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
