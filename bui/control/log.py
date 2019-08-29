"""Log specific to controls."""

import sys

from logbook import Logger, StreamHandler

stream = StreamHandler(sys.stdout, level="DEBUG", bubble=True)
stream.format_string = "{record.message}"
logger = Logger("bui.control")

class ControlLogger(Logger):

    """Specific logger to work on a given control class."""

    def __init__(self, control):
        name = f"bui.control.{control.name}"
        super().__init__(name)
        self.control = control

    def process_record(self, record):
        super().process_record(record)
        record.extra['control'] = self.control.name
