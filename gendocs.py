"""Generate documentations, using code docstrings with slight formatting."""

from html import escape
from importlib import import_module
import inspect
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
                        table[-1][i] = f"{table[-1][i].strip()}"
                        if table[-1][i][-1] not in "/[-":
                            table[-1][i] += " "
                        table[-1][i] +=  cell
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

        # Add the links
        doc += (
                f"[Open raw](https://raw.githubusercontent.com/vincent-lg/"
                f"bui/master/example/{path.name}) [Open in github]("
                f"https://github.com/vincent-lg/bui/blob/master/"
                f"example/{path.name})\n\n"
        )

        # Skip the initial doc
        add = "\n".join(lines[len(module.__doc__.splitlines()) + 1:]).lstrip("\n")
        doc += f"## Source code ({len(add.splitlines())} lines)\n\n"
        doc += "```python\n" + add + "\n```\n"
        return doc

def read_raw(path: Path) -> str:
    """Read a raw file, return HTML-appropriate documentation."""
    with path.open("r", encoding="utf-8") as file:
        content = file.read()

    parent = path.parent.name
    name = "/".join(path.parts[-2:])
    doc = dedent(fr"""
        <!DOCTYPE html>
        <html lang="en-US">
          <head>
           <meta charset="UTF-8">
            <title>Blind User Interface - {name}</title>
            <meta name="generator" content="Jekyll v3.8.5" />
            <meta property="og:title" content="{name}" />
            <meta property="og:locale" content="en_US" />
            <meta name="description" content="{name}" />
            <meta property="og:description" content="{name}" />
            <link rel="canonical" href="https://vincent-lg.github.io/bui/{parent}/{path.stem}.html" />
            <meta property="og:url" content="https://vincent-lg.github.io/bui/{parent}/{path.stem}.html" />
            <meta property="og:site_name" content="bui" />
            <script type="application/ld+json">
            {{"@type":"WebSite","headline":"Blind User Interface - {name}","url":"https://vincent-lg.github.io/bui/{parent}/{path.stem}.html","name":"{name}","description":"{name}","@context":"http://schema.org"}}</script>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <meta name="theme-color" content="#157878">
            <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
            <link rel="stylesheet" href="/bui/assets/css/style.css?v=1c99addae22d0f201ec863ee092d1195efd935b8">
          </head>
          <body>
            <div>
    """).strip()
    for i, line in enumerate(content.splitlines()):
        line = escape(line)
        doc += (f"\n      <span style=\"white-space: pre;\">"
                f"<a id=\"L{i + 1}\"></a>{line}</span><br />")
    doc += "\n    </div>\n  </body>\n</html>"
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

