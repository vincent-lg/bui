"""Press control, triggered when a key is pressed by the user."""

import re

from bui.control.base import Control
from bui.keyboard import KEYS, MODIFIERS

class Press(Control):

    """
    When the user presses on a key.

    This control is triggered when the user presses a key on her keyboard
    while the widget is selected, or while the window is focused, if
    this control is bound to a window itself.  Contrary to other controls,
    this one has sub-controls with the name of the key right in the method
    name for easy processing.

    ## Usage

    If you want to set up a control on the window that triggers when the
    user presses the 'a' key on her keyboard, you might add a method
    in the window class with the name:

        def on_press_a(self, ...):

    This method will only be called if the user presses the 'a' key on her
    keyboard.

    > Note: this control uses a uniform keyboard layout which is not
      affected by the user keyboard layout.  When the documentation says
      "the user presses the 'a' key", it means the position of the
      'a' on an international keyboard.  Someone with a different keyboard
      layout will have to press a different key.  For instance, someone
      on an AZERTY keyboard (used mostly in France) will have to type
      'q' to fire the method `on_press_a`.  If you want accurate keys that
      depend on the keyboard layout, use the [type](./type.md) control which
      has the same purpose but allows access to the key being pressed,
      taking into account the user keyboard.  There are cases, however,
      when it's more important to capture the "key at this position on the
      keyboard" rather than "what this key would write in the end".

    You can also use the same syntax to create a press control on a specific
    widget.  Assuming, for instance, you have a text entry of ID 'entry',
    you could intercept a user pressing on the 'a' key while this widget is
    focused by creating the following method:

        def on_press_a_entry(self):

    > The pressed key directly follows the control type separated with
      an underscore (`_`).  If this is a control on a specific object,
      the widget ID follows the control type and key, which might
      create some odd-looking method names.

    ### Sub-controls and main controls

    In both cases, you can create a method that will operate on the press
    control, regardless of what key has been pressed.  This can be done,
    in a window control, by creating a method `on_press`, and on a widget
    control, by creating a method `on_press_{widget ID}`.

    > Note: if you have both one ore more press sub-controls, and one main
      press control, the latter will be called only if the former isn't
      trigger.  Consider this example:

        class Interface(Window):

            def on_press_a(self):
                print("A was called.")

            def on_press(self):
                print("Another key (not A) was pressed.")

    In this case, the `on_press` method will only be called if the key
    is not an "a".

    ### Different keys, same method

    Also notice you can easily create methods that handle several keys:

        class Interface(Window):

            def on_press_a(self):
                ...
            on_press_b = on_press_a
            on_press_r = on_press_a

    This syntax will bind the keys 'a', 'b' and 'r' to the same method,
    so that if the user presses one of these keys, the same action will
    be performed.

    ### What keys to intercept?

    You can intercept virtually any key pressed with this control.  Your
    method has to contain the name of the key as a lowercase version.
    Here are some examples:

        def on_press_a(self, ...): # The user presses the 'a' key
        def on_press_5(self, ...): # The user presses the '5' key (above 't')
        def on_press_escape(self, ...): # The user presses the 'escape' key
        def on_press_space(self, ...): # The user presses the 'space' key

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

    There are othert keys but these are the most commonlyused.

    ### Pressing several keys

    You can also intercept controls if the user presses a keyboard shortcut,
    like CTRL + n.  This is done in a very straigthforward way:

        def on_press_ctrl_n(self):

    > Control key names form the key name.  They're separated with an
      underscore (_).

    The rule for control keys is that their lowercased name should be
    used.  More than one control key can be used in the method name,
    but in this case they have to be ordered:

    - `ctrl`: if present, the CTRL key should appear before everything.
    - `alt`: then comes the alt key.
    - `shift`: then comes the shift key.

    So this method:

        def on_press_ctrl_shift_x(self, ...):

    ... will be triggered if the user presses CTRL + Shift + x.  However:

        def on_press_alt_ctrl_o(self, ...):

    ... will not trigger (an error will be raised).  To work, you should
    change this method name like this:

        def on_press_ctrl_alt_o(self, ...):

    ### Link common actions with keyboard shortcuts

    It's common to want to link a keyboard shortcut with a simple
    action.  For instance, if we want to link 'Alt + F4' with the action
    "close the window".

    BUI offers an easy way to link these actions:

        class Interface(Window):

            # ...
            on_press_alt_f4 = close

    Although convenient, this code doesn't do any particular magic.  It
    is almost equivalent to the follwing, more understandable code:

        class Interface(Window):

            # ...
            def on_press_alt_f4(self):
                self.close()

    We simply directly link the action "close" to a specific keyboard
    shortcut.  Python doesn't see much of a difference, although the
    first syntax is just an alias for the `close` method.  This is
    a common action: `close` is a basic action that doesn't require
    any argument and can be linked with a control method in
    this way.

    ### Obtain the key in the control method

    With all this flexibility, sometimes you just need to know the real
    key the user pressed.  This information is contained inside the
    control object.  You can easily access it as a method argument?

        def on_press(self, key):
            print(f"The user pressed {key!r}.")

    If the user presses ESCAPE, this message will be displayed in the console:

        The user pressed the 'escape' key.

    The `key` argument is actually filled by the control manager.  When
    it examines your method signature and sees you want extra information,
    it looks at the control.  `key` is an attribute on the control, so
    it knows where it should come from.  You can also use the control
    itself:

        def on_press(self, control):

    `control` is a reserved name that wil always contain the control object.
    Read on control attributes in the next section to know what to use as
    your control method argument.  Of course, your control method can
    receive, beyond `self`, none, one or more argument depending on your
    needs.

    ## Control attributes

    The control object has the following attributes:

    | Attribute | Type      | Note                                |
    | --------- | --------- | ----------------------------------- |
    | key       | str       | The name of the key being pressed.  |
    | raw_key   | str       | The raw key with no control keys.   |
    | ctrl      | bool      | Is the CTRL key being pressed too?     |
    | meta      | bool      | Is the Meta key being pressed too?     |
    | alt       | bool      | Is the Alt key being pressed too?      |
    | shift     | bool      | Is the Shift key being pressed too?    |

    > The `raw_key` attribute is useful if you want to intercept 'a' but
      don't care if CTRL or Alt or all of the control keys is being pressed
      at the time.

    Use these attributes as your control method argument.  For instance:

        def on_press(self, raw_key, shift):

    Alternatively you can specify the `control` keyword argument in your
    method signature which will always contain the control object.

        def on_press(self, control):
            print(f"The user pressed on {control.key}.")

    """

    name = "press"
    widgets = {
            "window": "The user presses on her keyboard anywhere in the window",
    }

    has_sub_controls = True
    pattern_for_window = (
        fr"^on_press_(?P<key>({'_)?('.join([re.escape(mod) for mod in MODIFIERS])}_)?"
        fr"({'|'.join([re.escape(key) for key in KEYS])}))$")
    pattern_for_widgets = (
        fr"^on_press_(?P<key>({'_)?('.join([re.escape(mod) for mod in MODIFIERS])}_)?"
        fr"({'|'.join([re.escape(key) for key in KEYS])}))_{{id}}$")
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
