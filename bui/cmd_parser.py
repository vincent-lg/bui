"""Command-line argument parser for BUI.

This module contains the argument paser for BUI, which is active by default
if the BUI window is running as a Python script.  However, if it is frozen
(with PyInstaller or such), it will be inaccessible by default.  To enable
or disable it, look at the `start` function defined in the BUI tools
(see tools.py).

"""

import argparse
import asyncio

from bui.control import log as control_log
from bui.log import start_logging
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
    parser.add_argument("-l", "--log",
            help="Write in the bui.log log file", action="store_true")
    parser.add_argument("-c", "--debug-controls",
            help="Show subscribed control methods and fired controls, "
            "can take additional filters", nargs='*')

    args = parser.parse_args()
    if args.log:
        start_logging()
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
    if args.interactive:
        from bui.tools import PACKAGE
        PACKAGE.interactive.interact()
