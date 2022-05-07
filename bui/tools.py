"""This module contains BUI-specific tools."""

import asyncio
from contextlib import contextmanager
from importlib import import_module
import os
import platform

from bui.cmd_parser import init_args, before_displaying

## Constants
FORBID_START = False

def load_GUI():
    """
    Attempt to load a GUI toolkit, depending on several factors:

    1.  What is available: obviously, this is the first question.  If
        no toolkit has been installed, none can be used.
    2.  The GUI toolkit version, as not all versions are supported by BUI.
    3.  On what platform are we running?  This might determine some choice, as
        some toolkits on some platforms might not be as accessible.

    Returns:
        The dynamically-loaded package (which is a sub-package of
        `specific`).  This package should directly lead to a specific
        `Window` class and support all the other layout features and controls.

    Raises:
        RuntimeError: if no toolkit could be loaded, or using them wouldn't
                be good for accessibility.

    """
    # Supported GUI toolkits
    supported = (
            # GUI  Version Package Can use callable
            ('wx', (4, ), 'wx4', lambda name: name == 'nt'),
    )

    able = []
    for name, version, package, can_use in supported:
        try:
            module = import_module(name)
        except ImportError:
            continue
        else:
            # Check the version
            module_version = module.__version__
            if isinstance(module_version, str):
                module_version = module_version.split(".")
                try:
                    module_version = [int(piece) for piece in module_version]
                except ValueError:
                    continue

            for needed, actual in zip(version, module_version):
                if needed != actual:
                    can_use = None

            if can_use and can_use(os.name):
                able.append(import_module(f'bui.specific.{package}'))

    if not able:
        raise RuntimeError("no GUI toolkit could be found on this platform.")

    return able[0]

def start(window):
    """Start a window."""
    args = None
    if not FORBID_START:
        args = init_args()

    window = window.parse_layout(window)

    # Create an asyncio EventLoop and hand it to the generic (and
    # specific) window object, to watch for window events AND
    # asynchronous events at the same time
    if not FORBID_START:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        before_displaying(args, window, loop)
        try:
            loop.run_until_complete(window._start(loop))
        except asyncio.CancelledError:
            pass


        try:
            loop.run_until_complete(window._stop())
        except asyncio.CancelledError:
            pass

    return window

@contextmanager
def forbid_start():
    """Pseudo context manager to forbid BUI to start during the with clause."""
    global FORBID_START
    FORBID_START = True

    try:
        yield None
    finally:
        FORBID_START = False

PACKAGE = load_GUI()

