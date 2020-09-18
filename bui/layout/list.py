"""List object represented in layout."""

from bui.layout.attr import Attr
from bui.layout.component import Component

class List(Component):

    """
    Create a list of choices.

    A list is a widget offering several choices, prompting the user to
    choose one or several by selecting them.  This widget is not so
    different from a [table](table.md), but it doesn't contain several
    columns.  Each choice can be identified, that is, you can check the
    selection through indices or string identifiers.

    ```
    <window title="List demonstration">
      <list id=actions x=2 y=4>
        <choice id=upgrade>Update this software</choice>
        <choice id=remove>Uninstall this software</choice>
      </list<
    </window>
    ```

    You will notice that this widget is also very close from a
    [radio button](radio.md) widget.  This is not a coincidence.  A list
    can host a lot more choices, however, and be more easily refreshed if
    choices have to change.  Contrary to a [radio button](radio.md), a list
    can be empty or contain only one choice.  You can use the
    [choice](choice.md) tag to set default choices in the list, or modify
    the choices with the widget `choices` property (see below for details).

    ## Attributes

    | Name         | Required | Description              | Example     |
    | ------------ | -------- | ------------------------ | ----------- |
    | `x`          | Yes      | The widget's horizontal  | `<list     |
    |              |          | position in columns (0   | x=5>`       |
    |              |          | is left). This position  |             |
    |              |          | is relative to the       |             |
    |              |          | window width.            |             |
    | `y`          | Yes      | The widget's vertical    | `<list     |
    |              |          | position in rows (0      | y=2>`       |
    |              |          | is at the top). This     |             |
    |              |          | position is relative to  |             |
    |              |          | the window height.       |             |
    | `id`         | No       | The list identifier      | `<list       |
    |              |          | (ID).                    | id=what>`   |
    | `width`      | No       | The widget width, that   | `<list      |
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
    | `height`     | No       | The widget height, that  | `<list      |
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

    See also the [choice](./choice.md) tag to define the default choices
    in a list.

    ## Data

    The [list widget](../../widget/List.md) can be manipulated to add and
    remove choices, and know what choice (or what chocies) is (are)
    currently selected.

    | Attribute      | Meaning and type | Example                     |
    | -------------- | ---------------- | --------------------------- |
    | `choices`      | The choice (list | `self.choices =             |
    |                | of tuple). The   | (("update", "Update the     |
    |                | first element is | software"))`                |
    |                | the choice       |                             |
    |                | identifier (int  |                             |
    |                | or str), the     |                             |
    |                | second is the    |                             |
    |                | choice label     |                             |
    |                | (str).           |                             |

    You can easily update the entire list this way.  Just set the
    `choices` property on the [list widget](../../widget/List.md) instance:

        def on_click_update(self):
            \"\"\"A button of ID 'update' was clicked.\"\"\"
            # There is a list of ID 'actions' in the window
            list = self["actions"]
            list.choices = (
                ("update", "Update the software without configuration change"),
                ("reset", "Update and reset the configuration"),
                ("remove", "Uninstall the software altogether"),
            )

            selected = list.selected
            # selected will be either 'update', 'reset' or 'remove' (str)
            if choice == "update":
                # ...

    The `choices` property can be a tuple of tuples (with each
    choice being a two-tuple data: the choice identifier (an ID to retrieve
    it quickly, must be hashable, probably a `str`) and the choice label
    (a `str`).  You can also use a single `str` to represent both,
    in which case, the choice ID will be its indice in the list.  Giving
    identifiers to each choice is not always necessary, so to follow the
    same example:

        def on_click_update(self):
            \"\"\"A button of ID 'update' was clicked.\"\"\"
            # There is a list of ID 'actions' in the window
            list = self["actions"]
            list.choices = (
                "Update the software without configuration change",
                "Update and reset the configuration",
                "Uninstall the software altogether",
            )

            selected = list.selected
            # selected will be either 0, 1 or 2 (int)
            if choice == 0: # update
                # ...

    Using this property will reset the entire list.  You can also use
    the `add_choice` and `remove_choice` methods.

    | Method            | Signature       | Description               |
    | ----------------- | --------------- | ------------------------- |
    | `add_choice`      | `add_choice(    | Add a choice at the end   |
    |                   | choice: Union[  | of the list. The choice   |
    |                   | Any, Tuple[     | to specify as argument    |
    |                   | Hashable, Any]]`| can be a single string.   |
    |                   |                 | If so, the choice         |
    |                   |                 | identifier will be the    |
    |                   |                 | position of the string in |
    |                   |                 | the choice (starting at   |
    |                   |                 | 0). The choice can also   |
    |                   |                 | be a tuple of two     |
    |                   |                 | elements: the choice  |
    |                   |                 | identifier and the    |
    |                   |                 | choice label. The     |
    |                   |                 | choice identifier     |
    |                   |                 | often is a string too |
    |                   |                 | and the same goes for |
    |                   |                 | the label, although   |
    |                   |                 | you have freedom to   |
    |                   |                 | use other types, as   |
    |                   |                 | long as the           |
    |                   |                 | identifier is         |
    |                   |                 | hashable.             |

    ## Controls

    | Control                         | Method       | Description      |
    | ------------------------------- | ------------ | ---------------- |
    | [focus](../../control/focus.md) | `on_focus`   | The list is      |
    |                                 |              | focused or lose  |
    |                                 |              | focus.           |
    | [init](../../control/init.md)   | `on_init`    | The list is      |
    |                                 |              | ready to be      |
    |                                 |              | displayed, but   |
    |                                 |              | is not           |
    |                                 |              | displayed yet.   |
    | [press](../../control/press.md) | `on_press`   | The user         |
    |                                 |              | pressed on a     |
    |                                 |              | key of her       |
    |                                 |              | keyboard while   |
    |                                 |              | the list is      |
    |                                 |              | focused. This    |
    |                                 |              | control is       |
    |                                 |              | triggered        |
    |                                 |              | before the       |
    |                                 |              | key has had      |
    |                                 |              | any impact, so   |
    |                                 |              | you can cancel   |
    |                                 |              | the action at    |
    |                                 |              | this point.      |
    | [release](../../                | `on_release` | The user         |
    | control/release.md)             |              | relases a key on |
    |                                 |              | her keyboard.    |
    |                                 |              | This control can |
    |                                 |              | have sub-        |
    |                                 |              | controls.        |
    | [select](../../                 | `on_select`  | The list         |
    | control/select.md)              |              | selection has    |
    |                                 |              | changed.         |
    | [type](../../control/type.md)   | `on_type`    | The user types   |
    |                                 |              | a character      |
    |                                 |              | using her        |
    |                                 |              | keyboard. This   |
    |                                 |              | control can have |
    |                                 |              | sub-controls.    |

        class MainWindow(Window):

            def on_select_actions(self, widget, choice):
                print(f"The user selected the choice of ID {choice}.")

    """

    tag_name = "list"
    attrs = (
        Attr("x", help="The widget horizontal position", type=int),
        Attr("y", help="The widget vertical position", type=int),
        Attr("id", help="The widget identifier"),
        Attr("width", help="The widget width", type=int, default=1),
        Attr("height", help="The widget height", type=int, default=1),
        Attr("name", help="The name of the list", default=""),
        Attr("multisel",
                help="The list can contain multiple selected choices",
                default=False, if_present=True),
    )

    def __init__(self, layout, parent, x, y, id, width=1, height=1, name="",
            multisel=False):
        super().__init__(layout, parent)
        self.x = x
        self.y = y
        self.id = id
        self.width = width
        self.height = height
        self.name = name
        self.multisel = multisel
