"""Interactive console, supported for wxPython."""

import asyncio
import code
import queue
import sys
import threading
import trace

from bui.specific.wx4.thread import WX_THREAD

prompts = queue.Queue()

class AskUser(threading.Thread):

    def __init__(self, inputs):
        threading.Thread.__init__(self, daemon=True)
        self.inputs = inputs

    def run(self):
        self.thread_id = threading.current_thread().ident
        user_input = ""
        prompt = ">>> "
        while True:
            try:
                user_input = input(prompt)
            except (EOFError, KeyboardInterrupt):
                break

            asyncio.run_coroutine_threadsafe(self.inputs.put(user_input),
                    WX_THREAD.loop)
            prompt = prompts.get()

async def main():
    print("Begin")
    inputs = asyncio.Queue()
    user_input = ""
    window = WX_THREAD.window
    interactive = code.InteractiveConsole({"window": window})
    AskUser(inputs).start()
    prompt = ">>> "
    while user_input != "exit":
        user_input = await inputs.get()
        if interactive.push(user_input):
            prompt = "... "
        else:
            prompt = ">>> "

        prompts.put(prompt)

def interact():
    """Create a Python interactive console, communicating via async queue."""
    WX_THREAD.loop.create_task(main())
    print("Interactive...", WX_THREAD.loop)
