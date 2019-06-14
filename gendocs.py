"""Generate documentations, using code docstrings with slight formatting."""

from pathlib import Path
from textwrap import dedent

from bui.control import CONTROLS
from bui.layout import TAGS

def format_doc(doc: str) -> str:
    """
    Format the documentation, returning the formatted string.

    Args:
        doc (str): the documentation to be formatted

    Returns:
        formatted (str): the formatted doc.

    """
    doc = dedent(doc)

    # Read tables, collapse cells if needed
    watch_table = False
    formatted = ""
    table = []
    for line in doc.splitlines():
        if watch_table:
            #breakpoint()
            if not line.strip():
                tab_lines = [" | ".join(tab_line) for tab_line in table]
                formatted += "| " + " |\n| ".join(tab_lines) + " |\n\n"
                table = []
                watch_table = False
                continue

            cells = line.split("|")
            cells = [cell.strip() for cell in cells[1:-1]]
            if table and any(not cell for cell in cells):
                for i, cell in enumerate(cells):
                    if cell:
                        table[-1][i] = f"{table[-1][i].strip()} {cell}"
            else:
                table.append(cells)
        else:
            formatted += f"{line}\n"
            if line.strip() and all(char in " |-" for char in line):
                watch_table = True

    return formatted

# Browse different packages
doc_dir = Path("docs")
for name, Control in CONTROLS.items():
    if not Control.__doc__:
        continue

    doc = "# " + format_doc(Control.__doc__).lstrip()
    doc_file = doc_dir / "control" / f"{name}.md"
    with doc_file.open("w", encoding="utf-8") as file:
        file.write(doc)
        print(f"Write in {doc_file}")

for name, (Tag, _) in TAGS.items():
    if not Tag.__doc__:
        continue

    doc = "# " + format_doc(Tag.__doc__).lstrip()
    doc_file = doc_dir / "layout" / "tag" / f"{name}.md"
    with doc_file.open("w", encoding="utf-8") as file:
        file.write(doc)
        print(f"Write in {doc_file}")
