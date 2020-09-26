"""Package containing controls.

A control is an action performed at some point, usually triggered by the
user.  To some extent, they can be linked with the notion of events, found
in most GUI toolkits.  They're meant to be easier to connect and use the
full introspection strength of Python.  Behind the scenes, each control
is a class, though the user doesn't have to use tthat class except
if she really wants to.  Controls are linked with window methods
beginning with `on`, and the control name along with the widget
identifier can be used to create the method name (like `on_click_button`).

BUI will infer control types when a control is defined as being
"implicit" (a button control without specific control name is believed
to be "click", since it's usually a good default).

"""

from bui.control.base import CONTROLS
from bui.control.change import Change
from bui.control.check import Check
from bui.control.click import Click
from bui.control.close import Close
from bui.control.init import Init
from bui.control.press import Press
from bui.control.release import Release
from bui.control.right_click import RightClick
from bui.control.select import Select
from bui.control.type import Type
