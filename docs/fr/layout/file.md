# Layout in files

BUI recommends to always place the layout in an external file.  This will be easier for maintenance, especially if you work with designers who are not thrilled about understanding your code, but are really good at designing windows in a simple way.  Keeping the layout and code separate makes for happier teams.  Even alone, it will help you design and code as two steps instead of mixing everything in your beautiful Python scripts.  If you don't mind doing that, however, you can still write both layout and code in the same file, including your [layout in code](./code.md).

## An entire window

Most often, when you design a window, you place the layout in a separate file.  This file, by convention, is located at the same place as your Python script, and has the same name.  Instead of having a `.py` extension, however, it has a `.bui` extension.  Thus, you could have in your project something like this:

```
project/
        main.py
        main.bui
```

The `.py` file only contains your [Window](../class/Window.md) class along with your [control methods](../controloverview.md).  In the `main.bui` file, however, you only find the layout.  Therefore, the `main.bui` file could contain something like this:

```
<window>
  <button x=3 y=3 name="Center" />
</window>
```

This is, obviously, a short and minimalist example.  Most of the times, your `.bui` files might be much bigger.  This is another good reason for separating the layout from the rest, as it is not clearly code, just design.  This will also make your `.py` file much lighter in the end.

BUI will try to identify the layout of a [Window](../class/Window.md) class using the name of the file in which it is defined.  If the `layout` class attribute is not defined, it will assume the window layout lives in a file at the same location, with the same name except the `.py` extension is replaced by a `.bui` extension.

You can change all this however.  In your [Window](../class/Window.md) class, you can define the `bui` class attribute.  This should contain the absolute or relative path leading to the `.bui` file describing the window:

```python
from bui import Window

class MainWindow(Window):

    """Main window."""

    bui = "path/to/file.bui"
```

> Note: the path is relative to the location of the Python file containing the [Window](../class/Window.md) class.  You can also specify an absolute path (with a leadining slash).  In this case, the root is considered to be the current directory when the Python script is calle:

```python
class MainWindow(Window):

    """Main window."""

    bui = "/layout/main.bui"
```

The "layout" folder will be searched in the current directory.  Both notations are not identical, as the Python script containing the [Window](../class/Window.md) file may be in a different folder than the current directory.

## A dialog

BUI will follow the exact same steps to build dialogs.  In most cases, dialogs are really simple and do not deserve their own layout.  If, however, you want to change the default layout of a dialog, or want to create a more "complicated" and powerful one, you can use the [Dialog](../class/Dialog.md) class.  Again, the dialog layout will be sought in the same directory as the Python file containing the [Dialog](../class/Dialog.md) class.  You can override this behavior by setting the `bui` class attribute in the [Dialog](../class/Dialog.md) class:

```python
from bui import Dialog

class CustomDialog(Dialog):

    """Custom dialog, asking for somet extra information."""

    bui = "/layout/dialog/custom.bui"
```
