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
        self.x = leaf.x
        self.y = leaf.y
        self.width = leaf.width
        self.height = leaf.height
        self.id = leaf.id
        self.name = leaf.name

        # Dialog-specific attributes
        self.set_true = leaf.set_true
        self.set_false = leaf.set_false
        self.set = leaf.set

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
        if self.parent.widget == "dialog":
            if self.set_true or self.set_false or self.set:
                if self.set:
                    self.parent.set = self.set
                elif self.set_true:
                    self.parent.set = True
                elif self.set_true:
                    self.parent.set = False
                self.parent.close()

    def handle_press(self, control):
        """Do nothing if a button is pressed."""
        pass
