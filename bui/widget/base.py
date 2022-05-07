"""Base generic widget."""

import asyncio
from collections import defaultdict

from bui.control import CONTROLS
from bui.tasks import schedule

class Widget:

    """Parent class for all generic widgets."""

    widget = ""
    specific_package = None
    default_controls = {}
    implicit_control = ""

    def __init__(self, leaf):
        self.leaf = leaf
        self.specific = None
        self.parent = leaf.parent.widget if leaf.parent is not None else None
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

    def _process_control(self, control_name, options=None, callback=None):
        """Process an in-progress control."""
        options = options or {}
        Control = CONTROLS.get(control_name)
        if Control is None:
            raise ValueError(f"unknown control {control_name!r}")

        control = Control(self, **options)
        return control.process(options, callback=callback)

    def _bind_controls(self, window):
        """Bind the diget controls."""
        for name in self.default_controls.keys():
            Control = CONTROLS.get(name)
            Control._bind_methods(self, window)

    def schedule(self, coroutine):
        """Schedule the specified coroutine in the main event loop."""
        return schedule(coroutine)

    async def sleep(self, seconds):
        """
        Asynchronous sleep during the specified number of seconds.

        This method should ONLY be called in an asynchronous control method.
        It is a shortcut to `asyncio.sleep`.

        Args:
            seconds (int or float): the number of seconds to wait.

        """
        await asyncio.sleep(seconds)


class CachedProperty(property):

    """
    Cached property, to act like a property with inner cache.

    Use it like a standard property:

        class MyClass:

            @CachedProperty
            def x(self):
                return 5

            @x.setter
            def x(self, new_x):
                print(f"Setting x = {new_x}")

    Internally, however, the property content is cached when it's
    modified.  This is useful to define widget properties, as
    we don't want to read the specific widget (which might call an
    expensive method) each time we access the property.  However, when the
    property is modified, we both update the cache and send the required
    update to the specific widget.

    A CachedProperty, much like a property, can be read-only, or read and
    write.  If the property cannot be written, the cache is not modified.
    However, if the generic object containing the property hasn't been
    linked to a specific object yet (setting is still done in layout at this
    point, no window is created), a read-only property would still modify
    the cached when written with no error.

    """

    def __get__(self, obj, type=None):
        """Get the cached value."""
        if obj is not None:
            attr = self.fget.__name__
            cached_attr = f"cached_{attr}"
            if hasattr(obj, cached_attr):
                return getattr(obj, cached_attr)
            else:
                value = super().__get__(obj, type)
                setattr(obj, cached_attr, value)
                return value

    def __set__(self, obj, value):
        """Set the cache and call the fset function."""
        attr = self.fget.__name__
        cached_attr = f"cached_{attr}"
        if obj.specific is not None:
            res = self.fset(obj, value)
            if res is not None:
                value = res

        setattr(obj, cached_attr, value)
