"""Init control, used on window and widgets to perform actions on init."""

from bui.control.base import Control

class Init(Control):

    """
    When the window or widget is initialized.

    Contrary to other controls, this one is automatically triggered by
    the Blind User Interface when the window has been built from a valid
    layout, but before the said window is displayed.  This allows to load
    default data, as some data cannot be assigned otherwise.

    ## Usage

    This control is automatically scheduled when the window is ready to be
    displayed, but before the window is actually displayed, unless the
    control method is asynchronous.  This allows to use automatic or
    programmatic sampling to fill data on some widgets (like
    [lists](../layout/tag/list.md) or [tables](../layout/tag/table.md).
    Since it is not possible to assign data on these widgets in layout
    (filling these objects is a task for the developers, not the designers),
    this control can be useful to set default data:

        def on_init(self):
            # The window initializes
            table = self["products"]
            table.rows = (
                    ("Pocket watch", "$15", 80),
                    ...
            )

    ### Window control

    This control can be linked to a window.  Simply specify a method
    called `on_init` in your [Window](../widget/Window.md)-inherited class.
    This method will be called when the window is ready to display, but
    before it actually does.

        class Example(Window):

            def on_init(self).
                pass

    ### Widget control

    You can also link this control to most widgets.  Include the widget
    identifier in the method name.  For instance, if your widget has an ID
    of "products", then to fill it when the widget is ready to be displayed:

        def on_init_products(self):
            pass

    This second method is considered a good practice, as a window control
    for initialization might not be as clear.  Furthermore, you can use
    the `widget` argument in such a method, which does make things easier:

        def on_init_procuts(self, widget):
            # the table products is ready to be displayed
            widget.rows = (
                    ( ... ),
            )

    ### Asynchronous calls

    This control can be bound to an asynchronous method (that is, a
    coroutine).  However, in order to avoid slowing down the display of
    the window, notice that using such a method doesn't guarantee the
    initialization will be called before the window is displayed, which
    might create some logical errors depending on what you want to achieve:

        async def on_init(self, ...):

    As usual, just place the `async` keyword before the method
    definition to make it asynchronous.  Although you won't have
    control over when the information will appear, you will be able
    to divide the task in different periods of time.

    An alternative is also possible: if you want to keep the method
    synchronous (that is, it will always be called before the window
    appears) but you wish to create an asynchronous coroutine in it,
    you can use `self.schedule` which takes a coroutine as argument:

        class Example(Window):

            def on_init(self):
                # Notice you don't define it with async this time.  This
                # method will be executed before the window appears.
                # ... some initialization might be required
                self.schedule(self.start_task)

            async def start_task(self):
                # Start one or more tasks asyncyronously
                # It is likely this method will first be called after the
                # window has appeared on the user screen, though it is not
                # possible to control its timing.
                await self.sleep(5)
                # ... and 5 seconds later, perhaps do something else?

    The important thing to note here is that the `on_init` method remains
    synchronous: it will be called **before** the window appears, even
    if the method blocks, the window will take longer to display.
    However, we schedule the `start_task` method to run.  This method
    has been defined by the developer and is asynchronous.  BUI will
    start it and call the method whenever possible (notice, you won't
    be in control of when it is called, chances are it will be called
    after the window appears, this time).

    ## Control attributes

    This control doesn't have any attribute.  Notice, as usual, you
    can use the `widget` argument in your control method, if this is a
    widget control:

        def on_init_products(self, widget):

    """

    name = "init"
    widgets = {
            "window": "A window is initialized.",
    }

    def perform(self, options=None):
        """
        When the control is triggered.

        This method will be called when the window is ready to display,
        but before it actually appears on the screen.

        """
        super().perform(options)
