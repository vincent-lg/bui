"""Click control, used on buttons, menu items, and other widgets."""

from bui.control.base import Control

class Click(Control):

    """
    When the user clicks on the widget.

    This control probably is the most often used in any window.  It is
    triggered when the user clicks on a button or use a similar
    trigger.  If the user presses RETURN or SPACE on the widget, and
    if the operating system supports this action as a click, this
    control is also triggered, which makes things much easier for people
    not using the mouse to navigate.

    """

    name = "click"
    widgets = {
            "item": "A menu item is clicked",
    }

    def perform(self, options=None):
        """
        When the control is triggered.

        The default specific action that is performed depends on the
        chosen GUI toolkit, but you can expect that buttons
        will be clicked, menu items will close the menu bar and
        checkbox will be toggled.  You can prevent this control (this
        will be sent to the GUI toolkit which should abort the action
        as well).

        """
        super().perform(options)
