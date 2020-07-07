"""The wxPython implementation of a BUI custom dialog box."""

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

    def pop(self):
        self.wx_sizer.Fit(self.wx_dialog)
        return self.wx_dialog.ShowModal()

    def close(self):
        self.wx_dialog.Destroy()
