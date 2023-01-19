"""Contain the WXShared class."""

import asyncio
from collections import namedtuple
import threading

import wx
from pubsub import pub

from bui.control.base import NOT_SET
from bui.control.exceptions import StopControl
from bui.specific.wx4.constants import KEYMAP, CHARMAP
from bui.specific.wx4.log import logger
from bui.specific.wx4.thread import WX_THREAD, EVENT_COUNTER

class WXShared:

    """Mixin to share wx behavior, to be expected on all BUI widgets."""

    def watch_keyboard(self, wx_obj):
        """Bind to different wx events to watch the keyboard."""
        wx_obj.Bind(wx.EVT_KEY_DOWN, self._OnKeyDown)
        wx_obj.Bind(wx.EVT_CHAR, self._OnChar)
        wx_obj.Bind(wx.EVT_KEY_UP, self._OnKeyUp)

    def _OnKeyDown(self, e):
        """A key was pressed."""
        kwargs = self._get_control_args(e)
        self.process_control(e, "press", kwargs)

    def _OnChar(self, e):
        """A key was pressed leadng to a key type."""
        kwargs = {
                "unicode": chr(e.GetUnicodeKey()),
        }

        self.process_control(e, "type", kwargs)

    def _OnKeyUp(self, e):
        """A key was released."""
        kwargs = self._get_control_args(e)
        self.process_control(e, "release", kwargs)

    def _get_control_args(self, e):
        key_code = e.GetKeyCode()
        key = KEYMAP.get(key_code)

        if key is None:
            if key_code < 256:
                if key_code == 0:
                    key = "nul"
                elif key_code < 27:
                    key = f"ctrl{chr(key_code + 64)}"
                else:
                    key = chr(key_code)

                    key = CHARMAP.get(key, key)
            else:
                key = str(key_code)

        key = key.lower()

        # Add modifiers
        kwargs = {"raw_key": key}
        modified = ""
        modifiers = (
                (e.ControlDown(), "ctrl"),
                (e.AltDown(), "alt"),
                (e.ShiftDown(), "shift"),
        )

        for on, attr in modifiers:
            kwargs[attr] = on
            if on:
                if modified:
                    modified += "_"
                modified += attr

        if modified:
            if key:
                key = f"{modified}_{key}"
            else:
                key = modified

        kwargs["key"] = key
        return kwargs

    def process_control(self, e, control, options=None, close=False):
        """
        Process the control.

        This method can be called in the main thread or in
        the asynchrone thread.

        Args:
            e (wx.Event): the wxPython event.
            control (str): the control name to call.
            options (optional, dict): the control options.
            close (bool): if set to True, terminate the loop.

        If the generic widget is not subscribed to this control,
        look for the parent widget and so on.

        """
        event = next(EVENT_COUNTER)
        if WX_THREAD.in_queue:
            msg_post = f"Post event {event} ({e})"
            if threading.current_thread() is threading.main_thread():
                logger.debug(f"{msg_post}, redirect to async thread")
                WX_THREAD.loop.call_soon_threadsafe(
                        WX_THREAD.in_queue.put_nowait, (event,
                        self.process_control_in_thread, (control, options),
                        {}, close))
                if getattr(self, "wx_end", False):
                    rcv_event, status = WX_THREAD.out_queue.get()
                else:
                    rcv_event, status = event, True

                if rcv_event is None:
                    self.wx_end = True
            else:
                logger.debug(f"{msg_post}, already in async thread")
                rcv_event = event
                status = self.process_control_in_thread(event, control, options, close=close)

            logger.debug(f"  Received {rcv_event}-{event}, {status}, {e}")
            if rcv_event is None or (e and event == rcv_event and status):
                logger.debug("  Skip this event")
                e.Skip()

    def process_control_in_thread(self, event, control, options, close=False):
        logger.debug(f"  In async thread, process control {control} "
                f"from event {event} with options {options}")
        widget = self
        options = options or {}
        callback = close_loop if close else None
        while widget:
            try:
                result = widget.generic._process_control(control, options, callback)
            except StopControl:
                logger.debug("  This control was cancelled.")
                return False

            if result is NOT_SET:
                widget = widget.parent
                if widget is None:
                    break
            else:
                break

        return True

    def in_main_thread(self, callback, *args, **kwargs):
        """
        Call the specified callback in the main thread.

        This is useful, since the asyncio event loop runs in a separate
        thread.  It needs to call methods in the main thread where the
        wxPython event loop sits.

        Args:
            callable (Callable): any callable.

        Anu arguments or keyword arguments is supported.

        """
        wx.CallAfter(pub.sendMessage, "callable", callback=callback,
                args=args, kwargs=kwargs)

    def in_async_thread(self, callback, *args):
        """
        Schedule an asynchronous task to run in the asynchronous thread.

        Args:
            callback (callable): the callback.

        Additional positional arguments can be used.

        """
        loop = WX_THREAD.loop
        loop.call_soon_threadsafe(self._in_async_thread, callback, *args)

    def _in_async_thread(self, callback, *args):
        callback(*args)


def close_loop(task):
    WX_THREAD.close_event.set()
