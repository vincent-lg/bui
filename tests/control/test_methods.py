"""Test control methods.

This test checks that the proper `on_*` instance method are correctly
linked to controls, and that firing the controls does call the method.

"""

from bui import Window, start

from tests.control.helpers import is_registered

def test_window_control():
    """Test a window control with its associated method."""
    class Example(Window):

        layout = mark("""
          <window title="Test on window controls">
          </window>
        """)

        def on_press(self):
            self.pressed = True

    window = start(Example)
    window.pressed = False

    # Check that the control method is registered into the window object
    assert "press" in window.controls
    assert is_registered(window, "press", window.on_press)

    # Check that the on_press method is called when firing the control
    window._process_control("press", {"key": "a", "raw_key": "a"})
    assert window.pressed, "The control method wasn't called."

def test_widget_control():
    """Test a widget control with its associated method."""
    class Example(Window):

        layout = mark("""
          <window title="Test on widget controls">
            <button x=2 y=2 id="quit">Quit the window</button>
          </window>
        """)

        def on_click_quit(self):
            self.should_quit = True

    window = start(Example)
    window.should_quit = False

    # Check that the control method is registered into the widget object
    widget = window["quit"]
    assert "click" in widget.controls
    assert is_registered(widget, "click", window.on_click_quit)

    # Check that the on_click_quit method is called when firing the control
    widget._process_control("click")
    assert window.should_quit, "The control method wasn't called."

def test_implicit_widget_control():
    """Test the link between a control method and implicit widget control."""
    class Example(Window):

        """Window showing implicit controls."""

        layout = mark("""
          <window title="An example for implicit controls">
            <menubar>
              <menu name="File">
                <item id="quit">Quit this app right away</item>
              </menu>
            </menubar>
          </window>
        """)

        def on_quit(self):
            """The user pressed on the 'quit' menu item."""
            self.should_quit = True
    window = start(Example)
    window.should_quit = False

    # Check that the control method is registered into the widget object
    widget = window.parsed_layout.get("item").widget
    assert "click" in widget.controls
    assert is_registered(widget, "click", window.on_quit)

    # Check that the on_quit method is called when firing the control
    widget._process_control("click")
    assert window.should_quit, "The control method wasn't called."

def test_sub_window_controls():
    """Test a sub-control."""
    class Example(Window):

        layout = mark("""
          <window title="Test on window controls">
          </window>
        """)

        def on_press(self):
            self.pressed = 1

        def on_press_a(self):
            self.pressed = 2

    window = start(Example)
    window.pressed = 0

    # Check that the control method is registered into the window object
    assert "press" in window.controls
    assert is_registered(window, "press", window.on_press_a)

    # Check that the on_press_a method is called when firing the control
    window._process_control("press", {"key": "a", "raw_key": "a"})
    assert window.pressed == 2, "The control method wasn't called."

    # Check that the control method is registered into the window object
    assert is_registered(window, "press", window.on_press)

    # Check that the on_press method is called when firing the control
    window._process_control("press", {"key": "b", "raw_key": "b"})
    assert window.pressed == 1, "The control method wasn't called."

def test_sub_widget_controls():
    """Test a sub-control."""
    class Example(Window):

        layout = mark("""
          <window title="Test on window controls">
            <button x=2 y=3 id=count>Count me</button>
          </window>
        """)

        def on_press_count(self):
            self.pressed = 1

        def on_press_a_in_count(self):
            self.pressed = 2

    window = start(Example)
    window.pressed = 0
    widget = window["count"]

    # Check that the control method is registered into the widget object
    assert "press" in widget.controls
    assert is_registered(widget, "press", window.on_press_a_in_count)

    # Check that the on_press_a_count method is called when firing the control
    widget._process_control("press", {"key": "a", "raw_key": "a"})
    assert window.pressed == 2, "The control method wasn't called."

    # Check that the control method is registered into the widget object
    assert is_registered(widget, "press", window.on_press_count)

    # Check that the on_press_count method is called when firing the control
    widget._process_control("press", {"key": "b", "raw_key": "b"})
    assert window.pressed == 1, "The control method wasn't called."

def test_alias_window_control():
    """Test aliases on a window control."""
    class Example(Window):

        layout = mark("""
          <window title="Test on window controls">
          </window>
        """)

        def on_press_a(self):
            self.pressed = True
        on_press_b = on_press_a

    window = start(Example)
    window.pressed = False

    # Check that the control method is registered into the window object
    assert "press" in window.controls
    assert is_registered(window, "press", window.on_press_a)

    # Check that the on_press_a method is called when firing the control
    window._process_control("press", {"key": "a", "raw_key": "a"})
    assert window.pressed, "The control method wasn't called."
    window.pressed = False

    # Check that the control method is registered into the window object
    assert is_registered(window, "press", window.on_press_b)

    # Check that the on_press_b method is called when firing the control
    window._process_control("press", {"key": "b", "raw_key": "b"})
    assert window.pressed, "The control method wasn't called."

def test_alias_widget_control():
    """Test aliases on a widget control."""
    class Example(Window):

        layout = mark("""
          <window title="Test on window controls">
            <button x=2 y=0 id=quit>Quit or report</button>
          </window>
        """)

        def on_click_quit(self):
            self.pressed = True
        on_press_b_in_quit = on_click_quit

    window = start(Example)
    window.pressed = False
    widget = window["quit"]

    # Check that the control method is registered into the window object
    assert "press" in widget.controls
    assert is_registered(widget, "press", window.on_click_quit)

    # Check that the on_click_quit method is called when firing the control
    widget._process_control("click")
    assert window.pressed, "The control method wasn't called."
    window.pressed = False

    # Check that the control method is registered into the window object
    assert is_registered(widget, "press", window.on_press_b_in_quit)

    # Check that the on_press_b method is called when firing the control
    widget._process_control("press", {"key": "b", "raw_key": "b"})
    assert window.pressed, "The control method wasn't called."
