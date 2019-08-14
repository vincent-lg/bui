# Example: download

Show a download window with in-progress information.

This window simply illustrates the way BUI can work asynchronously.
Several files (heavy files on some connections) are downloaded at the
same time.  Their status is updated and their downloading doesn't block
the window in the slightest.  The overall code is quite easy to read as well.

Installation: to run this, install the aiohttp and aiofiles packages:

    pip install aiohttp cchardet aiodns aiofiles

Then simply run this script with BUI installed.

> Note: if not already set, you should install a GUI toolkit.

    pip install wxPython

## Source code (141 lines)

```python
import asyncio

import aiofiles
import aiohttp
from bui import Window, start

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
        self.downloading = False
        widget.rows = [(file, "Unknown", "Unknown", "Unknown") for file, _ in FILES]
        self.schedule(self.download_all())

    def on_start(self, widget):
        """The start button has been clicked by the user."""
        self.downloading = not self.downloading
        widget.name = "Pause" if self.downloading else "Start"
    on_press_space_start = on_start

    async def download_all(self):
        """Download all files asynchronously."""
        self.session = aiohttp.ClientSession()
        table = self["download"]
        tasks = []
        for i, (filename, url) in enumerate(FILES):
            row = table.rows[i]
            tasks.append(self.download(row, filename, url))

        await asyncio.gather(*tasks)

    async def download(self, row, filename, url):
        """Download one file asynchronously."""
        async with self.session.get(url) as response:
            if response.status != 200:
                row.status = "Error"
                return

            try:
                length = response.headers["Content-Length"]
            except KeyError:
                row.size = "Unknownable"
                size = -1
            else:
                try:
                    length = int(length)
                except ValueError:
                    row.size = "Unknownable"
                else:
                    row.size = human_size(length)
                    size = length

            # Download the file
            total = b""
            async with aiofiles.open(filename, "wb") as file:
                while response:
                    if self.downloading:
                        bytes = await response.content.read(1024)
                        if not bytes:
                            row.status = "Complete"
                            if size < 0:
                                size = len(total)
                            row.downloaded = human_size(size)
                            return

                        total += bytes
                        await file.write(bytes)
                        row.downloaded = human_size(len(total))
                        if size > 0:
                            percent = round((len(total) / size) * 100, 1)
                            row.status = f"{percent}%"
                        else:
                            row.status = "Downloading..."

                        await self.sleep(0.1)
                    else:
                        await self.sleep(0.2)

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
            self.schedule(self.download(row, name, url))
    on_add_file = on_add
    on_quit = close
    on_press_ctrl_q = close

    async def on_close(self):
        """Close the window, end the session."""
        print("Closing the session...")
        await self.session.close()
        print("... closed.")

def human_size(num):
    for unit in ('', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi'):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}B"
        num /= 1024.0

    return f"{num:3.1f}YiB"

start(DownloadExample)
```
