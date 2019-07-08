"""Test the Attr class, definiting attributes on widget tags."""

import pytest

from bui.layout.attr import Attr

def test_mandatory():
    """Test a mandatory attribute."""
    attr = Attr("title", "The window title")

    # Specifying a value should just return the same value
    result = attr.prepare("some title")
    assert result == "some title"

    # However, specifying no value should raise an exception
    with pytest.raises(ValueError):
        attr.prepare()

def test_optional():
    """Test an optional attribute, with a default value."""
    attr = Attr("id", "The widget identifier", default="")

    # Specifying a value should just return the same value
    result = attr.prepare("id")
    assert result == "id"

    # And specifying no value should return the default
    result = attr.prepare()
    assert result == ""

def test_default_callable():
    """Test an attribute with a default callable."""
    attr = Attr("name", "The widget name", default=lambda: "")

    # Specifying a value should just return the same value
    result = attr.prepare("me")
    assert result == "me"

    # And specifying no value should return the result of the default callable
    result = attr.prepare()
    assert result == ""

def test_type():
    """Test an attribute with another type."""
    attr = Attr("x", "the X coordinate", type=int)

    # Automatic convertion into int should occur
    result = attr.prepare("5")
    assert result == 5

    # However, an error while converting should be reported
    with pytest.raises(ValueError):
        attr.prepare("no number")

def test_if_present():
    """Test an attribute with an if_present value."""
    attr = Attr("checked", "Is this checkbox checked by default",
            default=False, if_present=True)

    # No value should give the default (False)
    result = attr.prepare()
    assert not result

    # Any value should give the if_present (True)
    result = attr.prepare(None)
    assert result
    result = attr.prepare("whatever")
    assert result
    result = attr.prepare(object())
    assert result
