"""Context menu object represented in layout."""

from bui.layout.attr import Attr
from bui.layout.component import Component

class Context(Component):

    """
    Create a context menu, a popup menu.

    A context menu is a menu that will pop up, usually in response to
    a right click (hence the name), though context menus can be
    more generic than that.  They can be used for pop-up menus
    (appear when the user presses a button, for instance).

    ```
    <context id=right>
      ...
    </context>
    ```

    ## Usage

    Like [dialogs](dialog.md), context menus are generated dynamically
    in response to a control.  It is, however, necessary to
    register them in the window layout, even though they don't
    "appear" on the screen before they're actually popped up.

    ### Register a context menu

    To register a context menu, use the `<context>` tag as
    a direct child of a window.

    ```
    <window title="Show context menu usage">
      <!-- A menu bar perhaps here -->
      <context id=right>
        <item>Cut</item>
        <item>Copy</item>
        <item>Paste</item>
        <menu name="Paste Special">
          <item>Mix...</item>
          <item>Merge...</item>
        </menu>
        <item>Property...</item>
      </context>

      <!-- The window grid... -->
    </window>
    ```

    To register a context menu, we place a `<context>` tag as
    a direct child of the [window](window.md) tag.  We give it
    a mandatory identifier (ID).  Inside of the context tag, we use
    [items](item.md) to represent choices and [menus](.menu.md)
    to represent sub-menus.

    Defining a context menu in layout will not pop anything on
    the screen.  This is just a way to register the menu, but you'll
    have to pop it.

    ### Pop it up

    After a menu has been registered and assigned an ID, you can easily
    pop it in response to a user action, in control methods:

    ```python
    class TestContextMenu(Window):

        layout = mark(\"\"\"
           # Insert the layout in the previous section...
       \"\"\")

        def on_right_click(self):
            \"\"\"The user has right clicked anywhere on the window.\"\"\"
            # We use the context menu's identifier ("right")
            self.pop_menu("right")
    ```

    And that's it.  The call to `pop_menu` will block until the
    user selects a choice.  When that's done, a control is fired and
    the menu closes.

    > How to intercept controls in this situation?

    You will have defined control methods to intercept these choices.
    The following section offers a complete example:

    ### Control methods and context menus

    We take the same example as previously and intercept the user
    clicking on "Cut" and "Copy".

    ```python
    class TestContextMenu(Window):

        layout = mark(\"\"\"
            <window title="Show context menu usage">
              <!-- A menu bar perhaps here -->
              <context id=right>
                <item>Cut</item>
                <item id=ctx_copy>Copy</item>
                <item>Paste</item>
                <menu name="Paste Special">
                  <item>Mix...</item>
                  <item>Merge...</item>
                </menu>
                <item>Property...</item>
              </context>

              <!-- The window grid... -->
              <text x=2 y=2 width=3 id=result read-only>Result</text>
            </window>
        \"\"\")

        def on_right_click(self):
            \"\"\"The user has right clicked anywhere on the window.\"\"\"
            self.pop_menu("right")

        def on_cut(self):
            \"\"\"The user has chosen "cut" in the context menu.\"\"\"
            self["result"].value = "The user chose to Cut!"

        def on_ctx_copy(self):
            \"\"\"The user has clicked on the "copy" menu item.
            (Note that this menu has a specific ID).
            \"\"\"
            self["result"].value = "The user chose to Copy!"
    ```

    It works because the context menu was registered beforehand and
    control methods were successfully connected to menu items.  Notice
    that the
    [note about identifiers in items](item.md#note-about-identifiers)
    also applies to items inside context menus: you might need to give
    them explicit IDs (like we did for the "Copy" item in the
    previous example) and adapt your control methods accordingly.

    ## Attributes

    | Name         | Required | Description              | Example     |
    | ------------ | -------- | ------------------------ | ----------- |
    | `id`         | Yes      | The context menu         | `<context   |
    |              |          | identifier (ID).         | id=right>`  |
    |              |          | Contrary to other        |             |
    |              |          | widgets, an identifier   |             |
    |              |          | is absolutely required,  |             |
    |              |          | otherwise you won't be   |             |
    |              |          | able to pop this context |             |
    |              |          | menu in a control        |             |
    |              |          | method.                  |             |

    > `id` is the only mandatory attribute.

    ## Data

    This tag will be turned into a [Context widget](../../widget/Context.md).

    | Attribute      | Meaning and type | Example                     |
    | -------------- | ---------------- | --------------------------- |
    | `id`           | The ID (str).    | `cid = self.id`             |
    |                | This attribute   |                             |
    |                | cannot be        |                             |
    |                | changed.         |                             |

    ## Controls

    This widget has no control.  Use the controls on
    [menu items](item.md#controls) instead.

    """

    tag_name = "context"
    attrs = (
        Attr("id", help="The widget identifier"),
    )

    def __init__(self, layout, parent, id):
        super().__init__(layout, parent)
        self.id = id
