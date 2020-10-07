# Row objects in a table widget

This tutorial walks through the [table widget](../widget/Table.md) and the row objects that are generated to represent each row.

## What is a table widget in BUI?

BUI offers you the [table widget](../widget/Table.md), created from a [table](../layout/tag/table.md) tag.  A [table widget](../widget/Table.md) is similar to a list, but it has several columns to store information.  Each row in the table will have to specify the data for each column.

Thus, BUI uses the vocabulary of a table, with columns, rows and cells.  Let's see an example of what we could store:

| Name    | Age | Grade |
| ----    | --- | ----- |
| Magalie | 14  | B+    |
| Viktor  | 15  | B-    |
| Ellis   | 13  | B     |
| Arthur  | 15  | A-    |

We've got an unsorted table with three columns and four rows.  To be sure we all use the same vocabulary:

- This table's coluvns are "Name", "Age" and "Grade".
- Viktor is 15.  The cell "15" is on the row describing "Viktor", second column.

> Notice that the table is not sorted, at least as far as we can see.  It's not showing student names in alphabetical order.  Students aren't sorted by age or grade either.  That will be a good opportunity to practice sorting the data afterward.

## Creating a table

Let's reproduce this example in BUI.  We'll create a window with only this table and fill the table with the information given in the previous section.

To test, create the layout in a file ("table.bui" for instance), and place it the following layout:

```
<window title="Student grades">
  <table x=2 y=2 id=students>
    <col>Name</col>
    <col>Age</col>
    <col>Grade</col>
  </table>
</window>
```

Notice that we specify the table columns in the layout.  But we don't write rows.  Writing rows is a developer work, but the designer should at least place the columns.

Then create a file to place the Python code (like "table.py" following the same example) and write in it:

```python
from bui import Window, start

class StudentGrades(Window):

    """Student grades, to show ways to manipulate a table widget."""

    def on_init_students(self, widget):
        """The 'students' table is ready to be displayed."""
        widget.rows = (
            ("Magalie", 14, "B+"),
            ("Viktor", 15, "B-"),
            ("Ellis", 13, "B"),
            ("Arthur", 15, "A-"),
        )


start(StudentGrades)
```

We'll focus on how we filled the table later.  Right now, let's run this script.  Run with Python but in interactive mode:

    python table.py -i

The `-i` flag tells BUI to open an interactive console.  This is extremely useful for debugging.  The window will open as usual, but if you go back to the console, you'll see that an interactive Python console has opened, waiting for you to enter instructions.  This console doesn't conflict with the window itself, so the window can run as normal, while you type Python code or go back to the window to click on things and so on.

Inside the Python console, the `window` variable contains our instantiated window:

    >>> window
    <bui.generic.window object>
    >>> type(window)
    <class '__main__.StudentGrades'>
    >>>

So now, let's explore our window, in particular our "students" widget, in the console, checking our results in the BUI window from time to time.

## Basic row objects

First, we have the `window` variable containing the window, but we need to get hold of the table.  This table is under the "students" ID, so we can easily retrieve it using the `[]` operator on the window:

    >>> students = window["students"]
    >>> students
    <bui.generic.table object>
    >>> print(students)
    bui.generic.table(students)
    rows (
        Row name=Magalie, age=14, grade=B+
        Row name=Viktor, age=15, grade=B-
        Row name=Ellis, age=13, grade=B
        Row name=Arthur, age=15, grade=A-
    )
    >>>

This is our [table widget](../widget/Table.md).  It has some useful magic methods Python can work with:

    >>> len(students) # Number of rows in the table
    4
    >>>

But probably the one you'll use most often is the `[]` operator that allows to get individual rows:

    >>> students[0]
    <Row(name='Magalie', age=14, grade='B+')>
    >>>

We queried for the row 0 (that is, the first row).  BUI returns the row describing Magalie, which is quite correct.  But what is that object?

    >>> magalie = students[0]
    >>> print(magalie)
    Row name=Magalie, age=14, grade=B+
    >>> type(magalie)
    <class 'bui.widget.table.Row'>
    >>>

