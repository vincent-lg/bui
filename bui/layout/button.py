"""Button object represented in layout."""

from bui.layout.attr import Attr
from bui.layout.component import Component

class Button(Component):

    """
    Create a clickable button on the interface.

    A button is a very common widget, needing to be defined inside
    of a [window](./window.md) tag.  The user can click on it and trigger
    a control method in response, except if the button is disabled.

    ```
    <window title="Test">
      <button x=1 y=3>My button</button>
      ...
    </window>
    ```

    > Notice that the button label is specified as the data for this
      tag.  This label cannot be empty.

    ## Attributes

    | Name         | Required | Description              | Example     |
    | ------------ | -------- | ------------------------ | ----------- |
    | `x`          | Yes      | The widget's horizontal  | `<button    |
    |              |          | position in columns (0   | x=5>`       |
    |              |          | is left). This position  |             |
    |              |          | is relative to the       |             |
    |              |          | window width.            |             |
    | `y`          | Yes      | The widget's vertical    | `<button    |
    |              |          | position in rows (0      | y=2>`       |
    |              |          | is at the top). This     |             |
    |              |          | position is relative to  |             |
    |              |          | the window height.       |             |
    | `width`      | No       | The widget width, that   | `<button    |
    |              |          | is, the number of        | width=2>`   |
    |              |          | columns it will use in   |             |
    |              |          | the window grid. A       |             |
    |              |          | widget with a width of   |             |
    |              |          | 2 will stretch one       |             |
    |              |          | additional column to the |             |
    |              |          | right. A widget with `x` |             |
    |              |          | set to 2 and `width` set |             |
    |              |          | to 3 will span `x=2`,    |             |
    |              |          | `x=3`, and `x=4`.  The   |             |
    |              |          | default is 1, so a       |             |
    |              |          | widget will remain in    |             |
    |              |          | its `x` column.          |             |
    | `height`     | No       | The widget height, that  | `<button    |
    |              |          | is, the number of        | height=2>`  |
    |              |          | rows it will use in      |             |
    |              |          | the window grid. A       |             |
    |              |          | widget with a height of  |             |
    |              |          | 2 will stretch one       |             |
    |              |          | additional row downward. |             |
    |              |          | A widget with `y` set    |             |
    |              |          | to 2 and `height` set    |             |
    |              |          | to 3 will span `y=2`,    |             |
    |              |          | `y=3`, and `y=4`.  The   |             |
    |              |          | default is 1, so a       |             |
    |              |          | widget will remain in    |             |
    |              |          | its `y` row.             |             |
    | `id`         | No       | The button identifier    | `<button    |
    |              |          | (ID). If not set, use    | id=quit>`   |
    |              |          | the button label.        |             |
    | `disabled`   | No       | If present, the button   | `<button    |
    |              |          | will be disabled by      | disabled>`  |
    |              |          | default.                 |             |
    | `set_true`   | No       | If inside of a dialog,   | `<button    |
    |              |          | set the dialog result to | set_true>`  |
    |              |          | `True` and close the     |             |
    |              |          | dialog. This field does  |             |
    |              |          | not require value, its   |             |
    |              |          | presence in the          |             |
    |              |          | `<dialog>` tag is        |             |
    |              |          | sufficient.              |             |
    | `set_false`  | No       | If inside of a dialog,   | `<button    |
    |              |          | set the dialog result to | set_false>` |
    |              |          | `False` and close the    |             |
    |              |          | dialog. This field does  |             |
    |              |          | not require value, its   |             |
    |              |          | presence in the          |             |
    |              |          | `<dialog>` tag is        |             |
    |              |          | sufficient.              |             |
    | `set`        | No       | If inside of a dialog,   | `<button    |
    |              |          | set the dialog result to | set=ok>`    |
    |              |          | the specified value and  |             |
    |              |          | close the dialog.        |             |

    The required attributes are `x`, and `y`.  It is recommended
    to also set an `id` although the shortened label (only lowercase
    letters will be used, spaces turned into the underscore) will be
    given if the `id` attribute is not set.

        <button x=2 y=5>Click on me!</button>

    (This will set a button with `id` of "click_on_me".)

    > The data is a translatable field.  If internationalization is
      set, it should contain the `ytranslate` path to the label and will
      be translated in the proper language as needed. Note that in this case,
      you absolutely need to set a proper ID, otherwise control methods
      won't be easy to bind to the button.

    ### Inside of dialogs

    If a button is defined inside of a [dialog](dialog.md) tag, it has three
    additional attributes that can be used: `set_true`, `set_false` and
    `set`.  All of them modify the dialog result and close the dialog
    when the button is pressed.

    It is very frequent to place `set_true` on a confirmation button
    (like "OK" or "Continue") and `set_false` on a cancellation button
    (like "Cancel" or "Close without modification").  It is then very
    simple to test the dialog result in the control method that popped
    the dialog (see [the page about custom dialogs](dialog.md)
    for more information).

    ## Data

    A button tag will be turned into a [Button](../widget/Button.md) object.
    You can access and modify its attributes in a control method.

    | Attribute      | Meaning and type | Example                     |
    | -------------- | ---------------- | --------------------------- |
    | `name`         | The name (str)   | `self.name = "Let's click"` |
    | `enabled`      | Whether the      | `if button.enabled:`        |
    |                | button is        |                             |
    |                | enabled (bool).  |                             |
    |                | This attribute   |                             |
    |                | cannot be set.   |                             |
    | `disabled`     | On or off (bool) | `print(self.disabled)`      |
    |                | Cannot be set.   |                             |

    These attributes can be accessed and set using the standard Python
    syntax for attributes.  Behind the scenes, these attributes are cached,
    handled by an extended `property()`, but you don't really need to
    worry about how it works.  Consider the following example:

        class Example(Window):

            def on_click_me(self, widget):
                \"\"\"The click me button has been clicked.\"\"\"
                widget.name = "Clicked on it"

    > Changing the name will not change the button ID.  Once set
      in layout, the ID won't change.

    A button also offers the following methods:

    | Name                     | Description                            |
    | ------------------------ | -------------------------------------- |
    | `enable()`               | Force the button to be enabled.        |
    | `disable`                | Force the button to be disabled.       |

    For instance:

        def on_init(self):
            '''The window initializes.'''
            restart = window["restart"]
            restart.disable()

    > Note: the `enabled` and `disabled` properties, along with the
      `enable()` and `disable()` methods, allow to change whether
      a button can be clicked by the user.  A disabled button (usually
      grayed out or marked unavailable) cannot be changed by the user.
      **However**, notice that some screen readers will skip over
      unavailable buttons and won't even signal them, so make sure
      no vital information is found in a disabled button.

    ## Controls

    | Control                           | Method       | Description    |
    | --------------------------------- | ------------ | -------------- |
    | [click](../../control/click.md)   | `on_click`   | The button is  |
    |                                 |              | being clicked on.|
    | [init](../../control/init.md)   | `on_init`    | The button is    |
    |                                 |              | ready to be      |
    |                                 |              | displayed, but   |
    |                                 |              | is not displayed |
    |                                 |              | just yet.        |
    | [press](../../control/press.md) | `on_press`   | The user presses |
    |                                 |              | on a key from her|
    |                                 |              | keyboard. This   |
    |                                 |              | control can have |
    |                                 |              | sub-controls.    |
    | [release](../../                | `on_release` | The user         |
    | control/release.md)             |              | relases a key on |
    |                                 |              | her keyboard.    |
    |                                 |              | This control can |
    |                                 |              | have sub-        |
    |                                 |              | controls.        |
    | [type](../../control/type.md)   | `on_type`    | The user types   |
    |                                 |              | a character      |
    |                                 |              | using her        |
    |                                 |              | keyboard. This   |
    |                                 |              | control can have |
    |                                 |              | sub-controls.    |

        class MainWindow(Window):

            def on_click_button(self):
                print(f"You clicked on the button of ID 'button'.")

    """

    tag_name = "button"
    attrs = (
        Attr("x", help="The widget horizontal position", type=int),
        Attr("y", help="The widget vertical position", type=int),
        Attr("width", help="The widget width", type=int, default=1),
        Attr("height", help="The widget height", type=int, default=1),
        Attr("id", help="The widget identifier", default=""),
        Attr("disabled", help="Disabled by default", default=False, if_present=True),
        Attr("set_true", help="Set the dialog to True and close it",
                default=False, if_present=True),
        Attr("set_false", help="Set the dialog to False and close it",
                default=False, if_present=True),
        Attr("set", help="Set the dialog to some value and close it",
                default="")
    )
    must_have_data = True

    def __init__(self, layout, parent, x, y, width=1, height=1,
            id="", disabled=False, set_true=False, set_false=False, set=""):
        super().__init__(layout, parent)
        self.x = x
        self.y = y
        self.name = ""
        self.width = width
        self.height = height
        self.id = id
        self.disabled = disabled
        self.set_true = set_true
        self.set_false = set_false
        self.set = set

    def complete(self):
        """Complete the widet, when all the layout has been set."""
        self.name = self.data
        if not self.id:
            self.id = self.deduce_id(self.name)

        if self.parent.tag_name != "dialog" and (self.set_true or self.set_false or self.set):
            raise ValueError("Can't yset set_true, set_false or set "
                    "attributes on a button that doesn't belong in a dialog")
