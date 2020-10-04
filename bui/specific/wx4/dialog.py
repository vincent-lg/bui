"""The wxPython implementation of a BUI custom dialog box."""

import asyncio

import wx

from bui.specific.base import *
from bui.specific.base.dialog import SpecificDialog
from bui.specific.wx4.window import WX4Window

class WX4Dialog(WX4Window, SpecificDialog):

    def _init(self):
        self.wx_parent = self.wx_dialog = wx.Dialog(self.generic.window.specific.wx_parent)
        self.wx_sizer = wx.BoxSizer(wx.VERTICAL)
        self.wx_dialog.SetSizer(self.wx_sizer)
        self.wx_sizer.Fit(self.wx_dialog)

    async def pop(self, **kwargs):
        self.dlg_event = asyncio.Event()
        self.in_main_thread(self.wx_pop, **kwargs)
        await self.dlg_event.wait()

    def wx_pop(self, **kwargs):
        """Pop the dialog in the main thread."""
        self.wx_sizer.Fit(self.wx_dialog)
        self.wx_dialog.ShowModal()
        self.dlg_event._loop.call_soon_threadsafe(
                self.dlg_event.set())

    def close(self):
        self.in_main_thread(self.destroy)

    def destroy(self):
        self.wx_dialog.Destroy()

