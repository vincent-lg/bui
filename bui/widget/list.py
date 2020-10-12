"""Module containing the generic List class, a generic list widget."""

from typing import Any, Hashable, Iterable, Tuple, Union

from bui.widget.base import Widget, CachedProperty

Choice = Union[Any, Tuple[Hashable, Any]]

class List(Widget):

    """
    The generic list widget.

    A list is to represent a choice given to the user, with
    several possible choices.  The user should select 0, 1 or more
    depending on the list type.  This list should be defined
    inside a [window](../layout/tag/window.md) tag.

    This is a generic widget which will be converted into a specific widget,
    depending on the used GUI toolkit.

    """

    widget = "list"
    class_name = "List"
    default_controls = {
        #"focus": "The list gets or loses focus",
        "init": "The window is initialized",
        "press": "The user presses on a key while the list is focused.",
        "release": "The user releases a key while the list is focused",
        "select": "The list selection changes.",
        "type": "The user types a character while the list is focused",
    }

    def __init__(self, leaf):
        super().__init__(leaf)
        self.x = leaf.x
        self.y = leaf.y
        self.id = leaf.id
        self.width = leaf.width
        self.height = leaf.height
        self.name = leaf.name
        self.multisel = leaf.multisel
        self._choices = []
        self._ids = {}
        self._pos = {}
        self._selected = (0, ) if self.multisel else 0

    def __len__(self):
        return len(self._choices)

    def __getitem__(self, item):
        try:
            item = self._ids[item]
        except KeyError:
            pass

        return self._choices[item]

    def __setitem__(self, item, choice):
        if isinstance(item, slice):
            items = list(range(item.start, item.stop))
            choices = choice
        else:
            items = [item]
            choices = []
            for i, item in enumerate(items):
                try:
                    key = self._ids[item]
                except KeyError:
                    pass
                else:
                    items[i] = key

                choices.append(self._choices[item])

        try:
            iter(choices)
            if len(choices) != len(items):
                raise TypeError
        except TypeError:
            raise TypeError("the number of choices doesn't match "
                    "the speicified indices") from None

        for item, choice in zip(items, choices):
            self.update_choice(item, choice)

    @CachedProperty
    def id(self):
        return self.leaf.id

    @property
    def choices(self):
        """Return the list choices."""
        return self._choices

    @choices.setter
    def choices(self, choices: Iterable[Choice]):
        """
        Modify the choices in the list.

        Args:
            choices (iterable): a list of choicess, where each choice can
                    be a label (preferably a str) or a tuple
                    (identifier, label) where identifier is hashable
                    (a string is often preferred).

        """
        try:
            iter(choices)
        except TypeError:
            raise TypeError("'choices' isn't a valid iterable")

        ids = {}
        pos = {}
        new_choices = []
        for i, choice in enumerate(choices):
            if isinstance(choice, (tuple, list)):
                id, label = choice
                label = str(label)
            else:
                id = i
                label = str(choice)

            new_choices.append(label)
            ids[id] = i
            pos[i] = id

        self._choices[:] = new_choices
        self._ids = ids
        self._pos = pos
        self._selected = (0, ) if self.multisel else 0
        self.specific.refresh()

    @property
    def selected(self):
        """Return the currently-selected choice ID or position."""
        selected = self._selected
        if self.multisel:
            return tuple(self._pos[index] for index in selected)

        return self._pos[selected]

    @selected.setter
    def selected(self, selected):
        """Change the selected label."""
        if self.multisel:
            choices = selected
        else:
            choices = (selected, )

        self._selected = ()
        for selected in choices:
            try:
                selected = self._ids[selected]
            except KeyError:
                pass

            try:
                self._choices[selected]
            except IndexError:
                raise IndexError(f"{selected!r} isn't a valid indice or key")
            else:
                self._selected += (selected, )

        self.specific.select(self._selected)

    def add_choice(self, choice: Choice):
        """
        Add a new choice at the end of the list.

        Args:
            choice (Choice): a choice, either a choice label (probably
                    a string) or a tuple of (choice identifier, choice label)
                    where both may be strings.  The choice identifier,
                    if specified, should be hashable.  The label
                    has no constraint (if it's not a string, then
                    str() will be called on it).

        Note:
            The label is what the user will see in the list, the
            identifier will identify the user selection for the
            developer.  If you don't specify any identifier,
            the choice position in the list will be used.

        """
        if isinstance(choice, tuple):
            id, label = choice
        else:
            id = len(self._choices)
            label = choice

        label = str(label)
        self._ids[id] = len(self._choices)
        self._pos[len(self._choices)] = id
        self._choices.append(label)
        self.specific.update_choice(len(self._choices) - 1, label)

    def update_choice(self, i, choice):
        """Update the specified choice."""
        self._choices[i] = str(choice)
        self.specific.update_choice(i, label)

    def remove_choice(self, identifier: Any):
        """
        Remove a choice in the list.

        Args:
            identifier (Any): the choice identifier or int position.

        """
        try:
            i = self._ids[identifier]
        except KeyError:
            i = identifier

        del self._choices[i]
        try:
            del self._ids[identifier]
        except KeyError:
            pass
        self.specific.remove_choice(i)
