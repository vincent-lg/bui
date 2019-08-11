"""The wxPython implementation of a BUI radio button group widget."""

import wx

from bui.specific.base import *
from bui.specific.base.radio import SpecificRadioButton

class WX4RadioButton(SpecificRadioButton):

    """Wx-specific radio button widget."""

    def _init(self):
        self.wx_choices = []
        window = self.parent
        self.wx_panel = wx.Panel(window.wx_parent)
        self.wx_grid = wx.GridSizer(cols=1)
        self.wx_obj = self.wx_add = self.wx_panel

        for i, (_, label) in enumerate(self.generic.choices):
            style = 0 if i > 0 else wx.RB_GROUP
            choice = wx.RadioButton(self.wx_panel, label=label, style=style,
                    name=label)
            self.wx_grid.Add(choice, proportion=1)
            self.wx_choices.append(choice)
            choice.Bind(wx.EVT_RADIOBUTTON, self.OnSelect)
            choice.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        self.wx_panel.SetSizer(self.wx_grid)
        window.add_widget(self)

    def refresh(self):
        """Refresh the available choices."""
        if not hasattr(self, "wx_choices"):
            return

        for choice in self.wx_choices:
            choice.Destroy()

        self.wx_choices[:] = []
        self.wx_grid = wx.GridSizer(cols=1)

        for i, (_, label) in enumerate(self.generic.choices):
            style = 0 if i > 0 else wx.RB_GROUP
            choice = wx.RadioButton(self.wx_panel, label=label, style=style,
                    name=label)
            self.wx_grid.Add(choice, proportion=1)
            self.wx_choices.append(choice)
            choice.Bind(wx.EVT_RADIOBUTTON, self.OnSelect)
            choice.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        self.wx_panel.SetSizer(self.wx_grid)

    def OnSelect(self, e):
        """When the selected radio button changes."""
        wx_choice = e.GetEventObject()
        index = self.wx_choices.index(wx_choice)
        self.generic._selected = index

    def OnKeyDown(self, e):
        window = self.parent
        if "press" in self.generic.controls:
            window._OnKeyDown(e, self)
        else:
            window._OnKeyDown(e)
        e.Skip()
