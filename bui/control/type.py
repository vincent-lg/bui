"""Type control, triggered when a key is typeed by the user."""

import re

from bui.control.base import Control
from bui.keyboard import KEYS, MODIFIERS

class Type(Control):

    """
    When the user types on her keyboard.

    This control is sent when the user presses on a key (or on
    a combination of keys) on her keyboard that would lead to writing
    a character.  Contrary to the [press control](press.md), this one
    is highly tied to the user keyboard layout and the state of the
    Caps Lock key.

    Assuming, for instance, the user is on an international QWERTY
    keyboard.  If she presses the ' key, this control will not be
    fired (' being a dead key on international QWERTY).  But if the user
    then presses on 'e', the "type" control will be sent with the typed
    key set to 'é'.

    In other words, this control is more useful to watch what user
    are typing rather than specific key presses on their keyboard.
    A type control is not sent each time a key is being pressed (as
    the example above demonstrated).  Not all key presses will result
    in a character being typed (arrow keys, for instance, will not).
    If you don't know which control to watch, read:
    [choose between press and type](../question/control/press-or-type.md).

    ## Usage

    The type control is somewhat similar in binding to the
    [press control](press.md).  Instead of specifying the key (or keys)
    being typed in the method name, you can directly place the character
    being typed:

        def on_type_I(self, ...):

    Notice: this method will only be called if the user types an uppercase
    'i', that is, if she types the Shift key then the 'i' key, or the
    Caps Lock key and the 'i' key then.  Contrary to [press](press.md),
    character names in the method are case-sensitive.

    You can use this control on a widget too.  Assuming you want to react
    if the user types a '8' while focusing on a list of ID "choices":

        def on_type_8_in_choices(self, ...):

    > Again, notice that contrary to [press](press.md), typing a '8' is
      not equivalent on all keyboard layouts.  Some will need to press she
      Shift key to do it, some will not, some might access the digit with
      other modifier keys.  And of course, this method will also be called
      if the Num Lock is on and the user presses the numpad8 key.

    ### Sub-controls and main controls

    As usual, a sub-control method always holds priority on a main control
    method:

        def on_type(self, unicode):
            # Main control intercepting almost anything
            ...

        def on_type_b(self):
            # sub-control
            ...

    The second method will be called if the user types a 'b'.  The
    first method will be called if the user types anything but a 'b'.

    ### What keys to intercept?

    As pointed out above, not all keys will lead to a character being
    typed.  You can write unicode characters directly in your
    method name, thanks to Python 3's unicode support in
    [identifiers](https://www.python.org/dev/peps/pep-3131/).

        def on_type_é(self):

    However, Python will not allow you to use all identifiers.  Creating
    such a method will raise a `SyntaxError`:

        def on_type_€(self):

    So as a general rule, if you are in doubt about what to capture
    or think the character in question would cause an error, just use
    a main control and check the `unicode` key as shown
    [below](#obtain-the-key-in-the-control-method).

    ### Obtain the key in the control method

    Although it is possible to place the typed character in the method
    name as shown above, it is more common to create a main control
    method and check the unicode value.  You can do so by specifying
    the `unicode` keyword argument in your control method:

        def on_type(self, unicode):
            if unicode == "€":
                ...

    ## Control attributes

    The control object has the following attributes:

    | Attribute | Type      | Note                                |
    | --------- | --------- | ----------------------------------- |
    | `unicode` | str       | The character being typed.          |

    Use these attributes as your control method argument.  For instance:

        def on_type(self, unicode):

    Alternatively you can specify the `control` keyword argument in your
    method signature which will always contain the control object.

        def on_type(self, control):
            print(f"The user will type {control.unicode}.")

    """

    name = "type"
    widgets = {
            "window": "The user typees on her keyboard anywhere in the window",
    }

    has_sub_controls = True
    pattern_for_window = fr"^on_type_(?P<unicode>.)$"
    name_for_widgets_without_options = "on_{control}_in_{wid}"
    pattern_for_widgets = fr"^on_type_(?P<unicode>.)_in_{{id}}$"
    options = ("unicode", )

    def __init__(self, widget, unicode):
        super().__init__(widget)
        self.unicode = unicode
