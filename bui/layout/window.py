"""Window object represented in layout."""

from bui.layout.attr import Attr
from bui.layout.component import Component

class Window(Component):

    """
    Window tag, to encompass widget tags.

    The window tag is the only one that is truly mandatory in your
    [layout](../overview.md).  It is used to describe both a window and
    dialog.  It will contain all your widgets (graphical elements).

    ```
    <window>
      ...
    </window>
    ```

    ## Attributes

    | Name         | Required | Description              | Example     |
    | ------------ | -------- | ------------------------ | ----------- |
    | `rows`       | No       | The number of rows in    | `<window    |
    |              |          | the window grid.         | rows=10>`   |
    |              |          | Default is `6`.          |             |
    | `cols`       | No       | The number of columns    | `<window    |
    |              |          | in the window grid.      | cols=5>`    |
    |              |          | Default is `6`.          |             |
    | `title`      | Yes      | The window or dialog     | `<window    |
    |              |          | title.  This attribute   | title="User |
    |              |          | is mandatory.            | Config">`   |

    You cannot set a window or dialog without a proper title.  Doing so
    would impair accessibility for screen readers.  If these tools can
    read anything at all on your window, it's the title bar, so be sure
    it's not empty.

    > `title` is a translatable attribute.  If internationalization is
      set, it should contain the `ytranslate` path to the title and will
      be translated in the proper language as needed.

    The `rows` and `cols` attributes are used to set the window grid.  You
    can think of them as the height (in rows) and width (in columns) of the
    grid.  Changing this value won't make the window any bigger, but
    it will give you more control on how to place the widget in the window
    itself.  On the other hand, having a large grid can make designing not
    so easy.  It all depends on your needs.

    > Note: you don't have to set the same number of rows and columns.
      This is just the default value.  You can set different values with no
      trap:

    ```
    <window cols=1 rows=8>
    ```

    This will set a window with only one column, but 8 rows.  If you place
    a widget in `x=0 y=0`, it will take all the window's width.  Again,
    this doesn't change the window size in any way, just the way widgets
    are placed on it.  You can picture the window to always be a
    square but sliced in different portions (squares or rectangles, more
    or less big depending on the height and width you set in the window
    tag).

    ## Data

    A window is a specific graphical element since it only contains other
    elements and has no meaning by itself.  Therefore, you cannot send
    it data, it wouldn't make much sense.  Instead, you should
    send data to the window's graphical elements themselves.

    However, some window attributes can be changed on the fly.

    | Attribute      | Meaning and type | Example                     |
    | -------------- | ---------------- | --------------------------- |
    | `title`        | The title (str)  | `self.title = "New title"`  |

    These attributes can be accessed and set using the standard Python
    syntax for attributes.  Behind the scenes, these attributes are cached,
    handled by an extended `property()`, but you don't really need to
    worry about how it works.  Suffice it to say that:

        class Example(Windows):

            def on_press_a(self):
                self.title = "You pressed A."

    ... will update the window title when the user presses the 'a' key
    on her keyboard.

    ## Controls

    The window tag is tied to the [Window](../../widget/Window.md) or
    [Dialog](../../widget/Dialog.md) class.  Therefore, when you write
    controls on either of these classes, you often want to catch controls
    on indidivual graphical elements in the window.  There are a few
    exceptions however:

    | Control                           | Method     | Description      |
    | --------------------------------- | ---------- | ---------------- |
    | [close](../../control/close.md) | `on_close`   | The window is    |
    |                                 |              | about to be      |
    |                                 |              | closed, but      |
    |                                 |              | isn't closed     |
    |                                 |              | yet.             |
    | [focus](../../control/focus.md) | `on_focus`   | The window is    |
    |                                 |              | focused or lose  |
    |                                 |              | focus.  This     |
    |                                 |              | usually happens  |
    |                                 |              | for a top window |
    |                                 |              | when the user    |
    |                                 |              | switches the     |
    |                                 |              | current app.     |
    | [init](../../control/init.md)   | `on_init`    | The window is    |
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

    Notice that we don't specify the window identifier.  It would make
    no sense here.  Therefore, to use these events, you should just add a
    method in the window class with the control name and no identifier:

        class MainWindow(Window):

            def on_focus(self):
                print(f"Am I focused? {'yes' if self.focused else 'no'}")

    """

    tag_name = "window"
    attrs = (
        Attr("title", help="The window title"),
        Attr("width", help="The window width", type=int, default=6),
        Attr("height", help="The window height", type=int, default=6),
    )

    def __init__(self, layout, parent, title, width=0, height=0):
        super().__init__(layout, parent)
        self.title = title
        self.width = width
        self.height = height
