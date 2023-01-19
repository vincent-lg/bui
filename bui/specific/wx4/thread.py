"""Thread for wxPython, containing the asyncio event loop."""

import asyncio
import inspect
from itertools import count
import platform
from queue import LifoQueue
import threading

EVENT_COUNTER = count()

class WXThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop = None
        self.in_queue = None
        self.out_queue = None
        self.do_not_listen = False
        self.close_event = None

    def run(self):
        """Start in a new thread."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.main_loop())

    async def main_loop(self):
        """Main loop."""
        self.loop = asyncio.get_event_loop()
        self.close_event = asyncio.Event()
        self.in_queue = asyncio.Queue()
        self.out_queue = LifoQueue()

        try:
            await self.process_all_events()
        except asyncio.CancelledError:
            pass

        await self.close_event.wait()

    async def process_all_events(self):
        event = ...
        while not event is None:
            event, callable, args, kwargs, close = await self.in_queue.get()
            if event is None:
                break

            args = args or ()
            kwargs = kwargs or {}
            kwargs["close"] = close
            if inspect.iscoroutine(callable):
                task = asyncio.create_task(coroutine)
                if event is not None:
                    self.out_queue.put_nowait((event, False))
            else:
                res = callable(event, *args, **kwargs)
                if event is not None:
                    self.out_queue.put_nowait((event, res))


WX_THREAD = WXThread()
