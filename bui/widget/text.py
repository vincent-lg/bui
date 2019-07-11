"""Module containing the generic Text class, a generic text widget."""

from bui.widget.base import Widget, CachedProperty

class Text(Widget):

    """
    The generic text widget.

    A text is meant to be contained inside a
    [window](../layout/tag/window.md) tag.  The user can edit the content
    of the text area which can be on one or several lines, cleared or
    masked like a password.

    This is a generic widget which will be converted into a specific widget,
    depending on the used GUI toolkit.

    """

    widget = "text"
    class_name = "Text"
    default_controls = {
        "change": "This text area's value has changed.",
        "init": "This text area is ready to be displayed.",
        "press": "The user presses on a key while the text area is focused.",
    }

    def __init__(self, leaf):
        super().__init__(leaf)
        self.id = leaf.id
        self.label = leaf.label
        self.value = leaf.value

    @CachedProperty
    def id(self):
        return self.leaf.id

    @CachedProperty
    def label(self):
        return self.specific.label

    @label.setter
    def label(self, label):
        self.specific.label = label

    @CachedProperty
    def value(self):
        return self.specific.value

    @value.setter
    def value(self, value):
        self.specific.value = value

    @property
    def enabled(self):
        """Return whether the text is enabled or not."""
        return self.specific.enabled

    @property
    def disabled(self):
        """Return whether the text is disabled or not."""
        return self.specific.disabled

    def enable(self):
        """Force-enable the text."""
        self.specific.enable()

    def disable(self):
        """Disable the text."""
        self.specific.disable()
