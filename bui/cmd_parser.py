"""Command-line argument parser for BUI.

This module contains the argument paser for BUI, which is active by default
if the BUI window is running as a Python script.  However, if it is frozen
(with PyInstaller or such), it will be inaccessible by default.  To enable
or disable it, look at the `start` function defined in the BUI tools
(see tools.py).

"""

import argparse
import asyncio
import code
import queue
import threading

def parse_args(window, loop):
    """
    Parse command-line arguments.

    Args:
        window (Window): the BUI window.
        loop (asyncio Loop): the event loop.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interactive", action="store_true",
            help="Start an interactive Python interpreeter in the console, "
            "won't block the BUI window.")

    inputs = asyncio.Queue()
    prompts = queue.Queue()

    def threaded():
        user_input = ""
        prompt = ">>> "
        while user_input != "exit":
            try:
                user_input = input(prompt)
            except EOFError:
                user_input = "exit"

            asyncio.run_coroutine_threadsafe(inputs.put(user_input), loop)
            prompt = prompts.get()

    async def main():
        user_input = ""
        interactive = code.InteractiveConsole({"window": window})
        prompt = ">>> "
        while user_input != "exit":
            user_input = await inputs.get()
            if interactive.push(user_input):
                prompt = "... "
            else:
                prompt = ">>> "

            prompts.put(prompt)

    args = parser.parse_args()
    if args.interactive:
        print("Interactive...")
        threading.Thread(target=threaded).start()
        loop.create_task(main())
