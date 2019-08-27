"""Contains constants and functions to interact with the keyboard."""

MODIFIERS = ("ctrl", "alt", "shift")

LEFT_PAD = (
    "escape f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 f12 "
    "grave 1 2 3 4 5 6 7 8 9 0 minus equal back "
    "tab q w e r t y u i o p left_bracket right_bracket return "
    "caplock a s d f g h j k l semicolon apostrophe antislash "
    "shift z x c v b n m comma dot slash "
    "ctrl windows alt space context"
).split()

MIDDLE_PAD = (
    "screenshot scroll pause "
    "insert home pageup "
    "delete end pagedown "
    "up left down right"
).split()

NUMPAD = (
    "numlock numpad_left numpad_right numpad_minus "
    "numpad7 numpad8 numpad9 numpad_plus "
    "numpad4 numpad5 numpad6 "
    "numpad1 numpad2 numpad3 numpad_enter "
    "numpad0 numpad_dot numpad_enter "
).split()

KEYS = tuple(LEFT_PAD + MIDDLE_PAD + NUMPAD)
