"""Base control.

All controls should inherit from the below class.

"""

import asyncio
from enum import Enum
import inspect
import re
from typing import Callable

from bui.control.exceptions import StopControl
from bui.control.log import ControlLogger

# Private constants
_WINDOW = None

# Dictionary of existing controls
CONTROLS = {}
NOT_SET = object()

class MetaControl(type):

    """Control metaclass."""

    def __new__(cls, name, bases, dct):
        control = super().__new__(cls, name, bases, dct)
        if control.name:
            CONTROLS[control.name] = control

        # Create a logger just for this class
        control.logger = ControlLogger(control)

        return control


class Control(metaclass=MetaControl):

    """Base control, parent class of all controls."""

    name = ""
    window_control = True
    widget_control = True
    has_sub_controls = False
    pattern_for_window = ""
    name_for_widgets_without_options = "on_{control}_{wid}"
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
                method_name = cls.name_for_widgets_without_options.format(
                        control=cls.name, wid=widget.id)
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
        report = f"Bound {cls.name} as "
        if implicit:
            report += "an implicit "
        else:
            report += "a "

        wid = ""
        if kind is _ControlScope.WINDOW:
            report += "window control "
        elif kind is _ControlScope.WIDGET:
            report += f"widget control of {widget.widget}"
            wid = getattr(widget, "id", "")
            if wid:
                report += f"({wid}) "
        else:
            report += "unknown scope "

        if options is not None:
            report += f"with options={options} "

        report += f"to the {method!r} method"
        report = report.replace("{", "{{").replace("}", "}}")
        cls.logger.debug(" " * 4 + report.strip(), widget=wid)

    def process(self, options=None, callback=None):
        """Process the control, calls a generic `on_` method if found."""
        #if self.name == "select": breakpoint()
        wid = getattr(self.widget, "id", "")
        self._report_fire(options)

        # Call handle_{control} on the widget
        method = getattr(self.widget, f"handle_{self.name}", None)
        if method:
            method(self)

        # Call the `on_...` method on the window
        options = options or {}
        methods = self.widget.controls.get(self.name, [])
        res = NOT_SET
        for group, method in methods:
            if res is not NOT_SET:
                continue

            to_test = {}
            for key, value in options.items():
                if key in group.keys():
                    to_test[key] = value

            if group and group == to_test:
                self._report_call(method, child=True, wid=wid)
                res = self._call_method(method)
                break

        # At this point we consider no match was found in the options,
        # so we call the parent control if appropriate.
        options = {}
        methods = self.widget.controls.get(self.name, [])
        for group, method in methods:
            if res is not NOT_SET:
                continue

            if group == options:
                self._report_call(method, wid=wid)
                res = self._call_method(method, callback=callback)
                break

        # Call after_{control} on the widget
        method = getattr(self.widget, f"after_{self.name}", None)
        if method:
            method(self)

        return res

    def stop(self, reason=""):
        """
        Stop the control, interrupt the contorl method.

        This method raises an exception that will interrupt the parent
        control method.  You might specify an optional reason for this
        control to be stopped.  This reason will be reported if you
        run the application in debug-control mode.

        Args:
            reason (str, optional): the reason for this control to be stopped.

        Raises:
            StopControl

        """
        wid = getattr(self.widget, "id", "")
        self._report_stop(reason, wid=wid)
        raise StopControl()

    def _call_method(self, method, callback=None):
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
            task = self.widget.schedule(result)
            if callback:
                task.add_done_callback(callback)
        elif callback:
            callback(None)

        return result

    def _report_fire(self, options: dict = None):
        report = f"Fire {self.name} control on {self.widget.widget}"
        wid = getattr(self.widget, "id", None)
        if wid:
            report += f"({wid}) "
        else:
            report += " "
        if options:
            report += f"with options={options}"
        report = report.replace("{", "{{").replace("}", "}}")
        self.logger.debug("  " + report.strip(), widget=wid)

    def _report_call(self, method: Callable, child: bool = False, wid: str = ""):
        report = "Match "
        if child:
            report += "child "
        else:
            report += "main "

        report += f"control to {method.__name__}, call it"
        report = report.replace("{", "{{").replace("}", "}}")
        self.logger.debug(" " * 4 + report.strip(), widget=wid)

    def _report_stop(self, reason: str = "", wid: str = ""):
        if reason:
            report = f"Stopping: {reason}"
        else:
            report = f"Stopping"
        report = report.replace("{", "{{").replace("}", "}}")
        self.logger.debug(6 * " " + report, widget=wid)


class _ControlScope:

    """Enumeration to define the control scope."""

    WINDOW = 'window control'
    WIDGET = 'widget control'
