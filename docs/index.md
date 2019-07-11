# Blind User Interface - the interface you can design with your eyes closed

Blind User Interface (BUI) is meant to be a simple toolkit to design user interfaces with a Pythonic syntax.  Having been created by a blind user, it gives a lot of importance to accessibility and compatibility with screen readers, while offering a comfortable user interface that anyone can use.  However, this restriction doesn't imply you cannot (and should not) create complex or really beautiful user interfaces with BUI.  You should and you can.  You might consider helping this project, however, to help create more elaborate interfaces should the need arise.

BUI relies on several core principles:

- An interface should not break or require any change in code when porting to a new platform.  Thus, BUI is compatible at least with Linux, Mac OS X and Windows platforms.
- A GUI toolkit perfectly accessible on Windows might break accessibility on Linux or Mac OS X.  Therefore, BUI might choose a different toolkit depending on the user's environment.
- Design and control should be separated: no more code to create interfaces should be necessary.  Designing beautiful interfaces is, after all, a work for the designers, not for the developers.  Developers should focus on the user interactions (that is, how to handle a mouse press on this button, or what to do if some text is typed in this field).
- A graphical user interface should be easy to test (in unittests for instance).  The stability of the user interface should be a core concern of the developer.

These simple concepts make for an interesting (and inovative, to some extent) approach to creating interfaces with BUI.

## Installation

To install BUI, you should simply run `pip`:

    pip install bui

Additionally, you should also install a GUI toolkit.  Remember that BUI will draw the bridge betwewen simple and portable code to the usable GUI toolkit on this platform.  For the time being, BUI is only compatible with wxPython, though this is to change in future versions:

    pip install wxPython

## Brief example

Here is a basic usage of BUI.  This example is briefly explained just below.  To test this script, place it in any file and run it with Python, having installed BUI and a supported GUI toolkit:

```python
from bui import Window, start

class HelloBUI(Window):

    """Class to represent a basic hello world window."""

    layout = mark("""
      <menubar>
        <menu name="File">
          <item>What is it?</item>
          <item>Quit</item>
        </menu>
      </menubar>

      <window cols=5 rows=5 title="A BUI demonstration">
        <button x=2 y=2 name="Click me!" />
        <text x=3 y=3 value="Nothing yet" />
      </window>
    """)

    def on_click_me(self):
        """When the 'Click me!' button is pressed."""
        self.get("text").value = "The button was clicked!"

    def on_quit(self):
        """When the user press the quit menu item in the File menu."""
        self.close()

    # Keyboard shortcuts
    def on_press_alt_f4(self):
        """When the user presses Alt + F4."""
        self.close()


start(HelloBUI)
```

That's it.  This little code will generate a window with:

1. A menu bar, containing only one menu (File) with different menu items.
2. A button in the center of the window, called "Click me!".
3. A text field below and to the right of this button where the text will be updated when the button is clicked.

In terms of code, here is what we do:

