"""Change control, triggered when a widget changes."""

import re

from bui.control.base import Control

class Change(Control):

    """
    When a change happens to a widget.

    This control, with different meanings depending on widgets, is used to
    notify changes or values to some widgets.  For instance, a change
    control on a text widget will be triggered each time the text area
    changes content.  The change control, no matter what widget, is
    triggered **after** the change has taken place.  It is nos possible
    to cancel the change at this point.

    ## Usage

    This control can only be bound with a widget of one of the supported
    types.  This control doesn't support sub-controls.

    ### Window control

    This control cannot be set on a window.  A change control on the
    window itself wouldn't make that much sense or would be much too
    general.  Of course, if you wish to watch several widgets with the
    same method, you can still use the syntax for aliasing control
    methods which might be quite handy in this situation.

    ### Widget control

    To call a method when a text of ID "first_name" is changed, for
    instance, define a method like so:

        def on_change_first_name(self, ...):

    Depending on the type of widget you want to watch, different attributes
    will be available (check the [control attributes](#attributes) to have
    the full list, or check the widget type for more information).

    ### text

    A widget of type [text](../layout/tag/text.md) will trigger a
    "change" control whenever the text content of the widget is changed.
    This control will be triggered if the user changes the text content
    in an editable field, but also if the program changes the text content
    with `widget.value = ...` for instance.

    Triggered by a text widget, this control will have the additional
    following attribute:

    | Attribute       | Description                                     |
    | --------------- | ----------------------------------------------- |
    | `text`          | The new text value.                             |

    For instance, with a window defining a text of ID "name", you could
    write something like:

        def on_change_name(self, text):
            print(f"Text set by the user: {text!r}")

    ## Control attributes

    The control object has the following attributes:

    | Attribute | Type      | Note                                |
    | --------- | --------- | ----------------------------------- |
    | text      | str       | Only for text widgets.  The new     |
    |           |           | content of the widget.              |

    Alternatively you can specify the `control` keyword argument in your
    method signature which will always contain the control object.  You
    can also use the `widget` keyword argument that will contain your
    specific widget.

    """

    name = "change"
    widgets = {
            "text": "The text content was changed.",
    }
    window_control = False
    options = ("text", )

    def __init__(self, widget, text=""):
        super().__init__(widget)
        self.text = text
