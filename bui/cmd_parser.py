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

from bui.control import log as control_log
from bui.widget.window import Window

def init_args():
    """
    Initialize the command parser, parse and return.

    This function can also be used to run operations before the window
    is actually created.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interactive", action="store_true",
            help="Start an interactive Python interpreeter in the console, "
            "won't block the BUI window.")
    parser.add_argument("-c", "--debug-controls",
            help="Show subscribed control methods and fired controls, "
            "can take additional filters", nargs='*')

    args = parser.parse_args()
    if args.debug_controls is not None:
        print("Running in 'debug controls' mode.")
        control_log.stream.push_application()

        # Handle optional filters
        filters = []
        for filter in args.debug_controls:
            widget, _, control = filter.partition("@")
            filters.append((widget, control))
        control_log.filters[:] = filters

    return args

def before_displaying(args, window, loop):
    """
    Called before displaying the window.

    Args:
        args (namespace): argument parser arguments.
        window (Window): the BUI window.
        loop (asyncio Loop): the event loop.

    """
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

    if args.interactive:
        print("Interactive...")
        threading.Thread(target=threaded).start()
        loop.create_task(main())
