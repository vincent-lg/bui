"""Release control, triggered when a key is released by the user."""

import re

from bui.control.base import Control
from bui.keyboard import KEYS, MODIFIERS

class Release(Control):

    """
    When the user releases one or several keys.

    This control is somewhat identical to [press](press.md), but
    fired when the user releases one or several keys on her keyboard.

    ## Usage

    If you want to set up a control on the window that triggers when the
    user releases the 'a' key on her keyboard, you might add a method
    in the window class with the name:

        def on_release_a(self, ...):

    This method will only be called if the user releases the 'a' key on her
    keyboard.

    You can also use the same syntax to create a release control on
    a specific widget.  Assuming, for instance, you have a text entry
    of ID 'entry', you could intercept a user releasing the 'a' key
    while this widget is focused by creating the following method:

        def on_release_a_in_entry(self):

    > The released key directly follows the control type separated with
      an underscore (`_`).  If this is a control on a specific widget,
      the widget ID follows the control type and key, separated by
      `_in_` (like `on_release_a_in_text`).

    ### Sub-controls and main controls

    In both cases, you can create a method that will operate on the release
    control, regardless of what key has been released.  This can be done,
    in a window control, by creating a method `on_release`, and on a widget
    control, by creating a method `on_release_{widget ID}`.

    > Note: if you have both one ore more release sub-controls, and one main
      release control, the latter will be called only if the former isn't
      triggered.  Consider this example:

        class Interface(Window):

            def on_release_a(self):
                print("A was released.")

            def on_release(self):
                print("Another key (not A) was released.")

    In this case, the `on_release` method will only be called if the key
    is not an "a".

    ### Different keys, same method

    Also notice you can easily create methods that handle several keys:

        class Interface(Window):

            def on_release_a(self):
                ...
            on_release_b = on_release_a
            on_release_r = on_release_a

    This syntax will bind the keys 'a', 'b' and 'r' to the same method,
    so that if the user releases one of these keys, the same action will
    be performed.

    ### What keys to intercept?

    You can intercept virtually any key released with this control.  Your
    method has to contain the name of the key as a lowercase version.
    Here are some examples:

        def on_release_a(self, ...): # The user releases the 'a' key
        def on_release_5(self, ...): # The user releases the '5' key
        def on_release_escape(self, ...): # The user releases the 'escape' key
        def on_release_space(self, ...): # The user releases the 'space' key

    All key names are lowercased.  Below is a table of commonly-used keys
    you can use in your method names:

    | Name     | Key       | Note                                  |
    | -------- | ----------- | ----------------------------------- |
    | back     | Backspace   | `                                   |
    | tab      | Tabulation  | -                                   |
    | return   | Return      | -                                   |
    | escape   | Escape      | -                                   |
    | space    | Spacebar    | -                                   |
    | delete   | Delete      | -                                   |
    | shift    | Shift       | May be used by the user OS.         |
    | alt      | Alt         | Open menubar on Windows.            |
    | home     | Home        | -                                   |
    | end      | End         | -                                   |
    | left     | Left arrow  | -                                   |
    | up       | Up arrow    | -                                   |
    | right    | Right arrow | -                                   |
    | down     | Down arrow  | -                                   |
    | numpadX  | X on numpad | Like `numpad0` or `numpad8`.        |
    | fX       | f<number>   | Like `f1` or `f12`.                 |
    | pageup   | Page Up     | -                                   |
    | pagedown | Page Down   | -                                   |

    There are other keys but these are the most commonly-used.

    ### Releasing several keys

    You can also intercept controls if the user releases a keyboard shortcut,
    like CTRL + n.  This is done in a very straightforward way:

        def on_release_ctrl_n(self):

    > Control key names form the key name.  They're separated with an
      underscore (_).

    The rule for control keys is that their lowercased name should be
    used.  More than one control key can be used in the method name,
    but in this case they have to be ordered:

    - `ctrl`: if present, the CTRL key should appear before everything.
    - `alt`: then comes the alt key.
    - `shift`: then comes the shift key.

    So this method:

        def on_release_ctrl_shift_x(self, ...):

    ... will be triggered if the user releases CTRL + Shift + x.  However:

        def on_release_alt_ctrl_o(self, ...):

    ... will not trigger (an error will be raised).  To work, you should
    change this method name like this:

        def on_release_ctrl_alt_o(self, ...):

    > Releasing a keyboard shortcut will fire several release controls.
      If the user presses on CTRL + Shift + A for instance, you will
      see three [press](press.md) controls followed by three
      [release](release.md) controls.  The first [press](press.md) control
      might be just 'ctrl', the second 'ctrl_shift', the third
      'ctrl_shift_a'.  Then comes the release controls: first
      'ctrl+shift+a', then... then it is difficult to predict what
      will be released.  Keys only used for modifiers might not raise
      consistent release controls.

    ### Link common actions with keyboard shortcuts

    It's common to want to link a keyboard shortcut with a simple
    action.  For instance, if we want to link 'Alt + F4' with the action
    "close the window".

    BUI offers an easy way to link these actions:

        class Interface(Window):

            # ...
            on_release_alt_f4 = close

    Although convenient, this code doesn't do any particular magic.  It
    is almost equivalent to the following, more understandable code:

        class Interface(Window):

            # ...
            def on_release_alt_f4(self):
                self.close()

    We simply directly link the action "close" to a specific keyboard
    shortcut.  Python doesn't see much of a difference, although the
    first syntax is just an alias for the `close` method.  This is
    a common action: `close` is a basic action that doesn't require
    any argument and can be linked with a control method in
    this way.

    ### Obtain the key in the control method

    With all this flexibility, sometimes you just need to know the real
    key the user released.  This information is contained inside the
    control object.  You can easily access it as a method argument?

        def on_release(self, key):
            print(f"The user released {key!r}.")

    If the user releases ESCAPE, this message will be displayed in the console:

        The user released the 'escape' key.

    The `key` argument is actually filled by the control manager.  When
    it examines your method signature and sees you want extra information,
    it looks at the control.  `key` is an attribute on the control, so
    it knows where it should come from.  You can also use the control
    itself:

        def on_release(self, control):

    `control` is a reserved name that will always contain the control object.
    Read on control attributes in the next section to know what to use as
    your control method argument.  Of course, your control method can
    receive, beyond `self`, none, one or more argument depending on your
    needs.

    ## Control attributes

    The control object has the following attributes:

    | Attribute | Type      | Note                                |
    | --------- | --------- | ----------------------------------- |
    | `key`     | str       | The name of the key being released. |
    | `raw_key` | str       | The raw key with no control keys.   |
    | `ctrl`    | bool      | Is the CTRL key being released too? |
    | `meta`    | bool      | Is the Meta key being released too? |
    | `alt`     | bool      | Is the Alt key being released too?  |
    | `shift`   | bool      | Is the Shift key being released too?|

    > The `raw_key` attribute is useful if you want to intercept 'a' but
      don't care if CTRL or Alt or all of the control keys is being released
      at the time.

    Use these attributes as your control method argument.  For instance:

        def on_release(self, raw_key, shift):

    Alternatively you can specify the `control` keyword argument in your
    method signature which will always contain the control object.

        def on_release(self, control):
            print(f"The user released on {control.key}.")

    """

    name = "release"
    widgets = {
            "window": "The user releases on her keyboard anywhere in the window",
    }

    has_sub_controls = True
    pattern_for_window = (
        fr"^on_release_(?P<key>({'_)?('.join([re.escape(mod) for mod in MODIFIERS])}_)?"
        fr"({'|'.join([re.escape(key) for key in KEYS])}))$")
    pattern_for_widgets = (
        fr"^on_release_(?P<key>({'_)?('.join([re.escape(mod) for mod in MODIFIERS])}_)?"
        fr"({'|'.join([re.escape(key) for key in KEYS])}))_in_{{id}}$")
    options = ("key", "raw_key", "ctrl", "meta", "alt", "shift")

    def __init__(self, widget, key, raw_key, ctrl=False, meta=False,
            alt=False, shift=False):
        super().__init__(widget)
        self.key = key
        self.raw_key = raw_key
        self.ctrl = ctrl
        self.meta = meta
        self.alt = alt
        self.shift = shift
