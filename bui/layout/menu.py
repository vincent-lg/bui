"""Menu object represented in layout."""

from bui.layout.attr import Attr
from bui.layout.component import Component

class Menu(Component):

    """
    Create a menu inside of a menu bar, toolbar or context menu.

    A menu is a generic representation of a menu in a
    [menu bar](menubar.md), [toolbar](toolbar.md) or
    [context menu](context.md).  As a wrapper around other menus or items,
    its shape can vary: in a [menu bar](menubar.md) for instance, menus
    always are necessary as direct children and they should contain items
    or other menus.

    ```
    <menu name="File">
      ...
    </menu>
    ```

    ## Usage

    Menus can have several purposes depending on where they are used:

    ### Menu bars

    In [menu bars](menubar.md), a menu is a direct child of the
    [menubar tag](menubar.md) and will represent the horizontal,
    expandable menu of a given application:

    ```
    <menubar>
      <menu name="File">
        <item>Quit</item>
      </menu>
    </menubar>
    ```

    In this example, the "File" menu is the only menu in the menu bar.
    If you click on it, the menu will expand and you will see the "Quit"
    menu item.

    Menus can also be used for sub-menus in menu bars:

    ```
    <menubar>
      <menu name="File">
        <item>New...</item>
        <item>Open...</item>
        <menu name="Import">
          <item>From a file...</item>
          <item>From a URL...</item>
        </menu>
        <item>Quit</item>
      </menu>
    </menubar>
    ```

    In this example, the "File" -> "Import" item is a sub-menu: if you
    click on it you see two possible choices: import from a file or
    from a URL.

    ### In toolbars

    Inside [toolbars](toolbar.md), menus are only used for sub-menus:

    ```
    <toolbar>
      <item>Cut</item>
      <item>Copy</item>
      <item>Paste</item>
      <menu name="Paste special">
        <item>Mix...</item>
        <item>Merge...</item>
      </menu>
      <item>Property...</item>
    </toolbar>
    ```

    ### In context menus

    In [context menus](context.md), as in [toolbars](toolbar.md), menus
    are used for sub-menus.  The layout looks very similar to a toolbar's:

    ```
    <context id=music>
      <item>Cut</item>
      <item>Copy</item>
      <item>Paste</item>
      <menu name="Paste special">
        <item>Mix...</item>
        <item>Merge...</item>
      </menu>
      <item>Property...</item>
    </toolbar>
    ```

    ## Attributes

    | Name         | Required | Description              | Example     |
    | ------------ | -------- | ------------------------ | ----------- |
    | `name`       | Yes      | The menu name. This      | `<menu       |
    |              |          | attribute is mandatory.  | name=File>`  |

    > `name` is a mandatory attribute.  Notice that we don't specify an ID
      (identifier), most of the time we'll only place IDs on
      [menu items](item.md).

    ## Data

    This tag will be turned into a [Menu widget](../../widget/Menu.md).
    This widget has no data per se.

    ## Controls

    This widget has no control.  Use the controls on
    [menu items](item.md#controls) instead.

    """

    tag_name = "menu"
    attrs = (
        Attr("name", help="The menu name"),
    )

    def __init__(self, layout, parent, name):
        super().__init__(layout, parent)
        self.name = name
