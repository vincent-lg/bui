"""Class containing the layout structure of a top component (like a window).

The `BUILayoutParser` actually creates such a layout and fills it according
to the provided text.  Then the `bui.Window` class can access the layout
and search for specific tags, or browse the list of nested components.

"""

from itertools import count
from queue import PriorityQueue

class Layout:

    """Layout of a top-level component (like a Window).

    This class is created by the `BUILayoutParser`.  It contains a list of top-level components defined in the layout.  Each component can contain others, assuming this is logically supported in the component structure.  A `Layout` object can:

    - Be browsed (iterated over with a for loop).
    - Search for a specific component using the `get` method.
    - Iterate over all nested components (see the `flat` property).

    """

    def __init__(self):
        self.components = []

    def __repr__(self):
        return f"<Layout with <{'>, <'.join([component.tag_name for component in self.components])}>"

    def __str__(self):
        return "\n\n".join([str(component) for component in self.components])

    def __iter__(self):
        return iter(self.components)

    @property
    def flat(self):
        """Return a flattened list of all components, including their children."""
        counter = count(1)
        components = PriorityQueue()
        for component in self.components:
            components.put((-1, next(counter), component))

        flat = []
        while not components.empty():
            depth, _, component = components.get()
            flat.append(component)
            for child in component.children:
                components.put((depth - 1, next(counter), child))

        return flat

    def get(self, tag: str):
        """
        Return the first tag with the given name or None.

        This allows for a flat search in the layout tree.

        Args:
            tag (str): the tag name to search.

        If more than one tag is present, returns the first.

        """
        tags = self.flat
        for match in tags:
            if match.tag_name == tag:
                return match
                return match
