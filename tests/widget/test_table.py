"""Test the table widget."""

import pytest

from bui.specific.base.table import SpecificTable
from bui.widget.table import AbcRow, Table
from tests.widget.helpers import *

DEFAULT_LAYOUT = """
    <window title="Just a test">
      <table x=0 y=0 id=table>
        <col>Name</col>
        <col>Age</col>
        <col>Grade</col>
      </table>
    </window>
"""

@pytest.fixture(autouse=True)
def mock_specific_table():
    """Mock the specific table."""
    mock_specific("Table")
    yield
    unmock_specific()

@pytest.fixture
def table():
    from bui import Window, start
    class TestWindow(Window):

        layout = mark(DEFAULT_LAYOUT)

    window = start(TestWindow)
    table = window["table"]
    return table

def test_no_abc_row():
    """Cannot instantiate AbcRow objects."""
    with pytest.raises(TypeError):
        AbcRow()

def test_init(table):
    """Test the proper initialization of a standard table."""
    assert table.id == "table"
    assert table.widget == "table"
    assert len(table) == 0, "the table should be empty"
    with pytest.raises(IndexError):
        table[0]

def test_add_remove_rows(table):
    """Test to add and remove rows."""
    table.add_row("Nigel", 11, "B")
    table.add_row(name="Silvia", age=12, grade="A")
    assert len(table) == 2

    # Check the individual row values
    assert table[0].name == "Nigel"
    assert table[0].age == 11
    assert table[0].grade == "B"
    assert table[1].name == "Silvia"
    assert table[1].age == 12
    assert table[1].grade == "A"

    # Accessing incorrect index rows should raise IndexError
    with pytest.raises(IndexError):
        table[2]
    with pytest.raises(IndexError):
        table[-8]

    # Requesting unknown column names as attributes should fail
    with pytest.raises(AttributeError):
        table[0].health

    # But one can also use column indices
    assert table[0][0] == "Nigel"
    assert table[0][1] == 11
    assert table[0][2] == "B"

    # Trying to add new rows with an incorrect signature should raise a ValueError
    with pytest.raises(ValueError):
        table.add_row(1, 2)
    with pytest.raises(ValueError):
        table.add_row("Vincent", 11, "A", 80)
    with pytest.raises(ValueError):
        table.add_row(age=12, name="Vincent")
    with pytest.raises(ValueError):
        table.add_row(name="Sibylin", age=12, grade="I", value=38)
    with pytest.raises(ValueError):
        table.add_row("hold", name="Sibylin", age=12, grade="I")

    # Finally, try to remove rows
    table.remove_row(1)
    assert len(table) == 1
    with pytest.raises(IndexError):
        table[1]

    assert table[0].name == "Nigel"

    row = table[0]
    table.remove_row(row)
    assert len(table) == 0

def test_edit_rows(table):
    """Edit the content of columns, single or multiple rows."""
    table.add_row("Mike", 18, "B")
    table.add_row("Magalie", 18, "B+")

    # Edit a single cell in the first row
    assert table[0].name == "Mike"
    table[0].name = "Oscar"
    assert table[0].name == "Oscar"

    # Edit a cell by indice
    table[1][0] = "Audrey"
    assert table[1].name == "Audrey"
    assert table[1][0] == "Audrey"

    # Change the entire second row
    assert table[1] == ("Audrey", 18, "B+")
    assert table[1] == ["Audrey", 18, "B+"]
    assert table[1] == {"name": "Audrey", "age": 18, "grade": "B+"}

    # Edit with a tuple
    table[1] = (1, 2, 3)
    assert table[1] == (1, 2, 3)
    assert table[1] == [1, 2, 3]
    assert table[1] == {"name": 1, "age": 2, "grade": 3}

    # Edit with a list
    table[1] = [4, 5, 6]
    assert table[1] == (4, 5, 6)
    assert table[1] == [4, 5, 6]
    assert table[1] == {"name": 4, "age": 5, "grade": 6}

    # Edit with a dict
    table[1] = {"name": 7, "age": 8, "grade": 9}
    assert table[1] == (7, 8, 9)
    assert table[1] == [7, 8, 9]
    assert table[1] == {"name": 7, "age": 8, "grade": 9}

    # Edit with one row
    table[1] = table[0]
    assert table[1].name == "Oscar"
    assert table[1].age == 18
    assert table[1].grade == "B"
    assert table[0].index == 0
    assert table[1].index == 1

    # Check that copying a row somewhere else like that dereferenced cells
    table[1].name = "Mike"
    assert table[0].name == "Oscar"

    assert table[1].name == "Mike"

    # Edit several rows at once
    table[:] = [
        ("name1", 18, "A"),
        ("name2", 19, "B"),
    ]
    assert table[0].name == "name1"
    assert table[0].age == 18
    assert table[0].grade == "A"
    assert table[1].name == "name2"
    assert table[1].age == 19
    assert table[1].grade == "B"

    # Edit all rows at once
    table.rows = (
        ("name3", 20, "C"),
        {"name": "name4", "age": 21, "grade": "D"},
    )
    assert table[0].name == "name3"
    assert table[0].age == 20
    assert table[0].grade == "C"
    assert table[1].name == "name4"
    assert table[1].age == 21
    assert table[1].grade == "D"

    # Editing several rows with wrong numbers of rows
    with pytest.raises(TypeError):
        table[:] = (
            ("name5", 20, "C"),
            ("name6", 21, "D"),
            ("name7", 22, "D"),
        )

    # Editing with wrong type should raise TypeError
    with pytest.raises(TypeError):
        table.rows = 8

    # Editing with a row of diffeent table shouldn't be allowed
    from bui import Window, start
    class SecondTest(Window):
        layout = mark("""
            <window title="Second test">
              <table x=0 y=0 id=table>
                <col>One</col>
                <col>Two</col>
              </table>
            </window>
        """)

    window = start(SecondTest)
    table2 = window["table"]
    row2 = table2.add_row(1, 2)
    with pytest.raises(TypeError):
        table.rows = [row2]

    with pytest.raises(TypeError):
        table[0] = row2

    # Comparing two rows of those tables will fail
    with pytest.raises(TypeError):
        table.rows[0] == table2.rows[0]

def test_table_with_0_or_1_column():
    """Creating a table with 0 or 1 column should fail."""
    from bui import Window, start

    # Test with 0 column
    class TestWindow(Window):

        layout = mark("""
            <window title="Shouldn't work">
              <table x=0 y=0 id=table>
              </table>
            </window>
        """)

    with pytest.raises(ValueError):
        start(TestWindow)

     # Testwith 1 column
    class TestWindow(Window):

        layout = mark("""
            <window title="Shouldn't work">
              <table x=0 y=0 id=table>
                <col>One</col>
              </table>
            </window>
        """)

    with pytest.raises(ValueError):
        start(TestWindow)
