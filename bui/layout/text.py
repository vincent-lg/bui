"""Text object represented in layout."""

from bui.layout.attr import Attr
from bui.layout.component import Component

class Text(Component):

    r"""
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
    | `x`          | Yes      | The widget's horizontal  | `<text  |
    |              |          | position in columns (0   | x=5>`       |
    |              |          | is left). This position  |             |
    |              |          | is relative to the       |             |
    |              |          | window width.            |             |
    | `y`          | Yes      | The widget's vertical    | `<text  |
    |              |          | position in rows (0      | y=2>`       |
    |              |          | is at the top). This     |             |
    |              |          | position is relative to  |             |
    |              |          | the window height.       |             |
    | `width`      | No       | The widget width, that   | `<text      |
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
    | `height`     | No       | The widget height, that  | `<text      |
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
    | `id`         | No       | The text identifier      | `<text      |
    |              |          | (ID). If not set,        | id=name>`   |
    |              |          | the text label.          |             |
    | `value`      | No       | The default value of     | `<text      |
    |              |          | the text widget.         | value=Me>`  |
    | `multiline`  | No       | If present, set the text | `<text      |
    |              |          | on multiple lines.       | multiline>` |
    | `read-only`  | No       | If present, the text     | `<text      |
    |              |          | field will be read-only, | read-only>` |
    |              |          | forbiding the user to    |             |
    |              |          | edit it. The text value  |             |
    |              |          | will still be editable   |             |
    |              |          | through code. Due to     |             |
    |              |          | system constraints, this |             |
    |              |          | behavior cannot be       |             |
    |              |          | altered, once set, a     |             |
    |              |          | read-only text cannot be |             |
    |              |          | turned back into an      |             |
    |              |          | editable one. Also note  |             |
    |              |          | that screen readers will |             |
    |              |          | probably ignore a        |             |
    |              |          | read-only text field and |             |
    |              |          | forbid to focus one, so  |             |
    |              |          | make sure this field     |             |
    |              |          | doesn't contain vital    |             |
    |              |          | information.             |             |
    | `hidden`     | No       | If present, hide the     | `<text      |
    |              |          | text, creating a         | hidden>`    |
    |              |          | password field.          |             |

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
    | `label`        | The label (str)  | `self.label = "Last name:"` |
    | `value`        | The content of   | `print(self.value)`         |
    |                | this text (str)  |                             |
    | `enabled`      | On or off (bool) | `print(self.enabled)`       |
    |                | Cannot be set.   |                             |
    | `disabled`     | On or off (bool) | `print(self.disabled)`      |
    |                | Cannot be set.   |                             |
    | `cursor`       | Cursor object.   | `print(self.cursor.pos)`    |
    | `hidden`       | Is the text      | `print(self.hidden)`        |
    |                | field hidden?    |                             |
    |                | Cannot be set.   |                             |


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
    | `enable()`               | Force the text to be enabled.          |
    | `disable`                | Force the text to be disabled.         |

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
    | `at_begin`    | Yes or no (bool).    | `if cursor.at_begin:`     |
    |               | Is true if the       |                           |
    |               | cursor stands at     |                           |
    |               | the beginning of     |                           |
    |               | the text widget      |                           |
    |               | `pos == 0`).         |                           |
    | `at_end`      | Yes or no (bool).    | `if cursor.at_end:`       |
    |               | Is true if the       |                           |
    |               | cursor stands at     |                           |
    |               | the end of the       |                           |
    |               | text widget, that    |                           |
    |               | if typing new        |                           |
    |               | letters would        |                           |
    |               | append to the        |                           |
    |               | current text (`pos   |                           |
    |               | == len(text)`).      |                           |
    | `col`         | The current column   | `col = cursor.col`              |
    |               | number (int),        |                                 |
    |               | starting from 0.     |                                 |
    |               | With `lineno`, this  |                                 |
    |               | helps to represent   |                                 |
    |               | the cursor position  |                                 |
    |               | as a 2D position in  |                                 |
    |               | the text (number of  |                                 |
    |               | lines from the top,  |                                 |
    |               | number of columns    |                                 |
    |               | from the left). This |                                 |
    |               | attribute is read-   |                                 |
    |               | only (see the `move` |                                 |
    |               | method to move the   |                                 |
    |               | cursor).             |                                 |
    | `lineno`      | Current line number  | `lineno = cursor.lineno`  |
    |               | (int) starting from  |                           |
    |               | 0. This attribute is |                           |
    |               | read-only, see the   |                                 |
    |               | `move` method to     |                                 |
    |               | change the cursor    |                                 |
    |               | position.            |                                 |
    | `pos`         | Current cursor       | `text.value[:cursor.pos]` |
    |               | position (int).      |                           |
    |               | This position is     |                           |
    |               | the one of the       |                           |
    |               | character index      |                           |
    |               | that will be         |                           |
    |               | "pushed" when the    |                           |
    |               | user types, so       |                           |
    |               | that `pos` is 0 if   |                           |
    |               | the cursor is at     |                           |
    |               | the beginning of     |                           |
    |               | the wdget, and       |                           |
    |               | `len(text)` if the   |                           |
    |               | cursor is at the     |                           |
    |               | very end of the      |                           |
    |               | text widget. This    |                           |
    |               | attribute is read-   |                           |
    |               | only, see the `move` |                                 |
    |               | method to change the |                                 |
    |               | cursor position.     |                                 |
    | `text_after`  | Text from the        | `cursor.text_after`       |
    |               | cursor position to   |                           |
    |               | the end of the       |                           |
    |               | widget, including    |                           |
    |               | both limits (str).   |                           |
    |               | It is identical to   |                           |
    |               | `text[pos:]`.        |                           |
    |               | If the cursor is     |                           |
    |               | under the 'o' of     |                           |
    |               | 'coffee', then       |                           |
    |               | `cursor.text_after`  |                           |
    |               | will return          |                           |
    |               | 'offee'.             |                           |
    | `text_before` | The text between the | `cursor.text_before`      |
    |               | beginning of the     |                           |
    |               | widget and the       |                           |
    |               | current cursor       |                           |
    |               | position, not        |                           |
    |               | including the        |                           |
    |               | character under the  |                           |
    |               | cursor. This is      |                           |
    |               | identical to         |                           |
    |               | `text[:pos]`. If the |                           |
    |               | cursor is under the  |                           |
    |               | 'o' of 'coffee',     |                           |
    |               | 'cursor.text_before` |                           |
    |               | will return 'c'.     |                           |

    The cursor also has some methods:

    | Method  | Signature                | Description                |
    | ------- | ------------------------ | -------------------------- |
    | `move`  | `move(pos: int, col:     | Move the cursor. Either    |
    |         | Optionao[int] = None)`   | specify only one number    |
    |         |                          | as argument for an         |
    |         |                          | absolute movement (the     |
    |         |                          | given position is the      |
    |         |                          | index of the text in the   |
    |         |                          | widget), or two numbers    |
    |         |                          | (`lineno` and `col`) for a |
    |         |                          | vertical movement taking   |
    |         |                          | into account the number of |
    |         |                          | lines and columns.         |

    ## Controls

    | Control                         | Method       | Description      |
    | ------------------------------- | ------------ | ---------------- |
    | [change](../../                 | `on_change`  | The text has     |
    | control/change.md)              |              | been changed,    |
    |                                 |              | either by the    |
    |                                 |              | user or the      |
    |                                 |              | program.         |
    | [init](../../control/init.md)   | `on_init`    | The text is      |
    |                                 |              | ready to be      |
    |                                 |              | displayed, but   |
    |                                 |              | is not           |
    |                                 |              | displayed yet.   |
    | [press](../../control/press.md) | `on_press`   | The user         |
    |                                 |              | pressed on a     |
    |                                 |              | key of her       |
    |                                 |              | keyboard while   |
    |                                 |              | the text is      |
    |                                 |              | focused. This    |
    |                                 |              | control is       |
    |                                 |              | triggered        |
    |                                 |              | before the       |
    |                                 |              | text is          |
    |                                 |              | actually         |
    |                                 |              | modified, and    |
    |                                 |              | you can          |
    |                                 |              | prevent the      |
    |                                 |              | default change   |
    |                                 |              | to the text.     |
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

            def on_init_first_name(self, widget):
                widget.value = "Vincent"

    """

    tag_name = "text"
    attrs = (
        Attr("x", help="The widget horizontal position", type=int),
        Attr("y", help="The widget vertical position", type=int),
        Attr("width", help="The widget width", type=int, default=1),
        Attr("height", help="The widget height", type=int, default=1),
        Attr("id", help="The widget identifier", default=""),
        Attr("value", help="The text default value", default=""),
        Attr("multiline", help="The text is on multiple lines",
                default=False, if_present=True),
        Attr("read-only", help="The text is read-only",
                default=False, if_present=True),
        Attr("hidden", help="The text is hidden (as a passord)",
                default=False, if_present=True),
    )
    must_have_data = True

    def __init__(self, layout, parent, x, y, width=1, height=1, id="",
            value="", multiline=False, read_only=False, hidden=False):
        super().__init__(layout, parent)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = ""
        self.id = id
        self.value = value
        self.multiline = multiline
        self.read_only = read_only
        self.hidden = hidden

    def complete(self):
        """Complete the widget, when all the layout has been set."""
        self.label = self.data
        if not self.id:
            self.id = self.deduce_id(self.data)
