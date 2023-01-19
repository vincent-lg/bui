"""Dialog object represented in layout."""

from bui.layout.attr import Attr
from bui.layout.component import Component

class Dialog(Component):

    """
    Custom dialog tag, to encompass widgets.

    The dialog tag allows to create a custom dialog box.  Contrary to the
    window tag, it doesn't describe a window and its elements.  Usually, a
    dialog is created in a control method (in response to user action).
    For instance, if a user presses on a button of a window, a dialog might
    appear to ask for additional information.

    Notice that this tag is reserved for custom dialogs.  BUI offers you
    other ways to create default dialogs.

    ```
    <dialog title="Give me more info here">
      ...
    </dialog>
    ```

    ## Usage

    There are two main usages of a dialog layout.  Both use a dialog
    tag and can be spawned from a window control method.

    ### Bare layout

    The first approach is to call the `pop_dialog` method of the `Window`
    class, giving it a string representation of the custom dialog layout.
    This allows for very quick processing.  Here is an example that
    creates a basic dialog box with a text input and two buttons: the
    window control method that spawns this dialog also has to handle the
    user input.

    ```
    class Example(Window):

        \"\"\"Example window.\"\"\"

        async def on_profile(self):
            \"\"\"The user clicked on the 'profile' button.\"\"\"
            dialog = await self.pop_dialog(\"\"\"
                <dialog title="Enter your name">
                  <text x=2 y=3 id=name>Enter your name here:</text>
                  <button x=1 y=5 set_true>OK</button>
                  <button x=4 y=5 set_false>Cancel</button>
                </dialog>
            \"\"\")

            # The call to the pop_dialog method will block until the user
            # has clicked on 'ok' or 'cancel'
            if dialog: # The user has pressed on OK
                name = dialog["name"].value
                print(f"The user entered the name: {name!r}")
            else: # The user has clicked on cancel
                print("The user cancelled the operation, do nothing.")
    ```

    The created dialog is contained inside a string representation.  This
    string representation holds the dialog layout.  The root tag is not
    [window](window.md) but `<dialog>`.  Inside of it is a normal window
    definition.  We create a dialog with a title.  Inside of it are
    three widgets: a text area and two buttons.

    The 'OK' button has the attribute `set_true` and the 'cancel' button
    has the attribute `set_false`.  This is a common shortcut that you will
    see in dialogs: a button spawned inside a dialog, if it has a set value,
    will close the dialog when pressed and set the value as a result of
    the dialog.  So when the 'OK' button is clicked, the button sets
    the dialog result to `True` and close the dialog.  That's why, in
    the control method that created the dialog, you can do something like:

        if dialog: # 'ok' has been clicked

    The `set_true` and `set_false`, along with the `set` attributes,
    cannot be used except on a button inside of a dialog.

    The `dialog` variable in the previous control method holds the
    dialog result (that is, a set value and the list of the widgets in
    the dialog), so you can get what the user entered in the 'name'
    field in a very straightforward way.

    ### Dialog class

    BUI also lets you the option to define a dialog class.  This is
    a good solution if you want to use the same dialog in different
    places of your program.  You have to set a
    [Dialog](../../widget/dialog.md) class in your program:

    ```python
    import hashlib

    from bui import Dialog

    class Hashes(Dialog):

        \"\"\"Dialog to show the list of supported hashes in Python and let the user choose one.\"\"\"

        # Note that you can (and maybe should) write the layout in a
        # separate .bui file.
        layout = mark(\"\"\"
            <dialog title="Available hashes">
              <table x=1 y=2 id=hashes>
                <col>Algorithm</col>
                <col>Digest size</col>
                <col>Guaranteed</col>
              </table>
              <button x=1 y=5 set_true>OK</button>
              <button x=4 y=5 set_false>Cancel</button>
            </dialog>
        \"\"\")

        def on_init(self):
            \"\"\"The dialog will be popped up just after.\"\"\"
            table = self["hashes"]
            for name in sorted(hashlib.algorithms_available):
                guaranteed = name in hashlib.algorithms_guaranteed
                algorithm = getattr(hashlib, name)()
                table.add_row(name, algorithm.digest_size,
                        'yes' if guaranteed else 'no')
    ```

    You can then use the window's `pop_dialog` method, giving it
    not the string layout, but the dialog class instead:

    ```python
    class Example(Window):

        async def on_hash(self):
            \"\"\"The user pressed on the 'hash' button.\"\"\"
            dialog = await self.pop_dialog(Hashes)
            # Block until 'ok' or 'cancel' has been pressed
            if dialog:
                hash_name = dialog["hashes"].selected.name
    ```

    The advantage of this method is that you don't have to redefine the
    layout and some control methods in the dialog itself.  This is useful
    if you want to pop the same dialog in different places of your program.
    Also note that you can set control methods in your dialog class (like
    `on_init` in the previous example).

    ## Attributes

    | Name         | Required | Description              | Example     |
    | ------------ | -------- | ------------------------ | ----------- |
    | `title`      | Yes      | The dialog title.  This  | `<dialog    |
    |              |          | attribute is mandatory.  | title="Tell |
    |              |          |                          | me more">`  |
    | `rows`       | No       | The number of rows in    | `<dialog    |
    |              |          | the dialog grid.         | rows=10>`   |
    |              |          | Default is `6`.          |             |
    | `cols`       | No       | The number of columns    | `<dialog    |
    |              |          | in the dialog grid.      | cols=5>`    |
    |              |          | Default is `6`.          |             |

    You cannot set a window or dialog without a proper title.  Doing so
    would impair accessibility for screen readers.  If these tools can
    read anything at all on your window, it's the title bar, so be sure
    it's not empty.

    > `title` is a translatable attribute.  If internationalization is
      set, it should contain the `ytranslate` path to the title and will
      be translated in the proper language as needed.

    The `rows` and `cols` attributes are used to set the dialog grid.  You
    can think of them as the height (in rows) and width (in columns) of the
    grid.  Changing this value won't make the window any bigger, but
    it will give you more control on how to place the widget in the window
    itself.  On the other hand, having a large grid can make designing not
    so easy.  It all depends on your needs.

    > Note: you don't have to set the same number of rows and columns.
      This is just the default value.  You can set different values with no
      trap:

    ```
    <dialog cols=1 rows=8>
    ```

    This will set a dialog with only one column, but 8 rows.  If you place
    a widget in `x=0 y=0`, it will take all the window's width.  Again,
    this doesn't change the window size in any way, just the way widgets
    are placed on it.  You can picture the window to always be a
    square but sliced in different portions (squares or rectangles, more
    or less big depending on the height and width you set in the window
    tag).

    ## Data

    A dialog is a specific graphical element since it only contains other
    elements and has no meaning by itself.  Therefore, you cannot send
    it data, it wouldn't make much sense.  Instead, you should
    send data to the dialog's graphical elements themselves.

    However, some dialog attributes can be changed on the fly.

    | Attribute      | Meaning and type | Example                     |
    | -------------- | ---------------- | --------------------------- |
    | `title`        | The title (str)  | `self.title = "New title"`  |

    These attributes can be accessed and set using the standard Python
    syntax for attributes.  Behind the scenes, these attributes are cached,
    handled by an extended `property()`, but you don't really need to
    worry about how it works.  Suffice it to say that:

        class Example(Dialog):

            def on_press_a(self):
                self.title = "You pressed A."

    ... will update the dialog title when the user presses the 'a' key
    on her keyboard.

    ## Controls

    The dialog tag is tied to the [Dialog](../../widget/Dialog.md)
    class.  Therefore, when you write controls on this class, you often
    want to catch controls on indidivual graphical elements in the dialog.
    There are a few exceptions however:

    | Control                           | Method       | Description    |
    | --------------------------------- | ------------ | -------------- |
    | [close](../../control/close.md) | `on_close`   | The dialog is    |
    |                                 |              | about to be      |
    |                                 |              | closed, but      |
    |                                 |              | isn't closed     |
    |                                 |              | yet.             |
    | [focus](../../control/focus.md) | `on_focus`   | The dialog is    |
    |                                 |              | focused or lose  |
    |                                 |              | focus.           |
    | [init](../../control/init.md)   | `on_init`    | The dialog is    |
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

    Notice that we don't specify the dialog identifier.  It would make
    no sense here.  Therefore, to use these events, you should just add a
    method in the dialog class with the control name and no identifier:

        class ExampleDialog(Dialog):

            def on_focus(self):
                print(f"Am I focused? {'yes' if self.focused else 'no'}")

    """

    tag_name = "dialog"
    attrs = (
        Attr("title", help="The dialog title"),
        Attr("width", help="The dialog width", type=int, default=6),
        Attr("height", help="The dialog height", type=int, default=6),
    )

    def __init__(self, layout, parent, title, width=0, height=0):
        super().__init__(layout, parent)
        self.title = title
        self.width = width
        self.height = height
