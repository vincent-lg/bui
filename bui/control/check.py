"""Check control, triggered when a checkbox changes state."""

import re

from bui.control.base import Control

class Check(Control):

    """
    When the user checks or unchecks a checkbox.

    This control, specific to [checkboxes](../layout/tag/checkbox.md),
    is triggered when a user checks or unchecks a checkbox.  This control
    has optional sub-controls to bind methods to the action of checking
    or unchecking a checkbox.

    ## Usage

    This control can only be bound with a widget.  The control type for
    this control is "check", although "checked" and "unchecked" can be used
    as sub-controls (see below).

    ### Window control

    This control cannot be set on a window.  Checking or unchecking an
    entire window makes no sense, it should always be bound to a
    [checkbox](../layout/tag/checkbox.md).

    ### Widget control

    To call a method when a checkbox of ID "option" is checked or
    unchecked, you can create a method name with the control type "check"
    like so:

        def on_check_option(self, ...):

    This method will be called whenever the "option" checkbox changes
    state.  It is quite common to explicitly require the "checked" argument
    in the method:

        def on_check_option(self, checked):
            if checked:
                print(f"The option checkbox has been checked.")
            else:
                print(f"The option checkbox has been unchecked.")

    If you want to call a specific method when the "option" checkbox is
    checked, replace the "check" control type with "checked":

            def on_checked_option(self):
                print("The option checkbox was checked.")

    Replace with "unchecked" to watch for this checkbox being unchecked:

            def on_unchecked_option(self):
                print("The option checkbox was unchecked.")

    Using such a syntax allows to separate in two different methods the
    actions to be called when the checkbox is checked and unchecked.
    However, seeing as there are not so many possibilities, most developers
    prefer to create a `on_check_...` method and do a simple condition on
    the "checked" argument, like the second example in this section.

    ### Sub-controls and main controls

    Like the [press](./press.md) control, sub-controls takes precedence
    over main controls.  If you have a method named `on_checked_option`, it
    will be called whenver the "option" checkbox is checked.  However, if
    you also have a `on_check_option` method, it will only be called
    when the checkbox is unchecked, seeing as there is no specific method
    to handle that situation.  In other words, `on_checked_...` and
    `on_unchedked_...` always have precedence and `on_check_...` will
    only be called if searching for the more specific method fails.

    As a general rule, due to the slight different in naming that could
    create confusion and the fact that there are only two states to watch,
    it is advisable to use either a main control or sub-controls for each
    checkbox you have to watch.

    Here is a detail of what happens:

    1. The user clicks on a checkbox of ID "option".  This checkbox is
        unchecked.
    2. The control "check" is fired.
    3. It first searches for a method named `on_checked_option` on the
        window.  If found, it calls it and stops.  If not...
    4. It searches for a method named `on_check_option`.

    Similarly, when the checkbox is unchecked:

    1. The user clicks on a checkbox of ID "option".  This checkbox is
        checked.
    2. The control "check" is fired.
    3. It first searches for a method named `on_unchecked_option` on the
        window.  If found, it calls it and stops.  If not...
    4. It searches for a method named `on_check_option`.

    ## Control attributes

    The control object has the following attributes:

    | Attribute | Type      | Note                                |
    | --------- | --------- | ----------------------------------- |
    | checked   | bool      | Whether the checkbox has been       |
    |           |           | checked or not.                     |
    | state     | str       | Either 'checked' or 'unchecked'. In |
    |           |           | practice, using this state as       |
    |           |           | argument is not often necessary     |
    |           |           | (much better to use the `checked`   |
    |           |           | boolean instead).                   |

    Use these attributes as your control method argument.  For instance:

        def on_check(self, checked):
            if checked:
                print("The option checkbox was checked.")
            else:
                print("The option checkbox was unchecked.")

    Alternatively you can specify the `control` keyword argument in your
    method signature which will always contain the control object.  You
    can also use the `widget` keyword argument that will contain your
    specific widget.

    """

    name = "check"
    widgets = {
            "checkbox": "The checkbox was checked or unchecked.",
    }

    has_sub_controls = True
    pattern_for_window = None
    pattern_for_widgets = (
        fr"^on_(?P<state>checked|unchecked)_{{id}}$")
    options = ("state", "checked")

    def __init__(self, widget, state, checked):
        super().__init__(widget)
        self.state = state
        self.checked = checked
