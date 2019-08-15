# BUI structure

The Blind User Interface has been designed to be a Python library linking simple Python code with powerful Graphical User Interface toolkits.  This tutorial will elaborate on the structure of this library with some examples.  The [next tutorial](layout.md) will have more practical value, detailing the layout used by BUI, but it is recommended to at least read through this first tutorial to better understand how BUI works.

## Basic structure

BUI is a bridge between Pythonic code and Graphical User Interface toolkits that are not, as a rule, designed to generate beautiful code in Python.  BUI makes some bold statements about User Interface designing and how to clearly separate it.  You will discover some principles in this tutorial and the rest of this series.

But first of all, BUI is meant to be simple and Pythonic.  It uses Python introspection, properties and special methods in a way that will be familiar to the developers.  It also clearly separates between the user interface layout (how the window should appear) and what it should do in response to user actions.  In some ways, this is similar to the Model View Controller paradigm, though BUI doesn't use exactly the same strategy either.

So we find ourselves with two components for the time being: the layout (which describes how the window appears) and the user actions (which define what to do when the user does something).  BUI keeps both separate and doesn't require a strong link between these components: the library is actually designed so that designers can work on the layout, developers on the interception of user actions.

So let's look at the layout first.

## Layout

BUI defines its layout in a different but simple format.  This language is a markup language, very similar to HTML in syntax, just using different tags.  Here's a small example:

```
<window title="Where to?">
  <text id=address x=2 y=2 width=3>Enter the address here</text>
</window>
```

Applying this layout will generate a window with a title bar and only one widget: a text area where the user can type.

> What to do to see it in action?

There are two options: one of them is to place this layout in a separate file, called `address.bui` for instance, while you place the `Window` code in a file named `address.py`.  Because the files have the same name (though not the same extension), BUI will know where to find the window layout.  However, to test it right away, here's the full code you could use: paste it in a file (say, `address.py`), save and run with Python:

```python
from bui import Window, start

class Address(Window):

    """A window to show a way to enter an address."""

    layout = mark(
        <window title="Where to?">
          <text id=address x=2 y=2 width=3>Enter the address here</text>
        </window>
    """)

start(Address)
```

The details of the code will be explained later.  We just create a class and give the layout of the window in a class variable, then feed the window to the `start` function.  This is developer work and BUI recommends to place layouts in `.bui` files whenever possible.

You can learn more about the [BUI layout](../layout/overview.md) by following this link.

## User actions

Leaving the designer task, we now turn to development.  To create a window in BUI, one should create a class inheriting from [Window](../widget/Window.md).  Here is the same example with more explanation:

```python
from bui import Window, start

class Address(Window):

    """A window to show a way to enter an address."""

    layout = mark(
        <window title="Where to?">
          <text id=address x=2 y=2 width=3>Enter the address here</text>
        </window>
    """)

start(Address)
```

1. First, we import two things from `bui`: the `Window` class and the `start` function.
2. We then create a class inheriting from `Window`.
3. We define the layout in the `layout` class variable of our `Window` class.  We wrap the layout in a call to `mark`.  The layout can (and probably should) be written in a separate file instead of in the middle of your code.
4. We then give this class to the `start` function which will create the window and show it.

So far, however, we haven't defined any user action.  If we run this script, we'll see the window with a text area in which we can write... but nothing else will happen.

BUI offers a way to intercept user actions: [controls](../control/overview.md).  Controls are somewhat similar to events in other GUI toolkit.  The main difference is that they are much more flexible and easy to connect to your `Window` class.  The way to intercept a control is simply by defining a method on the `Window` class, named `on_...`.  To illustrate, let's look at another example:

```python
from bui import Window, start

class PingPong(Window):

    """Very little window to show the control methods in action."""

    layout = mark("""
        <window title="Ping Pong">
          <button x=3 y=2 id=central>Ping</button>
        </window>
    """)

    def on_click_central(self, widget):
        """The 'central' button was clicked."""
        contrary = "pong" if widget.name == "ping" else "ping"
        widget.name = contrary

start(PingPong)
```

If you run this script, you will see a window with a button, labelled "ping" in the center.  Nothing extraordinary.  But if you click on this button, it will change its label to "pong".  And if you click it again, the label will change back to "ping".  You are allowed to test a dozen times if you want.

What happened here?  You created your first control method in BUI.  When the central button is clicked (we have given a clear identifier to this button, see the layout), the `on_click_central` method is called.  It can receive several parameters (the signature is very flexible) but we asked for the widget, that is, the button which was clicked on.  We read the name of this button and change it ("ping" to "pong", "pong" to "ping").

> How does it work?

When the `start` function is called, it will do a number of things: read your window layout, check that it's correct, then examine your class to see if there are control methods.  Control methods are the ones starting with `on_`.  When it sees one, it will check the method name to see what the control means.  Here, the first part of the method name, after the `on_`, is `click`.  So the control type is "click".  Then another underscore (`_`) and the widget identifier ("central").  So BUI will connect the `on_click_central` to the control "click" of the "central" object.  When the button is clicked, it checks for its controls and call them.

But control methods can be way more powerful than that.  They just don't make your life easier by connecting the control type and widget automatically.  Look at this example:

