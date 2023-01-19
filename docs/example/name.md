# Example: name

Show a window with a button to open a dialog.

Installation:

    pip install bui[demo]

To run this example:

    python download.py

[Open raw](https://raw.githubusercontent.com/vincent-lg/bui/master/example/name.py) [Open in github](https://github.com/vincent-lg/bui/blob/master/example/name.py)

## Source code (44 lines)

```python
from bui import Dialog, Window, start

class Hello(Window):

    layout = """
      <window title="Greetings">
        <button x=2 y=2 id=rename>What's your name?</button>
      </window>
    """

    async def on_rename(self):
        """The user clicked on the "rename" button."""
        dialog = await self.pop_dialog(Rename)
        if dialog: # set_true
            name = dialog["name"].value
            self.title = f"Greetings to {name}"
            self["rename"].name = f"Your name is {name}. Want to change it?"


class Rename(Dialog):

    """Dialog to change the user's name."""

    layout = """
      <dialog title="Change name">
        <text x=1 y=2 id=name>Enter your name here:</text>
        <button x=3 y=1 set_true id=ok disabled>OK</button>
        <button x=3 y=4 set_false>Cancel</button>
      </dialog>
    """

    def on_press_escape(self):
        """ESCAPE was pressed anywhere in the dialog."""
        self.set = False
        self.close()

    def on_change_name(self, text):
        if text:
            self["ok"].enable()
        else:
           self["ok"].disable()


start(Hello)
```
