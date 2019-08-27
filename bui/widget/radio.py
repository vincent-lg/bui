"""Module containing the generic RadioButton class, a generic radio button widget."""

from typing import Iterable, Tuple

from bui.widget.base import Widget, CachedProperty

class RadioButton(Widget):

    """
    The generic radio button widget.

    A radio button is to represent a group of choices, each choice being
    a button.  Selecting one forces the other ones to get unselected.
    This widget needs to be inside a [window](../layout/tag/window.md)
    tag.  It should have at least two choices, but you can set them
    initially with the [choice tag]../layout/tag/choice.md) or later
    with the `choices` property on this widget.

    This is a generic widget which will be converted into a specific widget,
    depending on the used GUI toolkit.

    """

    widget = "radio"
    class_name = "RadioButton"
    default_controls = {
        #"focus": "The radio button gets or loses focus",
        "init": "The window is initialized",
        "press": "The user presses on a key while the radio button is focused.",
        #"select": "The radio button selection changes.",
        "release": "The user releases a key while the radio button is focused",
        "type": "The user types a character while the radio button is focused",
    }

    def __init__(self, leaf):
        super().__init__(leaf)
        self.x = leaf.x
        self.y = leaf.y
        self.id = leaf.id
        self.width = leaf.width
        self.height = leaf.height
        self._choices = []
        self._selected = 0

    @CachedProperty
    def id(self):
        return self.leaf.id

    @property
    def choices(self):
        """Return the current choices."""
        return tuple(self._choices)

    @choices.setter
    def choices(self, choices: Iterable[Tuple[str, str]]):
        """
        Modify the radio button choices.

        Args:
            choices (iterable): an iterable containing choices, each
                    choice being a tuple with two elements (both of
                    `str`): the choice ID and the choice label.

        """
        try:
            iter(choices)
        except TypeError:
            raise TypeError("'choices' isn't a valid iterable")

        apply_choices = []
        for i, (choice_id, choice_label) in enumerate(choices):
            apply_choices.append((str(choice_id), str(choice_label)))

        if len(apply_choices) < 2:
            raise ValueError("you need to specify at least two choices")

        self._choices = apply_choices
        self.specific.refresh()
        self._selected = 0

    @property
    def selected(self):
        """Return the ID of the selected choice."""
        return self._choices[self._selected][0]

    @selected.setter
    def selected(self, choice: str):
        """Change the selected choice."""
        index = 0
        for i, (choice_id, choice_label) in enumerate(self._choices):
            if choice_id == choice:
                self._selected = i
                break
        else:
            raise ValueError(f"can't select choice of ID {choice!r}")

    def _init(self):
        """Widget initialization."""
        choices = []
        for tag in self.leaf.children:
            if tag.tag_name == "choice":
                choices.append((tag.id, tag.data))

        if len(choices) >= 2:
            self.choices = choices

        return super()._init()
