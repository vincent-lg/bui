"""Menubar object represented in layout."""

from bui.layout.attr import Attr
from bui.layout.component import Component

class Menubar(Component):

    """
    Create a menubar for this window.

    A menubar is traditionally at the top of your window, containing
    various possible actions.  It is not uncommon to link some of
    them to shortcut keys, or to connect them to buttons visible on
    the window itself.  BUI lets you define a menubar with menu items
    and sub-menus very easily:

    ```
    <window title="Menubar demo">
      <menubar>
        <menu name="File">
          <item>Quit</item>
        </menu>
      </menubar>
    </window>
    ```

    Creating a menubar involves three tags: menubar, [menu](menu.md)
    and [item](item.md).

    ## Usage

    To define a layout, in your menubar, you first need to create one
    or more [menus](menu.md).  The menus are traditionally horizontal
    labels on which the user of your application can click to unfold
    what the menu contains.  You might see a lot of applications with
    menus "file", "edit", "view" and so on.

    [menu tags](.menu.md) should be inside a menubar tag.  A menubar
    must have at least one menu, and can span on several menus.

    Each menu can then contain either:

    - [item](item.md): menu items, which can be selected.  Selecting and
        clicking on a menu item will close the menubar and fire a control.
    - [menu](menu.md): other menus, they will behave as sub-menus.

    In layout, the menubar should be defined at the top of the window.
    While not absolutely necessary, this is clearer in design.
    Positioning the menubar on the window grid is not necessary (we let
    the operating system do that).

    ### Simple menu

    Here's a simple example of a menubar with two menus, "File" and
    "Edit", and several choices in each menu.

    ```
    <window ...>
      <menubar>
        <menu name="File">
          <item>New...</item>
          <item>Open...</item>
          <item>Save...</item>
          <item>Quit</item>
        </menu>
        <menu name="Edit">
          <item>Cut</item>
          <item>Copy</item>
          <item>Paste</item>
        </menu>
      </menubar>
      ...
    </window>
    ```

    ### Sub-menus

    We can also use the [menu tag](menu.md) to create sub-menus inside
    of menus.  Replace the [item](item.md) tag by [menu](menu.md),
    give it a name, and place the items (or other menus) inside of it:

    ```
    <window ...>
      <menubar>
        <menu name="File">
          <item>New...</item>
          <item>Open...</item>
          <menu name="Import">
            <item>A file...</item>
            <item>A folder</item>
          </menu>
          <item>Quit</item>
        </menu>
      </menubar>

      ...
    </window>
    ```

    This will create a menubar with only one menu: "File".
    Inside of it are four choices: "new", "open", "import" and "quit".
    "Import" is a sub-menu, so by clicking on it we have two choices:
    import a file or import a folder.

    ## Attributes

    The menubar has no attribute.

    ## Data

    The menubar has no data to get or modify through the BUI API.
    Usually one will manipulate the [menu widgets](menu.md), or the
    [menu item widgets](item.md).

    ## Controls

    The menubar has no control.  Most of the time, you will simply
    use the controls of the [item widget](item.md).

    """

    tag_name = "menubar"
    attrs = ()
