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
        self.x = leaf.x
        self.y = leaf.y
        self.id = leaf.id
        self.label = leaf.label
        self.value = leaf.value
        self.multiline = leaf.multiline
        self.read_only = leaf.read_only
        self._cursor = Cursor(self)

    def __len__(self):
        return len(self.value)

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

    @property
    def cursor(self):
        return self._cursor

    def enable(self):
        """Force-enable the text."""
        self.specific.enable()

    def disable(self):
        """Disable the text."""
        self.specific.disable()


class Cursor:

    """
    Class to represent a cursor in a text field.

    A cursor object is created when a text widget is created.  This cursor
    object will be updated whenever the need arises.

    """

    def __init__(self, widget):
        self._pos = 0
        self._widget = widget

    @property
    def pos(self):
        return self._pos

    @property
    def at_begin(self):
        return self._pos == 0

    @property
    def at_end(self):
        return self._pos > len(self._widget)

    @property
    def text_before(self):
        return self._widget.value[:self._pos]

    @property
    def text_after(self):
        return self._widget.value[self._pos:]
