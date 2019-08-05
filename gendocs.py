"""Generate documentations, using code docstrings with slight formatting."""

from importlib import import_module
from pathlib import Path
from textwrap import dedent

from bui.control import CONTROLS
from bui.layout import TAGS
from bui.tools import forbid_start

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

def read_example(path: Path) -> str:
    """Read an example script, returning the formatted doc."""
    with forbid_start():
        module = import_module(".".join(path.parts)[:-3])

        doc = f"# Example: {path.stem}\n\n" + format_doc(module.__doc__)

        with path.open("r", encoding="utf-8") as file:
            lines = file.read().splitlines()

        # Skip the initial doc
        add = "\n".join(lines[len(module.__doc__.splitlines()) + 1:]).lstrip("\n")
        doc += f"## Source code ({len(add.splitlines())} lines)\n\n"
        doc += "```python\n" + add + "\n```\n"
        return doc

# Browse different packages
doc_dir = Path("docs")
for name, Control in CONTROLS.items():
    if not Control.__doc__:
        continue

    doc = f"# Control: {name}\n\n" + format_doc(Control.__doc__).lstrip()
    doc_file = doc_dir / "control" / f"{name}.md"
    with doc_file.open("wb") as file:
        file.write(doc.encode("utf-8"))
        print(f"Write in {doc_file}")

for name, (Tag, _) in TAGS.items():
    if not Tag.__doc__:
        continue

    doc = f"# Layout tag: {name}\n\n" + format_doc(Tag.__doc__).lstrip()
    doc_file = doc_dir / "layout" / "tag" / f"{name}.md"
    with doc_file.open("wb") as file:
        file.write(doc.encode("utf-8"))
        print(f"Write in {doc_file}")

# Examples
ex_dir = Path() / "example"
for path in ex_dir.glob("*.py"):
    doc = read_example(path)
    ex_path = doc_dir / "example" / (path.stem + ".md")
    with ex_path.open("wb") as md_file:
        md_file.write(doc.encode("utf-8"))
    print(f"Write in {ex_path}.")
