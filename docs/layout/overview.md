# Layout overview

Blind user Interface separates three important feature of any GUI toolkit:

- [Layout](./overview.md): the window design (or how it should appear at the screen) is clearly separated from the rest, in particular from the code.  Although it is possible, programtically, to create [dynamic layouts](./dynamic.md) on the fly, the task of designing it often better done in virtual isolation from the rest, by people who are better at designing.
- [Data model](../data/overview.md): the way to give data to the window, for instance, to display a list of information.  This is more a developer's job, but designers are required to understand the process in simple terms and describe the data flow their individual graphical elements could receive.
- [Control](../control/overview.md): controls are the handling of direct or indirect user actions.  They can be compared to events in most other toolkits and behave in a very similar manner.

This documentation and the related documents concern the layout philosophy and syntax.  This can be used by developers and designers alike.

## Basic principle

BUI is designed to strongly separate the layout from anything else.  Window layout can be described in [code](./code.md), but it is recommended to always keep it in a separate [file](./file.md).

The way to describe the window is a simple HTML-based layout language.  This type of language is easy to read and understand and doesn't require programming background to work with.  Here is a very short example of syntax:

```
<window>
    <button x=1 y=2 name="OK" />
    <button x=4 y=2 name="Cancel" />
</window>
```

This will create a window with only two buttons: OK and cancel, on the third line of the grid with some space left between them.

As you can see, the first step in our case is to defined a [window](./markup/window.md) markup.  This window will contain a grid that will use all the available space on the user screen.  By default, this grid has 6 rows and 6 columns, so that you have 36 available spots to use.  You can change the size of the grid (see the [window](./markup/window.md) markup for details).

Inside of this markup are all widgets (graphical elements) that should be displayed on the screen.  These widgets can be [buttons](./markup/button.md), [checkboxes](./markup/checkboxes.md), [text areas](./markup/text.md) and many others.  Each widget has to be positioned on the grid.

Widget positioning is handled by giving a `x` and `y` coordinate to the widget.  The top-left corner of the window is defined by `x=0` and `y=0`.  `x` will allow you to place the widget in a specific column (between `0` and the length of the grid `-1`) and `y` will allow you to place the widget in a specific row of the grid (from `0` to the height of the grid `-1`).

The default grid is 6 in width and 6 in height.  Therefore, each widget can be placed between rows `x=0` and `x=5`, and between row `y=0` and `y=5`.

> This 6/6 grid has been choosen because 6 can be divided by 2 and 3, making designing somewhat simple.  You can change this size very easily however.

**Important note**: the window height and width, as well as widget positioning using `x` and `y`, is relative to the grid.  It's not a size in pixels or inches or centimeters or a real unit.  This system is in part useful because you don't have to know how big the user screen will be to display a proper user interface.

> Need more customization?  If you have many widgets or you wish to lace them with greater accuracy, consider increasing the grid.  This will give you more "cells" to work with.

## Widget spanning

Positioning everything on a grid, with each widget in its cell, would make for small widgets that might be very hard to read.  BUI will try to guess a real size (in pixels) based on the user screen and the available room in the grid.  However, it is useful to indicate that a widget should display on 3 rows, or take 2 columns.  To do so, use the `width` and `height` attributes of every widget:

```
<window>
  <list x=0 y=0 width=2 height=3 />
  <button x=0 y=5 width=2 name="Submit" />
</window>
```

This will create a window with a list going from `x=0 y=0` (top-left) to `x=2 y=3`.  In other words, our list will take most of the screen, mainly the left portion of it.  Some room will still be available below and to the right of it.

Just after that is a button definition.  It will go from `x=0 y=5` (bottom-left corner) to `x=2 y=5`.  This button will "stretch" a bit on the right so it would be almost as wide as the list, though its height is still 1 since it hasn't been changed by the `height` property.

## Layout definition

There are a few ways to generate a window from the larmkup language shown above.  The recommended way is to keep this markup definition in a separate file, with the `.bui` extension, having the same name as the Python file.  All that is customisable.  If your team includes developers and designers, or even if you're alone on the project as the only developer, strongly consider keeping the layout in a separate [file](./file.md).  On creating the window, BUI will realize the layout is not present and will attempt to find it (you can help it if needed).

However, you can also write the layout in the [code](./code.md) itself.  Although this is not recommended, separating design and controls might not always be necessary and this does simplify some workflows.  It all depends on how you work, or intend on working.

Additionally, you have the option to generate layout [dynamically](./dynamic.md).  This often happens if, for instance, the user clicks on a button and you want to show a dialog.  Again, when this happens, you are encouraged to keep the dialog layout in a separate [file](./file.md), but you can also keep the layout in a Python str and ask BUI to render it.  What you will choose strongly depends on how you work.

## Layout description

The examples above show that the layout should contain at least a [window](./markup/window.md) markup, containing all widgets (graphical elements).  In fact, a layout can contain several other things:

- [menubar](./markup/menubar.md): the menu bar of this window, if any.  You don't have to specify this markup if your window doesn't contain any menu bar.
- [toolbar](./marku/toolbar.md): on the same principle, you can also define a tool bar in your window.  This is not mandatory.  You can define a menu bar, a tool bar, both or none of them.
- [window](./markup/window.md): the window layout containing what to display on the screen.  The [window](./markup/window.md) defines a rectangular grid where you can position your widgets (graphical elements).  As long as you have room in your grid, you can place any widget you like.  If BUI cannot display your window because the grid definition is incorrect, it will explain to you why and, hopefully, how to fix this error.

Usually we follow this order to define a window layout:

1. First, if applicable, the [menubar](./markup/menubar.md) definition.  You should leave a blank line between it and the rest, for clarity, though that's far from mandatory.
2. Next, if applicable, the [toolbar](./markup/toolbar.md) definition.  Again, if you have a toolbar, it might be good to add a blank line after its definition.
3. Finally, the [window](/markup/window.md) definition.  This is probably where you will spend most time in terms of layout.  Contrary to [menubar](./markup/menubar.md) and [toolbar](./markup/toolbar.md), the [window](./markup/window.md) definition is mandatory in every window or dialog.

> To learn more about a widget (graphical element) and see examples on how to use it, refer to its documentation.

- [List of graphical elements](./markup/index.html)
- [Back to the main documentation](../index.md)
