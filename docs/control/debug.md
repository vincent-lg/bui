# Debugging controls

Controls and control methods are so easy to create... but this simplicity comes with a price: at times, it's hard to know if a control was successfully connected, that is, if it found a control method.  For instance, you might add a button and not realize the button is not connected to any method (BUI will not warn you about that, at least, if you don't ask it to).

But BUI offers you some command-line arguments you can use to debug the created window.  One of them is `-c` (short for `--debug-controls`).  If you give BUI this flag, it will display a lot of information on controls:

- Which controls are bound?  A bound control is one that can find a control method.  BUI will explain in details why this control binds to this control method.  It can depend on options.  Note that binding happens when the window is created, not when control fire.
- Which is fired:  When this option is active, BUI will show you in real-time what control is fired with whatever option.  If the control has been bound to a control method, it will also indicate it.

## Debugging all controls

First, let's see how to use the debug controls mode.  You can only use this debug mode from a Python script, not a frozen executable.  This is a security risk and you shouldn't let your users play with fire if you can avoid it.  To use, run Python giving your script name, and then the `-c` command-line argument.  Here is an example of output when running the [download.py](../example/download.py) script in the "example" folder with this mode set:

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

The generated output can be quite verbose.  When debugging a large window with a lot of widgets and controls, it's hard to properly debug in this way.  You can, however, use filters.

## Filtering controls to debug

The `-c` option can take one or several arguments, each being a filter.  A filter can indicate a control name, a widget identifier, or both:

    filter=widget identifier@control type

Still running the [download example](../example/download.md), you could want to only display [init](init.md) controls:

```
> python download.py -c @init
Running in 'debug controls' mode.
  Binding control methods...
    Bound init as a widget control of table(download) to the 'on_init_download' method
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

We specify a `@` symbol before the control type we want to watch.  We can also watch a given widget:

```
> python download.py -c add_file
Running in 'debug controls' mode.
  Binding control methods...
    Bound click as an implicit widget control of item(add_file) to the 'on_add_file' method
...
```

Widget identifiers are specified as-is.  Control types should begin with a `@` symbol.  We can also combine both:

```
> python download.py -c start@click
Running in 'debug controls' mode.
  Binding control methods...
    Bound click as an implicit widget control of button(start) to the 'on_start' method
...
```

This will only watch the [click](click.md) on the widget of ID "start".

Need even more?  You can specify several filters separated by a space.  One of them will have to be checked for the control to appear:

```
> python download.py -c @init @click
Running in 'debug controls' mode.
  Binding control methods...
    Bound click as an implicit widget control of item(add_file) to the 'on_add_file' method
    Bound click as an implicit widget control of item(quit) to the 'on_quit' method
    Bound init as a widget control of table(download) to the 'on_init_download' method
    Bound click as an implicit widget control of button(start) to the 'on_start' method
    Bound click as an implicit widget control of button(add) to the 'on_add' method
```

We watch two controls this time.  [click](click.md) and [init](init.md).  Of course, you can also watch several widgets, several widgets with specific controls, and so on.
