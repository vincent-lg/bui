# Example: basic

BUI basic example.

This creates a small window with a menu bar, a text field and a button.
This example is useful to understand the basic principles of BUI.

[Open raw](https://raw.githubusercontent.com/vincent-lg/bui/master/example/basic.py) [Open in github](https://github.com/vincent-lg/bui/blob/master/example/basic.py)

## Source code (38 lines)

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
