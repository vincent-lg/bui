"""Module containing asynchronous tasks for BUI.

This adds a very thin layer over asyncio, hiding some more elaborate
details to allow for simple task handling.

"""

import asyncio

RUNNING = []


def schedule(coroutine):
    """
    Schedule the coroutine to run asynchronously.

    Args:
        coroutine (async def): coroutine to run.

    """
    loop = asyncio.get_event_loop()
    task = loop.create_task(coroutine)
    RUNNING.append(task)
    task.add_done_callback(done)
    return task


def done(task):
    """The specified task is done."""
    try:
        RUNNING.remove(task)
    except ValueError:
        pass


def cancel_all():
    """Cancel all tasks."""
    all_tasks = getattr(
        asyncio, "all_tasks", getattr(asyncio.Task, "all_tasks", None)
    )
    pending = all_tasks()
    for task in pending:
        try:
            task.cancel()
        except asyncio.CancelledError:
            pass
        finally:
            try:
                RUNNING.remove(task)
            except ValueError:
                pass

def run_remaining():
    """Asynchronously run the remaining tasks."""
    loop = asyncio.get_event_loop()
    for task in RUNNING:
        loop.run_until_complete(task)
