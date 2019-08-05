"""Close control, used on window and dialogs to perform actions when closed."""

from bui.control.base import Control

class Close(Control):

    """
    When the window or dialog is closed.

    Contrary to other controls, this one is automatically triggered by
    the Blind User Interface when the window is ready to be closed (that
    is, just before BUI stops itself), but before it actually closes
    it.  Cleaning up is possible at this point.  It is also possible
    to set this control on a dialog, to perform action when the
    dialog is closed.

    ## Usage

    This control is automatically scheduled when the window is ready to be
    closed, but before the window is actually destroyed, unless the
    control method is asynchronous.  Although less used than [init](init.md),
    this control can be useful to perform clean-up tasks before the
    window is closed, in response to user action or code.

        def on_close(self):
            # The window closes
            self.stop_it_all()

    ### Window control

    This control can be linked to a window.  Simply specify a method
    called `on_close` in your [Window](../widget/Window.md)-inherited class.
    This method will be called when the window is ready to close, but
    before it actually does.

        class Example(Window):

            def on_close(self):
                pass

    Also notice that placing such a control on a dialog class is possible.
    This allows to set some consistent behavior on a dialog when it closes.

    ### Widget control

    You cannot use this control on a widget.  A text or checkbox doesn't
    close and get a chance to clean itself up.  These tasks should be
    performed in the window itself.

    ### Asynchronous calls

    This control can be bound to an asynchronous method (that is, a
    coroutine).  However, notice that using such a method doesn't
    guarantee the method will be called before the window is destroyed, which
    might create some logical errors depending on what you want to achieve:

        async def on_close(self, ...):

    As usual, just place the `async` keyword before the method
    definition to make it asynchronous.  Although you won't have
    control over when the window is destroyed, you will be able
    to divide the task in different periods of time.

    ## Control attributes

    This control doesn't have any attribute.

        def on_close(self, control):

    """

    name = "close"
    widgets = {
            "window": "A window is closed.",
    }
    widget_control = False

    def perform(self, options=None):
        """
        When the control is triggered.

        This method will be called when the window is ready to be closed,
        but before it actually is destroys.

        """
        super().perform(options)
