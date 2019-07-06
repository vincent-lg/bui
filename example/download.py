"""Show a download window with in-progress information.

This window simply illustrates the way BUI can work asynchronously.
Several files (heavy files on some connections) are downloaded at the
same time.  Their status is updated and their downloading doesn't block
the window in the slightest.  The overall code is quite easy to read as well.

Installation: to run this, install the aiohttp and aiofiles packages:

    pip install aiohttp cchardet aiodns aiofiles

Then simply run this script with BUI installed.

> Note: if not already set, you should install a GUI toolkit.

    pip install wxPython

"""

import asyncio

import aiofiles
import aiohttp
from bui import Window, start

## Constants
TEKNOAXE = "http://www.teknoaxe.com/Music/mobile_direct_download.php"
FILES = [
    # ( File name, URL, optional arguments in a dictionary)
    ("python-3.7.tgz", "https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz", {}),
    ("Sheltered In Subdued Rain.mp3", TEKNOAXE, {"file": "Sheltered_In_Subdued_Rain.mp3"}),
    ("Metal and Medeival.mp3", TEKNOAXE, {"file": "Metal_and_Medeival.mp3"}),
    ("Isle of Doom.mp3", TEKNOAXE, {"file": "Isle_of_Doom.mp3"}),
    ("Wayward Ghouls.mp3", TEKNOAXE, {"file": "Wayward_Ghouls.mp3"}),
    ("Figuring Out the Technicalities.mp3", TEKNOAXE, {"file": "Figuring_Out_the_Technicalities.mp3"}),
    ("Until Your Engine Stops II.mp3", TEKNOAXE, {"file": "Until_Your_Engine_Stops_II.mp3"}),
    ("Disco Attempt_1.mp3", TEKNOAXE, {"file": "Disco_Attempt_1.mp3"}),
]

class DownloadExample(Window):

    """Class to represent a downloading dialog, using async operations."""

    layout = mark("""
      <window title="Blind User Interface - downloading">
        <table x=2 y=2 id="download">
          <col>File</col>
          <col>Status</col>
          <col>Downloaded</col>
          <col>Size</col>
        </table>
        <button x=3 y=4 name="Start" />
      </window>
    """)

    def on_init_download(self, widget):
        self.downloading = False
        widget.rows = [(file, "Unknown", "Unknown", "Unknown") for file, _, _ in FILES]
        self.schedule(self.download_all())

    def on_start(self, widget):
        """The start button has been clicked by the user."""
        self.downloading = not self.downloading
        widget.name = "Pause" if self.downloading else "Start"
    on_press_space_start = on_start

    async def download_all(self):
        """Download all files asynchronously."""
        table = self["download"]
        tasks = []
        async with aiohttp.ClientSession() as session:
            for i, (filename, url, options) in enumerate(FILES):
                row = table.rows[i]
                tasks.append(self.download(row, session, filename, url, options))

            await asyncio.gather(*tasks)

    async def download(self, row, session, filename, url, options):
        """Download one file asynchronously."""
        async with session.get(url, params=options) as response:
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

def human_size(num):
    for unit in ('', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi'):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}B"
        num /= 1024.0

    return f"{num:3.1f}YiB"

start(DownloadExample)
