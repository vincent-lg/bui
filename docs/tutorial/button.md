# Button tutorial

This tutorial will present buttons in more details: how to create them in [layout](layout.md), how to have users interact with them and so on.  Starting with buttons is a good way to quickly see BUI's advantages, strengths and possible weaknesses.

## Buttons in layout

To create a button in layout, use the [button](../layout/tag/button.md) tag.  This needs to be placed inside a [window](../layout/tag/window.md) tag.  Let's see a basic syntax of a button definition:

    <button x=0 y=1>Name of the button</button>

As usual, you should specify at least the `x` and `y` attributes, as was discussed in the [previous tutorial](layout.md#the-window-as-a-grid).  The button name (or label) is specified as the [data](layout.md#tag-data) of the [button tag](../layout/tag/button.md).

Here's a more complex example of layout creating several buttons on the window:

```
<window title="Button demonstration in BUI">
  <button x=2 y=1>Top button</button>
  <button x=0 y=3>Left button</button>
  <button x=5 y=3>Right button</button>
  <button x=2 y=5>Bottom button</button>
</window>
```

This will create a window with 4 buttons: one at the top, one at the left, one at the right and one at the bottom of the window.

Buttons have more [attributes](../layout/tag/button.md#attributes), but perhaps the most important one is `id`.  As pointed out in the [previous tutorial](layout.md#widget-identifiers), identifiers are used to refer to widgets.  They are the point of contact between the layout and the user interactions and both the designer and developer should know these identifiers.

An identifier is a string describing the widget.  Two widgets cannot have the same identifier.  In the case of buttons, BUI will try to infer an identifier using the button name (label) if the `id` attribute is not specified.  Although it can be extremely useful, particularly on small dialogs or windows, specifying an `id` attribute for buttons is still advised:

```
<window title="Button demonstration in BUI">
  <button x=2 y=1 id=top>Top button</button>
  <button x=0 y=3 id=left>Left button</button>
  <button x=5 y=3 id=right>Right button</button>
  <button x=2 y=5 id=bottom>Bottom button</button>
</window>
```

All you need to tell the developer in charge of user interactions is that your layout defines 4 buttons: "top", "left", "right" and "bottom".  The developer doesn't need to know where they are and how they appear.

To know and use the other button attributes, see the [button tag attributes](../layout/tag/button.md#attributes).

## Control methods

As a developer, we would be more interested in how to interact with users and react to user input.  In this tutorial, we'll see how to handle clicks on buttons.

You can begin by creating a file named "buttons.py".  Inside of it, paste the following code:

```python
from bui import Window, start

class Buttons(Window):

    """A buttons demonstration in BUI."""

    # Again, the layout is included here, but it's good practice
    # to write it in a separate file (buttons.bui in this case)
    layout = mark("""
      <window title="Button demonstration in BUI">
        <button x=2 y=1 id=top>Top button</button>
        <button x=0 y=3 id=left>Left button</button>
        <button x=5 y=3 id=right>Right button</button>
        <button x=2 y=5 id=bottom>Bottom button</button>
        <text x=2 y=3 id=report>Report</text>
      </window>
    """)

    # ... we'll write our control methods here

start(Buttons)
```

This is almost the exact same layout we used in the previous section.  The only thing we add is a text field in the middle of the window to report what we do.

### Control methods

To intercept user actions in BUI, the process is to create simple methods starting with `on_` in their name.  Let's code the first one:

```python
from bui import Window, start

class Buttons(Window):

    """A buttons demonstration in BUI."""

    # Again, the layout is included here, but it's good practice
    # to write it in a separate file (buttons.bui in this case)
    layout = mark("""
      <window title="Button demonstration in BUI">
        <button x=2 y=1 id=top>Top button</button>
        <button x=0 y=3 id=left>Left button</button>
        <button x=5 y=3 id=right>Right button</button>
        <button x=2 y=5 id=bottom>Bottom button</button>
        <text x=2 y=3 id=report>Report</text>
      </window>
    """)

    def on_top(self):
        """The top button was clicked."""
        self["report"].value = "The top button was clicked."

start(Buttons)
```

If you run this code, the window should appear.  Should you click (or press RETURN) on the top button, the text field will be updated: it should contain "The top button was clicked."

We've added only 3 lines (2 not counting the docstring).  Let's see what they do:

- We begin by creating a new method on the window, called `on_top`.  `on_` is the prefix of a control method, telling BUI that this method should be bound to a control.  `top` is the only remaining information.  BUI understands that we want to connect this control method to the action "the user clicks on the button of ID top".
- Inside the method, we call `self["report"]`.  This will return the widget with ID "report".  Looking at our layout, this is the text widget.  We update its value (the text it contains) using a simple property (`self["report"].value = "text to display"`).

We could link any other button in the same way.  For instance:

```python
from bui import Window, start

class Buttons(Window):

    """A buttons demonstration in BUI."""

    # Again, the layout is included here, but it's good practice
    # to write it in a separate file (buttons.bui in this case)
    layout = mark("""
      <window title="Button demonstration in BUI">
        <button x=2 y=1 id=top>Top button</button>
        <button x=0 y=3 id=left>Left button</button>
        <button x=5 y=3 id=right>Right button</button>
        <button x=2 y=5 id=bottom>Bottom button</button>
        <text x=2 y=3 id=report>Report</text>
      </window>
    """)

    def on_top(self):
        """The top button was clicked."""
        self["report"].value = "The top button was clicked."

    def on_left(self):
        """The left button was clicked."""
        self["report"].value = "The left button was clicked."

start(Buttons)
```

### Diving deeper inside control method binding

Let's examine in more details how BUI binds control methods to user actions.  We have seen that creating a method called `on_top` was enough to let BUI know we want to intercept user clicking on the button of ID "top".  But it seems to indicate we can only react to the click action, at least on buttons.  Fortunately, this is not true.

BUI has an interesting approach to binding user actions to control methods.  It examines the control method name and tries to infer information from there, with reason.  The more complete method name looks like this:

- `on_`: the prefix for a control method.
- `{control}`: the control type.
- `_`: another underscore.
- `{widget}`: the widget identifier.

What are controls?  You can think of them as user actions.  When the user clicks on the top button, BUI generates a "click" control and fires it on the "top" widget.  So the way to intercept the "click" control on the widget of ID "top" would be to create a method named `on_click_top`.  You can try with the same layout to bind to the right button:

```python
    def on_click_right(self):
        """The 'right' button was clicked."""
        self["report"].value = "The right button was clicked."
```

So then... `on_click_right` or `on_right` would do the same thing?  That's odd!

BUI will use a system of implicit controls on different widgets.  When a method `on_top` is created, BUI will realize "top" is a button.  What's more likely?  Bui will answer: "I guess we want to intercept the user clicking on the button".  So `on_top` and `on_click_top` would do the same thing.

> Using implicit controls might sound dangerous.  Better to specify the explicit control name each time.  But on some widgets, explicitly writing the control name doesn't make things easier to read in the end.  You will have to decide on which strategy to use given a specific context.

### Asynchronous control methods

In the previous example, the control method reacts directly to the control.  The action is not complete until the control method ends.  But BUI implements a neat feature to allow a control method to run longer without blocking the window.

Let's add a new method to see how it works:

```python
    async def on_bottom(self, widget):
        """The bottom button was clicked."""
        report = self["report"]
        report.value = (
                "Great!  Let's play hide-and-seek!  I'm counting, you hide!"
        )

        # Counting from 1 to 20 in 20 seconds
        for i in range(1, 21):
            widget.name = f"{i}"
            await self.sleep(1)

        report.value = "Are you hidden?  I'm coming!"
```

Run the window and click on the bottom button.  You will see some text being written to the report and then the button changes its name (label) from "Bottom button" to "1".  After a second, the button becomes "2".  And so on.  This doesn't freeze the window.  You can click on other buttons.  For that matter, you can click on the bottom button once more which will create two parallel loops and might give odd results (we'll see how to handle this in the next section).

For the time being, let's look at the code:

- First you have the `async` keyword in front of the method definition.  This has become a standard Python keyword to indicate the function (method in our case) is asynchronous (it can take awhile to process and its content shouldn't block the rest of the application).
- The method name is similar.  It obeys the same rules (we use `on_bottom` here, as shown above, we could have written `on_click_bottom` with the same result).
- We have an additional argument in the method, `widget`.  This is not specific to asynchronous methods.  It's just a shortcut (this argument will contain the button widget on which we clicked).  Control methods accept a wide range of arguments.
- We first get hold of the text (of ID "report").  This will be used several times in our method, no need to query for it each time.
- We update the content of the "report" widget.
- Next is a loop running 20 times.  Inside are only two actions:

   - First, we change the widget (the "bottom" button)'s name with a property.  This will update the button name (label) on the screen.
   - We then use the `await` keyword and pause for one second.  In the meantime, the window resume its normal activity (you can click on other things for instance).  After the second is over, the loop begins again...

- ... until we reach `i > 20`.  At this point we exit the loop, update the report one last time and the method ends.

Although light to use, this feature might not sound exactly necessary at first glance.  But consider, for instance, that you could download a file (like the software update) without freezing the rest of the application, without running the update in a separate thread or process (which makes updating so much easier).

### The init control

In the previous example, we have an asynchronous control method on which we can click several times while it's still running.  This leads to a lot of updates and confusing label changes.  Why, its counting 3, 4, then back to 1, then 6, then 2...  In this case, we would need to tell Python to not run the "hide-and-seek" counter if it's already running... and to wait for it to be over.

There are different options.  But a good way would be to store the state in a variable and avoid running the "hide-and-seek" counter if this state indicates "running".  It would be easier to store this data in the window object itself, so we can access it under `self` in our control method.  But we need to create this variable (this instance attribute) before the control runs.

The `init` control can be used for this very purpose.  It's called for every widget (including the window) when it's ready to be displayed, but before it's actually displayed.  You can think of `init` as somewhat equivalent to the `__init__` special method, although you shouldn't override the `__init__` special method in your window.

`init` is a control.  So we just need to create a method to intercept it.  Know how?

```python
    def on_init_bottom(self):
        """The bottom button is ready to be displayed, but isn't displayed yet."""
        self.hide_and_seek = False
```

So let's see a full example of how to use this feature:

```python
class Buttons(Window):

    """A buttons demonstration in BUI."""

    # ... layout and other controls

    def on_init_bottom(self):
        """The bottom button is ready to be displayed, but isn't displayed yet."""
        self.hide_and_seek = False

    async def on_bottom(self, widget):
        """The bottom button was clicked."""
        report = self["report"]
        if self.hide_and_seek:
            report.value = "I'm already counting, hurry up and hide!"
            return

        self.hide_and_seek = True
        report.value = "Great!  Let's play hide-and-seek!  I'm counting, you hide!"

        # Counting from 1 to 20 in 20 seconds
        for i in range(1, 21):
            widget.name = f"{i}"
            await self.sleep(1)

        report.value = "Are you hidden?  I'm coming!"
        self.hide_and_seek = False
```

The added code is really short.  If you run this and click on the bottom button, the hide-and-seek counter begins again.  But if you click on the same button again while the counter is running, the middle text will indicate the counter is already running and won't run it again.  All thanks to an instance attribute to keep the state!

## Conclusion

That was a first taste of BUI's abilities and simplicity, but of its flexibility too.  Flexibility comes to a price.  Although this document addresses some pitfalls, you might have trouble navigating in the word of layout and control by yourself.  But fortunately, there are more tutorials and even more documentation to help you.

- [Read the full documentation of the button tag](../layout/tag/button.md)
- [Learn more about controls](../control/overview.md)
- [A window with a menu bar](menubar.md)
- [Handling keyboard shortcuts](keyboard.md)
- [Checkboxes and radio buttons](choices.md)
- [Lists and tables](lists.md)
- [Dialogs](dialogs.md)
