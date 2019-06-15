# Control overview

A control in BUI is a user direct or indirect action.  They can be linked to events in most GUI toolkits.  For instance, if the user presses a key on her keyboard, or clicks with the mouse, a control is created.

A control can easily be linked with the user-defined class inheriting from [Window](../class/Window.md).  The way to link a control is to create a method with a specific name on the child of a [Window](../class/Window.md) class.  These [control methods](#Control-methods) are automatically linked before the [Window](../class/Window.md) object is created and errors can easily be reported to the developer.  This system makes it very easy to process specific controls from your [Window](../class/Window.md)-inherited class.

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

The method will be called when the window is focused or lose focus, basically when the user switches to a different window or comes back to it.  This is a [window control](#Window-control), meaning it is connected with the window itself and not with one of the widgets on the window.  The difference is detailed in the next section.

## Control types

Controls are separated into two categories:

- [Window controls](#Window-Control): the window controls are bound to the window and will fire regardless of the specific widget being focused.  Keyboard shorcuts are often intercepted at the window level, for instance.
- [Widget controls](#Widget-Control): the widget controls are linked to a specific widget on the window.  They will only fire in response to a direct user action if the widget is focused, although indirect widget controlss can still occur in some situations.  The [click control](./click.md) for instance often is a widget control, for we usually want to know if something specific was clicked on, rather than doing something anytime anything is clicked.

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

Well, this is not too useful, as this control would be called for every key but you don't know which.  Better to at least intercept the keyt pressed:

```python
class Example(Window):

    """Just an example, not displaying window layout here."""

    def on_press(self, key):
        print(f"The user pressed on {key}.")
```

> Note: control arguments are not specific to window controls and will be described in the [section on control attributes](#Control-attributes).

Both methods would be called any time a user presses a key, no matter what widget in the window is currely focused.

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

This is a [widget control](#Widget-control), yet we did not specify which control names to use.  Shouldn't we have used `on_click_quit` instead?

The answer is somewhat logical but it might take some time to get used to it: `on_click_quit` and `on_quit` do the same thing.  In fact, when BUI tries to bind the control methods, it notices the `on_quit` method.  It looks to see if `quit` is a control name.  It is not.  Then it checks your widgets.  There's one with ID `quit`, so BUI wonders if it's an implicit control.  The [item](../class/Item.md) widget has the "click" implicit control.

That's why a method named `on_quit` and `on_click_quit` do the same thing: menu items have an implicit control (when they're clicked).  Because we often want to do this (link a menu item with an action), BUI will assume what to do when we give it an `on_quit` method.

> Implicit controls are somewhat ambiguous at times.  It can be great for very obvious windows, but when you start using a lot of widgets with a lot of identifiers, implicit controls might be confusing.  This is all a choice and BUI lets you decide which to make.

If BUI cannot link a control method for any reason, it will try to explain why it failed and will provide additional information on how to fix this error.

## Main controls and sub-controls

Some controls provide additional flexibility.  You can add more information in the method name to intercept specific controls.  The best example is the [press control](./press.md), which is called when a key is being pressed by the user.

You can define an `on_press` method to intercept any key presses from the user.  But it's more common to want to intercept a specific key withint a method.  That avoids some trange-looking conditions to know what key was pressed and in what context.  The way to do it is to specify the key name in the method name:

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

Controls list their attributes in the specific control documentation page.  For instance, see the [attributes of the press control](./press.md#Control-attributes).