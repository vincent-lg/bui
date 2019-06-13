"""Base generic widget."""

from collections import defaultdict

from bui.control import CONTROLS

class Widget:

    """Parent class for all generic widgets."""

    widget = ""
    specific_package = None
    default_controls = {}
    implicit_control = ""

    def __init__(self, leaf):
        self.leaf = leaf
        self.id = leaf.id
        self.specific = None
        self.controls = defaultdict(list)

    def __repr__(self):
        return f"<bui.generic.{self.widget} object>"

    def __str__(self):
        return f"bui.generic.{self.widget}({self.id}"

    def create_specific(self):
        """
        Create the specific widget, using the `specific_package` attribute.

        If the specific object has already been created, don't recreate it and
        raise no exception.

        """
        if not self.specific:
            class_name = self.class_name
            SpecificWidget = getattr(self.specific_package, class_name)
            self.specific = SpecificWidget(self)

    def _init(self):
        """
        Private message, initialize the widget and its specific counterpart.

        This method should be called internally by BUI and not by the user.
        It performs some action to set the specific widget.  The specific
        widget is a GUI-toolkit dependent object and should be ignored
        by the user.  This method is called when the layout tree has been
        created, each generic widget is ready to be used but before
        the user should have access to this tree.  Therefore, when the user
        has access to the layout or widget tree, it is likely the widget
        has been properly initialized.

        """
        return self.specific._init()

    def _process_control(self, control_name, options=None):
        """Process an in-progress control."""
        options = options or {}
        Control = CONTROLS.get(control_name)
        if Control is None:
            raise ValueError(f"unknown control {control_name!r}")

        control = Control(self, **options)
        control.process(options)

    def _bind_controls(self, window):
        """Bind the diget controls."""
        for name in self.default_controls.keys():
            Control = CONTROLS.get(name)
            Control._bind_methods(self, window)
