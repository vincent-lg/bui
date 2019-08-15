"""Right-click control, used on most widgets to signal a right click."""

from bui.control.base import Control

class RightClick(Control):

    """
    When the user right clicks or presses the application key.

    This control is fired when the user right clicks on a widget
    or anywhere in the window.  This control is also fired when
    the user presses the application key while a widget in the window
    is focused.  It is common to link this control to the
    [context menu pop-up](../layout/tag/context.md).

    """

    name = "right_click"
    widgets = {
            "window": "The user right clicks in the window.",
    }

    def perform(self, options=None):
        """
        When the control is triggered.

        By default, no action is performed when right clicking.

        """
        super().perform(options)
