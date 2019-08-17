"""Base control.

All controls should inherit from the below class.

"""

import asyncio
from enum import Enum
import inspect
import re
from typing import Callable

# Private constants
_WINDOW = None

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
        global _WINDOW
        # Import the window if necessary
        if _WINDOW is None:
            from bui.widget.window import Window as _WINDOW

        if cls.has_sub_controls:
            # This control has sub-controls
            # sub-controls can all be linked to control methods
            if cls.window_control and widget is window:
                method_name = f"on_{cls.name}"
                bound = cls._register_method(widget, window, method_name)
                if bound:
                    cls._report_bound(_ControlScope.WINDOW, window,
                            method_name)

                if cls.pattern_for_window:
                    pattern = re.compile(cls.pattern_for_window)
                    contents = dir(window)
                    for content in contents:
                        match = pattern.search(content)
                        if match:
                            group = match.groupdict()
                            bound = cls._register_method(widget, window,
                                    content, group=group)
                            if bound:
                                cls._report_bound(_ControlScope.WINDOW,
                                        window, content, options=group)
            elif cls.widget_control:
                method_name = f"on_{cls.name}_{widget.id}"
                bound = cls._register_method(widget, window, method_name)
                if bound:
                    cls._report_bound(_ControlScope.WIDGET, widget,
                            method_name)

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
                            if bound:
                                cls._report_bound(_ControlScope.WIDGET,
                                        widget, content, options=group)

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
                if bound:
                    if cls.window_control and widget is window:
                        cls._report_bound(_ControlScope.WINDOW, window,
                                method_name, implicit=True)
                    else:
                        cls._report_bound(_ControlScope.WIDGET, widget,
                                method_name, implicit=True)

        if not bound:
            if cls.window_control and widget == window:
                method_name = f"on_{cls.name}"
                if cls._register_method(widget, window, method_name):
                    cls._report_bound(_ControlScope.WINDOW, window,
                            method_name)
                    return

            if cls.widget_control and hasattr(widget, "id"):
                method_name = f"on_{cls.name}_{widget.id}"
                if cls._register_method(widget, window, method_name):
                    cls._report_bound(_ControlScope.WIDGET, widget,
                            method_name)

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

    @classmethod
    def _report_bound(cls, kind: '_ControlScope', widget: 'Widget', method: str,
            options: dict = None, implicit: bool = False):
        if _WINDOW._debug_controls:
            report = f"Bound {cls.name} as "
            if implicit:
                report += "an implicit "
            else:
                report += "a "

            if kind is _ControlScope.WINDOW:
                report += "window control "
            elif kind is _ControlScope.WIDGET:
                report += f"widget control of {widget.widget}"
                wid = getattr(widget, "id", None)
                if wid:
                    report += f"({wid}) "
            else:
                report += "unknown scope "

            if options is not None:
                report += f"with options={options} "

            report += f"to the {method!r} method"
            print(" " * 4 + report.strip())

    def process(self, options=None):
        """Process the control, calls a generic `on_` method if found."""
        self._report_fire(options)

        # Call on_{control} on the widget
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
                self._report_call(method, child=True)
                return self._call_method(method)

        # At this point we consider no match was found in the options,
        # so we call the parent control if appropriate.
        options = {}
        methods = self.widget.controls.get(self.name, [])
        for group, method in methods:
            if group == options:
                self._report_call(method)
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

    def _report_fire(self, options: dict = None):
        if _WINDOW._debug_controls:
            report = f"Fire {self.name} control on {self.widget.widget}"
            wid = getattr(self.widget, "id", None)
            if wid:
                report += f"({wid}) "
            else:
                report += " "
            if options:
                report += f"with options={options}"
            print("  " + report.strip())

    def _report_call(self, method: Callable, child: bool = False):
        if _WINDOW._debug_controls:
            report = "Match "
            if child:
                report += "child "
            else:
                report += "main "

            report += f"control to {method.__name__}, call it"
            print(" " * 4 + report.strip())


class _ControlScope:

    """Enumeration to define the control scope."""

    WINDOW = 'window control'
    WIDGET = 'widget control'
