"""Test the radio widget."""

import pytest

from bui.widget.radio import RadioButton
from tests.widget.helpers import *

DEFAULT_LAYOUT = """
    <window title="Just a test">
      <radio x=0 y=0 id=actions>
        <choice id=update>Update the software</choice>
        <choice id=repair>Repair the software</choice>
      </radio>
    </window>
"""

@pytest.fixture(autouse=True)
def mock_specific_radio():
    """Mock the specific radio button group."""
    mock_specific("RadioButton")
    yield
    unmock_specific()

@pytest.fixture
def radio():
    from bui import Window, start
    class TestWindow(Window):

        layout = mark(DEFAULT_LAYOUT)

    window = start(TestWindow)
    radio = window["actions"]
    return radio

def test_init(radio):
    """Test the initialized radio button."""
    assert len(radio.choices) == 2
    assert radio.selected == "update"

    # Change selection
    radio.selected = "repair"
    assert radio.selected == "repair"

def test_update(radio):
    """Update the choices."""
    radio.selected = "repair"
    assert radio.selected == "repair"

    # Update the choices
    radio.choices = (
        ("update", "Update the software"),
        ("repair", "Repair the software"),
        ("remove", "Uninstall the software"),
    )
    assert radio.selected == "update"
    radio.selected = "remove"
    assert radio.selected == "remove"

def test_not_enoug_choices(radio):
    """Try to update without enough choices."""
    with pytest.raises(ValueError):
        radio.choices = ()

    with pytest.raises(ValueError):
        radio.choices = ((1, 2), )

    with pytest.raises(TypeError):
        radio.choices = 8
