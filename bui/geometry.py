"""Generic classes to represent geomgry points and rectangles.

These classes can be used across BUI and will present a common interface to
exchange more freely between GUI toolkits.  These only serve a short
role of representation.  When using the API, sending in tuples is
completely acceptable.

Classes:
    Point(x, y): a point on the window.
    Rectangle(top_x, top_y, bottom_x, bottom_y): a rectangle.
    Size(x, y): a size of a portion of the window.

In BUI, (x=0 y=0) is the top-left corner of the window.  The top-right
corner depends on the screen resolution.

These can be used as tuples, so you can easily unpack them:

    >>> from BUI import Point
    >>> point = Point(15, 30)
    >>> x, y = point # unpacking

Or you can use tuples instead of these gemoetry objects when calling
methods needing them.

    >>> window.size = (150, 150)

(Note that BUI has been designed to avoid having to use these methods
manually.)

"""

class Point:

    """A point object in pixels, with X and Y coordinates.

    X and Y are counted from 0.  The point at (x=0, y=0) is the
    top-left corner of your window.  X represents the horizontal axis
    and Y is the vertical axis.  Therefore, Point(x=50 y=0) is to
    the right of Point(x=0 y=0), while Point(x=0 y=50) is below
    Point(x=0, y=0).

    Packing this data in an object is just easier for debugging.  You
    can unpack it as a tuple:

        >>> x, y = Point(30, 50)

    Or use a tuple instead of a Point:

        >>> window.position = (30, 180)

    Note: negative X and Y coordinates ARE NOT accepted.

    """

    def __init__(self, x, y):
        self._x = self._y = None
        self.x = x
        self.y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        if x < 0:
            raise ValueError(f"x is negative ({x})")

        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        if y < 0:
            raise ValueError(f"y is negative ({y})")

        self._y = y

    def __repr__(self):
        return f"<Point(X={self._x}, Y={self._y})>"

    def __str__(self):
        return f"Point(X={self._x}, Y={self._y})"

    def __iter__(self):
        return iter((self._x, self._y))

    def __len__(self):
        return 2


class Rectangle:

    """A rectangle delimited by two points (top-left, bottom-right).

    X and Y are counted from 0.  The point at (x=0, y=0) is the
    top-left corner of your window.  X represents the horizontal axis
    and Y is the vertical axis.  Therefore, Point(x=50 y=0) is to
    the right of Point(x=0 y=0), while Point(x=0 y=50) is below
    Point(x=0, y=0).

    Packing this data in an object is just easier for debugging.  You
    can unpack it as a tuple:

        >>> (top_x, top_y), (bottom_x, bottom_y) = Rectangle((0, 0), (30, 50))

    Or use a tuple instead of a Point:

        >>> window.area = ((0, 0), (120, 150))

    Note: negative X and Y coordinates ARE NOT accepted.

    """

    def __init__(self, top_left, bottom_right):
        self._top_left = self._bottom_right = None
        self.top_left = top_left
        self.bottom_right = bottom_right

    @property
    def top_left(self):
        return Point(*self._top_left)

    @top_left.setter
    def top_left(self, top_left):
        x, y = top_left
        if x < 0:
            raise ValueError(f"x is negative ({x})")
        if y < 0:
            raise ValueError(f"y is negative ({y})")

        self._top_left = (x, y)

    @property
    def bottom_right(self):
        return Point(*self._bottom_right)

    @bottom_right.setter
    def bottom_right(self, bottom_right):
        x, y = bottom_right
        if x < 0:
            raise ValueError(f"x is negative ({x})")
        if y < 0:
            raise ValueError(f"y is negative ({y})")
        top_left = self._top_left
        if x < top_left[0]:
            raise ValueError(f"bottom-right X ({x}) is lower than top-left X ({top_left[0]})")
        if y < top_left[1]:
            raise ValueError(f"bottom-right Y ({y}) is lower than top-left Y ({top_left[1]})")

        self._bottom_right = (x, y)

    def __repr__(self):
        return (
            f"<Rectangle(top(X={self._top_left[0]}, Y={self._top_left[1]})"
            f", bottom(X={self._bottom_right[0]}, Y={self._bottom_right[1]}))>"
        )

    def __str__(self):
        return (
            f"Rectangle(top(X={self._top_left[0]}, Y={self._top_left[1]})"
            f", bottom(X={self._bottom_right[0]}, Y={self._bottom_right[1]}))"
        )

    def __iter__(self):
        return iter((self._top_left, self._bottom_right))

    def __len__(self):
        return 2


class Size:

    """A size object in pixels, with X and Y coordinates.

    X and Y are counted from 0.  The point at (x=0, y=0) is the
    top-left corner of your window.  X represents the horizontal axis
    and Y is the vertical axis.  Therefore, Point(x=50 y=0) is to
    the right of Point(x=0 y=0), while Point(x=0 y=50) is below
    Point(x=0, y=0).  Although this class seems very close to Point, the
    purpose is actually different: a size represents a window (or widget)
    size, whether Point represents an actual, absolute point on the window.

    Packing this data in an object is just easier for debugging.  You
    can unpack it as a tuple:

        >>> x, y = Size(30, 50)

    Or use a tuple instead of a Size:

        >>> window.sixze = (30, 180)

    Note: negative X and Y coordinates ARE NOT accepted.

    """

    def __init__(self, x, y):
        self._x = self._y = None
        self.x = x
        self.y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        if x < 0:
            raise ValueError(f"x is negative ({x})")

        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        if y < 0:
            raise ValueError(f"y is negative ({y})")

        self._y = y

    def __repr__(self):
        return f"<Size(X={self._x}, Y={self._y})>"

    def __str__(self):
        return f"Size(X={self._x}, Y={self._y})"

    def __iter__(self):
        return iter((self._x, self._y))

    def __len__(self):
        return 2
