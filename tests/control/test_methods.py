"""Test control methods.

This test checks that the proper `on_*` instance method are correctly
linked to controls, and that firing the controls does call the method.

"""

from bui import Window, start

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
    assert any(method == window.on_press for _, method in window.controls["press"])

    # Check that the on_press method is called when firing the control
    window._process_control("press", {"key": "a", "raw_key": "a"})
    assert window.pressed, "The control method wasn't called."

def test_widget_control():
    """Test a widget control with its associated method."""
    class Example(Window):

        layout = mark("""
          <window title="Test on widget controls">
            <button x=2 y=2 id="quit" name="Quit the window" />
          </window>
        """)

        def on_click_quit(self):
            self.should_quit = True

    window = start(Example)
    window.should_quit = False

    # Check that the control method is registered into the widget object
    widget = window["quit"]
    assert "click" in widget.controls
    assert any(method == window.on_click_quit for _, method in widget.controls["click"])

    # Check that the on_click_quit method is called when firing the control
    widget._process_control("click")
    assert window.should_quit, "The control method wasn't called."