```python
from bui import Window, start

class PingPong(Window):

    """Very little window to show the control methods in action."""

    layout = mark("""
        <window title="Ping Pong">
          <button x=3 y=2 id=central>Ping</button>
        </window>
    """)

    def on_click_central(self, widget):
        """The 'central' button was clicked."""
        contrary = "pong" if widget.name == "ping" else "ping"
        widget.name = contrary

    def on_press_p(self):
        """The user pressed 'p' on her keyboard."""
        central = self["central"]
        self.on_click_central(central)

start(PingPong)
```

We just added a new method, named `on_press_p`.  This deserves some explanation: if you look at the method name... you will understand it's a control method because it begins with `on_`.  Then comes the control type, `press`.  Then... what's that?  A single `p`?

[press](../control/press.md) is a control that can use with more precision the method name to infer information.  In this context, [press](../control/press.md) will expect the key name to be intercepted.  We specified `p`, so it will only link the "press" control type if the key being pressed is "p" to the `on_press_p` method.  So when the user presses the `p` key on her keyboard, this method will be called.  It will actually call `on_click_central` so that clicking on the button or pressing the `p` key will do the same thing.

> Why didn't we specify a widget identifier in the method name?  Like "on_press_p_central"?

Control methods can be specific to a widget or can be general to an entire window.  The first method we created, `on_click_central`, is specific to the "central" widget (that is, our button).  The second method, however, `on_press_p`, will fire when the user presses the 'p' key on her keyboard, no matter what widget is focused in the window.  But yes, we could have written a method named `on_press_p_central` which will only fire if the "central" widget is focused and the user presses 'p'.

You might also have noticed that the arguments we expected from our control methods vary.  In fact, the control will only give the control method the arguments it requires.  That is a more complex topic, discussed in details in the [documentation about controls](../control/overview.md).

## Widgets

We have seen a few different widgets in the previous sections, mainly [window](../layout/tag/window.md), [text](../layout/tag/text.md) and [button](../layout/tag/button.md).  There are, of course, many more.  This section will elaborate more on what they are.

When we created our "ping pong" window, we actually used a button widget directly:

    def on_click_central(self, widget):
        """The 'central' button was clicked."""
        contrary = "pong" if widget.name == "ping" else "ping"
        widget.name = contrary
```

The `widget` argument contains our widget (that is, our button).  We check its name and change it at the next line.  Pretty straightforward, all in all:

Widgets are objects.  When BUI reads your layout, it creates corresponding widgets that you will manipulate in your control methods.  You can also request a specific widget using the `[]` operator on the window:

```
    def on_press_p(self):
        """The user pressed 'p' on her keyboard."""
        central = self["central"]
        self.on_click_central(central)
```

In this example, we retrieve the widget of ID "central" (that is, our button).

It's important to realize that tags and widgets are two different concepts: a tag in your layout (like `<button ...>`) will, if correct, lead to the creation of a [Button widget](../widget/Button.md), but that's not always true.  Some tags don't generate widgets.  Some widgets are not meant to be created from tags.

Again, separate the window structure, defined in layout (with the pseudo-HTML language), meant to be used by designers, and the window structure defined in code with the widget hierarchy.  The widget objects will be available on control methods and other methods you might create in code.

### Generic and specific widgets

And things get a little more complicated: a widget is a Python object representing the widget on the window.  You have access to properties, attributes and methods on this widget.  This widget will remain the same no matter the GUI toolkit you use.

but in order to actually display a window, BUI will have to "convert" this widget into something the window toolkit can use.  For instance, a BUI button might be converted to a [wx.Button](https://wxpython.org/Phoenix/docs/html/wx.Button.html).  BUI will establish the connection between the widget object in its library and the actual object used by the GUI toolkit.

What does it mean?  When you enter `widget.name = ...` for instance, with `widget` being a BUI button, it will call the proper method on the [wx.Button](https://wxpython.org/Phoenix/docs/html/wx.Button.html) object to update the button name.

And when the [wx.Button](https://wxpython.org/Phoenix/docs/html/wx.Button.html) intercept events, it will send usable controls to BUI.

This system allows to share BUI widgets and use the same code no matter the used toolkit.

> Can I access the GUI toolkit objects from BUI?

Yes, but you should not.  As a lot of other frameworks, BUI is meant to remain generic and portable across toolkits.  If you access the used toolkit directly, BUI is probably not the right tool for you and you might be better off using the toolkit itself.

We use the term "generic" here to refer to a BUI widget, and specific to refer to the widget corresponding to the BUI widget on a specific graphical toolkit.  So in this example, [Button](../widget/Button.md) is a generic widget (it will not change no matter the toolkit), whereas [wx.Button](https://wxpython.org/Phoenix/docs/html/wx.Button.html) is a specific representation of a `Button` in the wxPython toolkit.

## Conclusion

This tutorial attempted to explain with examples some of the concepts of BUI.  You should be more familiar with the terms:

- [Layout and tags](../layout/overview.md),
- [Control and control methods](../control/overview.md),
- [Generic and specific widgets](../widget/overview.md).

If you have even a limited understanding of these concepts, you might head over to the [next section of this tutorial](layout.md).

