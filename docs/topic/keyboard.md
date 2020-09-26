# Managing the keyboard controls in BUI

Having a user interface react to keyboard presses can be extremely valuable for fluidity.  On the other hand, creating keyboard events (or controls, in BUI) can seem quite complex in some other tools.  BUI offers its own strategy, but being uncommon means it can feel quite alien to beginners with this tool.  This page attempts to shed light upon this interesting system.

## First glance at keyboard handling

BUI simplifies things as much as possible for users.  Keyboard controls have a straightforward connection, in terms of order, purpose and name.  Let us see a first example.  For clarity, we'll add the BUI layout right in the Python class.  Please bear in mind this is not recommended for production and will actually remove one of BUI's sgrength for developers.

```python
from bui import Window, start

class Example(Window):

    """An example window."""

    layout = mark("""
        <window title="An example">
          <text x=2 y=2 width=1 id=status read-only>What now?</text>
        </window>
    """)

    def on_press_a(self):
        """The user pressed the key A."""
        self["status"].value = "Ho, there's an A!"

start(Example)
```

Again, before describing the code, let's see what it does.  If you execute this tiny script, it will create a window with a read-only text field in the middle.  If you press the key A on your keyboard, the message is changed.

IN BUI terms, we've created a window with its layout and a control method.  The layout is simple enough and won't be detailed here: enough for a window and a text field in the middle of it.  But the control method deserves some explanation:

```python
    def on_press_a(self):
        """The user pressed the key A."""
        self["status"].value = "Ho, there's an A!"
```

Again, it's easy enough to read but it seems a bit magical.  So let's understand it.  How can this method bind to the key A?  Well, simply enough, thanks to its name.  The control method name can contain a lot of information and here's an example.  `on_press_a` will trigger ONLY when the user presses the letter A on her keyboard.  Try pressing anything else, it just won't work.

## A clarification for users with other keyboards

> I don't have a QWERTY keyboard... what's the key A for you... and for BUI?

A lot of frameworks don't really explain the connection between a key press and a letter because this can be quite complicated.  On a Frendch keyboard, the letter A is located where the Q is located on a QWERTY keyboard.  So which is which?  BUI will link to the user's keyboard layout in most cases with some exceptions what will be reported here.  So when you say "intercept A", it will intercept the key that would print an A.  On the French keyboard, this happens when you type the letter A, where the letter Q would be located on a QWERTY keyboard.

But that's not always true.  Let's try to intercept the key pressed for the digit 5.

```python
    ...
    def on_press_5(self):
        """The user pressed the key 5."""
        self["status"].value = "Ho, there's a 5, neat!"
```

Yes, that's as simple as that.  Let's run this script.  If you have a QWERTY keyboard, you can just type the letter 5.  But hold on... with a French keyboard, for instance, to type a 5, you would need to press the combination Shift + the letter corresponding to 5 (which happens to be the left parent on an AZERTY keyboard).

