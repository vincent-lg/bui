"""Module containing the generic Button class, a generic button widget."""

from bui.widget.base import Widget, CachedProperty

class Button(Widget):

    """
    The generic button widget.

    A button is meant to be contained inside a
    [window](../layout/tag/window.md) tag.  It can have a label and can
    be linked with specific control methods.

    This is a generic widget which will be converted into a specific widget,
    depending on the used GUI toolkit.

    """

    widget = "button"
    class_name = "Button"
    default_controls = {
        "click": "This button is being clicked on or activated from the keyboard",
        "press": "The user presses on a key while the button is focused.",
    }
    implicit_control = "click"

    def __init__(self, leaf):
        super().__init__(leaf)
        self.name = leaf.name
        self.id = leaf.id

    @CachedProperty
    def name(self):
        return self.specific.name

    @name.setter
    def name(self, name):
        self.specific.name = name

    @CachedProperty
    def id(self):
        return self.leaf.id

    def handle_click(self, control):
        """Do nothing if a button is clicked."""
        pass

    def handle_press(self, control):
        """Do nothing if a button is pressed."""
        pass