Row objects are based on the `Row` class.  If you are curious and want to see this class in [bui/widget/table.py](../raw/widget/table.html), you won't find it.  The closest you get is `AbcRow`.  Row classes are created dynamically for each table, but let's not get carried away in a complex topic right away.

So... we have a row.  That's great!  What can we do with it?

    >>> magalie.age
    14
    >>> magalie[2] # 3rd column, that is her grade
    'B+'
    >>>

Before going further, an important note here: the type of data we have specified is not the same.  Student names are strings (class `str`) obviously.  So are their grades (more on that later).  But their age is an integer (class `int`).  BUI will automatically convert to strings before placing things in the widget.  Keeping them as integers, though, has its use (particularly for sorting, as we shall see).

Okay, we've seen how to retrieve individual data from a row, which is good... but how about modifying individual cells?

    >>> magalie.age = 16
    >>> magalie[2] = "C+" # Change the 3rd column to C+ for Magalie
    >>> magalie
    <Row(name='Magalie', age=16, grade='C+')>
    >>>

Well, the changes appear to have been accepted.  But let's check: turn to your generated BUI window where you have the graphical table.  You should see that, yes, these changes were sent to the table and Magalie's age and grade have changed!

In summary: rows are represented in BUI like objects we can query or edit, either using index notation (like tuples), or using column names.

> Hold on!  We specified the second column as "Age", for instance (with a capital A).  Why can we query using the lowercase notation (`magalie.age`)?

When BUI reads your column tables, it will create two information per column: the column name ("Name" for the first column, for instance, with a capital N) and the column identifier.  Because we didn't specify any identifier in our column, BUI will use the column name, but will place it in lowercase format.  So our second column has name of "Age" and identifier of "age".  If you want to specify a different identifier, you can do so in layout:

```
<window ...>
  <table ...>
    <col id=identifier>Column name</col>
  </table>
</window>
```

Having BUI guess the column identifier makes our life easier and usually that's just what we want.  However, if you find this feature too strange or unpredictable, use clear identifier in the `<col>` tag.

## Multiple reads or editing

So far we've asked for a single row with the `[]` operator:

    >>> students[2]
    <Row(name='Ellis', age=13, grade='B')>
    >>>

But we can query several rows at the same time:

    >>> students[1:4]
    [<Row(name='Viktor', age=15, grade='B-')>, <Row(name='Ellis', age=13, grade='B')>, <Row(name='Arthur', age=15, grade='A-')>]
    >>>

You can, of course, browse on these objects and edit them as you please.

