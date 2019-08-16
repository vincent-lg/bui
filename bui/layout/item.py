"""Item object represented in layout."""

from bui.layout.attr import Attr
from bui.layout.component import Component

class Item(Component):

    """
    Create a menu item inside a menu, toolbar or context menu.

    A menu item is a clickable element in a menu.  It is used for
    a choice the user can select.  Inside of a
    [menu bar](menubar.md), selecting a menu item will fire
    a control and close the menu bar.  You can also use
    menu items inside of [toolbars[(toolbar.md) and
    [context menus](context.md).

    ## Usage

    A menu item is supposed to be the "last choice" in a menu:
    clicking on it doesn't open another menu (use the
    [menu tag](menu.md) to create sub-menus).  You need
    to specify the item name in the tag's data:

    ```
    <menubar>
      <menu name=File>
        <item>Quit</item>
      </menu>
    </menubar>
    ```

    In this example, if the user opens the menu bar, clicks
    on "File", the "Quit" menu item will be displayed.
    Clicking on it fires a [control](#controls) and close
    the menu bar.

    See [toolbar](toolbar.md) and [context](context.md)
    for examples on how to use menu items in these widgets.

    ## Attributes

    | Name         | Required | Description              | Example     |
    | ------------ | -------- | ------------------------ | ----------- |
    | `id`         | No       | The menu item identifier | `<item      |
    |              |          | (ID). If not set, use    | id=quit>`   |
    |              |          | the item name set in     |             |
    |              |          | data.                    |             |

    This tag has no required attribute, although its data must contain
    the text to be displayed.  It is also recommended to set an `id`
    even though the shortened name (only lowercase letters will be used,
    spaces turned into the underscore) will be given if the `id`
    attribute is not set.

        <item>Quit the app</item>

    (This will set a menu item with `id` of "quit_the_app".)

    > The data is a translatable field.  If internationalization is
      set, it should contain the `ytranslate` path to the name and will
      be translated in the proper language as needed. Note that in this case,
      you absolutely need to set a proper ID, otherwise control methods
      won't be easy to bind to the menu item.

    ### Note about identifiers

    It is not uncommon to have an application with several buttons,
    menu items, items inside toolbars or context menus, doing
    the same thing.  You might consider the
    [download example](../../example/download.md) that
    shows and solves this issue: a button is present at the bottom
    of the window to add a new file to the download list.  Clicking
    it opens a dialog to enter the file name and URL.  But you can
    also open the File menu in the menu bar and select the Add...
    button.  Both do the same thing.  What then?  Do they share
    the same identifier?

    No, they can't.  An identifier is unique.  Two widgets in your
    application can't share the same identifier.  In this case, we
    bind them to different IDs, create a control method to intercept
    one, then an alias, to say that clicking on the other will
    do the same thing.

    ```python
    class DownloadExample(Window):

        layout = mark(\"\"\"
          <window title="Blind User Interface - downloading">
            <menubar>
              <menu name="File">
                <item id=add_file>Add a file...</item>
              </menu>
            </menubar>

            <!-- ... -->
            <button x=4 y=5>Add</button>
          </window>
        \"\"\")

        # So the menu item to add has ID "add_file" while the Add button
        # on the window has ID "add" (we didn't change it)
        def on_add(self):
            \"\"\"The 'add' button was clicked.\"\"\"
            # ...
        on_add_file = on_add
    ```

    So if you have several buttons and menu items doing the same
    thing, be careful to give them different IDs, then,
    if necessary, bind to the same control using aliases.

    ## Data

    An item tag will be turned into an [Item](../widget/Item.md)
    widget.  This widget has no data for the time being.

    ## Controls

    | Control                           | Method       | Description    |
    | --------------------------------- | ------------ | -------------- |
    | [click](../../control/click.md)   | `on_click`   | The menu item  |
    |                                 |              | is being clicked |
    |                                 |              | on. This is an   |
    |                                 |              | implicit control |
    |                                 |              | for menu items.  |

        class MainWindow(Window):

            def on_click_quit(self):
                \"\"\"Click on the 'quit' menu item
                (you could have called your method on_quit, the
                "click" control type is implicit for menu items).
                \"\"\"
                print("Clicked on the menu item...")
                self.close()
    ```

    """

    tag_name = "item"
    attrs = (
        Attr("id", help="The widget identifier", default=""),
    )
    must_have_data = True

    def __init__(self, layout, parent, id):
        super().__init__(layout, parent)
        self.id = id

    def complete(self):
        """Complete the widet, when all the layout has been set."""
        if not self.id:
            self.id = self.deduce_id(self.data)
