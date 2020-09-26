"""Thread for wxPython, containing the asyncio event loop."""

import asyncio
import inspect
from itertools import count
from queue import LifoQueue
import threading

EVENT_COUNTER = count()

class WXThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop = None
        self.in_queue = None
        self.out_queue = None

    def run(self):
        """Start in a new thread."""
        asyncio.run(self.main_loop())

    async def main_loop(self):
        """Main loop."""
        self.loop = asyncio.get_event_loop()
        self.in_queue = asyncio.Queue()
        self.out_queue = LifoQueue()
        try:
            await self.process_all_events()
        except asyncio.CancelledError:
            pass

    async def process_all_events(self):
        while True:
            event, callable, args, kwargs = await self.in_queue.get()
            args = args or ()
            kwargs = kwargs or {}
            if inspect.iscoroutine(callable):
                asyncio.create_task(coroutine)
                if event is not None:
                    self.out_queue.put_nowait((event, False))
            else:
                res = callable(event, *args, **kwargs)
                if event is not None:
                    self.out_queue.put_nowait((event, res))

WX_THREAD = WXThread()
