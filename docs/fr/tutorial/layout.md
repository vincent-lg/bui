# BUI layout

As explained in the [previous tutorial](structure.md), BUI layout is meant to be independent from the code.  It is hoped that the layout will be maintained by designers that can use it with no programming background, while the user actions are implemented by developers through code.  This tutorial will elaborate on the layout: how to write it, its syntax of tags and attributes and its basic representation.

## Where to write it?

BUI layout can be defined [in code](../layout/code.md).  Most examples in this documentation will actually do so, in order to be self-contained.  But layout can (and should) be written in a separate file: a `.bui` file with the same name as the Python file containing the `Window` class.

So to use the [basic example](../example/basic.md), let's see how that would work:

1. Create a file, named `basic.bui`.  Open it with a standard editor (like notepad++ or Vim) and write the layout in it:

   ```
   <window title="A BUI demonstration">
     <menubar>
       <menu name=File>
         <item>What is it?</item>
         <item>Quit</item>
       </menu>
     </menubar>

     <button x=2 y=2>Click me!</button>
     <text x=3 y=3 id=report>Report</text>
   </window>
   ```

2. Create a file in the same folder, named `basic.py`.  In it write the Python code:

   ```python
   from bui import Window, start

   class HelloBUI(Window):

       """Class to represent a basic hello world window."""

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

3. Execute this script with Python:

       python basic.py

It should display the [basic example window](../example/basic.md).  The advantage here is that we've separated layout and code: the layout is in a file by itself, a file designers can edit without worrying about the code, while the code only contains Python, not the BUI layout.

## Syntax of the BUI layout

The BUI layout is not defined in Python code.  It uses a kind of HTML syntax that might seem familiar to some but strange to others.  This section describes in more details the syntax of the BUI layout.  If what you've written in `basic.bui` seems obvious, you might skip this section.

### Tags

Tags are the basic elements of the BUI layout.  They are placed between a less than sign (`<`) and a greater than sign (`>`).  More specifically, their name starts just after an opening less than sign (`<`).

For instance, consider the first line of the layout:

    <window title="A BUI demonstration">

In this context, the tag is `window`.  It's the first word after the opening less than sign (`<`).

Or on the next line:

    <menubar>

`menubar` is the tag.  This time, the closing greater than sign (`>`) follows the tag name.  We'll see why when we talk about attributes.

#### Opening and closing tags

This syntax defines an opening tag.  A less than sign (`<`), the tag name, optionally a space and some information, then a greater than sign (`>`).  But there's another syntax to close the tag: a less than sign (`<`), a slash (`/`), the tag name, and the greater than sign (`>`).

So the `menubar` tag begins at line 2:

    <menubar>

And it ends at line 7:

    </menubar>

What are between the opening and closing tags are sub-tags.  This allows to create a simple or complex hierarchy.  Let's elaborate on this.

The `menubar` tag opens inside the `window` tag.  Look at these lines:

    <window title="A BUI demonstration">
      <menubar>

The `window` tag is not closed, the `menubar` tag opens inside of it.  Actually if you look at this layout, you will notice that the `window` tag is not closed before the very last line.  So everything else is contained inside the `window` tag.  Let's see what is contained inside the `menubar`:

      <menubar>
        <menu name=File>
          <item>What is it?</item>
          <item>Quit</item>
        </menu>
      </menubar>

The `menu` tag is defined inside of the `menubar`.  What about the `item` tags?  They are defined inside the `menu` tag.  There are two items in the `menu`:

              <item>What is it?</item>
              <item>Quit</item>

For these tags, you'll notice that we close them right away, so they don't contain other tags.

This hierarchy is important.  All tags cannot be defined anywhere.  BUI will warn you if the layout is not correct.  Contrary to HTML, the syntax has to be correct and consistent: don't open a tag you don't close, close the tags in the same order that you opened them, sub-tags have to be specified in correct parent tags.

So the first lines define a menu bar.  What about the last?  Try to guess which tag is the parent of `<button>`.

If you've guessed `<window>`, you are correct.  The `<button>` tag is defined after the `menubar` tag has been closed.

> Indentation allows to better understand the hierarchy of opening and closing tags.  This indentation, contrary to Python, is not mandatory, but it will help you distinguish the window structure and help you avoid opening tags and forget to close them when the time comes.

### Tag attributes

Tags can have different attributes.  Attributes are defined after the tag name, between the less than sign and greater than sign.  A space separates them from the tag name and each other (a tag may have several attributes).  Attributes are used to give more information about the tag.  For instance:

        <menu name=File>

We say that the `menu` tag has an attribute `name` of value `File`.

Let's see another example:

      <text x=3 y=3 id=report>Report</text>

The `text` tag has three attributes: `x`, `y` and `id`, each with its own value.  Another example?

    <window title="A BUI demonstration">

The `window` tag has only one attribute: `title`.  Notice that we surround the title with double quotes (`"`).  This is due to the fact that the window title spans on multiple words (it contains spaces).  If we omit the double quotes, BUI will not be able to know where the attribute name beings and where the value ends.

> In HTML, you will almost always find double quotes around attribute values, even if the attribute value is contained in a single word.  This is not mandatory but you can follow this convention if you're confused about when to use double quotes and when not to.  This doesn't change anything for BUI:

        <menu name=File>

Is strictly equivalent to:

        <menu name="File">

So if you want to add double quotes around all attribute values, you can.

#### Mandatory or optional attributes

