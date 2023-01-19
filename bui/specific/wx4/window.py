"""The wxPython implementation of a BUI window.

In order to represent a BUI window with a grid, a wx.Window object is
created, containing a wx.Panel, containing a wx.GridBagSizer.  This
sizer is then used to place the BUI components on the window and
account for spanning that might occur.

"""

import asyncio
import traceback
from queue import Queue, Empty
import time
import threading
from typing import Dict, Union

from pubsub import pub
import wx

from bui.specific.base import *
from bui.specific.base.window import SpecificWindow
from bui.specific.wx4.shared import WXShared
from bui.specific.wx4.thread import WX_THREAD
from bui.tasks import cancel_all

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
            self.wx_app = wx.App(False)
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
        WX_THREAD.window = self.generic
        self._wx_init()
        area = self.usable_surface
        title = self.generic.title

        # Determine the optional parent
        if self.generic._bui_parent:
            parent = self.generic._bui_parent.specific.wx_frame
        else:
            parent = None

        self.wx_frame = wx.Frame(parent, title=title, name=title,
                size=tuple(area.bottom_right))
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

        # Start a WXThread if none exists
        if not WX_THREAD.is_alive():
            pub.subscribe(self.call, "callable")
            WX_THREAD.app = self.wx_app
            WX_THREAD.start()

    def position_for(self, widget):
        """
        Return the position for this widget.

        Args:
            widget (SpecificWidget): the specific widget.

        Returns:
            (x, y): position in pixels.

        """
        generic = widget.generic
        window = self.generic
        (top_x, top_y), (bottom_x, bottom_y) = self.usable_surface
        x = top_x + (generic.x / (window.width + 1)) * (bottom_x - top_x)
        y = top_y + (generic.y / (window.height + 1)) * (bottom_y - top_y)
        return (x, y)

    def size_for(self, widget):
        """
        Return the size for this widget.

        Args:
            widget (SpecificWidget): the specific widget to add.

        Returns:
            (x, y): size in pixels.

        """
        generic = widget.generic
        window = self.generic
        (top_x, top_y), (bottom_x, bottom_y) = self.usable_surface
        width = (bottom_x - top_x) * (generic.width / (window.width + 1)) - 5
        height = (bottom_y - top_y) * (generic.height / (window.height + 1)) - 5
        return (int(width), int(height))

    def add_widget(self, widget: SpecificWidget):
        """
        Add a widget on the window.

        Args:
            widget (SpecificWidget): the specific widget to add.

        """
        generic = widget.generic
        window = self.generic
        (top_x, top_y), (bottom_x, bottom_y) = self.usable_surface
        x = top_x + (generic.x / (window.width + 1)) * (bottom_x - top_x)
        y = top_y + (generic.y / (window.height + 1)) * (bottom_y - top_y)
        width = (bottom_x - top_x) * (generic.width / (window.width + 1)) - 5
        height = (bottom_y - top_y) * (generic.height / (window.height + 1)) - 5
        widget.wx_obj.SetPosition((int(x), int(y)))
        widget.wx_obj.SetSize(int(width), int(height))
        self.wx_sizer.Add(widget.wx_add)

    def show(self):
        """Show the window."""
        for wx_menu in self.wx_menus:
            wx_menu._complete(self)

        self.wx_frame.Show()

    async def _start(self, loop):
        """
        Start the window, watch events and allow async loop.

        Args:
            loop (AsyncLoop): the asynchronous event loop (see asyncio).

        """
        self.wx_app.MainLoop()

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
        if threading.current_thread() is threading.main_thread():
            self._close()
        else:
            self.in_main_thread(self._close)

    def _close(self):
        """Close this window, terminate loop if appropriate."""
        parent = None
        if self.wx_frame:
            # Show the parent window, if any
            parent = self.generic._bui_parent
            if parent is not None:
                parent.specific.wx_frame.Show()

            self.destroy(self.wx_frame)

        # Terminate the loop
        if parent is None:
            # The close event is to be set
            WX_THREAD.loop.call_soon_threadsafe(WX_THREAD.close_event.set)

            # Send a None event to the queue
            WX_THREAD.loop.call_soon_threadsafe(WX_THREAD.in_queue.put_nowait, (None, None, (), {}, False))

            # Send a "pass" to the output queue so it will skip all events
            WX_THREAD.out_queue.put_nowait((None, True))

    def destroy(self, wx_window):
        """Try and destroy the window."""
        wx_window.Show(False)
        wx_window.Destroy()

    def _OnContext(self, e, widget=None):
        """On context menu."""
        if widget:
            widget.generic._process_control("right_click")
        else:
            self.generic._process_control("right_click")

    async def pop_dialog(self, dialog: SpecificWidget, **kwargs):
        """Pop up a dialog."""
        dlg_queue = asyncio.Queue()
        self.in_main_thread(self.wx_pop_dialog, dialog, dlg_queue, **kwargs)
        return await dlg_queue.get()

    def wx_pop_dialog(self, dialog, bui_queue, **kwargs):
        """Pop the dialog in the main thread."""
        dialog = dialog.parse_layout(dialog, tag_name="dialog", **kwargs)
        wx_dialog = dialog.specific
        wx_dialog.wx_sizer.Fit(wx_dialog.wx_dialog)
        wx_dialog.wx_dialog.ShowModal()
        bui_queue._loop.call_soon_threadsafe(
                bui_queue.put_nowait, dialog)

    def pop_menu(self, context: SpecificWidget):
        """Pop a context menu, blocks until the menu is closed."""
        self.wx_frame.PopupMenu(context.wx_menu)

    async def pop_alert(self, title: str, message: str,
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
        queue = asyncio.Queue()
        self.in_main_thread(self.wx_pop_alert, title, message, danger,
                buttons, default, queue)
        status = await queue.get()
        return status

    def wx_pop_alert(self, title: str, message: str,
            danger: str, buttons: Dict[str, Union[bool, str]],
            default: str, queue):
        """Pop the alert in the main thread."""
        # Look for the icon
        icons = {
                "info": wx.ICON_INFORMATION,
                "warning": wx.ICON_WARNING,
                "error": wx.ICON_ERROR,
                "question": wx.ICON_QUESTION,
        }
        style = icons.get(danger, 0)
        if style == 0:
            raise ValueError(f"unknown danger: {danger!r}")

        button_styles = {
                "ok": wx.OK,
                "cancel": wx.CANCEL,
        }

        for button, button_style in button_styles.items():
            if button in buttons:
                style |= style

        if "yes" in buttons or "no" in buttons:
            style |= wx.YES_NO

        default_buttons = {
                "ok": wx.OK_DEFAULT,
                "cancel": wx.CANCEL_DEFAULT,
                "yes": wx.YES_DEFAULT,
                "no": wx.NO_DEFAULT,
        }
        style |= default_buttons[default]
        style |= wx.CENTRE
        parent = self.wx_parent
        dialog = wx.MessageDialog(parent, message, caption=title,
                style=style)
        ok = buttons.get("ok", False)
        cancel = buttons.get("cancel", False)
        yes = buttons.get("yes", False)
        no = buttons.get("no", False)
        if ok and cancel:
            dialog.SetOKCancelLabels(ok, cancel)
        elif isinstance(ok, str):
            dialog.SetOKLabel(ok)
        elif isinstance(yes, str) and isinstance(no, str) and isinstance(
                cancel, str):
            dialog.SetYesNoCancelLabels(yes, no, cancel)
        elif isinstance(yes, str) and isinstance(no, str):
            dialog.SetYesNoLabels(yes, no)

        old_focus = parent.FindFocus()
        res = dialog.ShowModal()
        old_focus.SetFocus()
        if res == wx.ID_OK:
            WX_THREAD.loop.call_soon_threadsafe(queue.put_nowait, "ok")
        elif res == wx.ID_CANCEL:
            WX_THREAD.loop.call_soon_threadsafe(queue.put_nowait, "cancel")
        elif res == wx.ID_YES:
            WX_THREAD.loop.call_soon_threadsafe(queue.put_nowait, "yes")
        elif res == wx.ID_NO:
            WX_THREAD.loop.call_soon_threadsafe(queue.put_nowait, "no")
        else:
            WX_THREAD.loop.call_soon_threadsafe(queue.put_nowait, "unknown")


    def prepare_other_window(self, window):
        """Prepare another window."""
        app = self.wx_app
        window.wx_app = app

    def open_window(self, window, child):
        """Open another window."""
        #self._wx_init()
        self.in_main_thread(self.wx_open_window, window, child)

    def wx_open_window(self, window, child):
        window = window.parse_layout(window)
        app = self.wx_app
        window.specific.wx_app = app
        #app.top_windows.append(window.wx_frame)
        if child:
            window.specific.wx_frame.CenterOnParent()
            window.specific.wx_frame.GetParent().Hide()

        window.specific.show()

    def call(self, callback, args=None, kwargs=None):
        """Execute the given callable."""
        args = args or ()
        kwargs = kwargs or {}
        callback(*args, **kwargs)
        #except RuntimeError:
        #    # Although not perfect, this will catch errors raised by
        #    # wxPython if the object was deleted.
        #    pass
