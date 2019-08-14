# Layout tag: checkbox

Create a checkbox on the interface.

A checkbox is a widget on a [window](./window.md).  It can be either
checked or unchecked.  Checking it can be done through the mouse or the
keyboard.  The checkbox can also be disabled, toggling it won't be
possible.  A [check](../../control/check.md) control will be triggered
when the checkbox changes state.

```
<window title="Test">
  <checkbox x=1 y=3>Toggle me</checkbox>
  ...
</window>
```

> Note: the checkbox name (its label) is specified as data of this tag.
  If not specified, the checkbox ID will be deduced from this data.

## Attributes

| Name         | Required | Description              | Example     |
| ------------ | -------- | ------------------------ | ----------- |
| `x` | Yes | The widget's horizontal position in columns (0 is left). This position is relative to the window width. | `<checkbox x=5>` |
| `y` | Yes | The widget's vertical position in rows (0 is at the top). This position is relative to the window height. | `<checkbox y=2>` |
| `width` | No | The widget width, that is, the number of columns it will use in the window grid. A widget with a width of 2 will stretch one additional column to the right. A widget with `x` set to 2 and `width` set to 3 will span `x=2`, `x=3`, and `x=4`.  The default is 1, so a widget will remain in its `x` column. | `<checkbox width=2>` |
| `height` | No | The widget height, that is, the number of rows it will use in the window grid. A widget with a height of 2 will stretch one additional row downward. A widget with `y` set to 2 and `height` set to 3 will span `y=2`, `y=3`, and `y=4`.  The default is 1, so a widget will remain in its `y` row. | `<checkbox height=2>` |
| `id` | No | The checkbox identifier (ID). If not set, use the checkbox name. | `<checkbox id=on>` |
| `checked` | No | Whether the checkbox is checked when the window first appears (not set by default). This attribute doesn't require a value, its presence is enough. | `<checkbox checked>` |

The required attributes are `x`, and `y`.  It is recommended to also
set an `id` although the shortened name (only lowercase
letters will be used, spaces turned into the underscore) will be
given if the `id` attribute is not set.

    <checkbox x=2 y=5>Toggle me!</checkbox>

(This will set a checkbox with `id` of "toggle_me".)

The checkbox name can contain a translatable field.  In this case,
giving the checkbox an ID is recommended.

By default, a checkbox will be unchecked when it appears on the window.
To create a checkbox that is checked by default, specify the attribute
`checked` with no value:

    <checkbox x=2 y=0 checked>On by default</checkbox>

You can also use the init control to programatically determine whether
the checkbox should be checked (in harmony to user options, for instance).

## Data

A checkbox tag will be turned into a [Checkbox](../../widget/Checkbox.md)
object.  You can access and modify its attributes in a control method.

| Attribute      | Meaning and type | Example                     |
| -------------- | ---------------- | --------------------------- |
| `name` | The name (str) | `self.name = "Other name"` |
| `checked` | On or off (bool) | `self.checked = False` |
| `enabled` | On or off (bool) Cannot be set. | `print(self.enabled)` |
| `disabled` | On or off (bool) Cannot be set. | `print(self.disabled)` |

> You can use a simple condition to test if the checkbox is checked:

    class Example(Window):

        layout = mark('''
          <window title="Are you sure?">
            <checkbox x=2 y=0 id="confirm">Do you really want to continue?</checkbox>
            <button x=0 y=4 name="OK" />
            <button x=2 y=4 name="Cancel" />
          </window>
        ''')

        def on_ok(self):
            if window["confirm"]: # equivalent to if window["confirm"].checked
                ...

These attributes can be accessed and set using the standard Python
syntax for attributes.  Behind the scenes, these attributes are cached,
handled by an extended `property()`, but you don't really need to
worry about how it works.  Consider the following example:

    class Example(Window):

        def on_check_option(self, widget, checked):
            '''The option checkbox has been checked or unchecked.'''                widget.name = f"checkbox {'checked' if checked else 'not checked'}"

> Changing the name will not change the checkbox ID.  Once set
  in layout, the ID won't change.

A Checkbox also offers the following methods:

| Name                     | Description                            |
| ------------------------ | -------------------------------------- |
| `check()` | Force the checkbox to be checked. |
| `uncheck()` | Force the checkbox to be unchecked. |
| `enable()` | Force the checkbox to be enabled. |
| `disable` | Force the checkbox to be disabled. |

For instance:

    def on_init(self):
        '''The window initializes.'''
        option = window["option"]
        option.check()

> Note: the `enabled` and `disabled` properties, along with the
  `enable()` and `disable()` methods, allow to change whether
  a checkbox can be set by the user.  A disabled checkbox (usually
  grayed out or marked unavailable) cannot be changed by the user.
  **However**, notice that some screen readers will skip over
  unavailable checkboxes and won't even signal them, so make sure
  no vital information is found in a disabled checkbox.

## Controls

| Control                           | Method       | Description    |
| --------------------------------- | ------------ | -------------- |
| [check](../../control/check.md) | `on_check` | The checkbox is checked or unchecked. |
| [init](../../control/init.md) | `on_init` | The checkbox is ready to be displayed, but is not displayed yet. |

    class MainWindow(Window):

        def on_checkk_checkbox(self, checked):
            print(f"You clicked on the checkbox of ID 'checkbox'.  Cecked? {checked}")

