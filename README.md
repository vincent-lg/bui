# Blind User Interface - the interface you can design with your eyes closed

Blind User Interface (BUI) is meant to be a simple toolkit to design user interfaces with a Pythonic syntax.  Having been created by a blind user, it gives a lot of importance to accessibility and compatibility with screen readers, while offering a comfortable user interface that anyone can use.  However, this restriction doesn't imply you cannot (and should not) create complex or really beautiful user interfaces with BUI.  You should and you can.  You might consider helping this project, however, to help create more elaborate interfaces should the need arise.

BUI relies on several core principles:

- An interface should not break or require any change in code when porting to a new platform.  Thus, BUI is compatible at least with Linux, Mac OS X and Windows platforms.
- A GUI toolkit perfectly accessible on Windows might break accessibility on Linux or Mac OS X.  Therefore, BUI might choose a different toolkit depending on the user's environment, with the developer's permission.
- Design and control should be separated: no more code to create interfaces should be necessary.  Designing beautiful interfaces is, after all, a work for the designers, not for the developers.  Developers should focus on the user interactions (that is, how to handle a mouse press on this button, or what to do if some text is typed in this field).
- A graphical user interface should be easy to test (in unittests for instance).  The stability of the user interface should be a core concern of the developer.

These simple concepts make for an interesting (and inovative, to some extent) approach to creating interfaces with BUI.

## Installation

To install BUI, you should simply run `pip`:

    pip install bui

## Brief example

Here is a basic usage of BUI.  This example is briefly explained just below.  To test this script, place it in any file and run it with Python, having installed BUI and a supported GUI toolkit:

```python
from bui import Window, start

class HelloBUI(Window):

    """Class to represent a basic hello world window."""

    layout = mark("""
      <window title="A BUI demonstration">
        <menubar>
          <menu name="File">
            <item>What is it?</item>
            <item>Quit</item>
          </menu>
        </menubar>

        <button x=2 y=2>Click me!</button>
        <text x=3 y=3 id=report>Report</text>
      </window>
    """)

    def on_click_me(self):
        """When the 'Click me!' button is pressed."""
        self["report"].value = "The button was clicked!"

    def on_quit(self):
        """When the user press the quit menu item in the File menu."""
        self.close()

    # Keyboard shortcuts
    def on_press_alt_f4(self):
        """When the user presses Alt + F4."""
        self.close()

    # Linking an alias to a method is so simple
    on_press_ctrl_q = on_press_alt_f4


start(HelloBUI)
```

That's it.  This little code will generate a window with:

1. A menu bar, containing only one menu (File) with different menu items.
2. A button in the center of the window, called "Click me!".
3. A text field below and to the right of this button where the text will be updated when the button is clicked.

You will find more explanation in the [documentation](https://vincent-lg.github.io/bui/) or by browsing through the [examples](https://vincent-lg.github.io/bui/example/).

## Documentation

- [BUI full documentation](https://vincent-lg.github.io/bui/)
- [BUI tutorial](https://vincent-lg.github.io/bui/tutorial/)

## License

Blind User Interface is available under the terms of the BSD Public License (v3).  In short, you can use this code for whatever reason, provided you keep the copyright identifying this code as from BUI.  Apart from that, you can use this code for whatever purpose, including to design commercial software.  You can find the full terms by reading the LICENSE file.
