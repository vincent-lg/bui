"""Helpers for testing BUI control."""

def is_registered(widget, control, method):
    """
    Test if the specified method is registered in the widget as a control.

    Args:
        widget (Widget): the widget subscribed to the control.
        control (str): the control name.
        method (instance method): the control method.

    Returns:
        registered (bool): whether the control method is registered in
        the widget for this control.

    """
    return any(t_method == method for _, t_method in widget.controls[control])
