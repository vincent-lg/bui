# Layout tag: text

Create a text area on the interface.

A text is a text area (or text input) on the [window](./window.md).
The user can write in it, except if the text is disabled, and controls
allow to react if the text is modified, selected, and more.

```
<window title="Test">
  <text x=1 y=3>Enter something here</text>
  ...
</window>
```

> Note: the text label (placed in the tag data) is mandatory.  It
  is required for any text area to have a label.  This requirement
  is a constraint placed on accessibility (no text area should be
  unlabelled, screen readers won't be able to report it correctly
  otherwise).  What you can do however is decide where this label
  will be situated in regard to the text area itself.  See the
  [tag attributes](#attributes) for details.

The text identifier (ID) is not mandatory.  However, if not set,
the text label will be used.

## Attributes

| Name         | Required | Description              | Example     |
| ------------ | -------- | ------------------------ | ----------- |
| `x` | Yes | The widget's horizontal position in columns (0 is left). This position is relative to the window width. | `<text x=5>` |
| `y` | Yes | The widget's vertical position in rows (0 is at the top). This position is relative to the window height. | `<text y=2>` |
| `id` | No | The text identifier (ID). If not set, the text label. | `<text id=name>` |
| `value` | No | The default value of the text widget. | `<text value=Me>` |
| `multiline` | No | If present, set the text on multiple lines. | `<text multiline>` |

The required attributes are `x`, and `y`.  It is recommended to also
set an `id` although the shortened label (only lowercase
letters will be used, spaces turned into the underscore) will be
given if the `id` attribute is not set.

    <text x=2 y=5>First namme:</text>

(This will set a text with `id` of "first_name".)

The text label can contain a translatable field.  In this case,
giving the text an ID is recommended.

## Data

A text tag will be turned into a [Text](../../widget/Text.md)
object.  You can access and modify its attributes in a control method.

| Attribute      | Meaning and type | Example                     |
| -------------- | ---------------- | --------------------------- |
| `label` | The label (str) | `self.label = "Last name:"` |
| `value` | The content of this text (str) | `print(self.value)` |
| `enabled` | On or off (bool) Cannot be set. | `print(self.enabled)` |
| `disabled` | On or off (bool) Cannot be set. | `print(self.disabled)` |
| `cursor` | Cursor object. | `print(self.cursor.pos)` |

> Use the `value` attribute to read or modify the text content:

    class Example(Window):

        layout = mark('''
          <window title="Introduce yourself">
            <text x=2 y=0 id="first_name">Enter your first name:</text>
            <button x=0 y=4 name="OK" />
            <button x=2 y=4 name="Cancel" />
          </window>
        ''')

        def on_ok(self):
            first_name = self["first_name"].value
            # 'first_name' will be a str with unix-style line breaks

> Note: `value` will get the content of the text area and make sure
  the line breaks inside this content are unix-liked (a simple `\n`,
  not `\r\n` or `\r`).

These attributes can be accessed and set using the standard Python
syntax for attributes.  Behind the scenes, these attributes are cached,
handled by an extended `property()`, but you don't really need to
worry about how it works.  Consider the following example:

    class Example(Window):

        def on_click_ok(self, widget):
            '''The OK button was clicked.'''
            widget = this["first_name"] # admitting first_name is a text
            widget.label = "First name:"
            widget.value = "Vincent"

> Changing the label will not change the text ID.  Once set
  in layout, the ID won't change.

A Text also offers the following methods:

| Name                     | Description                            |
| ------------------------ | -------------------------------------- |
| `enable()` | Force the text to be enabled. |
| `disable` | Force the text to be disabled. |

For instance:

    def on_init(self):
        '''The window initializes.'''
        text = window["first_name"]
        text.disable()

> Note: the `enabled` and `disabled` properties, along with the
  `enable()` and `disable()` method, allow to change whether
  a text can be set by the user.  A disabled text (usually
  grayed out or marked unavailable) cannot be changed by the user.
  **However**, some screen readers will skip over disabled text without
  even displaying it.  Make sure to not place vital content
  in a disabled text.

### Cursor object

The cursor object can be accessed through the `cursor` read-only
attribute of the widget.  A cursor object represents the point at
which the cursor (or insertion point) is located.  This object has
additional attributes of its own and some methods (see below
for examples).

| Attribute     | Name and type        | Example                   |
| ------------- | -------------------- | ------------------------- |
| `at_begin` | Yes or no (bool). Is true if the cursor stands at the beginning of the text widget `pos == 0`). | `if cursor.at_begin:` |
| `at_end` | Yes or no (bool). Is true if the cursor stands at the end of the text widget, that if typing new letters would append to the current text (`pos == len(text) - 1`). | `if cursor.at_end:` |
| `pos` | Current cursor position (int). This position is the one of the character indice that will be "pushed" when the user types, so that `pos` is 0 if the cursor is at the beginning of the wdget, and `len(text)` if the cursor is at the very end of the text widget. | `text.value[:cursor.pos]` |
| `text_after` | Text from the cursor position to the end of the widget, including both limits (str). It is identical to `text[pos:]`. If the cursor is under the 'o' of 'coffee', then `cursor.text_after` will return 'offee'. | `cursor.text_after` |
| `text_before` | The text between the beginning of the widget and the current cursor position, not including the character under the cursor. This is identical to `text[:pos]`. If the cursor is under the 'o' of 'coffee', 'cursor.text_before` will return 'c'. | `cursor.text_before` |

## Controls

| Control                           | Method       | Description    |
| --------------------------------- | ------------ | -------------- |
| [change](../../control/change.md) | `on_change` | The text has been changed, either by the user or the program. |
| [init](../../control/init.md) | `on_init` | The text is ready to be displayed, but is not displayed yet. |
| [press](../../control/press.md) | `on_press` | The user pressed on a key of her keyboard while the text is focused. This control is triggered before the text is actually modified, and you can prevent the default change to the text. |

    class MainWindow(Window):

        def on_init_first_name(self, widget):
            widget.value = "Vincent"

