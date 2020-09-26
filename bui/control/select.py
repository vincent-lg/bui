"""Select control, triggered when the selection changes for a widget."""

from bui.control.base import Control

class Select(Control):

    """
    When the selection changes for a widget.

    This control can have many differemnt meanings depending on the
    widget it affects.  On the [table](../layout/tag/table.md) and
    [list](../layout/tag/list.md) widget, it is triggered when
    the selection of one or more choices change, whether the user
    made that change or not.  On the [text](../layout/tag/text.md)
    widget, this control is triggered when the selected text changes,
    whether the user made that change or not.

    ## Usage

    This control can only be bound with a widget.  The control type for
    this control is "select".

    ### Window control

    This control cannot be set on a window.  Selecting or unselecting an
    entire window makes no sense, it should always be bound to a
    widget.

    ### Widget control

    If, for instance, a [list](../layout/tag/list.md) widget of ID "students" is present in the window, to trigger a method when the selection in this list changes would require to create a method named `on_select_students`.

        def on_select_students(self, ...):

    This method will be called whenever the "students" list changes
    in selection.  It is quite common to explicitly require the
    "selected" argument in the method:

        def on_select_students(self, selected):
            print(f"The new selection is: {selected}")

    ## Control attributes

    The control object has the following attributes:

    | Attribute | Type      | Note                                |
    | --------- | --------- | ----------------------------------- |
    | selected  | selection | What has been selected?  The object |
    |           |           | type will vary depending on the     |
    |           |           | widget to which this control is     |
    |           |           | bound.  In list and table widgets,  |
    |           |           | `selected` will contain a `Choice`  |
    |           |           | or `Row` object if the list or      |
    |           |           | table allows only one selection.    |
    |           |           | If the `multisel` attribute has     |
    |           |           | been set, however, `selected` will  |
    |           |           | contain a tuple of `Choice` or      |
    |           |           | `Row` objects.  For the text        |
    |           |           | widget, `selected` will contain the |
    |           |           | selected text, as a `str`.          |

    Use these attributes as your control method argument.  For instance:

        def on_seleect_answer(self, selected):

    Since the control can be interrupted, you shouldn't try to access
    the current selection with `widget.selected` for instance.  This will
    most likely return the "previous" selection, since the change
    in selection hasn't been applied in BUI yet and can be cancelled.
    Thus, you should always ask for the selection, using the
    `selected` keyword argument in your control methods.

    Alternatively you can specify the `control` keyword argument in your
    method signature which will always contain the control object.  You
    can also use the `widget` keyword argument that will contain your
    specific widget.

    ## Control interruption

    This control can be interrupted.  In this case, the selection will
    be cancelled and the list, table or text will keep the
    previous selection.  This can be useful to avoid selection
    of content that shouldn't be selected.  Keep in mind, however,
    that preventing selection might not be a good way to indicate
    an invalid operation to your users.

    To interrupt a control, call the `control.stop` method.  You'll
    need to add the `control` argument in your control method:

        def on_select_students(self, selected, control):
            if selected. == "John": # Never select John, for some reason
                control.stop()

    """

    name = "select"
    options = ("selected", )

    def __init__(self, widget, selected):
        super().__init__(widget)
        self.selected = selected
