# Example: checkbox

Show a window with several checkboxes.

This is particularly useful to see the way to create checkboxes and how to
bind them to control methods, as there are different possible strategies.

> Note: if not already set, you should install a GUI toolkit.

    pip install wxPython

## Source code (28 lines)

```python
from bui import Window, start

class CheckboxExample(Window):

    """Class to show several checkboxes on the window."""

    layout = mark("""
      <window title="Blind User Interface - checkboxes">
        <checkbox x=3 y=0 id="gif">GIF</checkbox>
        <checkbox x=1 y=1 id="png">PNG</checkbox>
        <checkbox x=4 y=2 id="jpg">JPEG</checkbox>
      </window>
    """)

    def on_check_gif(self, checked):
        print(f"Check GIF: {checked}")

    def on_checked_jpg(self):
        print("JPEG was checked.")

    def on_unchecked_jpg(self):
        print("JPEG was unchecked.")

    def on_check_jpg(self):
        print("JPEG state was changed.")


start(CheckboxExample)
```
