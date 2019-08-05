"""The Dialog class.

A dialog is in a lot of ways similar to a window.  It also has control
methods and can use various widgets.  A dialog is popeed from a window.

"""

from bui.widget.window import Window

class Dialog(Window):

    """
    The Dialog main class.

    A Dialog is similar to a Window, in that it can contain various
    widgets and control methods.  A dialog is popped from a
    window, however.

    """

    widget = "dialog"
    class_name = "Dialog"

    def __init__(self, leaf):
        super().__init__(leaf)
        self.set = None

    def __bool__(self):
        return bool(self.set)
