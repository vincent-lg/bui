"""Log specific to controls."""

import sys

from logbook import Logger, StreamHandler

filters = []
stream = StreamHandler(sys.stdout, level="DEBUG", bubble=True)
stream.format_string = "{record.message}"
logger = Logger("bui.control")

def filter_record(record, handler):
    """Check if the record can be logged."""
    if not filters:
        return True

    for widget, control in filters:
        wid = record.kwargs.get("widget", None)
        if wid is None:
            return True

        if widget:
            if widget == wid:
                if not control:
                    return True
            else:
                continue
        if control:
            if control == record.extra["control"]:
                return True

            continue

    return False

stream.filter = filter_record

class ControlLogger(Logger):

    """Specific logger to work on a given control class."""

    def __init__(self, control):
        name = f"bui.control.{control.name}"
        super().__init__(name)
        self.control = control

    def process_record(self, record):
        super().process_record(record)
        record.extra['control'] = self.control.name
