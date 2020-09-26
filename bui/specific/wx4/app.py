"""wx.App redefinied to support asynchronous operations.

This code has been inspired by wxasync (https://github.com/sirk390/wxasync).
It is modified to get some distance from wx in itself, although the App
object in this case sersves as a bridge between wxPython and asynchronous
code.  The latter is optionally used inside of controls (that is, the
user can define the control method to be asynchronous).

"""

import asyncio

import wx
from asyncio.events import get_event_loop
import asyncio
import platform

import wx

# Constants
IS_MAC = platform.system() == "Darwin"

class AsyncApp(wx.App):

    """
    wx.App redefined to allow asynchronous operations.

    Mainly override wx.App.MainLoop in order to run a (mostly) non-blocking
    version of it while still using the event loop provided by asyncio.

    """

    def __init__(self, top_window):
        self.loop = asyncio.get_event_loop()
        self.top_window = top_window
        self.top_windows = []
        self.exiting = False
        self.tasks = []
        super().__init__()

    async def MainLoop(self):
        """Asynchronous version of combined asyncio and wxPython event loops."""
        # inspired by https://github.com/wxWidgets/Phoenix/blob/master/samples/mainloop/mainloop.py
        evtloop = wx.GUIEventLoop()
        with wx.EventLoopActivator(evtloop):
            while any(self.top_windows) and not self.exiting:
                if IS_MAC:
                    # evtloop.Pending() just returns True on MacOs
                    evtloop.DispatchTimeout(0)
                else:
                    while evtloop.Pending():
                        evtloop.Dispatch()

                # We don't stop more than necessary, doing otherwise will create latency
                await asyncio.sleep(0.0000000000001)
                self.ProcessPendingEvents()
                evtloop.ProcessIdle()

            # At this point we just exit the main loop
            self.ExitMainLoop()

    def ExitMainLoop(self):
        self.exiting = True

    def StartAsync(self, coroutine):
        """
        Start the coroutine asynchronously.

        Args:
            coroutine (asynchronous funciton): the function to execute.

        Because we use the event loop to schedule the task, the task itself
        doesn't execute right away.  The task should avoid blocking
        calls, as this will slow the entire loop down.

        """
        task = self.loop.create_task(coroutine)
        task.add_done_callback(self.OnTaskCompleted)
        self.tasks.append(task)

    def OnTaskCompleted(self, task):
        """The task is ready (with an exception or a result)."""
        try:
            # This gathers completed callbacks (otherwise asyncio will show a warning)
            # Note: exceptions from callbacks raise here
            # we just let them bubble as there is nothing we can do at this point
            _res = task.result()
        except asyncio.CancelledError:
            # Cancelled because the window was destroyed, this is normal so ignore it
            pass
        self.tasks.remove(task)