# Analyze widget classes
widgets = (
        ("button", "Button"),
        ("checkbox", "Checkbox"),
        ("context", "Context"),
        ("dialog", "Dialog"),
        ("item", "Item"),
        ("list", "List"),
        ("menu", "Menu"),
        ("menubar", "Menubar"),
        ("radio", "RadioButton"),
        ("table", "Table"),
        ("text", "Text"),
        ("text", "Cursor"),
        ("window", "Window"),
)
for module_name, class_name in widgets:
    module = import_module(f"bui.widget.{module_name}")
    cls = getattr(module, class_name)

    lineno = inspect.getsourcelines(cls)[1]
    doc = (
            f"# {class_name} in [widget/{module_name}:{lineno}]"
            f"(../raw/widget/{module_name}.html#L{lineno})"
    )

    doc += f"\n\n{inspect.cleandoc(cls.__doc__)}"

    # Method summary
    doc += "\n\n## Class summary"

    properties, methods = [], []
    for name, member in inspect.getmembers(cls):
        if name.startswith("_"):
            continue

        if isinstance(member, property):
            properties.append((name, member))
            continue

        if not callable(member):
            continue

        methods.append((name, member))

    # Properties
    if properties:
        doc += f"\n\nThis class offers {len(properties)} propert{'y' if len(properties) < 2 else 'ies'}.\n"
        doc += "\n| Property | Get | Set |"
        doc += "\n| -------- | --- | --- |"

        for name, pro in properties:
            fget, fset = "**Can't read.**", "**Can't write**"
            if pro.fget:
                if pro.fget.__doc__ is None:
                    breakpoint()
                fget = inspect.cleandoc(pro.fget.__doc__).splitlines()[0]

            if pro.fset:
                if pro.fset.__doc__ is None:
                    breakpoint()
                fset = inspect.cleandoc(pro.fset.__doc__).splitlines()[0]

            doc += f"\n| [{name}](#{name}) | {fget} | {fset} |"

    # Methods
    doc += f"\n\nThis class offers {len(methods)} method{'' if len(methods) < 2 else 's'}.\n\n"
    doc += dedent("""
            | Method | Signature | Description |
            | ------ | --------- | ----------- |
    """).strip()
    for name, method in methods:
        first_line = inspect.cleandoc(method.__doc__).splitlines()[0]
        signature = inspect.signature(method)
        parameters = dict(signature.parameters)
        parameters.pop("self", None)
        parameters = ", ".join([str(p) for p in parameters.values()])
        doc += (
                f"\n| [{name}](#{name}) | "
                f"`{name}({parameters})` | {first_line} |"
        )

    # Longer description
    if len(properties):
        doc += "\n\n## Properties"
        for name, pro in properties:
            if pro.fget and pro.fset:
                can = "can get and be set"
            elif pro.fget:
                can = "can only get (read-only)"
            else:
                can = "can only be set"
            doc += f"\n\n### {name}\n\nThis property {can}."
            if pro.fget:
                doc += "\n\n#### Get"
                lineno = inspect.getsourcelines(pro.fget)[1]
                doc += (
                        f"\n\n[See the source code]("
                        f"../raw/widget/{module_name}.html#L{lineno})"
                )
                doc += "\n\n" + inspect.cleandoc(pro.fget.__doc__)
            if pro.fset:
                doc += "\n\n#### Set"
                lineno = inspect.getsourcelines(pro.fset)[1]
                doc += (
                        f"\n\n[See the source code]("
                        f"../raw/widget/{module_name}.html#L{lineno})"
                )
                doc += "\n\n" + inspect.cleandoc(pro.fset.__doc__)

    # Methods
    doc += "\n\n## Methods"
    for name, method in methods:
        signature = inspect.signature(method)
        parameters = dict(signature.parameters)
        short = ", ".join([str(p) for p in parameters.values()])
        doc += f"\n\n### {name}\n\n`{name}({short})`"
        lineno = inspect.getsourcelines(method)[1]
        doc += (
                f"\n\n[See the source code]("
                f"../raw/widget/{module_name}.html#L{lineno})"
        )
        doc += "\n\n| Parameter | Type | Default |"
        doc += "\n| --------- | ---- | ------- |"
        for parameter in parameters.values():
            if parameter.name == "self": # Assume this is the instance keyword
                annotation = f"`{class_name}`"
            elif parameter.annotation is not parameter.empty:
                annotation = "`" + inspect.formatannotation(parameter.annotation) + "`"
            else:
                annotation = "*Not set*"

            doc += f"\n| {parameter.name} | "
            doc += f"{annotation} | "
            if parameter.default is not parameter.empty:
                doc += f"`{parameter.default!r}`"
            doc += " |"

        doc += "\n\n" + inspect.cleandoc(method.__doc__)

    dump = doc_dir / "widget" / f"{class_name}.md"
    with dump.open("wb") as file:
        file.write(doc.encode("utf-8"))
    print(f"Write in {dump}")

# Write the raw files
control_dir = Path() / "bui/control"
for path in control_dir.glob("*.py"):
    if path.stem.startswith("__"):
        continue

    doc = read_raw(path)
    raw_path = doc_dir / "raw" / "control" / (path.stem + ".html")
    with raw_path.open("wb") as html_file:
        html_file.write(doc.encode("utf-8"))
    print(f"Write in {raw_path}.")

layout_dir = Path() / "bui/layout"
for path in layout_dir.glob("*.py"):
    if path.stem.startswith("__"):
        continue

    doc = read_raw(path)
    raw_path = doc_dir / "raw" / "layout" / (path.stem + ".html")
    with raw_path.open("wb") as html_file:
        html_file.write(doc.encode("utf-8"))
    print(f"Write in {raw_path}.")

widget_dir = Path() / "bui/widget"
for path in widget_dir.glob("*.py"):
    if path.stem.startswith("__"):
        continue

    doc = read_raw(path)
    raw_path = doc_dir / "raw" / "widget" / (path.stem + ".html")
    with raw_path.open("wb") as html_file:
        html_file.write(doc.encode("utf-8"))
    print(f"Write in {raw_path}.")