For instance, let's say we want to increase every student's age of 1 (it's the beginning of a new school year):

    >>> for row in students[0:4]:
    ...     row.age += 1
    ...
    >>> print(students)
    bui.generic.table(students)
    rows (
        Row name=Magalie, age=17, grade=C+
        Row name=Viktor, age=16, grade=B-
        Row name=Ellis, age=14, grade=B
        Row name=Arthur, age=16, grade=A-
    )
    >>>

We actually wanted to browse through every row of the table, so no need to specify the slice notation here:

    for row in students:
        ...

> When we browse a table like that and change a cell of all rows, does the widget update one time per query?

Yes, the table updates four times in all.  There's no mass updating as you could find in some query languages, or bulk updating like in Django.  But the process is still extremely fast.  BUI will cache as much as it possibly can to make the updating as effective as possible while still ensuring applying the changes.

## Editing an entire row, or even several rows

Remember, in our `StudentGrades` class, we have edited the table content in a strange way:

```python
    def on_init_students(self, widget):
        """The 'students' table is ready to be displayed."""
        widget.rows = (
            ("Magalie", 14, "B+"),
            ("Viktor", 15, "B-"),
            ("Ellis", 13, "B"),
            ("Arthur", 15, "A-"),
        )
```

It's a shortcut to edit the entire table rows.  Before seeing how that works, let's edit a single row.

    >>> students[1]
    <Row(name='Viktor', age=16, grade='B-')>
    >>> students[1] = ("Hermes", 15, "B")
    >>> students[1]
    <Row(name='Hermes', age=15, grade='B')>
    >>>

We read and update the second row here (of index 1).  We change the row specifying all three columns in a tuple.  Viktor is now Hermes, he is 15 and has only been graded with a B.

We can use a tuple to edit an entire row like this.  We just have to make sure we specify as many columns as are necessary, otherwise BUI will raise an exception and no modification will be performed.  You can also use a dictionary, with the column identifiers as keys.  This might be easier to read:

    >>> students[1] = {"name": "Bernard", "age": 15, "grade": "B"}
    >>> students[1]
    <Row(name='Bernard', age=15, grade='B')>
    >>>

Writing columns in a dictionary might be easier to read.  Which to use is really a matter of choice.

We can also copy a row into another.

    >>> students[3] = students[1]
    >>> students[3]
    <Row(name='Bernard', age=15, grade='B')>
    >>>

We copy all the data of the second row into the fourth row.  It's a copy: modifying the second row afterward won't modify the fourth.

Edit several rows in the same fashion: just wrap the number of rows in a tuple or list of the same length: let's edit row 2 and 3 for instance.

    >>> students[1:3] = (("Olaf", 14, "A-"), ("Eloise", 15, "A"))
    >>> print(students)
    bui.generic.table(students)
    rows (
        Row name=Magalie, age=17, grade=C+
        Row name=Olaf, age=14, grade=A-
        Row name=Eloise, age=15, grade=A
        Row name=Bernard, age=15, grade=B
    )
    >>>

This notation is a good shortcut, but it's not a great win for readability.  First, you have to make sure, when you edit two rows, you're giving it two rows.  Giving it an incorrect number of rows will raise an exception, because BUI just doesn't know what we want to do, there are ways to insert or remove rows, we'll see them next.  The exception is if we change the `rows` property itself, like we did in the `on_init_students` control method.  Doing so will reset the entire table with the rows we have given it.

## Adding or removing rows

We can add a new row at the end of the table using the `add_row` method:

    >>> students.add_row("Pauline", 15, "C-")
    <Row(name='Pauline', age=15, grade='C-')>
    >>> len(students)
    5
    >>>

This method will insert a new row at the bottom of the table.  We specify the columns (name, age and grade) as positional arguments.  We could also add a row using named arguments, which is easier to understand:

    >>> students.add_row(name="Edgar", age=17, grade="D+")
    <Row(name='Edgar', age=17, grade='D+')>
    >>>

Although you could, in theory, add a row using positional and keyword arguments at the same time, doing so is not advisable: choose a method and keep it, mixing both would make things really awkward.

We can also remove a row.  Say we want to remove Pauline, who is in row 5?

    >>> students.remove_row(4)
    >>> students[4]
    <Row(name='Edgar', age=17, grade='D+')>
    >>>

Row of index 4 (the fifth row) now is Edgar.  Pauline has been removed from the table.  Let's remove Edgar as well!

    >>> edgar = students[4]
    >>> students.remove_row(edgar)
    >>> students[4]
    Traceback (most recent call last):
      File "<console>", line 1, in <module>
      File ".../bui/bui/widget/table.py", line 206, in __getitem__
        row = self._rows[item]
    IndexError: list index out of range
    >>> len(students)
    4
    >>>

This time, we removed a row using the row object itself.  We try to access to the fifth row... but there's no fifth row now.  The table only has four rows.

## Sorting the table

Let's revert to our first table, we've played quite a lot with it already:

    >>> students.rows = (
    ...     ("Magalie", 14, "B+"),
    ...     ("Viktor", 15, "B-"),
    ...     ("Ellis", 13, "B"),
    ...     ("Arthur", 15, "A-"),
    ... )
    >>>

First, let's sort by students' names, easy to do:

    >>> students.sort()
    >>> print(students)
    bui.generic.table(students)
    rows (
        Row name=Arthur, age=15, grade=A-
        Row name=Ellis, age=13, grade=B
        Row name=Magalie, age=14, grade=B+
        Row name=Viktor, age=15, grade=B-
    )
    >>>

Of course, you can also check the result by switching to your BUI window.  Arthur is now at the top of the table, then Ellis, Magalie and Viktor.  Notice that "Magalie" is selected.  Why?  When we reset the table, BUI selected the first row automatically, that is "Magalie".  When sorting the table, BUI makes sure selection is preserved, so that we now select the third row, even though Magalie has changed position.

We have used the `sort` method on the table.  It's very similar to a list's, having optional `key` and `reverse` argument.  Let's try to sort by age:

    >>> students.sort(key=lambda row: row.age)
    >>> print(students)
    bui.generic.table(students)
    rows (
        Row name=Ellis, age=13, grade=B
        Row name=Magalie, age=14, grade=B+
        Row name=Arthur, age=15, grade=A-
        Row name=Viktor, age=15, grade=B-
    )
    >>>

Using a lambda to sort isn't the best option though.  We could use `attrgetter` which is precisely here for us.  Let's try, sorting by grades in reverse order:

    >>> from operator import attrgetter
    >>> students.sort(key=attrgetter("grade"), reverse=True)
    >>> print(students)
    bui.generic.table(students)
    rows (
        Row name=Viktor, age=15, grade=B-
        Row name=Magalie, age=14, grade=B+
        Row name=Ellis, age=13, grade=B
        Row name=Arthur, age=15, grade=A-
    )
    >>>

We sort by reverse grades this time.  Using `attrgetter` is just more optimized when sorting a lot of data.

> Why is Ellis after Magalie and not before?

Viktor has B-, Magalie has B+, Ellis has B... in theory Ellis should be between his two classmates.  But no, Ellis is after Magalie.  The reason is that the grade column is a string.  And Python sorts these strings alphabetically, the default.  If you want to sort by numeric grades, instead of giving letters, students should have a grade as an integer.  Yet we might not want to show the user this information.  We'll see how to do this in [the next section](#customize-the-row-class).

Turns out, sorting is very easy in a table and very much like what you're used, with the `list.sort` method or `sorted` function.  Python has a very powerful mechanism to sort, that would be a shame not to use it in BUI.

## Hidden columns

It often happens that we wish to add information to each row, but we don't wish for that information to be visible by the user.  The most common use case for this is a column with identifiers or slugs: we want to have this information in our rows, but we don't want this column to show to users.

In this example, we would like to sort students by grade.  The problem is, their grade is represented by a letter.  Python doesn't really know how to sort that, save alphabetically.  One solution would be to add each grade as a number (say a percentage point).  We'll see another way to handle this situation later.

First let's add our numeric grade column in our BUI file:

```
<window title="Student grades">
  <table x=2 y=2 id=students>
    <col>Name</col>
    <col>Age</col>
    <col>Grade</col>
    <col hidden>Numeric</col>
  </table>
</window>
```

In this case, we've added a hidden column as a fourth column in the table: a hidden column is defined with the `<col>` tag as usual, but with the `hidden` attribute.

If we modify only that part, we'll get an error when running our Python file.  We also need to add this information in each row:

```python
from bui import Window, start

class StudentGrades(Window):

    """Student grades, to show ways to manipulate a table widget."""

    def on_init_students(self, widget):
        """The 'students' table is ready to be displayed."""
        widget.rows = (
            ("Magalie", 14, "B+", 90),
            ("Viktor", 15, "B-", 82),
            ("Ellis", 13, "B", 85),
            ("Arthur", 15, "A-", 92),
        )


start(StudentGrades)
```

Now, we can run this example:

    python table.py -i

Nothing different at first sight.

But if you switch to the open Python console and try to see the rows:

```
>>> window["students"].rows
[
    <Row(name='Magalie', age=14, grade='B+', numeric=90)>,
    <Row(name='Viktor', age=15, grade='B-', numeric=82)>,
    <Row(name='Ellis', age=13, grade='B', numeric=85)>,
    <Row(name='Arthur', age=15, grade='A-', numeric=92)>
]
>>>
```

Our hidden column is not displayed to the user, but it does appear in the row object.  We can modify it of course.  Most importantly, however, this solves an issue we hadn't been able to solve yet: how to sort students by grade?  We can do that now, using the "numeric" column:

```
>>> from operator import attrgetter
>>> window["students"].sort(key=attrgetter("numeric"), reverse=True)
>>> window["students"].rows
[
    <Row(name='Arthur', age=15, grade='A-', numeric=92)>,
    <Row(name='Magalie', age=14, grade='B+', numeric=90)>,
    <Row(name='Ellis', age=13, grade='B', numeric=85)>,
    <Row(name='Viktor', age=15, grade='B-', numeric=82)>
]
>>>
```

This time, we can safely sort through the grades, since they are just numeric values.

> Are hidden columns supposed to be at the end of our row?

No, hidden columns can be anywhere in the table row.  Identifiers tend to be first, for instance.  That's not a problem for BUI, it can easily find out what to actually display to the user and what to skip when modified.

The problem with this approach in our particular example: we need to set the numeric grade manually.  It's not so bad with only 4 students, but with a lot of them, it might be best to do it automatically.  So we'll now see how to do that.

## Customize the row class

Let's work with the use case just explained in the previous section: we have assigned letter grades to students.  But we would like to sort them in a logical order, according to their grade value.  The proposed solution in the previous section adds a hidden column with the numeric grade, but has the downside of forcing the developer to add a number matching each grade manually.  This can be fine at times, but it sure can be improved.

There are different ways to solve this problem, but probably the best would be to extend the row class itself: by defining a new row class, we could add an extra information for each row but make sure this information isn't displayed in the table.  The numeric grade, in this case, will be present, but will not appear in the table.

It's time to see what these row objects are: we've seen earlier that they are of a certain type:

    >>> type(magalie)
    <class 'bui.widget.table.Row'>
    >>>

... but if you check, there's no `Row` class inside this file.  The class is actually created dynamically each time a table is created.  Therefore, each table widget has its own row class.  Row classes contain the table columns, for instance, so it's important different classes are used, if you happen to have different tables in your application.

In short, `'bui.widget.table.Row'` is a dynamic class created by BUI for the table of student grades.  But we can override this class and that's what we're going to do now.

Let's close the window (you can press CTRL + C in your console to close both the interactive console and the BUI window at once) and head over to the `table.py` file.

A row class needs to inherit from `AbcRow`, which is defined in `bui.widget.table`.  It also needs to include the column names in a tuple, defined as a class variable.  This information isn't created automatically if BUI handles a custom class, so be sure to include it:

```python
from bui.widget.table import AbcRow

class StudentRow(AbcRow):

    """Class to represent a row in the student table."""

    columns = ("name", "age", "grade")
```

Each time the grade column is modified (at creation or later), we should change the grade numeric value.  We'll keep the numeric value in an attribute on the row object.  Contrary to "name", "age" and "grade", the numeric grade won't be a column in the table, only developers will have access to it.

How could we be sure to do something when the "grade" column is updated?  Fortunately, the row object has an update mechanism: just add a method, named `update_{column name}`, and this method will be called when the column is updated, whether at the row creation or later.  That's convenient, since that's what we want!

So create a `update_grade` method in your class:

```python
from bui.widget.table import AbcRow

NUMERIC = {
    "A+": 98,
    "A": 95,
    "A-": 91,
    "B+": 88,
    "B": 85,
    "B-": 81,
    "C+": 78,
    "C": 75,
    "C-": 71,
    "D+": 68,
    "D": 65,
    "D-": 61,
    "F": 25,
}

class StudentRow(AbcRow):

    """Class to represent a row in the student table."""

    columns = ("name", "age", "grade")

    def update_grade(self, grade):
        """The grade is about to be updated for thiw row."""
        self.numeric_grade = NUMERIC.get(grade.upper(), 0)
```

We've drawn a very simple match between letters and numeric grades here, just to show a full example.  Each time the "grade" column is changed, which happens when the row is first created, but also if the row changes afterward, the `numeric_grade` attribute receives the numeric value for the grade letter, or 0 if the letter grade isn't in the dictionary we're using.

Our class should work, but we have to tell BUI to use it.  You have to change the `row_class` attribute of our table widget **before** any row is created.  When to do that?  Best do it in our `on_init` method of our window, since this method already exists.  Just remember to do it before any row is created in the table:

```python
class StudentGrades(Window):

    """Student grades, to show ways to manipulate a table widget."""

    def on_init_students(self, widget):
        """The 'students' table is ready to be displayed."""
        widget.row_class = StudentRow
        widget.rows = (
            ("Magalie", 14, "B+"),
            ("Viktor", 15, "B-"),
            ("Ellis", 13, "B"),
            ("Arthur", 15, "A-"),
        )
```

We give it the class itself, to let BUI know we will use our custom class.  Each time a row is added, an object of our `StudentRow` class will be created.  Here's the full code of the `table.py` file, if you're lost:

```python
from bui import Window, start
from bui.widget.table import AbcRow

NUMERIC = {
    "A+": 98,
    "A": 95,
    "A-": 91,
    "B+": 88,
    "B": 85,
    "B-": 81,
    "C+": 78,
    "C": 75,
    "C-": 71,
    "D+": 68,
    "D": 65,
    "D-": 61,
    "F": 25,
}

class StudentRow(AbcRow):

    """Class to represent a row in the student table."""

    columns = ("name", "age", "grade")

    def update_grade(self, grade):
        """The grade is about to be updated for thiw row."""
        self.numeric_grade = NUMERIC.get(grade.upper(), 0)


class StudentGrades(Window):

    """Student grades, to show ways to manipulate a table widget."""

    def on_init_students(self, widget):
        """The 'students' table is ready to be displayed."""
        widget.row_class = StudentRow
        widget.rows = (
            ("Magalie", 14, "B+"),
            ("Viktor", 15, "B-"),
            ("Ellis", 13, "B"),
            ("Arthur", 15, "A-"),
        )


start(StudentGrades)
```

Let's run it again in interactive mode:

    python table.py -i

Let's see if our row class works:

    >>> students = window["students"]
    >>> magalie = students[0]
    >>> magalie
    <StudentRow(name='Magalie', age=14, grade='B+')>
    >>> type(magalie)
    <class '__main__.StudentRow'>
    >>> magalie.numeric_grade
    88
    >>>

That's great!  Not only did our table widget create objects of our `StudentRow` class, but the `update_grade` method was called for each row and now, each student has a `numeric_grade` attribute which is not in the table.  Magalie has 88, since she has been graded with a B+.  To be sure, let's update it:

    >>> magalie.grade = "C-"
    >>> magalie.numeric_grade
    71
    >>> magalie.grade = "B+"
    >>>

How cool is that?

So now we can sort students by grade in a more logical order:

    >>> from operator import attrgetter
    >>> students.sort(key=attrgetter("numeric_grade"), reverse=True)
    >>> print(students)
    bui.generic.table(students)
    rows (
        StudentRow name=Arthur, age=15, grade=A-
        StudentRow name=Magalie, age=14, grade=B+
        StudentRow name=Ellis, age=13, grade=B
        StudentRow name=Viktor, age=15, grade=B-
    )
    >>>

Notice that we sort on the `numeric_grade` attribute this time, not on the `grade` column.  And notice the difference in result.  Arthur is at the top of the table this time, because he has been graded with A-.  And Ellis is between Magalie and Viktor, which is much more consistent.

Custom table rows require to create an additional class to represent the row, inheriting from `bui.widget.table.AbcRow`.  It can host methods that will be called by BUI when a column updates.  It can also contain custom methods to encode more behavior in the row itself.  For instance, in the [download example](../example/download.md), each row contains a file to be downloaded.  Each row has a `download` method which can be used to start downloading this file.

> Why didn't we add `numeric_grade` in the `__init__` method of our `StudentRow` class?

For one thing, Python doesn't require it at all.  For another, we can be absolutely positive that `update_grade` is called when the row is created: otherwise, it would mean we are trying to create a student row without a grade, and BUI won't allow us to do that in the first place.  You can, however, redefine the `__init__` method on a row, but in this case, be sure to call the parent constructor, otherwise BUI will be most unhappy:

```python
class StudentRow(AbcRow):

    """A student row."""

    columns = ("name", "age", "grade")

    def __init__(self, *args, **kwargs):
        self.numeric_grade = 0
        super().__init__(*args, **kwargs)
```

Be also sure to have your `__init__` method support arbitrary positional or keyword arguments, as this is a requirement for BUI rows.  In effect, if you can sleep at night without overriding the `__init__` method, you might end up with something more robust.  But the choice is definitely yours to make.
