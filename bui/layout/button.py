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
    | `id`         | No       | The button identifier    | `<button    |
    |              |          | (ID). If not set, use    | id=quit>`   |
    |              |          | the button label.        |             |

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

    ## Data

    A button tag will be turned into a [Button](../class/Button.md) object.
    You can access and modify its attributes in a control method.

    | Attribute      | Meaning and type | Example                     |
    | -------------- | ---------------- | --------------------------- |
    | `name`         | The name (str)   | `self.name = "Let's click"` |

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

    ## Controls

    | Control                           | Method       | Description    |
    | --------------------------------- | ------------ | -------------- |
    | [click](../../control/click.md)   | `on_click`   | The button is    |
    |                                 |              | being clicked on.  |

        class MainWindow(Window):

            def on_click_button(self):
                print(f"You clicked on the button of ID 'button'.")

    """

    tag_name = "button"
    attrs = (
        Attr("x", help="The widget horizontal position", type=int),
        Attr("y", help="The widget vertical position", type=int),
        Attr("id", help="The widget identifier", default=""),
        Attr("set_true", help="Set the dialog to True and close it",
                default=False, if_present=True),
        Attr("set_false", help="Set the dialog to False and close it",
                default=False, if_present=True),
        Attr("set", help="Set the dialog to some value and close it",
                default="")
    )
    must_have_data = True

    def __init__(self, layout, parent, x, y, id="", set_true=False,
            set_false=False, set=""):
        super().__init__(layout, parent)
        self.x = x
        self.y = y
        self.name = ""
        self.id = id
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
