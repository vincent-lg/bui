"""Module containing the generic Text class, a generic text widget."""

from typing import Optional

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
        "release": "The user releases a key while the text is focused",
        "type": "The user types a character while the text is focused",
    }

    def __init__(self, leaf):
        super().__init__(leaf)
        self.x = leaf.x
        self.y = leaf.y
        self.id = leaf.id
        self.width = leaf.width
        self.height = leaf.height
        self.label = leaf.label
        self.value = leaf.value
        self.multiline = leaf.multiline
        self.read_only = leaf.read_only
        self._hidden = leaf.hidden
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
        """Return the text Cursor object."""
        return self._cursor

    @property
    def hidden(self):
        """Return whether the text is hidden or not."""
        return self.specific.hidden

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
        self._lineno = 0
        self._col = 0
        self._widget = widget

    @property
    def pos(self):
        """Return the current position as an indice."""
        return self._pos

    @property
    def lineno(self):
        """Return the current line number (vertical position of the cursor)."""
        return self._lineno

    @property
    def col(self):
        """Return the current column (horizontal position of the cursor)."""
        return self._col

    @property
    def at_begin(self):
        """Return True if the cursor is at the beginning of the text field."""
        return self._pos == 0

    @property
    def at_end(self):
        """Return True if the cursor is at the end of the text field."""
        return self._pos >= len(self._widget)

    @property
    def text_before(self):
        """Return the text before the cursor."""
        return self._widget.value[:self._pos]

    @property
    def text_after(self):
        """Return the text after the cursor."""
        return self._widget.value[self._pos:]

    @property
    def line(self):
        """Return the current line of text."""
        return self._widget.value.splitlines()[self._lineno]

    def move(self, pos: int, col: Optional[int] = None):
        """
        Move the cursor.

        This method accepts two possible signatures:
            move(position): moves the cursor to the absolute position
                    in the text.
            move(lineno, col): move the cursor at a given line number
                    and column number.

        """
        if col is None:
            self._widget.specific.move(pos)
        else:
            self._widget.specific.vertical_move(pos, col)
