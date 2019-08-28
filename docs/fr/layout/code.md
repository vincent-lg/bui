# Layout in code

Although this is not recommended, you can define your window layout in your Python code.  BUI strongly encourages placing your design in a separate [file](./file.md).  This is both easier for development and maintenance.  However, it doesn't forbid placing the layout in plain Python code.

## The Window class

One of the first steps in your task as a developer will be to play with the [Window](../class/Window.md) class.  In your Python code, you might end up with something like this:

```python
from bui import Window

class MainInterface(Window):

    """My main interface, that should open when the program starts."""

    pass
```

To define the layout in code, create a `layout` class attribute and give it the window definition.  You are probably better off using a multiline string, as the example below shows:

```python
class MainInterface(Window):

    """My main interface, that should open when the program starts."""

    layout = """
      <window>
        <button x=0 y=0 name="Why not click me?" />
      </window>
    """
```

BUI will know that the layout has been defined in the `layout` class attribute.  Inside, just place the window layout, as [you normally would](./overview.md).

## Rendering arbitrary strings

If, for some reason, you don't want to place the window layout in the `layout` class attribute, you can [ask BUI to dynamically generate the window from a string](./dynamic.md).  Again, you are encouraged to place this content in a separate [file](./file.md), but if you have good reasons not to do so, you can render a window from a string (class `str`).

### Rendering an entire window

You don't have to create even a `Window` class to generate a window.  This allows for quick testing from designers, to see how their window will render in the end.  Of course, this also prevents you from adding [controls](../control/overview.md), so you cannot easily link a user action to a certain behavior of your window.  In other words, a window generated with this method might be nice, but it will not do anything whenever you press on the buttons or select a menu.

The `start` function defined in the `bui` package is usually called with a [Window](../class/Window.md) class to get started.  You can give it a plain `str` instead:

```python
from bui import start

start("""
  <window>
    <button x=0 y=0 name="Why not click me?" />
  </window>
""")
```

### Rendering a popup dialog

Most times, if a user clicks on a button, you will want a certain action to occur.  This "action" can be a dialog appearing on the screen, on top of your original window.  As usual, you have two ways to do it:

- Referring to a file that contains the dialog layout.
- Generating a dialog based on a given Python string (class `str`).

This document will only show the latter option.  You can use the [Window](../class/Window.md) instance method [popup_string](../class/Window.md#popup_string) to create a popup window with a given layout.

```python
class MainInterface(Window):

    """My main interface, that should open when the program starts."""

    layout = """
      <window>
        <button x=0 y=0 name="Click me!" />
      </window>
    """

    def on_click_me(self):
        """When the user clicks on the 'click me' button."""
        layout = """
          <window>
            <text x=1 y=2 name="Please type your name here" />
          </window>
        """

        # Popup the dialog
        name = self.popup_string(layout)
        print(f"Your entered the name {name}.")
```

Although not particularly pretty, this syntax allows you to create a quick dialog.  The dialog will "popup" on top of your main window.  Your main window will not be accessible again until the popup dialog is closed.  We use the `popup_string` method and give it the layout to display as a Python string.  This method, as does [render](../class/Window.md#render), will return the dialog result (that is, the information the user provided before closing the dialog).

### Rendering a follow-up window

Sometimes, when a button is clicked, you want to dismiss the current window and switch to a new one.  BUI calls this type of action "following", since the new window follows the previous, but the previous one is dismissed when the new one appears.  This is most often useful when you have a dialog-like window with "previous" and "next" buttons.  Clicking on "next" will switch to a new dialog but the previous one will be closed.  Notice that there are other ways to handle this common situation.

Again, you can keep the new window layout in a separate [file](./file.md).  You also can generate the new window with a plain string containing the window layout.  Instead of using [popup_string](../class/Window.md#popup-string), you will use the [followup_string](../class/Window.md#followup-string) method:

```python
class MainInterface(Window):

    """My main interface, that should open when the program starts."""

    layout = """
      <window>
        <button x=0 y=0 name="Click me!" />
      </window>
    """

    def on_click_me(self):
        """When the user clicks on the 'click me' button."""
        layout = """
          <window>
            <text x=1 y=2 name="Please type your name here" />
          </window>
        """

        # Follow-up with the new dialog.  Notice that althoug this control
        # "pauses" waiting for user input, the old window itself will be
        # dismissed as soon as this method is called.
        name = self.followup_string(layout)
        print(f"Your entered the name {name}.")
        print("But where is my window?")
```

In the previous example, notice that the dialog asking you to enter your name appears and the old window is closed immediately.  The `on_click_me` method continues, but when the user closes the new dialog... there is no window at all unless you generate a new one.
