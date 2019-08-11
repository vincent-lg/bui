"""Class to represent an attribute in a layout tag.

An attribute in this case is similar to a HTML attribute:

    <window title="Something good">

In this case, the attribute is `title`.  Some markups (tags) have mandatory
or optional attributes and they must match the specifications.  Attributes
are listed in the layout class (see for instance `bui/layout/window.py`).

An `Attr` object is somewhat similar to an argument in `argparse`, and
possesses very similar attributes.

"""

NO_DEFAULT = object()
NO_VALUE = object()

class Attr:

    """
    A tag attribute, mandatory or not.

    It can have a default value and a type to be converted.  It should
    always have a name (first argument) and a help text.

    Args:
        name (str): the attribute name.
        help (str): the help text, given in case of errors for instance.
        type (any, optional): the attribute type (default str).  It can
                be set to another class, like `type=int` for an integer
                conversion.  In this case, the attribute will be converted
                before the layout class is created, and an error message
                will be sent if the conversion fails.
        default (any): a default value.  It can be ca callable, in which
                case, this callable will be called and its return value
                will be used as a default.
        if_present: set a default value if the attribute is set, no matter
                what the value the user specified.  This is useful for
                toggable attributes.

    """

    def __init__(self, name, help, type=str, default=NO_DEFAULT,
            if_present=NO_DEFAULT):
        self.name = name
        self.help = help
        self.type = type
        self.default = default
        self.if_present = if_present

    @property
    def python_name(self):
        """Return a Python identifier."""
        return self.name.replace("-", "_")

    def prepare(self, value=NO_VALUE):
        """
        Prepare and return the proper value for this attribute, if possible.

        Otherwise, a clear `ValueError` is raised.

        The `value` can be `None` to indicate an attribute without value:

            <checkbox checked>

        If you leave the argument empty, this is assumed to mean that
        this attribute wasn't given.  In which case, the default value will
        be returned, if any, or a proper error message will be raised.

        """
        if value is not NO_VALUE and self.if_present is not NO_DEFAULT:
            return self.if_present

        if value is NO_VALUE:
            if self.default is NO_DEFAULT:
                raise ValueError(f"the attribute {self.name} is mandatory, "
                        f"but no value was given to it.  {self.help}")
            elif callable(self.default):
                return self.default()

            return self.default

        # A value has been specified. Is it of the proper type?
        try:
            value = self.type(value)
        except ValueError:
                raise ValueError(f"the attribute {self.name} received an "
                        f"invalid value ({value} of type {type(value)}).  {self.help}") from None

        return value
