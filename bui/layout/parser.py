"""Class to parse a layout description described in a pseudo-HTML syntax.

The `html.parser.HTMLParser` class is actually used, so that the parser
could interpret more complex instructions.  It also interprets other
markups.  However, contrary to HTML, the language is meant to be strict
in content (you shouldn't close an outer tag with an inner tag not being
closed, for instance).

The layout definition can be found in specific `.bui` files, or within the
source code of a [Window](Window.md) or [Dialog](Dialog.md) class, in the
`layout` class attribute.

See [layout overview](../layout/overview.md) for more details.

"""

from html.parser import HTMLParser

from bui.layout.layout import Layout
from bui.layout import TAGS

class BUILayoutParser(HTMLParser):

    """Parser object of BUI layout."""

    def __init__(self, filename, start_line=0):
        super().__init__()
        self.filename = filename
        self.start_line = start_line
        self.current_component = None
        self.layout = Layout()

    @property
    def cur_line(self):
        return self.start_line + self.getpos()[0]

    @property
    def cur_offset(self):
        return self.getpos()[1]

    @property
    def pos(self):
        return f"{self.filename} [line {self.cur_line}, col {self.cur_offset}]"

    def handle_starttag(self, name, attrs):
        """
        The beginning of a tag has been met.

        Args:
            name (str): the tag name, always lowercase.
            attrs (tuple): a tuple of attributes, each element being
                    a tuple containing (attribute name, attribute value),
                    both as str.

        """
        Tag, parent_types = TAGS.get(name, (None, None))
        if Tag is None:
            raise ValueError(f"Error {self.pos}: unknown tag {name}")

        # Browse attributes
        remaining = list(Tag.attrs)
        values = {}
        for attr_name, value in attrs:
            candidates = [attr for attr in remaining if attr.name == attr_name]
            if not candidates:
                raise ValueError(f"Error {self.pos}: tag {name}, unknown attribute {attr_name}")

            attr = candidates[0]
            try:
                value = attr.prepare(value)
            except ValueError as err:
                raise ValueError(f"Error {self.pos}: attribute {attr.name}, {err}") from None
            else:
                values[attr.python_name] = value
                remaining.remove(attr)

        for attr in remaining:
            try:
                value = attr.prepare()
            except ValueError as err:
                raise ValueError(f"Error {self.pos}: attribute {attr.name}, {err}") from None
            else:
                values[attr.python_name] = value

        # If there's already one open component, add it to the element if possible
        Tag.can_be_inside(parent_types, self.current_component)
        if self.current_component:
            tag = Tag(self.layout, self.current_component, **values)
            self.current_component.children.append(tag)
            self.current_component = tag
        else:
            tag = Tag(self.layout, None, **values)
            self.current_component = tag
            self.layout.components.append(tag)

    def handle_endtag(self, tag):
        current = self.current_component
        if current:
            if not current.data and current.must_have_data:
                raise ValueError(f"Error {self.pos}: component {current.tag_name} should have data")

            self.current_component = current.parent
        else:
            raise ValueError(f"Error {self.pos}: structural error, mismatched tags")

    def handle_data(self, data):
        if self.current_component:
            self.current_component.data = data.strip()
