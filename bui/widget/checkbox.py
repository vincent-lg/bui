"""Module containing the generic Checkbox class, a generic checkbox widget."""

from bui.widget.base import Widget, CachedProperty

class Checkbox(Widget):

    """
    The generic checkbox widget.

    A checkbox is meant to be contained inside a
    [window](../layout/tag/window.md) tag.  It can have a label and can
    be checked or not checked.

    This is a generic widget which will be converted into a specific widget,
    depending on the used GUI toolkit.

    """

    widget = "checkbox"
    class_name = "Checkbox"
    default_controls = {
        "check": "This checkbox is being checked or unchecked.",
        "init": "This checkbox is ready to be displayed.",
        "press": "The user presses on a key while the checkbox is focused.",
        "release": "The user releases a key while the checkbox is focused",
        "type": "The user types a character while the checkbox is focused",
    }
    implicit_control = "click"

    def __init__(self, leaf):
        super().__init__(leaf)
        self.x = leaf.x
        self.y = leaf.y
        self.width = leaf.width
        self.height = leaf.height
        self.id = leaf.id
        self.name = self.cached_name = leaf.name
        self.cached_checked = leaf.checked
        self._enabled = True

    def __bool__(self):
        return self.checked

    @CachedProperty
    def id(self):
        return self.leaf.id

    @CachedProperty
    def name(self):
        return self.specific.name

    @name.setter
    def name(self, name):
        self.specific.name = name

    @CachedProperty
    def checked(self):
        return self.specific.checked

    @checked.setter
    def checked(self, checked):
        self.specific.checked = checked

    @property
    def enabled(self):
        """Return whether the checkbox is enabled or not."""
        return self._enabled

    @property
    def disabled(self):
        """Return whether the checkbox is disabled or not."""
        return not self._enabled

    def check(self):
        """Force check this checkbox."""
        self.checked = True

    def uncheck(self):
        """Force uncheck this checkbox."""
        self.checked = False

    def enable(self):
        """Force-enable the checkbox."""
        self.specific.enable()

    def disable(self):
        """Disable the checkbox."""
        self.specific.disable()

    def handle_check(self, control):
        """Do nothing if a checkbox is clicked."""
        pass

    def handle_init(self, control):
        """Do nothing if a checkbox is pressed."""
        pass

    def handle_press(self, control):
        """Do nothing if a checkbox is pressed."""
        pass
