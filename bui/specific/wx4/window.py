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
from bui.specific.wx4.shared import WXShared

WX_APP = None

class WX4Window(WXShared, SpecificWindow):

    def __init__(self, generic):
        super().__init__(generic)
        self.wx_app = None
        self.wx_display = None
        self.wx_menus = []

    @property
    def usable_surface(self):
        self._wx_init()
        rect = self.wx_display.ClientArea
        return Rectangle((rect.x, rect.y), (rect.width, rect.height))

    def _wx_init(self):
        """Initialize wx (creating a wx.App) if necessary."""
        global WX_APP
        if self.wx_app:
            pass
        elif WX_APP:
            self.wx_app = WX_APP
        elif not self.wx_app:
            self.wx_app = AsyncApp(self)
            WX_APP = self.wx_app

        if not self.wx_display:
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
        #self.wx_app.top_windows.append(self.wx_frame)
        self.wx_parent = self.wx_panel = wx.Panel(self.wx_frame)
        self.wx_sizer = wx.BoxSizer(wx.VERTICAL)

        # Bind press and type controls
        if "press" in self.generic.controls:
            self.watch_keyboard(self.wx_panel)
        if "right_click" in self.generic.controls:
            self.wx_frame.Bind(wx.EVT_CONTEXT_MENU, self._OnContext)

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

    def show(self):
        """Show the window."""
        for wx_menu in self.wx_menus:
            wx_menu._complete(self)

        self.wx_frame.Show()

    def _start(self, loop):
        """
        Start the window, watch events and allow async loop.

        Args:
            loop (AsyncLoop): the asynchronous event loop (see asyncio).

        """
        self.wx_app.top_windows.append(self.wx_frame)
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

    def _OnContext(self, e, widget=None):
        """On context menu."""
        if widget:
            widget.generic._process_control("right_click")
        else:
            self.generic._process_control("right_click")

    def pop_dialog(self, dialog: SpecificWidget):
        """Pop up a dialog."""
        return dialog.pop()

    def pop_menu(self, context: SpecificWidget):
        """Pop a context menu, blocks until the menu is closed."""
        self.wx_frame.PopupMenu(context.wx_menu)

    def prepare_other_window(self, window):
        """Prepare another window."""
        app = self.wx_app
        window.wx_app = app

    def open_window(self, window, child):
        """Open another window."""
        #self._wx_init()
        app = self.wx_app
        window.wx_app = app
        app.top_windows.append(window.wx_frame)
        if child:
            window.specific.wx_frame.SetParent(self.wx_frame)
        window.show()
