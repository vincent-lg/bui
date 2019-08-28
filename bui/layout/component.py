"""Parent class of all window components in a layout stand-point."""

NO_VALUE = object()

class Component:

    tag_name = "to set"
    attrs = ()
    must_have_data = False
    has_widget = True

    def __init__(self, layout, parent):
        self.layout = layout
        self.parent = parent
        self.children = []
        self.id = ""
        self.data = ""
        self.widget = None

    def __repr__(self):
        return f"<{self.tag_name.capitalize()}(attrs={len(self.attrs)}), has_data={bool(self.data)})>"

    def __str__(self):
        return self.display(0)

    @property
    def provided_attrs(self):
        """Return a list [(attr, value)] of attributes."""
        values = []
        for attr in self.attrs:
            value = getattr(self, attr.name, NO_VALUE)
            values.append((attr, value))

        return values

    @property
    def opening(self):
        """
        Return the opening tag without the trailing >.

        For instance:
            <window
        Or:
            <button id=btn x=2 y=5

        """
        provided = self.provided_attrs
        attrs = ""
        for attr, value in provided:
            if attrs:
                attrs += " "

            name = attr.name
            if value is not NO_VALUE:
                value = str(value)
                if " " in value:
                    value = repr(value)

                attrs += f"{name}={value}"
            else:
                attrs += f"{name}"

        if attrs:
            return f"<{self.tag_name} {attrs}"
        else:
            return f"<{self.tag_name}"

    def display(self, ident: int) -> str:
        """
        Display this tag with child tags if appropriate.

        Args:
            ident (int): the identation level.

        Returns:
            formatted (str): the formatted string representation.

        """
        tag = self.opening
        if self.children:
            tag += ">"
            for child in self.children:
                tag += f"\n{(ident + 1) * 2 * ' '}{child.display(ident=ident + 1)}"
            tag += f"\n{ident * 2 * ' '}</{self.tag_name}>"
        elif self.data:
            tag += f">{self.data}</{self.tag_name}>"
        else:
            tag += f" />"

        return tag

    @classmethod
    def can_be_inside(cls, parent_types, parent):
        """
        Can this tag be included in a parent tag?

        Args:
            parent_types (object): None, one or more parents in a tuple.
            parent (Component): the parent component.

        Returns:
            can_be (bool): can this tag be included?

        Raises:
            ValueError: give more details about the reason why, in case of rejection.

        """
        if parent_types is None:
            if parent:
                raise ValueError(f"{cls.tag_name} should be a parent tag, not contained in <{parent.tag_name}>")

            return True

        if isinstance(parent, parent_types):
            return True

        if not isinstance(parent_types, (list, tuple)):
            parent_types = (parent_types, )

        allowed = [f"<{tag.tag_name}>" for tag in parent_types]
        if len(allowed) > 1:
            allowed = ", ".join(allowed[:-1]) + " or " + allowed[-1]
        else:
            allowed = allowed[0]

        raise ValueError(f"component {cls.tag_name} should be placed inside {allowed}")

    def complete(self):
        """Complete the widet, when all the layout has been set."""
        pass

    @staticmethod
    def deduce_id(deduce_from: str) -> str:
        """
        Try and return a deduced identifier.

        An identifier must be a lowercase version of the given data with only
        letters.  Spaces in the data are replaced with the
        underscore (_).  A tabulation will break parsing.  Letters are
        copied as-is.  Non-letter symbols are just ignored.

        Args:
            deduce_from (str): the origin or the identifier to deduce.

        Examples:
            >>> Component.deduce_id("click me!")
            `click_me`
            >>> Component.deduce_id("Quit\tCTRL + Q")
            'quit'

        """
        identifier = ""
        for char in deduce_from:
            if char.isalpha():
                identifier += char.lower()
            elif char == " " and not identifier.endswith("_"):
                identifier += "_"
            elif char == "\t":
                break

        return identifier.strip("_")