- We import the `bui` package, most specifically the [Window](./class/Window.md) class and the `start` function.  Usually you won't need to import more than the [Window](./class/Window.md) class, except for a window meant to open with your program.
- We create a class, `HelloBUI`, inheriting from [Window](./class/Window.md).  So far, this is all very standard.
- The `layout` class attribute deserves some explanation.  You can see it contains a multiline string.  In this string is defined the window layout, that is, how it should appear.  It contains something like simple HTML syntax, though it's not the HTML you will find on websites.  The syntax is, it is hoped, somewhat easy to read.  The menu bar is defined first, with its single menu (File) and a set of menu items in this menu.
- Below is our actual window, in the `window` tag.  This one might be trickier: we define the window with a size (both width in columns and height in rows).  You can picture the end result as a grid.  On this grid we will place our widgets in the window.  You can choose a big or small grid (it will give you more power to place widgets with a greater precision, but the size will always be relative to the window and screen size as defined by the operating system).
- In the window, we have two widgets: a button and a text field.  `x` and `y` are given to place the widget in this grid.  Note that `x=0, y=0` is the upper-left corner of the window, thus, `x=2 y=2` with a window of 5 colums and 5 rows will be in the middle.  And `x=3 y=3` will be a bit below and to the right of this widget.
- Notice we wrap this multi-line string in a call to `mark()`. This function is only available in a class inheriting from [Window](./class/Window.md) and only serves for debugging purposes, to show the error with greater accuracy (and tell you where it went wrong).
- That's it for the window layout.  The next methods are controls (event handlers).  They are written by developers and are meant to intercept user actions (like "this button was clicked").
- Our first control method is `on_click_me`.  BUI will automatically bind that to the action "the 'click me!' button was clicked".  The process deserves [its own documentation](./control/overview.md).  For the time being, suffice it to say that when the user clicks on the button, this method is called with no argument.
- The only thing it does is update the text field.  The `get` method is called to retrieve the **only** field of type text.  If you have two, you'll have to give a better identifier, but because there's only one, BUI understands what we want to do.  We then update it (that is, change its value attribute).  So that when the user clicks on this button, the text field will be updated.
- The second method, `on_quit`, is called when the users clicks on the Quit menu item in the File menu.  Again, BUI is smart enough to establish the connection.  Should it have its doubts, it will ask you to clarify in plain English and will not be as mean as not linking control methods that have no apparent meaning to it.
- In this method we just call the `close` method of the window to terminate.
- The `on_press_alt_f4` is a control method that will be called whenever the user presses 'Alt + F4' when the window is focused.  We close it.  Notice that we include the key names in the method name, which tends to be much easier to read and link.
- This was a class, we give it to `start` which will be responsible for starting a new window, try to find a toolkit it can use and then use it.

Notice that most of the code is actually used by our window layout.  You can (and maybe should) place the HTML window layout in a separate file, so that designers can edit it wihout seeing and worrying about your code.  On your side, you don't really need to know how the window is designed, as long as you know the controls to interact with users.

## Documentation

BUI's documentation can be found here, or in the *docs* folder in the repository itself :

- Supported infrastructure
  - [Supported Python versions](support/python.md)
  - [Supported graphical toolkit](support/gui.md)
  - [Supported platforms](support/platform.md)
- Layout syntax
  - [BUI's layout language overview](layout/overview.md)
  - [Describing the layout in code](layout/code.md)
  - [Describing the layout in a separate file](layout/file.md)
  - [Building the layout dynamically](layout/dynamic.md)
  - [List of supported markup tags](layout/tag/index.md)
    - [menubar](layout/tag/menubar.md)
      - [menu](layout/tag/menu.md)
      - [item](layout/taag/item.md)
    - [toolbar](layout/tag/toolbar.md)
    - [window](layout/tag/window.md)
      - [book](layout/tag/book.md)
      - [button](layout/tag/button.md)
      - [checkbox](layout/tag/checkbox.md)
      - [list](layout/tag/list.md)
      - [tab](layout/tag/tab.md)
      - [table](layout/tag/table.md)
      - [text](layout/tag/text.md)
      - [tree](layout/tag/tree.md)
- Data models
  - [BUI data model overview](data/overview.md)
  - [Data types](data/types.md)
    - [int, float and str](data/int-float-str.md)
    - [Datetime](data/datetime.md)
    - [list and tuples](data/list-tuples.md)
    - [dict](data/dict.md)
- Controls
  - [BUI controls overview](control/overview.md)
  - [List of controls](control/list.md)
    - [change](control/change.md)
    - [check](control/check.md)
    - [click](control/click.md)
    - [context](control/context.md)
    - [press](control/press.md)
    - [select](control/select.md)

## License

Blind User Interface is available under the terms of the BSD Public License (v3).  In short, you can use this code for whatever reason, provided you keep the copyright identifying this code as from BUI.  Apart from that, you can use this code for whatever purpose, including to design commercial software.  You can find the full terms by reading the LICENSE file.
