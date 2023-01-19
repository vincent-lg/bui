# Dialog boxes and external windows in BUI

A user interface is not often contained within one window with no dialog.  Asking for confirmation, displaying information or errors, prompting for new information, usually take place in a dialog.  Visually, a dialog box "pops" on top of your window, which remains "visible" but cannot be reached by the user until the dialog is closed.

External windows, on the other hand, are windows that open without rendering their parent inaccessible: users can navigate back to the parent window and use it.  This is less common but it might make sense in some context.

BUI supports both dialogs and external windows and they can be surprisingly close in terms of code.

## The dialog

To illustrate the way dialogs work in BUI, we are going to use a simple example: a window with a button.  When pressing this button, a dialog should pop to ask the user to enter its name:

```python
class Hello(Window):

    layout = """
      <window title="Greetings">
        <button x=2 y=2 id=rename>What's your name?</button>
      </window>
    """

    def on_rename(self):
        """The user clicked on the "rename" button."""
        print("Rename the user!")

start(Hello)
```

### A dialog in layout

To pop a dialog, we have to call the `pop_dialog` method on the window.  We can specify the dialog layout as a string: this is the layout you're used to defining in BUI, the only difference is that the `<window>` tag is replaced by the `<dialog>` tag.

We also need to slightly alter our control method: to handle a dialog might take awhile and the `pop_dialog` method is asynchronous (we must use `await` in front of it).  And because of this, we also need to use `async` in front of the method itself:

```python
    async def on_rename(self):
        """The user clicked on the "rename" button."""
        print("Rename the user!")
        await self.pop_dialog(...)
```

Let's write our first attempt:

```python
    async def on_rename(self):
        """The user clicked on the "rename" button."""
        print("Rename the user!")
        await self.pop_dialog("""
            <dialog title="Change name">
              <text x=1 y=2 id=name>Enter your name here:</text>
            </dialog>
        """)
```

We give to `self.pop_dialog` a layout that should look familiar to you, except that the `<window>` tag now is a `<dialog>` tag.   This dialog tag contains a text box.

If you try this code, you will see a window appearing with a single button.  Should you click on the button, you will see a new dialog appear and obscure the first window: in this dialog, there's only a text field.

But you cannot do much.  You can type your name, but you don't have a way to submit it.  Or even cancel your input.  You can close the dialog and go back to the main window but that's not really helpful.

Most dialog boxes have at least a "OK" and "Cancel" button.  But BUI doesn't assume that's what you want.  You can easily add them, but that needs to be done manually.  Fortunately, it's not too complicated:

```python
    async def on_rename(self):
        """The user clicked on the "rename" button."""
        print("Rename the user!")
        await self.pop_dialog("""
            <dialog title="Change name">
              <text x=1 y=2 id=name>Enter your name here:</text>
              <button x=3 y=1 set_true>OK</button>
              <button x=3 y=4 set_false>Cancel</button>
            </dialog>
        """)
```

We have added two buttons to our layout.  The "OK" button with an attribute `set_true` and the "Cancel" button with a `set_false` attribute.

These two attributes mean: when the button is clicked, just close the dialog.  But "OK" has to tell the window: "the dialog was submitted" while "cancel" has to tell the window "the dialog was cancelled".  This is done through the value returned by `pop_dialog`: if a `set_true` button was clicked, the dialog closes and `true` is sent to the window.  If a `set_false` button was clicked, the dialog closes and `false` is sent to the window.

To check this, let's elaborate on our method.  We need to catch the result of `pop_dialog` and test it:

```python
    async def on_rename(self):
        """The user clicked on the "rename" button."""
        print("Rename the user!")
        dialog = await self.pop_dialog("""
            <dialog title="Change name">
              <text x=1 y=2 id=name>Enter your name here:</text>
              <button x=3 y=1 set_true>OK</button>
              <button x=3 y=4 set_false>Cancel</button>
            </dialog>
        """)

        if dialog: # set_true
            print("The dialog was submitted")
        else: # set_false
            print("The dialog was cancelled")
```

If you try this code and click on the button, you will see the dialog again.  If you click on "OK", in your console, you should see that the dialog was submitted.  If you click on the button again and then click on "Cancel", you should see in your console that the dialog was cancelled.  The same thing will happen if you click on the button and close the dialog.

Finally, we need to retrieve the value entered by the user.  This will be contained inside the text field of the dialog, the one under the ID "name".  We can access dialog elements just like window elements, using the `[]` operators.  Of course, be sure to use these operators on the value returned by `pop_dialog`:

```python
    async def on_rename(self):
        """The user clicked on the "rename" button."""
        print("Rename the user!")
        dialog = await self.pop_dialog("""
            <dialog title="Change name">
              <text x=1 y=2 id=name>Enter your name here:</text>
              <button x=3 y=1 set_true>OK</button>
              <button x=3 y=4 set_false>Cancel</button>
            </dialog>
        """)

        if dialog: # set_true
            name = dialog["name"].value
            print(f"The dialog was submitted by {name}")
        else: # set_false
            print("The dialog was cancelled")
```