If you run this script, what would you need to press if you had a French keyboard?  You would guess SHIFT + ( because that's how you would type a 5.  And that would be a wrong guess.  That's the limit: BUI will not know how to type a 5 with this layout.  So it will just listen for the key which would lead to a 5 in QWERTY: that is the ( parent in French.  So to see the message "Ho, there's a 5, neat!" with a French keyboard, you would need to press ( .

> Why is that?  BUI seemed to link to the keyboard layout in the previous example... and it's not doing it now?

The rule is unfortunately a bit complex and BUI can't do much about it.  Basically, if you try to intercept a latin letter on a latin keyboard, the user keyboard layout will be used.  That's why when we want to intercept a letter A, we could enter the letter A in French (where the Q is located in QWERTY).  But this logic doesn't apply if you want to intercept digits or punctuation signs because their position is not 100% guaranteed on all keyboards.  Unfortunately, besides being complex, this rule doesn't even make sense when it comes to non-latin keyboards, but that's the way things are.

To summarize: if you want to intercept a key which is just a latin letter (between A and Z) then go on.  The user keyboard layout will be used whenever possible.  If you want to intercept digits or punctuation signs for some actions, you might need to adapt your documentation for international users.

## Basic control method recap

We've seen that to intercept a key press, you just need to call a `on_press_...` method, where you'll provide the key press.

* Easy if you want to intercept a letter.  Just write `on_press_LETTER` in your method name, like `on_press_j`.  Use the lowercase version of the letter however.
* Easy enough when you want to intercept digits.  Just enter the digit in the method name, like `on_press_3`.  But bear in mind that the way to type a digit on other keyboards mighyt not be the same key as you.  However, `on_press_3` will listen for the key position on QWERTY keyboards.  This might not be the user's key position.
* Not so easy for punctuation signs.  `on_press_;` is not a valid Python name, so it's not allowed.  In this situation, it's necessary to write a [main control](#main-control).  We'll see that next.

Before we go, though, keep in mind, all these examples so far have been of [window controls](../control/index.md#window-control), not [widget controls](../control/index.md#widget-control).  When we asked to intercept the key A, we wanted to intercept it no matter the focused widget on the window.  This holds true no matter what part of the window the user is on at the time.

## Main controls and sub-controls

`on_pres_LETTER` is a sub-control.  Remember why?

- `on_` is just the logical prefix for a control method, no matter its type ;
- `press` is the control name, so it's mandatory in both cases.
- `_letter`: this is extra information which depends on the control type.

Extra information: if present, that's a sub-control.  If not, that's a main control.  The [press](../control/press.md) control makes a heavy use of extra information.  It can contaain the key press.  So `on_press_a` is a sub-control method which ONLY triggers if the user presses the key A on her keyboard.

But it's possible to write a main control too that would trigger no matter the key pressed.  Since we don't specify the key being pressed, the method name will simply be `on_press`.  Let's see that:

```python
from bui import Window, start

class Example(Window):

    """An example window."""

    layout = mark("""
        <window title="An example">
          <text x=2 y=2 width=1 id=status read-only>What now?</text>
        </window>
    """)

    def on_press(self):
        """Some key was pressed."""
        self["status"].value = "Some key was pressed... but which one?"

start(Example)
```

If you run this script, you'll see the method fired each time you press a key, no matter what key.

Great... but not very useful as is, is it?  It would be good to know what key was pressed:

```python
    ...
    def on_press(self, key):
        """Some key was pressed."""
        self["status"].value = f"The user pressed the key: {key}"
```

Now run this script and press on keys on your keyboard.  You'll see the message changing.

> Hold on, what's the difference between the last examples?

In the last example, we added an argument to ou `on_press` method.  The argument is named `key`.  The name of the argument is important.  Arguments let BUI know that more information is needed to process this control.  BUI will try to provide it with the information required.  `key` is an [attribute of the press control](../control/press.md#control-attributes).  That's the one we often use.

In addition, we modify the message to display to add `{key}` through a simple f-string.

So let's try this script!  Open it and then press keys and see the message changing.  Here's a small example:

- If you press A, then you see "The user pressed the key: a" .  No surprise.
- If you press ESCAPE, you see "The user pressed the key: escape" .  Interesting, so you ca nbind to the ESCAPE key too.
- If you press the DELETE key, you see "The user pressed the key: delete" .  Still interesting.
- If you press CTRL + J, you see "The user pressed the key: ctrl_j" .  Wow, still more interesting!

All these keys can be interceted through sub-control methods.  You could, for instance, create an `on_press_ctrl_q` method to intercept the CTRL + Q combination.  Or `on_press_escape` to intercept the escape key.  This script can be used to see the key name if you have a doubt about which key press you could intercept.

But let's go back to this question: how to intercept a punctuation sign?  Say, you want to intercept when the user presses the key for ; on her keyboard.  But you can't write `on_press_;`, this is not a valid Python name.  So what to do?  You can use the main control for that, though it does look a bit harder to read.

```python
    ...
    def on_press(self, key):
        """Some key was pressed."""
        if key == ";":
            self["status"].value = "I intercepted a ;"
```

This works.  If you run this script and press the key for ; the message will appear.  It's not as readable, because you need to run a condition in a main control method and BUI is built to avoid that, since it tends to make code harder to read if you have a lot of conditions to test various keys.

Again, an oddity for users with non-QWERTY keyboards:  this method might fire when you press ; no matter where this key is on your keyboard.  If you don't have any, though, BUI will revert to the position of the key on a QWERTY keyboard.  This might not pose huge challenges but keep it in mind when writing user documentation for other languages.

## Special keys

As we saw before, it's fairly easy to intercept "special" keys, like the escape key.  Keys have a name in BUI and this name can be used in control method names to create a sub-control method.  Here are some examples:

```
from bui import Window, start

class Example(Window):

    """An example window."""

    layout = mark("""
        <window title="An example">
          <text x=2 y=2 width=1 id=status read-only>What now?</text>
        </window>
    """)

    def on_press_escape(self):
        """The user pressed on the ESCAPE key."""
        self["status"].value = "This is the ESCAPE key."

    def on_press_f1(self):
        """The user pressed on the F1 key."""
        self["status"].value = "This is the F1 key."

    def on_press_pageup(self):
        """The user pressed on the Page Up key."""
        self["status"].value = "This is the Page Up key."

    def on_press_return(self):
        """The user pressed on the RETURN key."""
        self["status"].value = "This is the RETURN key."

    def on_press_numpad7(self):
        """The user pressed on the NUMPAD 7 key."""
        self["status"].value = "This is the 7 numeric keypad."

start(Example)
```

In this example, we intercept ESCAPE, F1, Page Up, RETURN and the 7 on the numeric keypad.  The names are quite straightforward, in reading anyway.  Here's a diagram of key names you can use.  Remember that the user keyboard layout might affect most of them:

Here is the left pad:

    escape   f1 f2 f3 f4    f5 f6 f7 f8    f9  f10  f11  f12
    grave  1  2  3  4  5  6  7  8  9  0     minus equal back
    tab     q  w  e  r  t  y  u  i  o  p  left_bracket right_bracket return
    caplock  a  s  d  f  g  h  j  k  l  semicolon apostrophe antislash
    shift     z  x  c  v  b  n  m comma dot slash
    ctrl windows alt           space                    context

Now the middle pad:

    screenshot scroll pause
    insert     home   pageup
    delete     end    pagedown

               up
    left       down   right

And here's the numeric keypad:

    numlock     numpad_left numpad_right numpad_minus
    numpad7     numpad8     numpad9      numpad_plus
    numpad4     numpad5     numpad6
    numpad1     numpad2     numpad3      numpad_enter
    numpad0                 numpad_dot

Notice that some of these keys will not be usable in every situation as they might be reserved by the operating system.  Be careful around ctrl, shift, windows and alt in particular, because they usually are modifiers and can be used in combinations with others.

## Combinations

If you need to intercept a key combination (that is, one key pressed with modifiers like Shift or CTRL), you need to include the modifier names in the method control name.  As we've seen, this is not simple enough: `on_press_ctrl_j` will be called when the user presses CTRL + J on her keyboard.

However, there are rules about the order of modifiers to use:

- First in the name should be "ctrl", if CTRL is involved in the shortcut.
- Next should be "alt", if Alt is involved in the shortcut.
- Then should be "shift", if Shift is involved in the shortcut.

Again, remember, all names are lowercase.  So if you want to intercept the shortcut CTRL + Alt + J, create a method called `on_press_ctrl_alt_j`.  `on_press_alt_ctrl_j` will not work.

On Windows, combinations with Alt are for reserved for access to individual menus in the menu bar.  Therefore, binding these keys might not work ornot have the expected behavior.

## Cancelling default action

BUI will allow you to override some actions that can usually be performed by the keyboard.  For instance, let's imagine we have a text widget on a window.  In a text widget, the user usually can type text, except if it's read-only.  But what if you want to intercept the letter K... and not allow the user to type it in hthe text field?

We can use another feature of controls: they can optionally receive the control object.  And the control object has a method called `stop` that will raise an exception and cancel the control immediately.  Let's modify our example to see how that would work:

```python
from bui import Window, start

class Example(Window):

    """An example window."""

    layout = mark("""
        <window title="An example">
          <text x=2 y=2 width=1 id=notepad multiline>Notepad</text>
        </window>
    """)

    def on_press_k(self, control):
        """The user pressed on the letter K."""
        self["notepad"].value = "Well, too bad but that was a K."
        conttrol.stop()

start(Example)
```

If you run this program, you will see a text in the window very similar to the one we had before.  But this one you can type in this field.  All will go as planned, but if you press K, then your typed character will be cancelled and a message will replace whatever you have typed in the notepad field.

Needing to call `control.stop()` might be scarce.  It usually involves widget controls, we'll see them next, because the operation will most definitely vary depending on the focused widget.  Nevertheless, this feature can be handy at times in designing some widgets.
