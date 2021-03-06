# Layout tag: radio

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
| `x` | Yes | The widget's horizontal position in columns (0 is left). This position is relative to the window width. | `<radio x=5>` |
| `y` | Yes | The widget's vertical position in rows (0 is at the top). This position is relative to the window height. | `<radio y=2>` |
| `id` | Yes | The radio button group identifier (ID). Contrary to most other tags, you need to set this attribute. | `<radio id=actions>` |
| `width` | No | The widget width, that is, the number of columns it will use in the window grid. A widget with a width of 2 will stretch one additional column to the right. A widget with `x` set to 2 and `width` set to 3 will span `x=2`, `x=3`, and `x=4`.  The default is 1, so a widget will remain in its `x` column. | `<radio width=2>` |
| `height` | No | The widget height, that is, the number of rows it will use in the window grid. A widget with a height of 2 will stretch one additional row downward. A widget with `y` set to 2 and `height` set to 3 will span `y=2`, `y=3`, and `y=4`.  The default is 1, so a widget will remain in its `y` row. | `<radio height=2>` |

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
| `choices` | The available choices (lsit) | `self.choices = (("ch1", "Choice 1"))` |
| `selected` | ID of the selected choice (str) or indice of the choice if no ID is set (int). | `self.selected = "ch1"` |

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
| [focus](../../control/focus.md) | `on_focus` | The radio button is focused or loses focus. |
| [init](../../control/init.md) | `on_init` | The radio is ready to be displayed, but is not displayed just yet. |
| [press](../../control/press.md) | `on_press` | The user presses on a key from her keyboard. This control can have sub-controls. |
| [release](../../control/release.md) | `on_release` | The user relases a key on her keyboard. This control can have sub-controls. |
| [select](../../control/select.md) | `on_select` | The selected choice has changed for this radio button. |
| [type](../../control/type.md) | `on_type` | The user types a character using her keyboard. This control can have sub-controls. |

    class MainWindow(Window):

        def on_select_actions(self, widget, selected):
            print(f"The user selected the action {selected}.")

