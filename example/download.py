"""Show a download window with in-progress information.

This window simply illustrates the way BUI can work asynchronously.
Several files (heavy files on some connections) are downloaded at the
same time.  Their status is updated and their downloading doesn't block
the window in the slightest.  The overall code is quite easy to read as well.

Internally, BUI handles this situation with a table (to display the
download in progress) and custom rows (the row object of the table
is altered).  Thus, most of the logic has been moved in the
`DownloadRow` class, leaving the window quite sparse.  This example
also illustrates buttons, menu bars and dialogs.

Installation:

    pip install bui[demo]

To run this example:

    python download.py

"""

import asyncio

import aiofiles
import aiohttp
from bui import Window, start
from bui.widget.table import AbcRow

## Constants
FILES = [
    # ( File name, URL)
    ("python-3.7.tgz", "https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz"),
]

class DownloadExample(Window):

    """Class to represent a downloading dialog, using async operations."""

    layout = mark("""
      <window title="Blind User Interface - downloading">
        <menubar>
          <menu name="File">
            <item id=add_file>Add a file...</item>
            <item id=quit>Quit</item>
          </menu>
        </menubar>

        <table x=2 y=2 id="download">
          <col>File</col>
          <col>Status</col>
          <col>Downloaded</col>
          <col>Size</col>
        </table>
        <button x=1 y=5>Start</button>
        <button x=4 y=5>Add</button>
      </window>
    """)

    def on_init_download(self, widget):
        """The 'download' table is ready to be displayed."""
        widget.row_class = DownloadRow
        widget.downloading = False
        widget.rows = [(file, "Unknown", "Unknown", "Unknown") for file, _ in FILES]
        self.schedule(self.download_all())

    async def on_close(self):
        """Close the window, end the session."""
        await self.session.close()

    def on_add(self):
        """The 'add' button was clicked."""
        dialog = self.pop_dialog("""
            <dialog title="Add a file to download">
              <text x=1 y=1 id=name>Name of the file to add to the download list:</text>
              <text x=1 y=3 id=url>URL of the file to download from the Internet3:</text>
              <button x=0 y=5 set_true>OK</button>
              <button x=4 y=5 set_false>Cancel</button>
            </dialog>
        """)

        if dialog:
            name = dialog["name"].value
            url = dialog["url"].value
            table = self["download"]
            row = table.add_row(name, "Unknown", "Unknown", "Unknown")
            row.url = url
            self.schedule(row.download(self.session))
    on_add_file = on_add
    on_press_ctrl_a = on_add
    on_quit = close
    on_press_ctrl_q = close

    def on_start(self, widget):
        """The start button has been clicked by the user."""
        table = self["download"]
        table.downloading = not table.downloading
        widget.name = "Pause" if table.downloading else "Start"

    async def download_all(self):
        """Download all files asynchronously."""
        self.session = aiohttp.ClientSession()
        table = self["download"]
        tasks = []
        for i, (filename, url) in enumerate(FILES):
            row = table.rows[i]
            row.url = url
            tasks.append(row.download(self.session))

        await asyncio.gather(*tasks)


class DownloadRow(AbcRow):

    """
    Class to represent a row in the download table.

    Columns:
        file: the file name.
        status: the status of the downloaded file.
        downloaded: how many bytes were downloaded (human-readable).
        size: the file size (human-readable).

    Extra information is contained in these objects (but not displayed
    in the row):
        file_size: the total size of the file in bytes (as an int).
        progress: the number of downloaded bytes (as an int).
        url: the file URL.

    Methods:
        complete(size): mark the download as complete.
        async download(session): start downloading the file.

    """

    columns = (
            ("file", "File", False),
            ("status", "Status", False),
            ("downloaded", "Downloaded", False),
            ("size", "Size", False),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._progress = 0
        self._file_size = -1
        self.url = ""

    @property
    def file_size(self):
        return self._file_size

    @file_size.setter
    def file_size(self, file_size):
        """Update the file size, and size column."""
        self._file_size = file_size
        if file_size >= 0:
            self.size = human_size(file_size)

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, progress):
        """Update the progress and downloaded column."""
        self._progress = progress
        self.downloaded = human_size(progress)
        size = self._file_size
        if size >= 0:
            pct = round((progress / size) * 100, 1)
            self.status = f"{pct}%"
        else:
            self.status = "Downloading"

    def complete(self, size):
        """Mark as complete."""
        self.file_size = size
        self.progress = size
        self.status = "Complete"

    async def download(self, session):
        """Download one file asynchronously."""
        async with session.get(self.url) as response:
            if response.status != 200:
                self.status = "Error"
                return

            try:
                length = response.headers["Content-Length"]
            except KeyError:
                self.size = "Unknownable"
            else:
                try:
                    length = int(length)
                except ValueError:
                    self.size = "Unknownable"
                else:
                    self.file_size = length

            # Download the file
            total = 0
            async with aiofiles.open(self.file, "wb") as file:
                while response:
                    if self.widget.downloading:
                        bytes = await response.content.read(1024)
                        if not bytes:
                            self.complete(total)
                            return

                        total += len(bytes)
                        await file.write(bytes)
                        self.progress = total
                        await self.widget.sleep(0.1)
                    else:
                        await self.widget.sleep(0.2)


def human_size(num):
    for unit in ('', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi'):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}B"
        num /= 1024.0

    return f"{num:3.1f}YiB"

start(DownloadExample)