If the dialog was submitted (we check the return value of `pop_dialog`), then we can access the dialog elements using `dialog{"item ID"]`. So `dialog["name"]` will return the text widget of the now-closed dialogs.  And `dialog["name"].value` will return the text written inside that text field.

If you try the above code and click on the button, then fill in a name and click on "OK", you should see the name in your console.

Let's go just a bit farther to illustrate: we would like to change the window title and the button name when we submit the dialog.  It's quite simple to do.  Here's the full code:

```python
from bui import Window, start

class Hello(Window):

    layout = """
      <window title="Greetings">
        <button x=2 y=2 id=rename>What's your name?</button>
      </window>
    """

    async def on_rename(self):
        """The user clicked on the "rename" button."""
        dialog = await self.pop_dialog("""
            <dialog title="Change name">
              <text x=1 y=2 id=name>Enter your name here:</text>
              <button x=3 y=1 set_true>OK</button>
              <button x=3 y=4 set_false>Cancel</button>
            </dialog>
        """)

        if dialog: # set_true
            name = dialog["name"].value
            self.title = f"Greetings to {name}"
            self["rename"].name = f"Your name is {name}. Want to change it?"

start(Hello)
```

When we click on the rename button, we get a dialog box.  If we set a name and click on "OK", then the window title will change and the button's name will change as well.

### A dialog in a separate class

Setting a dialog in layout is fine if you don't need something too fancy.  Oftentimes, we prefer to define a dialog in its very own class.  The process is quite straightforward.  We'll use the same example:

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
        <button x=3 y=1 set_true>OK</button>
        <button x=3 y=4 set_false>Cancel</button>
      </dialog>
    """


start(Hello)
```

The first change is in the `on_rename` method.  We still use `pop_dialog` but instead of sending in a string defining our layout, we specify `Rename`.  That's our class and you can see its definition a few lines below.

The `Rename` class inherits from `Dialog`.  The layout is strictly identical to the previous example.  In fact, if you run this script, you shouldn't see any difference.

But there is one important difference: our class inheriting from `Dialog` can implement control methods.  And although that seems a very basic change, it makes a whole lot of difference.

Let's start by adding a simple keyboard shortcut: if we press `ESCAPE` anywhere in the dialog, it should close.  That's just a method away:

```python
class Rename(Dialog):

    """Dialog to change the user's name."""

    layout = """
      <dialog title="Change name">
        <text x=1 y=2 id=name>Enter your name here:</text>
        <button x=3 y=1 set_true>OK</button>
        <button x=3 y=4 set_false>Cancel</button>
      </dialog>
    """

    def on_press_escape(self):
        """ESCAPE was pressed anywhere in the dialog."""
        self.set = False
        self.close()
```

Everything happens in our `on_press_escape` method:

- We manually set the value of the dialog.  `set_false` or `set_true` button clicks would do that, but in our case, we have to set the dialog explicitly.  We set it to `false` because a press on `ESCAPE` should just cancel the operation ;
- We then call the `close` method on our dialog.  Nothing more.

If you try this code, click to open the dialog and press escape.  The dialog should close but the window's title or button's name shouldn't change.

Something a bit more advanced?  How about making sure that the user does enter a name before clicking on "OK"?  We could do that in different ways but here, we're going to make the "OK" button unavailable if there's no text in the "name" field.

What we can do is make "OK" disabled by default and then enable it only when there is text in the field.  We would need to check each time the text updates.  And to do that, we can use the `change` control: it will be called when the text changes:

```python
class Rename(Dialog):

    """Dialog to change the user's name."""

    layout = """
      <dialog title="Change name">
        <text x=1 y=2 id=name>Enter your name here:</text>
        <button x=3 y=1 set_true id=ok disabled>OK</button>
        <button x=3 y=4 set_false>Cancel</button>
      </dialog>
    """

    # ...

    def on_change_name(self, text):
        if text:
            self["ok"].enable()
        else:
           self["ok"].disable()
```

First, notice a few things in the layout, particularly in the description of the "OK" button.  We need to give it an ID.  We also set it to be disabled by default, with the `disabled` attribute.

Then we add the `on_change_name` method.  It will be called each time the text in the "name" field is updated.  The `text` argument is supplied by `change`, it will contain the new text in the widget (it's not there yet, the `on_change` method can cancel the operation if need be).

Next we check if there is any text in the field: if yes, we enable the button.  If not, we disable the button.

You can try this code: if you click on the button to open the dialog, the "OK" button should be disabled.  But it will be enabled again as soon as you type a letter in the field.  If you remove it though, the button will be disabled again.

In short, describing dialogs in separate classes allow to add control methods on the dialog which might be extremely useful.  Also note that this can be used to check the validity of the input (we could have set an `on_click_ok` method for instance, in the previous example).

