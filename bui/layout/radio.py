"""Radio button object represented in layout."""

from bui.layout.attr import Attr
from bui.layout.component import Component

class RadioButton(Component):

    """
    Create a radio button with multiple choices.

    A radio button is represented by multiple, mutually-exclusive buttons.
    Each button in the group can't be selected without the other ones
    in the same group being de-selected.

    ```
    <window title="Table demonstration">
      <radio id=choices x=2 y=4>
        <choice>Choice 1</choice>
        <choice>Choice 2</choice>
        <choice>Choice 3</choice>
      </radio>
    </window>
    ```

    Using the `<radio>` landmark creates an empty radio button group.
    A radio button must have at least two choices (if less, consider using
    a [checkbox](checkbox.md)).  You can use the `<choice>` tag inside
    of the `<radio>` to create a selectable choice in the group, or use the
    method `add_choice` of a [RadioButton](../../widget/radio_button.py)
    widget to add the button programmatically.

    ## Attributes

    | Name         | Required | Description              | Example     |
    | ------------ | -------- | ------------------------ | ----------- |
    | `x`          | Yes      | The widget's horizontal  | `<radio     |
    |              |          | position in columns (0   | x=5>`       |
    |              |          | is left). This position  |             |
    |              |          | is relative to the       |             |
    |              |          | window width.            |             |
    | `y`          | Yes      | The widget's vertical    | `<radio     |
    |              |          | position in rows (0      | y=2>`       |
    |              |          | is at the top). This     |             |
    |              |          | position is relative to  |             |
    |              |          | the window height.       |             |
    | `id`         | Yes      | The radio button group   | `<radio     |
    |              |          | identifier (ID). Contrary| id=actions>`|
    |              |          | to most other tags, you  |             |
    |              |          | need to set this         |             |
    |              |          | attribute.               |             |
    | `width`      | No       | The widget width, that   | `<radio     |
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
    | `height`     | No       | The widget height, that  | `<radio     |
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

    See also the [choice](./choice.md) tag to define the choices
    in a radio button group.

    > Note: the radio button identifier is mandatory.  You cannot dcreate a
      radio button without a valid identifier.  The reason for this constraint
      is due to the fact that this widget, in particular, will be edited
      in your application.  Lacking an identifier, you won't be able to do
      that.

    ## Data

    The [radio button widget](../../widget/radio_button.md) can be manipulated
    to add and remove choices, and know the selected choice.

    | Attribute      | Meaning and type | Example                     |
    | -------------- | ---------------- | --------------------------- |
    | `choices`      | The available    | `self.choices = (("ch1",    |
    |                | choices (lsit)   | "Choice 1"))`               |
    | `selected`     | ID of the        | `self.selected = "ch1"`     |
    |                | selected choice  |                             |
    |                | (str) or indice  |                             |
    |                | of the choice if |                             |
    |                | no ID is set     |                             |
    |                | (int).           |                             |

    You can easily update the entire radio button this way.  Just set the
    `choices` property on the
    [radio button widget](../../widget/RadioButton.md) instance, specifying
    a list of choices where each choice is a tuple of two values: ID
    (as a `str`) and label to be displayed (as a `str`).  Th ID will be
    returned when this choice is selected:

        def on_click_update(self):
            # A button of ID 'update' was clicked
            # There is a radio button of ID 'actions' in the window
            actions = self["actions"]
            actions.choices = (
                ("update", "Update the software"),
                ("repair", "Repair the software"),
                ("reinstall", "Remove the software configuration and install it again"),
                ("remove", "Uninstall this software"),
            )

            action = actions.selected
            # action will be either "update", "repair", "reinstall" or "remove"

            # You can of course change the selected choice
            actions.selected = "reinstall"

    ## Controls

    | Control                         | Method       | Description      |
    | ------------------------------- | ------------ | ---------------- |
    | [focus](../../control/focus.md) | `on_focus`   | The radio        |
    |                                 |              | button is        |
    |                                 |              | focused or       |
    |                                 |              | loses focus.     |
    | [init](../../control/init.md)   | `on_init`    | The radio is     |
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
    | [select](../../                 | `on_select`  | The selected     |
    | control/select.md)              |              | choice has       |
    |                                 |              | changed for      |
    |                                 |              | this radio       |
    |                                 |              | button.          |
    | [type](../../control/type.md)   | `on_type`    | The user types   |
    |                                 |              | a character      |
    |                                 |              | using her        |
    |                                 |              | keyboard. This   |
    |                                 |              | control can have |
    |                                 |              | sub-controls.    |

        class MainWindow(Window):

            def on_select_actions(self, widget, selected):
                print(f"The user selected the action {selected}.")

    """

    tag_name = "radio"
    attrs = (
        Attr("x", help="The widget horizontal position", type=int),
        Attr("y", help="The widget vertical position", type=int),
        Attr("id", help="The widget identifier"),
        Attr("width", help="The widget width", type=int, default=1),
        Attr("height", help="The widget height", type=int, default=1),
    )

    def __init__(self, layout, parent, x, y, id, width=1, height=1):
        super().__init__(layout, parent)
        self.x = x
        self.y = y
        self.id = id
        self.width = width
        self.height = height