Some attributes are mandatory, some optional.  BUI will help you determine which is which.  First of all, when you use a tag, check its documentation: BUI provides extensive documentation on each tag.  For instance, you see the `button` tag.  Just head over to the [button tag documentation](../layout/tag/button.md).  There's a section on tag attributes with a table.  For each attribute, the fact that the attribute is mandatory or optional is clearly stated.

For instance, if you read the [button attributes](../layout/tag/button.md#attributes), you will see that only `x` and `y` are mandatory, so you can't define a button without placing it on the window (which is somewhat logical).  If you try and remove one of these attributes, BUI will warn you about it and won't display the window at all.

On the other hand, if you head over to [the text tag attributes](../layout/tag/text.md#attributes), you will see that `id` is not mandatory.  That doesn't mean we cannot use it in our layout, just we don't have to:

      <text x=3 y=3 id=report>Report</text>

#### Attributes with no value

Some attributes don't require a value.  Their presence is enough to know what to do.  Specify the attribute name, but no equal sign or value is necessary after that.  Again, checking the [text tag attributes](../layout/tag/text.md#attributes), you should see the `multiline` attribute:

> `multiline`: if present, set the text on multiple lines.

This attribute doesn't require a value.  If it's present the text can contain several lines.  If not it's a single line widget.  To set our `report` text as a multiline text widget in your `basic` layout, we could do something like:

      <text x=3 y=3 id=report multiline>Report</text>

Attributes with no value are traditionally written after the others.  This is absolutely not required but it might help others read your layout.

For each attribute you will see a brief example of how to use it.  Don't dismiss this example as it might give you more information on how to use the attribute in context.

### Tag data

Finally, a last element about tags: their data.  Tag data is written outside the less than and greater than sign, between the opening and closing tag:

          <item>What is it?</item>

Here, "What is it?" is the data of the `item` tag.

The tag data is a kind of attribute in some ways (it is actually documented as such): it has different meanings for various tags and some tags don't require data at all.  Inside [the item tag](../layout/tag/item.md), data should contain the menu item name.  It cannot be omitted.  if not present, BUI will generate an error.

Tag data don't require quotation marks even if they span on several words.  The next less than sign (`<`) is just expected to be the end of the data.

As a rule, tags that contain sub-tags will not often have data.  Although the syntax would be understandable, it might not be so obvious, so that tags with data usually don't expect sub-tags of their own.

## The window as a grid

BUI defines the window as a simple grid on which you can place widgets.  This concept is extremely important for the layout.  You might have noticed each widget needs to be placed on the window with `x` and `y` attributes.  So let's see what it is:

By default, when BUI creates a window, it generates an invisible grid of 6 by 6.  `x` is the number of columns on this grid (starting from 0) and `y` is the number of rows on this grid (starting from 0 too).  The widget at `x=0`  `y=0` is positioned in the top-left corner of the window.  With a grid of 6 by 6 (the default), the widget placed on `x=5` `y=5` is in the bottom-right corner of the window.  `x=0` `y=5` is in the bottom-left corner, `x=5` `y=0` is in the top-right corner.  From there you can decide to place widgets on the grid with accuracy.

A widget can use several columns and/or rows on this grid.  For instance, if you want to have a big text field taking 2 columns and 3 rows of this window, you could do something like this:

    <text x=2 y=1 width=2 height=3 multiline>...</text>

`width` and `height` are optional attributes.  They indicate how much you want to span this widget horizontally and vertically.  So in this case, the upper-left corner of the text area is `x=2` `y=1`, but the widget spans two columns and three rows.  So its upper-right corner is `x=3` `y=1`.  Its bottom-left corner is `x=2` `y=4` and its bottom-right corner is `x=3` `y=4`.

This might need some getting-used to.  Describing the layout in this way is flexible and easy to extend, and not too complicated.  If you have to, draw a simple grid on paper with 6 columns and 6 rows and place your widgets in them, knowing that they can span in either (or both) directions.

## Widget identifiers

A last concept on widget should be understood before going to the next section.  Widgets can have identifiers (specified in the `id` attribute of the widget tag).  This identifier will help retrieve the widget in code.

      <text x=3 y=3 id=report>Report</text>

This text widget has an identifier of `report`.

Identifiers should be unique: no two widgets should have the same one.  In some cases, BUI will infer the identifier if you don't specify it.  This might be useful for some widgets (menu items or buttons, for instance), but this might lead to unexpected situations too.  And some widgets don't require identifiers anyway.

> How to know when to use identifiers and when not to?

The first thing is to read the tag documentation.  It provides some examples and usually explains why the `id` attribute is necessary, why it is not, or why it could be inferred by BUI if it's missing.  If you are a designer, however, the rule of thumb is to place clear identifiers on widgets the user will happen to interact with (buttons, tables, radio buttons...).

## What's next?

Now that you have a greater understanding of the BUI layout, it will be easier to play around with real windows.  The next tutorials show a greater range of examples of various widgets in various conditions.  If you are a window designer, not much interested in the Python code, you might only read the first section of each tutorial (which describes the layout).  The next section (describing control methods) is more a developer thing.  If you are a developer, however, you might want to read each tutorial, or at least, follow the ones you are interested in.

- [Using buttons](buttons.md)
- [A window with a menu bar](menubar.md)
- [Handling keyboard shortcuts](keyboard.md)
- [Checkboxes and radio buttons](choices.md)
- [Lists and tables](lists.md)
- [Dialogs](dialogs.md)
