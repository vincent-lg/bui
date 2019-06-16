# Data overview

Data flows are extremely important in any user interface.  BUI separates these data flows in an obvious, Pythonic approach, while linking them to [layout](../layout/overview.md) and [controls](../layout/controls.md).  Thus, data flows are not only accessible through code or through layout, but can be used from both sides.

## Through layout

When creatin a `.bui` file containing the [window layout](../layout/overview.md), a designer can place default data in this layout.  This defaut data will only appear to debug the produced window and will allow to "see what the window would display" without writing any code.  This feature will be used mostly by designers (developers will feed the individual widget in Python code, see the next section for details).

Test data flows can be written in the layout by itself, using a rootless `<data>` tag.  Inside of this tag will be a list of widgets you can to feed, and inside of each widget, the data flows you would send to them.  Here's an example in BUI layout format:

```
<window>
  <list id=choices x=2 y=2 />
</window>

<data>
  <flow id="choices">
    <items>
      Choice 1
      Choice 2
      Choice 3
      Choice 48
    </items>
  </flow>
</data>
```

The important tag here is `<data>`. Best to write it below the window layout, as this syntax is only for testing.  Inside this `<data>` tag are `<flow>` sub-tag, one `<flow>` tag per widget to feed.  In this example, we feed only one widget: the one with ID `choices` (that is, our list, defined in the `<window>` tag).

Inside the `<flow>` tag we have sub-tags depending on the type of widget to feed.  Here, `choices` is a list, so it has the attribute `items`.  We create an `<items>` tag and place the choices in this list, with one choice on each line.  When we generated this window in test mode, not only do we see the list, but it has been filled with the various choices we have provided.

> How is that useful?  The main interest is to be able to add data so designers can "see" what their window would look like, but don't need to write a single line of code to actually see this window in action.  Of course, in the end, developers will have to write the correct [controls](../control/overview.md) and see how they can fee data in the application.

## Through code

Developers can easily feed data to their widget through [control methods](../control/overview.md|Control-methods).  The resulting code is easy to understand but let's look at it in more details:

```python
class Example(Window):

    """
    A BUI window, to show how control methods can fee data to widgets.

    We assume the following layout:
      <window>
        <button x=2 y=3 name="Click me" />
      </window>

    """

    def on_click_me(self, widget):
        """This method is called when the 'click_me' button is clicked."""
        widget.name = "I was clicked, at least once."
```

One property of [control methods](../control/overview.md#Control-methods) is that they can receive additional arguments.  `widget` is one of them.  When the `on_click_me` method is called, `widget` will contain the generic button on which the user just clicked.

> A [generic button](../class/Button.md) is created from a [button](../layout/tag/button.md) tag in the layout.  These are two different objects, created from different classes.

So `widget` contains a [Button](../class/Button.md) object.  This object has several properties and methods, one of them is `name`.  So calling `widget.name = ...` in our example will transmit the new name to the actual button class used by BUI to represent your window.  In other words, this simple code will update the button name (or its label, if you wish, as both things are similar in BUI).

How does it link to data flows?  The generic widget properties and methods are part of the data flow.  So in formal terms, when we do this:

    widget.name = "I was clicked, at least once."

... we feed "I was clicked, at least once." to the generic button's `name` property.

Generic widgets have properties and methods to interact with them, they are documented both in the widget tag (in layout) and in the generic widget (in code) since they can be used in both contexts.

> Of course, you can read and write most properties.  We have written in the button's `name` property, but we can read it also, with `widget.name`.  Sometimes, propertiescan be read but not set, this is described and explained in the documentation page of this tag or class.

Methods, on the other hand, allow for some operations that would look strange with simple properties.  Let's take the same example with our button:

```python
class Example(Window):

    """
    A BUI window, to show how control methods can fee data to widgets.

    We assume the following layout:
      <window>
        <button x=2 y=3 name="Click me" />
      </window>

    """

    def on_click_me(self, widget):
        """This method is called when the 'click_me' button is clicked."""
        widget.name = "I was clicked, at least once."
        widget.disable()
```

`disable()` is a method on the generic button that will force the button to be marked as disabled (further clicks on it won't work).  Having a property to do this, like `widget.disable = True` would make things harder to read in Python code.  Again, these methods are listed in the tag or class documentation.

