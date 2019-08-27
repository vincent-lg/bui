# Control overview

A control in BUI is a user direct or indirect action.  They can be linked to events in most GUI toolkits.  For instance, if the user presses a key on her keyboard, or clicks with the mouse, a control is created.

A control can easily be linked with the user-defined class inheriting from [Window](../class/Window.md).  The way to link a control is to create a method with a specific name on the child of a [Window](../class/Window.md) class.  These [control methods](#control-methods) are automatically linked before the [Window](../class/Window.md) object is created and errors can easily be reported to the developer.  This system makes it very easy to process specific controls from your [Window](../class/Window.md)-inherited class.

## Control methods

A control method's name begins with `on_` (that is, `on` followed by an underscore).  The rest of the name depends on the type of control and the control structure, as some controls can be used to link with very specific actions.

To take a very basic example, in your class, you can easily intercept the [focus](./focus.md) control like this:

```python
from bui import Window

class Example(Window):

    """Just an example, not displaying window layout here."""

    def on_focus(self):
        print("The window was either focused or lost focus.")
```

The method will be called when the window is focused or lose focus, basically when the user switches to a different window or comes back to it.  This is a [window control](#window-control), meaning it is connected with the window itself and not with one of the widgets on the window.  The difference is detailed in the next section.

## Control types

Controls are separated into two categories:

- [Window controls](#window-control): the window controls are bound to the window and will fire regardless of the specific widget being focused.  Keyboard shorcuts are often intercepted at the window level, for instance.
- [Widget controls](#widget-control): the widget controls are linked to a specific widget on the window.  They will only fire in response to a direct user action if the widget is focused, although indirect widget controlss can still occur in some situations.  The [click control](./click.md) for instance often is a widget control, for we usually want to know if something specific was clicked on, rather than doing something anytime anything is clicked.

A control is not defined as a window or widget control by itself.  All controls can be used in both cases with some exceptions.  This is mentioned on the specific control documentation page.

### Window control

Window controls bind an action to the entire window with all its content.  Binding at this level means that widgets will send the control to their parent window when it occurs.

For instance, you could intercept any key pressed in the window, regardless of what is being focused at the time:

```python
from bui import Window

class Example(Window):

    """Just an example, not displaying window layout here."""

    def on_press(self):
        print("Some key is pressed.")
```

Well, this is not too useful, as this control would be called for every key but you don't know which.  Better to at least intercept the key being pressed:

```python
class Example(Window):

    """Just an example, not displaying window layout here."""

    def on_press(self, key):
        print(f"The user pressed on {key}.")
```

> Note: control arguments are not specific to window controls and will be described in the [section on control attributes](#control-attributes).

Both methods would be called any time a user presses a key, no matter what widget in the window is currely focused.

If, for instance, you have two widgets on your window: a [button](../layout/tag/button.md) and a [table](../layout/tag/table.md).  The `on_press` method will be called when the user presses a key on her keyboard, regardless if the button or table is focused.

### Widget control

Widget controls are linked to a specific widget and only fire if this widget is focused or if firing the control makes sense for this widget.  Here is a possible window layout that might explain the situation with more clarity:

```
<window>
  <text id=text1 x=0 y=2 />
  <text id=text2 x=5 y=2 />
</window>
```

If, in your [Window](../class/Window.md)-inherited class, you want to intercept when the second text entry (text2) gets focused or loses focus:

```python
class Example(Window):

    """An example to show a widget control."""

    def on_focus_text2(self):
        print("The text2 widget gets or loses focus.")
```

The method's name contains:

- `on_`: `on` followed by an underscore.
- `{control name}`: the control name followed by another underscore.
- `{widget ID}`: the widget identifier.

The widget identifier is the one specified in the layout with the `id` attribute.  If none is set, BUI will try to assume a proper identifier for the widget, although it's not recommended to let BUI guess as it would create implicit code and may cause hard-to-debug errors after some time.

Again, most controls can be both window or widget controls, though they might have different meanings.  Read the specific control documentation page for details and examples.

## Implicit controls

Most widgets have an implicit control which is the default control for this widget.  You can omit the control name in your control method.  Let's see an example:

```python
class Example(Window):

    """Window showing implicit controls."""

    # Note: we use an in-code layout for clarity here, which is not
    # recommended in BUI.

    layout = mark("""
      <menubar>
        <menu name="File">
          <item id="quit">Quit this app right away</item>
        </menu>
      </menubar>

      <window title="An example for implicit controls">
      </window>
    """)

    def on_quit(self):
        """The user pressed on the 'quit' menu item."""
        self.close() # closes the window
```

The method name here is `on_quit`.  It's easy to read and somewhat obvious what it does: when the `File` menu is opened, if the user selects "Quit this app right away", this method is called.  But hold, it's a bit odd at firs glance.

This is a [widget control](#widget-control), yet we did not specify which control name to use.  Shouldn't we have used `on_click_quit` instead?

The answer is somewhat logical but it might take some time to get used to it: `on_click_quit` and `on_quit` do the same thing.  In fact, when BUI tries to bind the control methods, it notices the `on_quit` method.  It looks to see if `quit` is a control name.  It is not.  Then it checks your widgets.  There's one with ID `quit`, so BUI wonders if it's an implicit control.  The [item](../class/Item.md) widget has the "click" implicit control.

That's why a method named `on_quit` and `on_click_quit` do the same thing: menu items have an implicit control (when they're clicked).  Because we often want to do this (link a menu item with an action), BUI will assume what to do when we give it an `on_quit` method.

> Implicit controls are somewhat ambiguous at times.  It can be great for very obvious windows, but when you start using a lot of widgets with a lot of identifiers, implicit controls might be confusing.  This is all a choice and BUI lets you decide which to make.  As a guiding rule, however, you could decide to use only implicit controls with widgets that do not need to intercept more than one control (like menu items, where it's obvious).

If BUI cannot link a control method for any reason, it will try to explain why it failed and will provide additional information on how to fix this error.

## Main controls and sub-controls

Some controls provide additional flexibility.  You can add more information in the method name to intercept specific controls.  The best example is the [press control](./press.md), which is called when a key is being pressed by the user.

You can define an `on_press` method to intercept any key press from the user.  But it's more common to want to intercept a specific key withint a method.  That avoids some trange-looking conditions to know what key was pressed and in what context.  The way to do it is to specify the key name in the method name:

    def on_press_a(self, ...):

This method will only be called if the user presses the 'a' key on her keyboard. You can intercept most keys in such a way:

    def on_press_i(self, ...): # intercepts the 'i' key
    def on_press_9(self, ...): # Intercepts the '9' key
    def on_press_shift_o(self, ...): # intercepts the 'Shift + o' shortcut
    def on_press_alt_f1(self, ...): # Interpts the 'Alt + F1' shortcut
    def on_press_return(self, ...): # Intercepts the 'RETURN' key

All these methods are called sub-controls.  Contrary to a simple control method (`on_{control type}`), they provide additional information in their name (in this context, what key combination is pressed).  When you read the specific control documentation page, you will see more details on how to use it as main or sub-control (read, for instance, the [press control](./press.md)) documentation page.

## Control attributes

In most of the examples provided here, the control method doesn't take any additional argument, except `self`.  You can, however, write control methods that need more arguments.  The argument names are used to guide BUI, so you cannot use arbitrary names (this will depend on the selected control).  Available on all controls are two names: `control` (which, if present, contain the control object), and `widget` (which, if present, contains the widget on which this control was triggered).

Let's take an easy example, again with the [press control](./press.md).

```python
class Example(Window):

    """Example, showing control method arguments."""

    def on_press(self, control):
        """
        This method is a main control, called anytime a key is
        pressed in the window, no matter what key.

        """
        print(f"The user pressed on {control.key}.")
```

The `on_press` method will intercept any key pressed while the window is being focused.  But this time, this method takes an additional argument: `control`.  This will contain the control object.  `key` is an attribute on the control object (for a [press control](./press.md)) so that `control.key` will contain the name of the key pressed by the user.

Additional arguments can take the name of control attributes.  Control attributes are different for every control.  We just saw that the [press control](./press.md) has a `key` attribute, containing the key pressed by the user.  If that's all we need, we can instead have a `key` argument in the control method:

```python
class Example(Window):

    """Example, showing control method arguments."""

    def on_press(self, key):
        """
        This method is a main control, called anytime a key is
        pressed in the window, no matter what key.

        """
        print(f"The user pressed on {key}.")
```

When the control is triggered, it examines the signature of the control method to call.  It will try to match the expected argument name with its own attributes.  That's why your control method can have none, one or more arguments that will depend on the control being triggered.  Again, remember that `control` and `wiedget` will always be available to use in a control method no matter the control.

Controls list their attributes in the specific control documentation page.  For instance, see the [attributes of the press control](./press.md#control-attributes).

## Asynchronous control methods

Control methods embed the asynchronous power of Python, introduced in Python 3.4 and 3.5.  Writing an asynchronous control method is extremely simple and allows to perform some task but not block other tasks happening at the same time.  A more typical approach would be, for this system, to use threads, but BUI has a clean way to create asynchronous control methods which doesn't require any additional code.  Of course, you can still use threads or sub-processes, if you so choose.

To use the power of asynchronous programming, just add the `async` keyword before your control method definition.  Inside of it, you will then be able to use the `await` keyword, along with other features dedicated to asynchronous operations.  Here is a very short example:

```python
from bui import Window, start

class HelloBUI(Window):

    """Class to represent a basic hello world window."""

    layout = mark("""
      <window title="Asynchronous hello from the Blind User Interface">
        <button x=2 y=2 id="slow" name="Slow clicker" />
      </window>
    """)

    async def on_click_slow(self, widget):
        """On clicking the slow clicker."""
        i = 10
        while i > 0:
            widget.name = f"{i} seconds..."
            await self.sleep(1)
            i -= 1

        widget.name = "... TOO LATE! Want to try again?"


start(HelloBUI)
```

Take a look at the `on_click_slow` control method.  It is an asynchronous method (a coroutine), defined with the `async` keyword before the `def` keyword.  In it you find a rather simple loop with an asynchronous pause every second: when the user clicks on the button, this method starts, the user sees the button name change to "10 seconds...", then a pause of 1 second, the button changes to "9 seconds..." and so on.  This doesn't block the rest of the program.  The user can click on other buttons or even shut down the window.  And the user can click on the button again even while it's counting down.  This can be avoided with a little added code.

> The `sleep` method of the [Window](../widget/Window.md) class is a shortcut to call `asyncio.sleep`, no more or less.

A control method can be synchronous (the default), that is blocking, or asynchronous (add the `async` keyword in front of the method definition).  A synchronous method is blocking, that is to say, if you put calls to `time.sleep` in them (or perform other blocking operations), your program will freeze, you won't be able to do anything on it during this freeze, including clicking on other buttons.  However, a control method can easily be asynchronous.  In this case, it is started as usual when the user performs the action triggering the control, but the control method could take time to perform and it won't block the rest of the program.

For instance, a control method could download a file using asynchronous operations.  The file might come from the Internet and downloading it would take some time.  This won't be an issue, since the method won't block.  Or it could delegate some automatic tasks to a game which wouldn't block either.

> Note: beware, though: when this document says "won't block", this is only true if your control method doesn't use blocking functions.  If you use the `requests` library to download a file, for instance, even though the `request` library is synchronous, you won't be able to benefit from this feature.  Look for asynchronous libraries ([aiohttp](https://aiohttp.readthedocs.io/) to query data from the Internet, [aiofiles](https://pypi.org/project/aiofiles/) to read and write data on the user's disk, and so on).

You can see an example of a download window in the [example/download.py](../example/download.md) file.  This shows how one can download several files at once without blocking the window in any way, reporting accurate information on the individual download status (percentage, size and so on).

## Debugging controls

Controls and control methods are so easy to create... but this simplicity comes with a price: at times, it's hard to know if a control was successfully connected, that is, if it found a control method.  For instance, you might add a button and not realize the button is not connected to any method (BUI will not warn you about that, at least, if you don't ask it to).

But BUI offers you some command-line arguments you can use to debug the created window.  One of them is `-c` (short for `--debug-controls`).  If you give BUI this flag, it will display a lot of information on controls:

- Which controls are bound?  A bound control is one that can find a control method.  BUI will explain in details why this control binds to this control method.  It can depend on options.  Note that binding happens when the window is created, not when control fire.
- Which is fired:  When this option is active, BUI will show you in real-time what control is fired with whatever option.  If the control has been bound to a control method, it will also indicate it.

You can only use this debug mode from a Python script, not a frozen executable.  This is a security risk and you shouldn't let your users play with fire if you can avoid it.  To use, run Python giving your script name, and then the `-c` command-line argument.  Here is an example of output when running the [download.py](../example/download.py) script in the "example" folder with this mode set:

```
> python download.py -c
Running in 'debug controls' mode.
  Binding control methods...
    Bound close as a window control to the 'on_close' method
    Bound press as a window control with options={'key': 'ctrl_q'} to the 'on_press_ctrl_q' method
    Bound click as an implicit widget control of item(add_file) to the 'on_add_file' method
    Bound click as an implicit widget control of item(quit) to the 'on_quit' method
    Bound init as a widget control of table(download) to the 'on_init_download' method
    Bound click as an implicit widget control of button(start) to the 'on_start' method
    Bound press as a window control with options={'key': 'ctrl_a'} to the 'on_press_space_start' method
    Bound click as an implicit widget control of button(add) to the 'on_add' method
  Fire init control on window
  Fire init control on menubar
  Fire init control on menu
  Fire init control on item(add_file)
  Fire init control on item(quit)
  Fire init control on table(download)
    Match main control to on_init_download, call it
  Fire init control on button(start)
  Fire init control on button(add)
...
```

The window will open as usual.  In the console however, you will see a lot of input.  Let's detail it:

- You first see the controls being bound to a control method.  For each control that can bind, BUI will explain in details why it chose to bind this control (with these options) to this method.  The message "bound close as a window control to the 'on_close' method" shouldn't surprise you too much, once you're familiar with the terms [window control](#window-control), [widget control](#widget-control), and [control method](#control-methods).
- There are more complicated lines at binding, like "bound press as a window control with options={'key': 'ctrl_q'} to the 'on_press_ctrl_q' method".  This is how BUI binds a control with options to a control method.
- When binding [widget controls](#widget-control), notice that BUI will show the widget type with its ID whenever possible: "bound init as a widget control of table(download) to the 'on_init_download' method"
- As described above, some controls can be [implicit](#implicit-controls), so the control method doesn't have to include the control type.  This is usually the case with menu items and buttons, as shown in this line for instance: "bound click as an implicit widget control of item(add_file) to the 'on_add_file' method"
- Next BUI will show the controls that are fired.  Just before the window is displayed, the [init](init.md) control is fired by every widget on the window, thus the following lines like: "fire init control on window"
- If a fired control is bound to a control method, the call to the control method is reported: "match main control to on_init_download, call it".  This allows to see in real-time what is being called, and for what reason.

The generated output can be quite verbose...