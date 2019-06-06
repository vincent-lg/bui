# Markup: window

The window markup is the only one that is truly mandatory in your [layout](../overview.md).  It is used to describe both a window and dialog.  It will contain all your widgets (graphical elements).

```
<window>
  ...
</window>
```

## Attributes

| Name         | Required | Description | Meaning |
| ------------ | -------- | ----------- | ------- |
| `rows`       | No       | The number of rows in the window grid. Default is `6`. | `<window rows=10>` |
| `cols`       | No       | The number of columns in the window grid. Default is `6`. | `<window cols=5>` |
| `title`      | No       | The window or dialog title.  If not set, a default title will be sought. | `<window title="User Interface">` |

Although no attribute is mandatory, you will msot likely provide a title attribute at least.  Having a window or dialog without a custom title will bother BUI to some extent.  it will try to come up with a name, but chances are it won't be what you want.

> `title` is a translatable attribute.  if internation[alization is set, it should contain the ytranslate path to the title and will be translated in the proper language as needed.

The `rows` and `cols` attributes are used to set the window grid.  You can think of them as the height (in rows) and width (in columns) of the grid.  Changing this value won't make the window any bigger, but it will give you more control on how to place the widget in the window itself.  On the other hand, having a large grid can make designing not so easy.  It all depends on your needs.

> Note: you don't have to set the same number of rows and columns.  This is just the default value.  You can set different values with no trap:

```
<window cols=1 rows=8>
```

This will set a window with only one column, but 8 rows.  If you place a widget in `x=0 y=0`, it will take all the window's width.  Again, this doesn't change the window size in any way, just the way widgets are placed on it.  You can picture the window to always be a square but sliced in different portions (squares or rectangles, more or less big depending on the height and width you set in the window markup).

## Data

A window is a specific graphical element since it only contains other elements and has no meaning by itself.  Therefore, you cannot send it data, it wouldn't make much sense.  Instead, you should send data to the window's graphical elements themselves.

## Controls

The window markup is tied to the [Window](../../class/Window.md) or [Dialog](../../class/Dialog.md) class.  Therefore, when you write controls on either of these classes, you often want to catch controls on indidivual graphical elements in the window.  There are a few exceptions however:

| Control                            | Method         | Description      |
| ---------------------------------- | -------------- | ---------------- |
| [focus](../../control/focus.md)    | `on_focus`     | The window is focused or lose focus.  This usually happens for a top window when the user switches the current application for instance. |

Notice that we don't specify the window identifier.  It would make no sense here.  Therefore, to use this event, you should just add a method in the window class with the control name and no identifier:

```
class MainWindow(Window):

    """Main window designed in main.bui."""

    def on_focus(self):
        """The window loses or gains focus."""
        print(f"Am I focused? {'yes' if self.focused else 'no'}")
```

