"""Register fixtures for pytest."""

from bui.tools import forbid_start
import pytest

@pytest.fixture(autouse=True)
def no_BUI_start():
    """This fixture makes sure BUI will not start and enter a blocking loop."""
    with forbid_start():
        yield
