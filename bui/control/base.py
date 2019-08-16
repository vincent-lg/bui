"""Base control.

All controls should inherit from the below class.

"""

import asyncio
import inspect
import re

class Control:

    """Base control, parent class of all controls."""

    name = ""
    window_control = True
    widget_control = True
    has_sub_controls = False
    pattern_for_window = ""
    pattern_for_widgets = ""
    options = ()

    def __init__(self, widget):
        self.widget = widget

    @classmethod
    def _bind_methods(cls, widget, window):
        """
        Bind one or more methods to this control.

        Args:
            widget (Widget): the widget on which are controls.
            window (Window); othe window on which are control methods.

        """
        if cls.has_sub_controls:
            # This control has sub-controls
            # sub-controls can all be linked to control methods
            if cls.window_control and widget is window:
                method_name = f"on_{cls.name}"
                bound = cls._register_method(widget, window, method_name)
                if bound and window._debug_controls:
                    print(
                            f"    Bound {cls.name} as a window control "
                            f"to the {method_name!r} method"
                    )

                if cls.pattern_for_window:
                    pattern = re.compile(cls.pattern_for_window)
                    contents = dir(window)
                    for content in contents:
                        match = pattern.search(content)
                        if match:
                            group = match.groupdict()
                            bound = cls._register_method(widget, window,
                                    content, group=group)
                            if bound and window._debug_controls:
                                print(
                                    f"    Bound {cls.name} as a window "
                                    f"control with {group} to the "
                                    f"{content!r} method"
                                )
            elif cls.widget_control:
                method_name = f"on_{cls.name}_{widget.id}"
                bound = cls._register_method(widget, window, method_name)
                if bound and window._debug_controls:
                    print(
                            f"    Bound {cls.name} as a widget control "
                            f"of {widget.id} to the {method_name!r} method"
                    )

                if cls.pattern_for_widgets:
                    pattern = cls.pattern_for_widgets.format(id=widget.id)
                    pattern = re.compile(pattern)
                    contents = dir(window)
                    for content in contents:
                        match = pattern.search(content)
                        if match:
                            group = match.groupdict()
                            bound = cls._register_method(widget, window,
                                    content, group=group)
                            if bound and window._debug_controls:
                                print(
                                    f"    Bound {cls.name} as a widget "
                                    f"control of {widget.id} with "
                                    f"{group} to the {content!r} method"
                                )

            return

        bound = False
        if widget.implicit_control == cls.name:
            # This is an implicit control, don't force-add any method
            if cls.window_control and widget is window:
                method_name = f"on_{cls.name}"
            elif cls.widget_control:
                method_name = f"on_{widget.id}"
            else:
                method_name = None

            if method_name:
                bound = cls._register_method(widget, window, method_name,
                        force=False)
                if bound and window._debug_controls:
                    if cls.window_control and widget is window:
                        print(
                            f"    Bound {cls.name} as an implicit window "
                            f"control to the {method_name!r} method"
                        )
                    else:
                        print(
                            f"    Bound {cls.name} as an implicit widget "
                            f"control of {widget.id} to the "
                            f"{method_name!r} method"
                        )

        if not bound:
            if cls.window_control and widget == window:
                method_name = f"on_{cls.name}"
                if cls._register_method(widget, window, method_name):
                    if window._debug_controls:
                        print(
                            f"    Bound {cls.name} as a window control "
                            f"to the {method_name!r} method"
                        )
                    return

            if cls.widget_control and hasattr(widget, "id"):
                method_name = f"on_{cls.name}_{widget.id}"
                if cls._register_method(widget, window, method_name):
                    if window._debug_controls:
                        print(
                            f"    Bound {cls.name} as a widget control of "
                            f"{widget.id} to the {method_name!r} method"
                        )

    @classmethod
    def _register_method(cls, widget, window, method_name, force=True, group=None):
        """Try to register a control method."""
        group = group or {}
        method = getattr(window, method_name, None)
        if method:
            former, control = window.control_methods.get(method_name, (None, None))
            if former and force:
                raise ValueError(
                        f"attempting to connect control {widget}"
                        f"[{cls.name}] but fails because {former}[{control}] "
                        f"is using the same method ({method_name}).  Please "
                        f"clarify their respective IDs and use explicit "
                        f"names to avoid this conflit.")

            widget.controls[cls.name].append((group, method))
            window.control_methods[method_name] = (widget, cls.name)
            return True

        return False

    def process(self, options=None):
        """Process the control, calls a generic `on_` method if found."""
        # Call on_{control} on the widget
        print(f"  Fire {self.name} control with options={options}")
        method = getattr(self.widget, f"handle_{self.name}", None)
        if method:
            method(self)

        # Call the `on_...` method on the window
        options = options or {}
        methods = self.widget.controls.get(self.name, [])
        for group, method in methods:
            to_test = {}
            for key, value in options.items():
                if key in group.keys():
                    to_test[key] = value

            if group and group == to_test:
                if method.__self__._debug_controls:
                    print(
                        f"    Match sub-control to "
                        f"{method.__name__}, call it"
                    )
                return self._call_method(method)

        # At this point we consider no match was found in the options,
        # so we call the parent control if appropriate.
        options = {}
        methods = self.widget.controls.get(self.name, [])
        for group, method in methods:
            if group == options:
                if method.__self__._debug_controls:
                    print(
                        f"    Match parent control to "
                        f"{method.__name__}, call it"
                    )
                return self._call_method(method)

    def _call_method(self, method):
        """Call a control method with optional arguments."""
        signature = inspect.signature(method)
        parameters = tuple(signature.parameters.keys())
        kwargs = {}
        for key in self.options:
            if key in parameters:
                kwargs[key] = getattr(self, key)

        if "control" in parameters:
            kwargs["control"] = self

        if "widget" in parameters:
            kwargs["widget"] = self.widget

        result = method(**kwargs)
        if asyncio.iscoroutine(result):
            self.widget.schedule(result)

        return result
