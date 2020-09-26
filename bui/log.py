"""Log facility for BUI.

BUI doesn't use the standard library's `logging`, but the
[logbook](https://logbook.readthedocs.io/en/stable/) alternative.
Helper top-level functions are provided so you can easily control
logging in your application (logging is turned off by default, except
if you specify otherwise).  Read
[BUI log](https://bui-project.org/log.html) for more information.

"""

from logbook import FileHandler, Logger, StreamHandler
import sys

# Two handlers are created.  Notice that other parts of the application
# will create handlers as well, these two are general handlers (one stream
# handler configured on `sys.stdout`, one file handler set on "bui.log"
# although you can change the file name).
stream = StreamHandler(sys.stdout, encoding="utf-8", level="INFO",
        bubble=True)
stream.format_string = (
        "[{record.level_name}] {record.channel}: {record.message}"
)
file = FileHandler("bui.log", encoding="utf-8", level="INFO", delay=True,
        bubble=True)
file.format_string = (
        "{record.time:%Y-%m-%d %H:%M:%S.%f%z} [{record.level_name}] "
        "{record.channel}: {record.message}"
)

# At this point, neither handler is used, if we create the logger and
# write in it, nothing will be logged unless `push_application`
# is called on the handlers.
logger = Logger("bui")

def start_logging():
    """Start logging, push the logger."""
    stream.push_application()
    file.push_application()
